#ITS
import os
import configparser
config = configparser.ConfigParser()
ITSBase = []
ITSBytes = []
ITSChars = []
Vers = 0
SettingsFile = config.read('options.ini')
AutoSetVersion = config['Values']['AutoSetVersion']
Version = config["Values"]['Version']
IncludePotsAndHorses = config['Values']['IncludePotsAndHorses']
PrintItemID = config['Values']['PrintItemID']
PrintSize = config['Values']['PrintSize']
PrintRot = config['Values']['PrintRot']
PrintCoords = config['Values']['PrintCoords']
File1 = input("Drag file here: ")
if AutoSetVersion == 'False':
    Vers1 = input("November Proto or Final? P/F ")
    Vers = Vers1.lower()
elif AutoSetVersion == 'True':
    Vers = Version.lower()
File2 = os.path.basename(File1)
File3 = File1.lower().strip(".its")
OutputFile = open(File3 + ".txt", 'w', encoding="UTF-8")
ITSFile = open(File3 + ".ITS", 'rb')
if Vers == 'p':
    CTEFile = open("itsp.tbl", 'r', encoding="UTF-8")
else:
    CTEFile = open("itsf.tbl", 'r', encoding="UTF-8")
#ContTypeP = ["a chest", "a pot", "a wooden horse", ] 
ContTypeF = ["Free-Standing", "a Sasa Chest", "a Pot", "a Wooden Horse", "a Chest", "a Gale Shrine Chest", "a Clover", "some Grass", "a Watermelon", "a Locked Box", "a Bloom Pod", "a Guardian Fruit", "an Electric Chest", "a Clam Shell", "a Flower", "a Flaming Chest", "an One-Eyed Doll", "a Frozen Chest", "a Crystal Rock", "an Iron Rock"]
ContState = ["on land 1", "underwater", "buried", "on land 2", "a required pickup", "powerslash only", "sei-an canal", "sunken ship tidal", "on land 3"]
Entries = 0
ContentID = 0
Unk1 = 0
Unk2 = 0
ContStateID = 0
SizeX = 0
SizeY = 0
SizeZ = 0
RotX = 0
RotY = 0
RotZ = 0
CoordsX = 0
CoordsY = 0
CoordsZ = 0
ContTypeID = 0
IsStrayBead = 0
IsPraise = 0

