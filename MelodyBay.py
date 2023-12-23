from tkinter import*
from ttkbootstrap.constants import*
from ttkbootstrap.dialogs import Messagebox
from tkinter import filedialog
import ttkbootstrap as tb
import os
import shutil
import time
import subprocess
import threading
import wave
import struct
import sys
import json

root = tb.Window(themename = "superhero")
root.title("Melody Bay")
print ()
root.iconbitmap(os.getcwd() + '\Images\MelodyBay.ico')
root.iconbitmap(default=os.getcwd() + '\Images\MelodyBay.ico')
app_width = 650
app_height = 500
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
X = int((screen_width - app_width) / 2)
Y = int((screen_height - app_height) / 2)
root.geometry ((f'{app_width}x{app_height}+{X}+{Y}'))

songList = []
fullPath = ""
slash = chr(92)


config = None
configDir = os.getcwd() + slash + "config.json"

def save_config():
    json.dump(config, open(configDir, "+w"), indent=4)

if not os.path.isfile(configDir):
    config = {
        "SoundDirectory": ""
    }
    save_config()
else:
    config = json.load(open(configDir, "r"))

def chooseSoundPath():
    result = Messagebox.okcancel("Choose your romfs/Data/StreamingAssets/sound/Switch folder from your game dump.", "Choose Sound Folder")
    if result == "OK":
        result = True
    else:
        result = False
    if result:
        config["SoundDirectory"] = filedialog.askdirectory(title = "romfs/Data/StreamingAssets/sound/Switch")
        if not os.path.isfile(config["SoundDirectory"] + slash + "BGM2.acb") or not os.path.isfile(config["SoundDirectory"] + slash + "BGM2.awb"):
            Messagebox.show_error("The sound folder should contain BGM2.acb and BGM2.awb.", "Invalid path.")
            return chooseSoundPath()

        save_config()

    return result

while config["SoundDirectory"].strip() == "":
    if not chooseSoundPath():
        sys.exit()

if os.path.isfile(os.getcwd() + slash + "SonicAudioTools" + slash + "AcbEditor.exe") == False or os.path.isfile(os.getcwd() + slash + "vgaudio" + slash + "VGAudioCli.exe") == False:
    Messagebox.show_error('Please make sure VGAudio and SonicAudioTools are in the MelodyBay directory.', "Error")
    sys.exit()

with open('SongList.txt') as my_file:
    for line in my_file:
        songList.append(line)

#Functions
def startSwapMusic_in_bg():
    threading.Thread(target=swapMusic())

