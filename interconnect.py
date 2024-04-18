class InterConnectClass:
    def __init__(self):
        self.CacheController1 = None
        self.CacheController2 = None
        self.CacheController3 = None
        self.CacheController4 = None

        self.DirectoryController = None
        

    def WriteBackRequestToDirectoryController(self, core, data, address, dataWriteBack, stateWriteBack):
        print("Write Back request forwaded to Directory Controller")
        self.DirectoryController.WriteBack(address, data, core, dataWriteBack, stateWriteBack)

    def RequestToDirectoryController(self, core, address, transaction, lm=False):
        print("Interconnect called")
        self.DirectoryController.Execute(core, address, transaction, lm)

    def DataResponseToCacheController(self, core, data, address, transaction): # If the core asks asks for data then forward using this
        print("Directory COntroller (Data)--> InterConnect Network --> Cache Controller")
        if(core==1):
            self.CacheController1.DataResponse(data, address, transaction)
        if(core==2):
            self.CacheController2.DataResponse(data, address, transaction)
        if(core==3):
            self.CacheController3.DataResponse(data, address, transaction)
        else:
            self.CacheController4.DataResponse(data, address, transaction)


    def ResponseToCacheController(self, core, address, transaction, lm): # RequestToDirectoryControllerIf only state updating needs to be done
        print("Interconnect Network called from Direcory Controller to Cache Controller")
        if(core==1):
            self.CacheController1.Response(address, transaction, lm)
        elif(core==2):
            self.CacheController2.Response(address, transaction, lm)
        elif(core==3):
            self.CacheController3.Response(address, transaction, lm)
        else:
            self.CacheController4.Response(address, transaction, lm)

def int_to_5_bit_binary(num):
    binary_str = bin(num)[2:]  # Convert to binary and remove the '0b' prefix
    binary_str = binary_str.zfill(5)  # Pad with zeros to ensure a 5-bit representation
    return binary_str
