import random

class CacheLine:
    
    def __init__(self):
        self.tag = "00000" # Binary Number as 32 address we need 5 bits
        self.data = int("0"*32,2) # 32 bit 
        self.state = "" # Binary Number as we have 3 states (M, S, I)
        
class CacheSet:
    def __init__(self):
        self.lines = [CacheLine() for _ in range(2)]
        self.lru_bits = "0"

class CacheController:
    def __init__(self, core, InterConnectNetworkObject):
        self.cache = [CacheSet() for _ in range(2)]
        self.InterConnectNetwork = InterConnectNetworkObject
        self.core = core
        self.random_index = None
        self.random_set = None
        
    def update_lru_bits(self, set):
        self.cache[set].lru_bits = "1"
        self.cache[1-set].lru_bits = "0"     ###Doubt
    
    def get_set(self,address):
        if(address%2 == 0):
            return 0
        else:
            return 1
        
    def WriteBack(self, address, data):
        random_index = self.random_index
        random_set = self.random_set
        if self.cache[random_set].lines[random_index].state == "M" or self.cache[random_set].lines[random_index].state == "I":
            self.cache[random_set].lines[random_index].data = data
            self.cache[random_set].lines[random_index].state = "M"
            dataWriteBack = True
            stateWriteBack = False
            self.InterConnectNetwork.WriteBackRequestToDirectoryController(self.core, data, address, dataWriteBack, stateWriteBack)
            self.random_index = None
            self.random_set = None

    def DataResponse(self, data, address, transaction):
        print("Cache Controller got Data Response got from Interconnect")
        dataWriteBack = False
        stateWriteBack = False
  
        if self.random_index == None :
            random_index = random.randint(0,1)
            random_set = self.get_set(address)

        else:
            random_index = self.random_index
            random_set = self.random_set
            
        if(self.cache[random_set].lines[random_index].data == 0 or self.cache[random_set].lines[random_index].tag == "00000"): # writing the data in cache's empty location
            print("Writing data into emply space of cache -- Location = "+ str(random_index))
            if(transaction=="GetShared"):
                self.cache[random_set].lines[random_index].data = data
                self.cache[random_set].lines[random_index].state = "S"
                self.cache[random_set].lines[random_index].tag = address
                print("Data Received in S State")
                print("Updated Cache Line - "+str(self.cache[random_set].lines[random_index].tag)+" "+str(self.cache[random_set].lines[random_index].state)+" "+str(self.cache[random_set].lines[random_index].data))
            elif(transaction=="GetModified"):
                self.cache[random_set].lines[random_index].data = data
                self.cache[random_set].lines[random_index].state = "M"
                self.cache[random_set].lines[random_index].tag = address
            self.update_lru_bits(random_set)
            
        else:
            if((self.cache[random_set].lines[random_index].state == "S" or self.cache[random_set].lines[random_index].state == "M") and self.cache[random_set].lines[random_index].tag != address): # Eviction of data incase the location in cache is occupied
                old_state = self.cache[random_set].lines[random_index].state
                old_data = self.cache[random_set].lines[random_index].data
                old_address = self.cache[random_set].lines[random_index].tag
                print("Cache Line needs to be Evaculated to Put new data at index = "+str(random_index))
                if(transaction=="GetShared"):
                    self.cache[random_set].lines[random_index].data = data
                    self.cache[random_set].lines[random_index].state = "S"
                    self.cache[random_set].lines[random_index].tag = address
                elif(transaction=="GetModified"):
                    self.cache[random_set].lines[random_index].data = data
                    self.cache[random_set].lines[random_index].state = "M"
                    self.cache[random_set].lines[random_index].tag = address
                self.update_lru_bits(random_set)
                print("Write Back Request --> InterConnect Network --> Directory Controller")
                if(old_state == "M" or old_state == "S"):
                    dataWriteBack = False
                    stateWriteBack = True
                    self.InterConnectNetwork.WriteBackRequestToDirectoryController(self.core, old_data, old_address, dataWriteBack, stateWriteBack) # Write back the old data to directory controller incase of eviction
            else:
                if(transaction=="GetShared"):
                    print("Latest Data received in shared state")
                    self.cache[random_set].lines[random_index].data = data
                    self.cache[random_set].lines[random_index].state = "S"
                    self.cache[random_set].lines[random_index].tag = address
                elif(transaction=="GetModified"):
                    print("Latest Data received in modified state")
                    self.cache[random_set].lines[random_index].data = data
                    self.cache[random_set].lines[random_index].state = "M"
                    self.cache[random_set].lines[random_index].tag = address
                self.update_lru_bits(random_set)
            self.random_index = None
            self.random_set = None
            
    def Response(self, address, transaction, lm):
        if(lm):
            for set in self.cache:
                for line in set.lines:
                    if(line.tag == address):
                        print("Data Invalidated for address = "+str(address)+" at core = "+str(self.core)+"** DATA EVICTION **")
                        line.state = ""
                        line.data = 0
                        line.tag = ""
                        return
        elif(transaction=="GetModified"): ## If this core1 has issued GetModified tran then it will get dataResponse and other core will get Response from Directory Controller
            for set in self.cache:
                for line in set.lines:
                    if(line.tag == address):
                        line.state = "I"
                        print("Data Invalidated for address = "+str(address)+" at core = "+str(self.core))
                        return
        elif(transaction == "ChangeStateToShared"):
            for set in self.cache:
                for line in set.lines:
                    if(line.tag == address):
                        line.state = "S"
                        print("Data Access altered from M to S address = "+str(address)+" at core = "+str(self.core))
                        return             

    def GetShared(self, core, address, transaction):
        print(address)
        for i, set in enumerate(self.cache):
            for line in set.lines:
                if(line.tag == address and (line.state == "M" or line.state == "S")): # START FROM HERE
                    print("Data Hit in Cache of Core = "+str(core))
                    self.update_lru_bits(i)
                    return line.data
        self.InterConnectNetwork.RequestToDirectoryController(self.core, address, transaction, False)
        return 
    
    def GetModified(self, core, address, transaction):
        flag=True
        for set in range(2):
            for line in range(2):
                if(self.cache[set].lines[line].tag == address):
                    flag=False
                    if(self.cache[set].lines[line].state == "M"):
                        print("Data hit in cache and state match as M")
                        self.update_lru_bits(set)
                        return self.cache[set].lines[line].data # In case of hit
                    else:
                        print("Data hit in cache but non-functional state = "+str(self.cache[set].lines[line].state))
                        self.random_index = line
                        self.random_set = set
                        self.InterConnectNetwork.RequestToDirectoryController(self.core, address, transaction, False)
        if flag:
            self.InterConnectNetwork.RequestToDirectoryController(self.core, address, transaction, False)

        return
            

    def Put(self, transaction, address):
        if transaction == "PUT":
            for set in range(2):
                for line in range(2):
                    if(self.cache[set].lines[line].tag == address ):
                        self.cache[set].lines[line].state = "I"
                        self.cache[set].lines[line].data = 0
                        self.cache[set].lines[line].tag = ""               
                        print("Data Invalidated for address = "+str(address)+" at core = "+str(self.core))
                        self.InterConnectNetwork.RequestToDirectoryController(self.core, address, transaction, lm=True)
                        break