def test():
    for line in CTEFile:
        ITSBase.append(line)
        
    for item in ITSBase:
        #print(item)
        try:
            item1, item2 = item.split(': ')
            ITSBytes.append(item1)
            ITSChars.append(item2)
        except ValueError:
            #print("Malformed value at" + item)
            pass

    Entries = int.from_bytes(ITSFile.read(4), 'little')
    Text = "Entries: " + str(Entries) + "\n\n"
    OutputFile.write(Text)
    print("Done!") #man these files are so small i might as well lmao
    i = 0

    while i <= Entries - 1:
        ContentID = 0
        ContStateID = 0
        ContTypeID = 0
        index = 0
        ContentID = int.from_bytes(ITSFile.read(1), 'little')
        ContentIDHex = str("0x" + format(ContentID, 'x').zfill(2))
        if ContentIDHex == '0xcc':
            IsStrayBead = True
            IsPraise = False
        elif ContentIDHex == '0x59':
            IsPraise = True
            IsStrayBead = False
        else:
            IsStrayBead = False
            IsPraise = False
        Unk1 = int.from_bytes(ITSFile.read(1), 'little')
        Unk2 = int.from_bytes(ITSFile.read(1), 'little')
        ContStateID = int.from_bytes(ITSFile.read(1), 'little')
        SizeX = int.from_bytes(ITSFile.read(1), 'little')
        SizeY = int.from_bytes(ITSFile.read(1), 'little')
        SizeZ = int.from_bytes(ITSFile.read(1), 'little')
        RotX = int.from_bytes(ITSFile.read(1), 'little')
        RotY = int.from_bytes(ITSFile.read(1), 'little')
        RotZ = int.from_bytes(ITSFile.read(1), 'little')
        CoordsX = int.from_bytes(ITSFile.read(1), 'little')
        CoordsY = int.from_bytes(ITSFile.read(1), 'little')
        CoordsZ = int.from_bytes(ITSFile.read(1), 'little')
        Unk3 = int.from_bytes(ITSFile.read(1), 'little')
        Unk4 = int.from_bytes(ITSFile.read(1), 'little')
        Unk5 = int.from_bytes(ITSFile.read(1), 'little')
        ContTypeID = int.from_bytes(ITSFile.read(1), 'little')
        ContTypeIDHex = str("0x" + format(ContTypeID, 'x').zfill(2))
        if IncludePotsAndHorses == 'False':
            if ContTypeIDHex == '0x02':
                SkipPots = True
            elif ContTypeIDHex != '0x02':
                if ContTypeIDHex == '0x03':
                    SkipPots = True
                else:
                    SkipPots = False
            else:
                SkipPots = False
        elif IncludePotsAndHorses == 'True':
             SkipPots = False
        if Vers == 'p' and IsPraise == True:
            ITSFile.seek(7, 1)
            PraiseValue = int.from_bytes(ITSFile.read(1), 'little')
            Dest = 7
        elif Vers == 'p' and IsPraise == False:
            Dest = 15
        elif Vers == 'f' and IsStrayBead == True:
                ITSFile.seek(7, 1)
                StrayBeadValue = int.from_bytes(ITSFile.read(1), 'little')
                Dest = 15
        elif Vers == 'f' and IsPraise == True:
                ITSFile.seek(7, 1)
                PraiseValue = int.from_bytes(ITSFile.read(1), 'little')
                Dest = 15
        elif Vers == 'f' and IsPraise == False and IsStrayBead == False:
                Dest = 23
        #Actual Text
        if SkipPots == True:
            i += 1
            ITSFile.seek(Dest, 1)
            pass
        if SkipPots == False:
            Text = "Entry: " + str(i) + "\n"
            OutputFile.write(Text)
            #print(Text)
            if PrintItemID == 'True':
                Text = "Item ID is " + str(ContentIDHex) + "\n"
                OutputFile.write(Text)
                #print(Text)
            elif PrintItemID == 'False':
                pass
            for x in ITSBytes:
                if x == ContentIDHex: #If we find it, print it out.
                    ContentIDHex = ContentIDHex.zfill(4)
                    #print("Index found at " + str(index))
                    if ContentIDHex == '0xcc':
                        Text = "Item is Stray Bead #" + str(StrayBeadValue + 1) + "\n"
                        OutputFile.write(Text)
                        #print(Text)
                    elif ContentIDHex == '0x59':
                        Text = "Item is " + str(PraiseValue) + " praise" + "\n"
                        OutputFile.write(Text)
                        #print(Text)
                    else:
                        Text = "Item is " + str((ITSChars[index].replace('\n',''))) + "\n"
                        OutputFile.write(Text)
                        #print(Text)
                    pass
                else:
                    if index >= len(ITSChars) - 1: #Print it MAYBE
                        Text = "{" + str(ContentIDHex) + "}"
                        #print(Text)
                        pass
                    else: #Iterate value
                        index+=1
            Text = "Container is " + str(ContState[ContStateID]) + "\n"
            OutputFile.write(Text)
            #print(Text)
            if PrintSize == 'True':
                Text = "Size is " + str(SizeX) + ", " + str(SizeY) + ", " + str(SizeZ) + "\n"
                OutputFile.write(Text)
                #print(Text)
            elif PrintSize == 'False':
                pass
            if PrintRot == 'True':
                Text = "Rotation is " + str(RotX) + ", " + str(RotY) + ", " + str(RotZ) + "\n"
                OutputFile.write(Text)
                #print(Text)
            elif PrintSize == 'False':
                pass
            if PrintCoords == 'True':
                Text = "Coords are " + str(CoordsX) + ", " + str(CoordsY) + ", " + str(CoordsZ) + "\n"
                OutputFile.write(Text)
                #print(Text)
            elif PrintCoords == 'False':
                pass
            Text = "Container is " + str(ContTypeF[ContTypeID]) + "\n"
            OutputFile.write(Text)
            #print(Text)
            Text = "~~~~~~~~~~~~~~~~~~~~\n\n"
            OutputFile.write(Text)
            #print(Text)
            ITSFile.seek(Dest, 1)
            i += 1

test()