def swapMusic():
    if manualLoop.get() == 1:
        try:
            (int(startEntry.get()))
            (int(endEntry.get()))  
            if (int(startEntry.get())) >= (int(endEntry.get())):
                errorMessage = Messagebox.show_error("Starting Sample point MUST be larger than Ending Sample point", "Error")
                return
        except ValueError:
            errorMessage = Messagebox.show_error("You must put in a numbers for Starting Samples and Ending Sampels to manually loop. If you want the program to automatically loop, turn off input Looping points manually", "Error")
            return
    progressBar['value'] = 0
    root.update()
    for i, ele in enumerate(songList):
        songList[i] = ele.replace("\n", '')
    test = songCombo.get()
    tester = test.replace("#", '')
    tester = tester.split() 
    tester[0]
    songNumber = int(tester[0])
    songNumber = songNumber - 1
    VGAudioCliArgs = fullPath
    if os.path.isfile(VGAudioCliArgs) == False:
        errorMessage = Messagebox.show_error ("Invalid file path", "Error")
        return
    else:
        try:
            os.rename (VGAudioCliArgs, VGAudioCliArgs.replace(" ", "_"))
            VGAudioCliArgs = VGAudioCliArgs.replace(" ", "_")
        except FileNotFoundError:
            errorMessage = Messagebox.show_error ("Place your Music files in the directory next to Melody Bay & try again. (also ensure that your filepath has no spaces or special characters! Otherwise try renaming the file)", "Error")
            return
    progressBar['value'] += 20
    root.update()
    userTrack = os.path.split(VGAudioCliArgs)
    convertedTrack = str(userTrack[1])
    trackNoExt = convertedTrack.replace (".mp3", "")
    newAudio = os.getcwd() + '\\' + trackNoExt + '.wav'
    print (os.getcwd() + slash + convertedTrack + ".wav")
    if os.path.isfile(os.getcwd() + slash + convertedTrack + ".wav") == True:
        os.remove (os.getcwd() + slash + convertedTrack + ".wav")
    subprocess.call(['C:\\windows\\system32\\cmd.exe', '/C', 'ffmpeg -i ' + VGAudioCliArgs + " -ar 48000 " + newAudio])
    fileOutput = (f"{songNumber:05}"'_streaming.lopus')
    vgAudioCli = os.getcwd() + '\\vgaudio\\VGAudioCli.exe ' + '"' + newAudio + '" ' + '--bitrate ' + '"' + '96000' +'" ' + '--CBR ' + fileOutput
    os.system (vgAudioCli)
    dummyFileNumber = songNumber + 1
    dummyFile = (f"{dummyFileNumber:05}"'_streaming.lopus')
    if dummyFileNumber == 10 or dummyFileNumber == 18 or dummyFileNumber == 21 or dummyFileNumber == 59 or dummyFileNumber == 71 or dummyFileNumber == 73:
        sampleRate = 48000.0 # hertz
        duration = 1.0 # seconds
        frequency = 440.0 # hertz
        obj = wave.open('sound.wav','w')
        obj.setnchannels(1) # mono
        obj.setsampwidth(2)
        obj.setframerate(sampleRate)
        for i in range(99999):
            value = 0
            data = struct.pack('<h', value)
            obj.writeframesraw( data )
        obj.close()
        generateDummyFile = os.getcwd() + '\\vgaudio\\VGAudioCli.exe ' + os.getcwd() + '\\sound.wav ' + '--bitrate ' + '"' + '96000' +'" ' + '--CBR ' + dummyFile
        print (generateDummyFile)
        os.system (generateDummyFile)

    time.sleep(2)
 
    if os.path.isfile(fileOutput) == False:
        errorMessage = Messagebox.show_error ("Failed to convert audio is FFmpeg installed correctly?", "Error")
        return
    else:
        try:
            base_file, ext = os.path.splitext(fileOutput)
            os.rename (fileOutput, base_file + ".bin")
        except FileExistsError:
            os.remove (base_file + '.bin')
            os.rename (fileOutput, base_file + ".bin")
    
    if dummyFileNumber == 10 or dummyFileNumber == 18 or dummyFileNumber == 21 or dummyFileNumber == 59 or dummyFileNumber == 71 or dummyFileNumber == 73:
        try:
            base_dummy, ext = os.path.splitext(dummyFile)
            os.rename (dummyFile, base_dummy + ".bin")
        except FileExistsError:
            os.remove (base_dummy + '.bin')
            os.rename (dummyFile, base_dummy + ".bin")

    progressBar['value'] += 20
    root.update()

    try:
        os.mkdir(os.getcwd() + "\\MusicMod\\")
    except:
        pass

    if os.path.isfile(os.getcwd() + "\\MusicMod\\BGM2.acb") == False:
        shutil.copy(config["SoundDirectory"] + "\\BGM2.acb", os.getcwd() + "\\MusicMod\\BGM2.acb")
    if os.path.isfile(os.getcwd() + "\\MusicMod\\BGM2.awb") == False:
        shutil.copy(config["SoundDirectory"] + "\\BGM2.awb", os.getcwd() + "\\MusicMod\\BGM2.awb")

    customMusic = base_file + '.bin'  
    sonicAudioToolsFolderCreation = os.getcwd() + '\\SonicAudioTools\\AcbEditor.exe ' + os.getcwd() + "\\MusicMod\\BGM2.acb"
    sonicAudioToolsMuiscReplacement = os.getcwd() + '\\SonicAudioTools\\AcbEditor.exe ' + os.getcwd() + "\\MusicMod\\BGM2"

    if os.path.isdir(os.getcwd() + '\\MusicMod\\BGM2\\') == False:
        os.system (sonicAudioToolsFolderCreation)
        time.sleep(1)
        shutil.move(customMusic, os.getcwd() + '\\MusicMod\\BGM2\\' + customMusic)
        try:
            shutil.move(f"{dummyFileNumber:05}"'_streaming.bin', os.getcwd() + '\\MusicMod\\BGM2\\' + f"{dummyFileNumber:05}"'_streaming.bin')
        except FileNotFoundError:
            pass
    else:
        shutil.move(customMusic, os.getcwd() + '\\MusicMod\\BGM2\\' + customMusic)
        try:
            shutil.move(f"{dummyFileNumber:05}"'_streaming.bin', os.getcwd() + '\\MusicMod\\BGM2\\' + f"{dummyFileNumber:05}"'_streaming.bin')
        except FileNotFoundError:
            pass

    os.system (sonicAudioToolsMuiscReplacement)
    shutil.rmtree (os.getcwd() + "\\MusicMod\\BGM2")
    progressBar['value'] += 20
    root.update()

    if os.path.isdir(os.getcwd() + '\\CustomMusic') == False:
        os.mkdir (os.getcwd() + '\\CustomMusic')

    trackTuple = os.path.split(VGAudioCliArgs)
    trackName = str(trackTuple[1])
    
    shutil.move(VGAudioCliArgs, os.getcwd() + '\\CustomMusic\\' + trackName)
    trackDirectory = '\\CustomMusic\\' + trackName

    if os.path.isdir(os.getcwd() + '\\CustomMusic\\LooperOutput') == True:
        shutil.rmtree (os.getcwd() + '\\CustomMusic\\LooperOutput')

    if manualLoop.get() == 0:
        subprocess.call(['C:\\windows\\system32\\cmd.exe', '/C', 'pymusiclooper export-points --alt-export-top 0 --export-to txt --path ', os.getcwd() + trackDirectory])

        word_list = open(os.getcwd() + '\\CustomMusic\\LooperOutput\\loops.txt').read().split()

        try:
            startingLoopSamples = int(word_list[0])
            startingLoopHex = startingLoopSamples.to_bytes(3, "big")
        except OverflowError:
            os.remove (os.getcwd() + '\\CustomMusic\\' + trackName)
            errorMessage = Messagebox.show_error("Song was too long, please select a different song or manually input the looping points", "Error")
        except:
            errorMessage = Messagebox.show_error("Something went wrong, is the file name in English?", "Error")

        try:
            endingLoopSamples = int(word_list[1])
            endingLoopHex = endingLoopSamples.to_bytes(3, "big")
        except OverflowError:
            os.remove (os.getcwd() + '\\CustomMusic\\' + trackName)
            errorMessage = Messagebox.show_error("Song was too long, please select a different song or manually input the looping points", "Error")
        
    else:
        try:
            startingLoopSamples = int(startEntry.get())
            startingLoopHex = startingLoopSamples.to_bytes(3, "big")
        except OverflowError:
            os.remove (os.getcwd() + '\\CustomMusic\\' + trackName)
            errorMessage = Messagebox.show_error("Song was too long, please select a different song or manually input the looping points", "Error")
        except:
            errorMessage = Messagebox.show_error("Something went wrong, is the file name in English?", "Error")

        try:
            endingLoopSamples = int(endEntry.get())
            endingLoopHex = endingLoopSamples.to_bytes(3, "big")
        except OverflowError:
            os.remove (os.getcwd() + '\\CustomMusic\\' + trackName)
            errorMessage = Messagebox.show_error("Song was too long, please select a different song or manually input the looping points", "Error")

    startItems = []

    for sValue in startingLoopHex:
        startItems.append( f'\\x{sValue:02x}' )

    startHex = "".join(startItems)

    
    progressBar['value'] += 20
    root.update()
    endItems = []

    for eValue in endingLoopHex:
        endItems.append( f'\\x{eValue:02x}' )

    endHex = "".join(endItems)
    startSearch = startHex.encode()

    #bytelist
    if songNumber == 0:
        pass
    elif songNumber == 1:
        startByteLocationOne = 90443
        endByteLocationOne = 8496
        endByteLocationTwo = 90447
    elif songNumber == 2:
        pass
    elif songNumber == 3:
        startByteLocationOne = 90541
        endByteLocationOne = 8524
        endByteLocationTwo = 90455
    elif songNumber == 4:
        startByteLocationOne = 90459
        endByteLocationOne = 8538
        endByteLocationTwo = 90463
    elif songNumber == 5:
        startByteLocationOne = 90467
        endByteLocationOne = 8552
        endByteLocationTwo = 90471
    elif songNumber == 6:
        startByteLocationOne = 90475
        endByteLocationOne = 8566
        endByteLocationTwo = 90479
    elif songNumber == 7:
        startByteLocationOne = 90483
        endByteLocationOne = 8580
        endByteLocationTwo = 90487
    elif songNumber == 8:
        startByteLocationOne = 90491
        endByteLocationOne = 8594
        endByteLocationTwo = 90495
    elif songNumber == 9:
        startByteLocationOne = 90499
        startByteLocationTwo = 90507
        endByteLocationOne = 8608
        endByteLocationTwo = 8623
        endByteLocationThree = 90503
        endByteLocationFour = 90512
    elif songNumber == 10:
        startByteLocationOne = 90499
        startByteLocationTwo = 90507
        endByteLocationOne = 8608
        endByteLocationTwo = 8623
        endByteLocationThree = 90503
        endByteLocationFour = 90512
    elif songNumber == 11:
        startByteLocationOne = 90515
        endByteLocationOne = 8636
        endByteLocationTwo = 90519
    elif songNumber == 12:
        startByteLocationOne = 90523
        endByteLocationOne = 8650
        endByteLocationTwo = 90527
    elif songNumber == 13:
        startByteLocationOne = 90531
        endByteLocationOne = 8664
        endByteLocationTwo = 90535
    elif songNumber == 14:
        pass
    elif songNumber == 15:
        startByteLocationOne = 90539
        endByteLocationOne = 8692
        endByteLocationTwo = 90543
    elif songNumber == 16:
        startByteLocationOne = 90547
        endByteLocationOne = 8706
        endByteLocationTwo = 90550
    elif songNumber == 17:
        startByteLocationOne = 90555
        startByteLocationTwo = 90563
        endByteLocationOne = 8720
        endByteLocationTwo = 8734
        endByteLocationThree = 90559
        endByteLocationFour = 90567
    elif songNumber == 18:
        startByteLocationOne = 90555
        startByteLocationTwo = 90563
        endByteLocationOne = 8720
        endByteLocationTwo = 8734
        endByteLocationThree = 90559
        endByteLocationFour = 90567
    elif songNumber == 19:
        startByteLocationOne = 90571
        endByteLocationOne = 8748
        endByteLocationTwo = 90575
    elif songNumber == 20:
        startByteLocationOne = 90579
        startByteLocationTwo = 90587
        endByteLocationOne = 8762
        endByteLocationTwo = 8776
        endByteLocationThree = 90583
        endByteLocationFour = 90591
    elif songNumber == 21:
        startByteLocationOne = 90579
        startByteLocationTwo = 90587
        endByteLocationOne = 8762
        endByteLocationTwo = 8776
        endByteLocationThree = 90583
        endByteLocationFour = 90591
    elif songNumber == 22:
        startByteLocationOne = 90595
        endByteLocationOne = 8790
        endByteLocationTwo = 90599
    elif songNumber == 23:
        startByteLocationOne = 90603
        endByteLocationOne = 8804
        endByteLocationTwo = 90606
    elif songNumber == 24:
        startByteLocationOne = 90611
        endByteLocationOne = 8818
        endByteLocationTwo = 90615
    elif songNumber == 25:
        startByteLocationOne = 90915
        endByteLocationOne = 9490
        endByteLocationTwo = 90919
    elif songNumber == 26:
        startByteLocationOne = 90907
        endByteLocationOne = 9476
        endByteLocationTwo = 90910
    elif songNumber == 27:
        startByteLocationOne = 90899
        endByteLocationOne = 9462
        endByteLocationTwo = 90903
    elif songNumber == 28:
        startByteLocationOne = 90619
        endByteLocationOne = 8832
        endByteLocationTwo = 90623
    elif songNumber == 29:
        startByteLocationOne = 90923
        startByteLocationTwo = 90931
        endByteLocationOne = 9504
        endByteLocationTwo = 9518
        endByteLocationThree = 90927
        endByteLocationFour = 90935
    elif songNumber == 30:
        startByteLocationOne = 90923
        startByteLocationTwo = 90931
        endByteLocationOne = 9504
        endByteLocationTwo = 9518
        endByteLocationThree = 90927
        endByteLocationFour = 90935
    elif songNumber == 31:
        startByteLocationOne = 90939
        endByteLocationOne = 9532
        endByteLocationTwo = 90943
    elif songNumber == 32:
        pass
    elif songNumber == 33:
        startByteLocationOne = 90627
        endByteLocationOne = 8860
        endByteLocationTwo = 90631
    elif songNumber == 34:
        startByteLocationOne = 90635
        endByteLocationOne = 8874
        endByteLocationTwo = 90639
    elif songNumber == 35:
        pass
    elif songNumber == 36:
        startByteLocationOne = 90643
        endByteLocationOne = 8902
        endByteLocationTwo = 90647
    elif songNumber == 37:
        startByteLocationOne = 90651
        endByteLocationOne = 8916
        endByteLocationTwo = 90655
    elif songNumber == 38:
        startByteLocationOne = 90659
        endByteLocationOne = 8930
        endByteLocationTwo = 90663
    elif songNumber == 39:
        startByteLocationOne = 90667
        endByteLocationOne = 8944
        endByteLocationTwo = 90671
    elif songNumber == 40:
        startByteLocationOne = 90683
        startByteLocationTwo = 90955
        endByteLocationOne = 8972
        endByteLocationTwo = 9560
        endByteLocationThree = 90687
        endByteLocationFour = 90959
    elif songNumber == 41:
        startByteLocationOne = 90683
        startByteLocationTwo = 90955
        endByteLocationOne = 8972
        endByteLocationTwo = 9560
        endByteLocationThree = 90687
        endByteLocationFour = 90959
    elif songNumber == 42:
        startByteLocationOne = 90691
        endByteLocationOne = 8986
        endByteLocationTwo = 90695
    elif songNumber == 43:
        startByteLocationOne = 90699
        endByteLocationOne = 9000
        endByteLocationTwo = 90703
    elif songNumber == 44:
        startByteLocationOne = 90707
        endByteLocationOne = 9014
        endByteLocationTwo = 90711
    elif songNumber == 45:
        startByteLocationOne = 90715
        endByteLocationOne = 9028
        endByteLocationTwo = 90719
    elif songNumber == 46:
        startByteLocationOne = 90731
        endByteLocationOne = 9056
        endByteLocationTwo = 90735
    elif songNumber == 47:
        startByteLocationOne = 90963
        endByteLocationOne = 9574
        endByteLocationTwo = 90967
    elif songNumber == 48:
        pass
    elif songNumber == 49:
        pass
    elif songNumber == 50:
        startByteLocationOne = 90739
        endByteLocationOne = 9084
        endByteLocationTwo = 90743
    elif songNumber == 51:
        startByteLocationOne = 90947
        endByteLocationOne = 9546
        endByteLocationTwo = 90951
    elif songNumber == 52:
        pass
    elif songNumber == 53:
        startByteLocationOne = 90747
        startByteLocationTwo = 90971
        endByteLocationOne = 9112
        endByteLocationTwo = 90751
        endByteLocationThree = 90975
    elif songNumber == 54:
        pass
    elif songNumber == 55:
        startByteLocationOne = 90755
        endByteLocationOne = 9126
        endByteLocationTwo = 90759
    elif songNumber == 56:
        startByteLocationOne = 90763
        endByteLocationOne = 9140
        endByteLocationTwo = 90767
    elif songNumber == 57:
        startByteLocationOne = 90771
        endByteLocationOne = 9154
        endByteLocationTwo = 90775
    elif songNumber == 58:
        startByteLocationOne = 90779
        startByteLocationTwo = 90787
        endByteLocationOne = 9168
        endByteLocationTwo = 9182
        endByteLocationThree = 90783
        endByteLocationFour = 90791
    elif songNumber == 59:
        startByteLocationOne = 90779
        startByteLocationTwo = 90787
        endByteLocationOne = 9168
        endByteLocationTwo = 9182
        endByteLocationThree = 90783
        endByteLocationFour = 90791
    elif songNumber == 60:
        startByteLocationOne = 90795
        endByteLocationOne = 9196
        endByteLocationTwo = 90799
    elif songNumber == 61:
        startByteLocationOne = 90803
        endByteLocationOne = 9210
        endByteLocationTwo = 90807
    elif songNumber == 62:
        pass
    elif songNumber == 63:
        startByteLocationOne = 90811
        endByteLocationOne = 9238
        endByteLocationTwo = 90815
    elif songNumber == 64:
        startByteLocationOne = 90819
        endByteLocationOne = 9252
        endByteLocationTwo = 90823
    elif songNumber == 65:
        pass
    elif songNumber == 66:
        startByteLocationOne = 90827
        endByteLocationOne = 9280
        endByteLocationTwo = 90831
    elif songNumber == 67:
        startByteLocationOne = 90835
        endByteLocationOne = 9294
        endByteLocationTwo = 90839
    elif songNumber == 68:
        startByteLocationOne = 90843
        endByteLocationOne = 9308
        endByteLocationTwo = 90847
    elif songNumber == 69:
        startByteLocationOne = 90851
        endByteLocationOne = 9322
        endByteLocationTwo = 90855
    elif songNumber == 70:
        startByteLocationOne = 90859
        startByteLocationTwo = 90867
        endByteLocationOne = 9336
        endByteLocationTwo = 9350
        endByteLocationThree = 90863
        endByteLocationFour = 90871
    elif songNumber == 71:
        startByteLocationOne = 90859
        startByteLocationTwo = 90867
        endByteLocationOne = 9336
        endByteLocationTwo = 9350
        endByteLocationThree = 90863
        endByteLocationFour = 90871
    elif songNumber == 72:
        startByteLocationOne = 90875
        startByteLocationTwo = 90883
        endByteLocationOne = 9364
        endByteLocationTwo = 9378
        endByteLocationThree = 90879
        endByteLocationFour = 90887
    elif songNumber == 73:
        startByteLocationOne = 90875
        startByteLocationTwo = 90883
        endByteLocationOne = 9364
        endByteLocationTwo = 9378
        endByteLocationThree = 90879
        endByteLocationFour = 90887
    elif songNumber == 74:
        pass
    elif songNumber == 75:
        pass
    elif songNumber == 76:
        startByteLocationOne = 90891
        endByteLocationOne = 9420
        endByteLocationTwo = 90895
    elif songNumber == 77:
        startByteLocationOne = 90724
        endByteLocationOne = 9042
        endByteLocationTwo = 90727
    elif songNumber == 78:
        startByteLocationOne = 90979
        endByteLocationOne = 9616
        endByteLocationTwo = 90983
    elif songNumber == 79:
        startByteLocationOne = 90987
        endByteLocationOne = 9630
        endByteLocationTwo = 90991
    elif songNumber == 80:
        startByteLocationOne = 90995
        endByteLocationOne = 9644
        endByteLocationTwo = 90999
    elif songNumber == 81:
        pass
    elif songNumber == 82:
        pass

    with open(os.getcwd() + "\\MusicMod\\BGM2.acb", 'rb+') as f:
        try:
            f.seek(startByteLocationOne)
            f.write(startingLoopHex) 
        except NameError:
            pass
        try:
            f.seek(startByteLocationTwo)
            f.write(startingLoopHex)
        except NameError:
            pass
        try:
            f.seek(endByteLocationOne)
            f.write(endingLoopHex) 
        except NameError:
            pass
        try:
            f.seek(endByteLocationTwo)
            f.write(endingLoopHex) 
        except NameError:
            pass
        try:
            f.seek(endByteLocationThree)
            f.write(endingLoopHex) 
        except NameError:
            pass
        try:
            f.seek(endByteLocationFour)
            f.write(endingLoopHex) 
        except NameError:
            pass
    progressBar['value'] += 20
    root.update()
    finishedMessage = Messagebox.ok("File Replacement complete!", "Success")
    os.remove (newAudio)

