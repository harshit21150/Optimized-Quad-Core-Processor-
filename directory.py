class DirectoryLine:
    def __init__(self):
        self.state = "I" # Binary Number as we have 3 states (M, S, I)
        self.sharer = "0000" # Hot encoded for 4 cores
        self.arr = [self.state, self.sharer]
        

# For every directory controller, i have defined a main memory and a directory corresponding to every memory address
class DirectoryControllerClass: 
        def __init__(self, InterConnectNetwork):
            self.memory = [int("0"*32, 2) for _ in range(32)] # Initial Memory of 32bit X 32 Address
            self.directory = [DirectoryLine() for i in range(32)] # Initial Directory  same size as main memory
            self.InterConnectNetwork = InterConnectNetwork

        def Execute(self, core, address, transaction, lm=False):
            print("Directory Controller got request from Cache Controller "+str(transaction))
            state = self.directory[address].state
            sharer = self.directory[address].sharer

            if(transaction == "PUT"):
                if(sharer == "1000"):                
                    self.InterConnectNetwork.ResponseToCacheController(1, address, transaction, lm)
                elif(sharer == "0100"):
                    self.InterConnectNetwork.ResponseToCacheController(2, address, transaction, lm)
                elif(sharer=="0010"):            
                    self.InterConnectNetwork.ResponseToCacheController(3, address, transaction, lm)
                else:
                    self.InterConnectNetwork.ResponseToCacheController(4, address, transaction, lm)
                self.directory[address].sharer = "0000"
                self.directory[address].state = "I"

             # incase of non evacuation of data from cache
            elif(transaction == "GetShared"):
                # As this is write through i have the updated data at the memory and the non-requestor core will be the modifier
                if(state == "M" or state == "S"):
                    if(core==1):
                        self.directory[address].sharer = "1" + sharer[1:]
                    elif(core==2 or core==3):
                        self.directory[address].sharer = sharer[:core-1] + "1" + sharer[core:]
                    else:
                        print("hello"+sharer[:core-1])
                        self.directory[address].sharer = sharer[:core-1] + "1" # Including both core in sharer
                        self.directory[address].state = "S"
                if(state == "I"):
                    if(core == 1):
                        self.directory[address].sharer =  "1" + sharer[1:] # Including both core in sharer
                    elif(core==2 or core==3):
                        self.directory[address].sharer =  sharer[:core-1] +"1" + sharer[core:]
                    else:
                        self.directory[address].sharer = "0001" # Including both core in sharer
                    print("Sharer List Updated to "+self.directory[address].sharer)
                    self.directory[address].state = "S"
                    print("Directory State Changed from I to S")
                self.InterConnectNetwork.DataResponseToCacheController(core, self.memory[address], address, transaction)
                quad_core=[1,2,3,4]
                quad_core.remove(core)
                print(quad_core)
                for i in quad_core:
                    self.InterConnectNetwork.ResponseToCacheController(i, address, "ChangeStateToShared", False)
                

            elif(transaction == "GetModified"):
                if(state == "M"):
                    print("Modified access to core is switched from core = "+str(core)+ " to core = "+str(3-core))
                    self.InterConnectNetwork.ResponseToCacheController(3-core, address, transaction, False)
                    if(core == 1):
                        self.directory[address].sharer = "1000" # Including both core in sharer
                        print("Sharer list updated to 1000")
                    elif(core ==2):
                        self.directory[address].sharer = "0100" # Including both core in sharer
                        print("Sharer list updated to 0100")
                    elif(core ==3):
                        self.directory[address].sharer = "0010" # Including both core in sharer
                        print("Sharer list updated to 0010")
                        
                    else:
                        self.directory[address].sharer = "0001" # Including both core in sharer
                        print("Sharer list updated to 0001")

                elif(state == "S"):
                    self.directory[address].state = "M"
                    if(int(self.directory[address].sharer,2) == 3):   
                        quad_core=[1,2,3,4]
                        quad_core.remove(core)
                        for i in quad_core:
                            self.InterConnectNetwork.ResponseToCacheController(i, address, transaction, False)
                elif(state == "I"):
                    if(core == 1):
                        self.directory[address].sharer = "1000" # Including both core in sharer
                    elif(core==2):
                        self.directory[address].sharer = "0100"
                    elif(core==3):
                        self.directory[address].sharer = "0010"
                        
                    else:
                        self.directory[address].sharer = "0001" # Including both core in sharer
                    self.directory[address].state = "M"
                    quad_core=[1,2,3,4]
                    quad_core.remove(core)
                    print(quad_core)
                    for i in quad_core:
                        self.InterConnectNetwork.DataResponseToCacheController(core, self.memory[address], address, transaction)

        def WriteBack(self, address, data, core, dataWriteBack, stateWriteBack):
            print("dataWriteBack = "+str(dataWriteBack)+" stateWriteBack = "+str(stateWriteBack))
            if(dataWriteBack and not stateWriteBack):
                self.memory[address] = data
                if(self.directory[address].sharer=="1111"):
                    self.InterConnectNetwork.ResponseToCacheController(core, address, "GetModified")
            elif(not dataWriteBack and stateWriteBack):
                quad_core=[1,2,3,4]
                quad_core.remove(core)
                for i in quad_core:
                    if(int(self.directory[address].sharer,2)==i):
                        self.directory[address].state = "I"
                        self.directory[address].sharer = "0000"
                    elif(int(self.directory[address].sharer,2)==3):
                        self.directory[address].state = "S"
                        if(core == 1):
                            self.directory[address].sharer = "0111"
                        elif(core==2):
                            self.directory[address].sharer = "1011"
                        elif(core==3):
                            self.directory[address].sharer = "1101"
                        elif(core==4):
                            self.directory[address].sharer = "1110"
                            
            else:
                print("Invaid Call to Write Back of Directory Controller")