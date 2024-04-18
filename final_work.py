from core import *
from directory import *
from interconnect import *

InterConnectNetwork = InterConnectClass()
Core1 = Core(1,InterConnectNetwork)
Core2 = Core(2,InterConnectNetwork)
Core3 = Core(3,InterConnectNetwork)
Core4 = Core(4,InterConnectNetwork)
DirectoryController = DirectoryControllerClass(InterConnectNetwork)

InterConnectNetwork.CacheController1 = Core1.cacheController
InterConnectNetwork.CacheController2 = Core2.cacheController
InterConnectNetwork.CacheController3 = Core3.cacheController
InterConnectNetwork.CacheController4 = Core4.cacheController

InterConnectNetwork.DirectoryController = DirectoryController
DirectoryController.memory = [0]*32

with open("dump.txt","w") as dump, open("log.txt","w") as log:
    with open("instFile.txt","r") as file:
        for instruction in file:
            instruction = instruction.split(" ")
            if len(instruction) == 3:
                [core, command, address] = instruction
                core = int(core)
                if(core == 1):
                    Core1.Execute(command, address)
                elif(core==2):
                    Core2.Execute(command, address)
                    
                elif(core==3):
                    Core3.Execute(command, address)
                    
                else:
                    Core4.Execute(command, address)
            else:
                [core, command, address, immediate] = instruction
                core = int(core)
                if(core == 1):
                    Core1.Execute(command, address, int(immediate[1:],2))
                elif(core == 2):
                    Core2.Execute(command, address, int(immediate[1:],2))
                elif(core == 3):
                    Core3.Execute(command, address, int(immediate[1:],2))
                else:
                    Core4.Execute(command, address, int(immediate[1:],2))


            

            log.write(str(instruction)+"\n")
            log.write("Core1\n")
            for cacheSet in range(2):
                for cacheIndex in range(2):
                    if(Core1.cacheController.cache[cacheSet].lines[cacheIndex].tag==''):
                        string = '00000'
                    else:
                        string = int_to_5_bit_binary(int(Core1.cacheController.cache[cacheSet].lines[cacheIndex].tag))
                    log.write("{"+string+" {"+str(Core1.cacheController.cache[cacheSet].lines[cacheIndex].state)+"} "+str(Core1.cacheController.cache[cacheSet].lines[cacheIndex].data)+"}\n")

                # log.write("{"+str(bin(int(Core1.cacheController.cache[cacheIndex].tag)))+" {"+str(Core1.cacheController.cache[cacheIndex].state)+"} "+str(Core1.cacheController.cache[cacheIndex].data)+"}\n")
            log.write("Core2\n")
            for cacheSet in range(2):
                for cacheIndex in range(2):
                    if(Core2.cacheController.cache[cacheSet].lines[cacheIndex].tag==''):
                        string = '00000'
                    else:
                        string = int_to_5_bit_binary(int(Core2.cacheController.cache[cacheSet].lines[cacheIndex].tag))
                    log.write("{"+string+" {"+str(Core2.cacheController.cache[cacheSet].lines[cacheIndex].state)+"} "+str(Core2.cacheController.cache[cacheSet].lines[cacheIndex].data)+"}\n")


            log.write("Core3\n")
            for cacheSet in range(2):
                for cacheIndex in range(2):
                    if(Core3.cacheController.cache[cacheSet].lines[cacheIndex].tag==''):
                        string = '00000'
                    else:
                        string = int_to_5_bit_binary(int(Core3.cacheController.cache[cacheSet].lines[cacheIndex].tag))
                    log.write("{"+string+" {"+str(Core3.cacheController.cache[cacheSet].lines[cacheIndex].state)+"} "+str(Core1.cacheController.cache[cacheSet].lines[cacheIndex].data)+"}\n")

            log.write("Core4\n")
            for cacheSet in range(2):
                for cacheIndex in range(2):
                    if(Core4.cacheController.cache[cacheSet].lines[cacheIndex].tag==''):
                        string = '00000'
                    else:
                        string = int_to_5_bit_binary(int(Core4.cacheController.cache[cacheSet].lines[cacheIndex].tag))
                    log.write("{"+string+" {"+str(Core4.cacheController.cache[cacheSet].lines[cacheIndex].state)+"} "+str(Core1.cacheController.cache[cacheSet].lines[cacheIndex].data)+"}\n")

            

            dump.write("\n[")
            for lineIndex in range(len(DirectoryController.memory)):
                dump.write(str(format(lineIndex,'06b'))+" "+str(DirectoryController.memory[lineIndex])+", Directory Entry = "+str(DirectoryController.directory[lineIndex].state)+" {"+str(DirectoryController.directory[lineIndex].sharer)+"}\n")
            dump.write("]\n")
            
            for set1 in range(2):
                for line1 in range(2):
                    if(Core1.cacheController.cache[set1].lines[line1].state == "I"):
                        Core1.cacheController.cache[set1].lines[line1].data = 0
                        Core1.cacheController.cache[set1].lines[line1].state = ""
                        Core1.cacheController.cache[set1].lines[line1].tag = ""
                    elif(Core2.cacheController.cache[set1].lines[line1].state == "I"):
                        Core2.cacheController.cache[set1].lines[line1].data = 0
                        Core2.cacheController.cache[set1].lines[line1].state = ""
                        Core2.cacheController.cache[set1].lines[line1].tag = ""
                    elif(Core3.cacheController.cache[set1].lines[line1].state == "I"):
                        Core3.cacheController.cache[set1].lines[line1].data = 0
                        Core3.cacheController.cache[set1].lines[line1].state = ""
                        Core3.cacheController.cache[set1].lines[line1].tag = ""
                    elif(Core4.cacheController.cache[set1].lines[line1].state == "I"):
                        Core4.cacheController.cache[set1].lines[line1].data = 0
                        Core4.cacheController.cache[set1].lines[line1].state = ""
                        Core4.cacheController.cache[set1].lines[line1].tag = ""
                    