def loopChecker ():
    if manualLoop.get() == 1:
        progressBar.pack_forget()
        musicSwap_button.pack_forget()
        startEntryLabel.pack()
        startEntry.pack()
        endEntryLabel.pack()
        endEntry.pack()
        musicSwap_button.pack()
        musicSwap_button.pack(pady=20)
        progressBar.pack()
    else:
        startEntry.pack_forget()
        endEntry.pack_forget()
        startEntryLabel.pack_forget()
        endEntryLabel.pack_forget()

def browseFile():
    root.filename = filedialog.askopenfilename(title = "Select a music file", filetypes = [("Audio Files", "*.mp3 *.wav")])
    global fullPath
    fullPath = root.filename
    songOnly = os.path.split(root.filename)
    browsedFile.config(text = songOnly[1])

def showInfo():
    Messagebox.ok("Welcome to Melody Bay!\nStep 1: Obtain the music you'd like to use in game & put it next to Melody Bay\nStep 2: Select the music you'd like to replace\nStep 3:Select the music you'd like to use via the Browse Custom Music File button.\nStep 4: if you need to, check Input Looping Points Manually (a lot of songs don't require this)\nStep 5: click Add My Custom Music!\nWith that you're done and put take the Switch folder from the MusicMod folder and replace it with the one in your Switch Direcotry! (if it isn't there recreate the directory structure to the Switch folder!)\nIf you have music that happens to not loop properly I highly encourage inputting the looping points manually in Samples. You can find the samples via an audio app such as Audacity.\n Currently this application does NOT support combo music, you can look forward to that in a future update!\nFor Emulators same idea, but it goes into your mods folder\nIf you'd like more information you can contact me on Twitter/Discord/GameBanana/Github, Username: Joshua_A_Daniel", "How to")

SMRPGText = tb.Label(text="Select the Music you'd like to replace", bootstyle="default")
SMRPGText.pack(pady=(20, 10))
songCombo = tb.Combobox(root, bootstyle = "success", width = 40, values = songList)
songCombo.pack(pady=0)
songCombo.current(0)

browse = tb.Button(text="Browse Custom Music File", bootstyle="primary", command = browseFile)
browse.pack(pady=20)

#Labels
browsedFile = tb.Label(text="No File Currently Selected", bootstyle="default",)
browsedFile.pack(pady=(0, 0))

startEntryLabel = tb.Label(text="Enter Starting loop in Samples", bootstyle="default")
endEntryLabel = tb.Label(text="Enter Ending loop in Samples", bootstyle="default")

#Roundtoggle
manualLoop = IntVar()
checkloopstyle = tb.Checkbutton(bootstyle="success, round-toggle", text="Input Looping Points Manually", variable = manualLoop, onvalue = 1, offvalue = 0, command = loopChecker)
checkloopstyle.pack (pady=(20, 0))

#Entrylabels
startEntry = tb.Entry(root)
endEntry = tb.Entry(root)

#Buttons
musicSwap_button = tb.Button(text="Add My Custom Music!", bootstyle="success", command = startSwapMusic_in_bg)
musicSwap_button.pack(pady=10)


#Progress bar
progressBar = tb.Progressbar(root, bootstyle='success striped', maximum = 100, length = 200, value = 0)
progressBar.pack(pady = 20)

#ChoosePathButton
choose_path_button = tb.Button(text = "Choose Sound Path", bootstyle="default", command = chooseSoundPath)
choose_path_button.pack(side=BOTTOM, anchor="e")

#InfoButton
info_Button = tb.Button(text = "How to use Melody Bay", bootstyle="default", command = showInfo)
info_Button.pack(side=BOTTOM, anchor="e", pady=10)

root.mainloop()