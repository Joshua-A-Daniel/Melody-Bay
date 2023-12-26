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
    wavFile = os.getcwd() + slash + trackNoExt + ".wav"
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
        duration = 30.0 # seconds
        frequency = 440.0 # hertz
        obj = wave.open('sound.wav','w')
        obj.setnchannels(1) # mono
        obj.setsampwidth(2)
        obj.setframerate(sampleRate)
        for i in range(99999):
            value = 99
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

    if os.path.isdir(os.getcwd() + '\\LooperOutput') == True:
        shutil.rmtree (os.getcwd() + '\\LooperOutput')

    print (wavFile)

    if manualLoop.get() == 0:
        subprocess.call(['C:\\windows\\system32\\cmd.exe', '/C', 'pymusiclooper export-points --alt-export-top 0 --export-to txt --path ', wavFile])
        time.sleep(1)
        word_list = open(os.getcwd() + '\\LooperOutput\\loops.txt').read().split()

        try:
            startingLoopSamples = int(word_list[0])
            startingLoopHex = startingLoopSamples.to_bytes(4, "big")
        except OverflowError:
            os.remove (os.getcwd() + '\\CustomMusic\\' + trackName)
            errorMessage = Messagebox.show_error("Song was too long, please select a different song or manually input the looping points", "Error")
        except:
            errorMessage = Messagebox.show_error("Something went wrong, is the file name in English?", "Error")

        try:
            endingLoopSamples = int(word_list[1])
            endingLoopHex = endingLoopSamples.to_bytes(4, "big")
        except OverflowError:
            os.remove (os.getcwd() + '\\CustomMusic\\' + trackName)
            errorMessage = Messagebox.show_error("Song was too long, please select a different song or manually input the looping points", "Error")
        
    else:
        try:
            startingLoopSamples = int(startEntry.get())
            startingLoopHex = startingLoopSamples.to_bytes(4, "big")
        except OverflowError:
            os.remove (os.getcwd() + '\\CustomMusic\\' + trackName)
            errorMessage = Messagebox.show_error("Song was too long, please select a different song or manually input the looping points", "Error")
        except:
            errorMessage = Messagebox.show_error("Something went wrong, is the file name in English?", "Error")

        try:
            endingLoopSamples = int(endEntry.get())
            endingLoopHex = endingLoopSamples.to_bytes(4, "big")
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
        startByteLocationOne = 90442
        endByteLocationOne = 8495
        endByteLocationTwo = 90446
    elif songNumber == 2:
        pass
    elif songNumber == 3:
        startByteLocationOne = 90450
        endByteLocationOne = 8523
        endByteLocationTwo = 90454
    elif songNumber == 4:
        startByteLocationOne = 90458
        endByteLocationOne = 8537
        endByteLocationTwo = 90462
    elif songNumber == 5:
        startByteLocationOne = 90466
        endByteLocationOne = 8551
        endByteLocationTwo = 90470
    elif songNumber == 6:
        startByteLocationOne = 90474
        endByteLocationOne = 8565
        endByteLocationTwo = 90478
    elif songNumber == 7:
        startByteLocationOne = 90482
        endByteLocationOne = 8579
        endByteLocationTwo = 90486
    elif songNumber == 8:
        startByteLocationOne = 90490
        endByteLocationOne = 8593
        endByteLocationTwo = 90494
   
    elif songNumber == 9:
        startByteLocationOne = 90498
        startByteLocationTwo = 90506
        endByteLocationOne = 8607
        endByteLocationTwo = 8621
        endByteLocationThree = 90502
        endByteLocationFour = 90510
    elif songNumber == 10:
        startByteLocationOne = 90498
        startByteLocationTwo = 90506
        endByteLocationOne = 8607
        endByteLocationTwo = 8621
        endByteLocationThree = 90502
        endByteLocationFour = 90510
    elif songNumber == 11:
        startByteLocationOne = 90514
        endByteLocationOne = 8635
        endByteLocationTwo = 90518
    elif songNumber == 12:
        startByteLocationOne = 90522
        endByteLocationOne = 8649
        endByteLocationTwo = 90526
    elif songNumber == 13:
        startByteLocationOne = 90531
        endByteLocationOne = 8663
        endByteLocationTwo = 90534
    elif songNumber == 14:
        pass
    elif songNumber == 15:
        startByteLocationOne = 90538
        endByteLocationOne = 8691
        endByteLocationTwo = 90542
    elif songNumber == 16:
        startByteLocationOne = 90547
        endByteLocationOne = 8705
        endByteLocationTwo = 90550
    elif songNumber == 17:
        startByteLocationOne = 90554
        startByteLocationTwo = 90562
        endByteLocationOne = 8719
        endByteLocationTwo = 8733
        endByteLocationThree = 90558
        endByteLocationFour = 90566
    elif songNumber == 18:
        startByteLocationOne = 90554
        startByteLocationTwo = 90562
        endByteLocationOne = 8719
        endByteLocationTwo = 8733
        endByteLocationThree = 90558
        endByteLocationFour = 90566
    elif songNumber == 19:
        startByteLocationOne = 90570
        endByteLocationOne = 8747
        endByteLocationTwo = 90574
    elif songNumber == 20:
        startByteLocationOne = 90578
        startByteLocationTwo = 90586
        endByteLocationOne = 8761
        endByteLocationTwo = 8775
        endByteLocationThree = 90582
        endByteLocationFour = 90590
    elif songNumber == 21:
        startByteLocationOne = 90578
        startByteLocationTwo = 90586
        endByteLocationOne = 8761
        endByteLocationTwo = 8775
        endByteLocationThree = 90582
        endByteLocationFour = 90590
    elif songNumber == 22:
        startByteLocationOne = 90594
        endByteLocationOne = 8789
        endByteLocationTwo = 90598
    elif songNumber == 23:
        startByteLocationOne = 90602
        endByteLocationOne = 8803
        endByteLocationTwo = 90606
    elif songNumber == 24:
        startByteLocationOne = 90610
        endByteLocationOne = 8817
        endByteLocationTwo = 90614
    elif songNumber == 25:
        startByteLocationOne = 90914
        endByteLocationOne = 9489
        endByteLocationTwo = 90918
    elif songNumber == 26:
        startByteLocationOne = 90906
        endByteLocationOne = 9475
        endByteLocationTwo = 90910
    elif songNumber == 27:
        startByteLocationOne = 90898
        endByteLocationOne = 9461
        endByteLocationTwo = 90902
    elif songNumber == 28:
        startByteLocationOne = 90618
        endByteLocationOne = 8831
        endByteLocationTwo = 90622
    elif songNumber == 29:
        startByteLocationOne = 90922
        startByteLocationTwo = 90930
        endByteLocationOne = 9503
        endByteLocationTwo = 9517
        endByteLocationThree = 90926
        endByteLocationFour = 90934
    elif songNumber == 30:
        startByteLocationOne = 90922
        startByteLocationTwo = 90930
        endByteLocationOne = 9503
        endByteLocationTwo = 9517
        endByteLocationThree = 90926
        endByteLocationFour = 90934
    elif songNumber == 31:
        startByteLocationOne = 90938
        endByteLocationOne = 9531
        endByteLocationTwo = 90942
    elif songNumber == 32:
        pass
    elif songNumber == 33:
        startByteLocationOne = 90626
        endByteLocationOne = 8859
        endByteLocationTwo = 90630
    elif songNumber == 34:
        startByteLocationOne = 90634
        endByteLocationOne = 8873
        endByteLocationTwo = 90638
    elif songNumber == 35:
        pass
    elif songNumber == 36:
        startByteLocationOne = 90642
        endByteLocationOne = 8901
        endByteLocationTwo = 90646
    elif songNumber == 37:
        startByteLocationOne = 90650
        endByteLocationOne = 8915
        endByteLocationTwo = 90654
    elif songNumber == 38:
        startByteLocationOne = 90658
        endByteLocationOne = 8929
        endByteLocationTwo = 90662
    elif songNumber == 39:
        startByteLocationOne = 90666
        endByteLocationOne = 8943
        endByteLocationTwo = 90670
    elif songNumber == 40:
        startByteLocationOne = 90682
        startByteLocationTwo = 90954
        endByteLocationOne = 8971
        endByteLocationTwo = 9559
        endByteLocationThree = 90686
        endByteLocationFour = 90958
    elif songNumber == 41:
        startByteLocationOne = 90682
        startByteLocationTwo = 90954
        endByteLocationOne = 8971
        endByteLocationTwo = 9559
        endByteLocationThree = 90686
        endByteLocationFour = 90958
    elif songNumber == 42:
        startByteLocationOne = 90690
        endByteLocationOne = 8985
        endByteLocationTwo = 90694
    elif songNumber == 43:
        startByteLocationOne = 90698
        endByteLocationOne = 8999
        endByteLocationTwo = 90702
    elif songNumber == 44:
        startByteLocationOne = 90706
        endByteLocationOne = 9013
        endByteLocationTwo = 90710
    elif songNumber == 45:
        startByteLocationOne = 90714
        endByteLocationOne = 9027
        endByteLocationTwo = 90718
    elif songNumber == 46:
        startByteLocationOne = 90730
        endByteLocationOne = 9055
        endByteLocationTwo = 90734
    elif songNumber == 47:
        startByteLocationOne = 90962
        endByteLocationOne = 9573
        endByteLocationTwo = 90966
    elif songNumber == 48:
        pass
    elif songNumber == 49:
        pass
    elif songNumber == 50:
        startByteLocationOne = 90738
        endByteLocationOne = 9083
        endByteLocationTwo = 90742
    elif songNumber == 51:
        startByteLocationOne = 90946
        endByteLocationOne = 9545
        endByteLocationTwo = 90950
    elif songNumber == 52:
        pass
    elif songNumber == 53:
        startByteLocationOne = 90746
        startByteLocationTwo = 90970
        endByteLocationOne = 9111
        endByteLocationTwo = 90750
        endByteLocationThree = 90974
    elif songNumber == 54:
        pass
    elif songNumber == 55:
        startByteLocationOne = 90754
        endByteLocationOne = 9125
        endByteLocationTwo = 90758
    elif songNumber == 56:
        startByteLocationOne = 90762
        endByteLocationOne = 9139
        endByteLocationTwo = 90766
    elif songNumber == 57:
        startByteLocationOne = 90770
        endByteLocationOne = 9153
        endByteLocationTwo = 90774
    elif songNumber == 58:
        startByteLocationOne = 90778
        startByteLocationTwo = 90786
        endByteLocationOne = 9167
        endByteLocationTwo = 9181
        endByteLocationThree = 90782
        endByteLocationFour = 90790
    elif songNumber == 59:
        startByteLocationOne = 90778
        startByteLocationTwo = 90786
        endByteLocationOne = 9167
        endByteLocationTwo = 9181
        endByteLocationThree = 90782
        endByteLocationFour = 90790
    elif songNumber == 60:
        startByteLocationOne = 90794
        endByteLocationOne = 9195
        endByteLocationTwo = 90798
    elif songNumber == 61:
        startByteLocationOne = 90802
        endByteLocationOne = 9209
        endByteLocationTwo = 90806
    elif songNumber == 62:
        pass
    elif songNumber == 63:
        startByteLocationOne = 90810
        endByteLocationOne = 9237
        endByteLocationTwo = 90814
    elif songNumber == 64:
        startByteLocationOne = 90818
        endByteLocationOne = 9251
        endByteLocationTwo = 90822
    elif songNumber == 65:
        pass
    elif songNumber == 66:
        startByteLocationOne = 90826
        endByteLocationOne = 9279
        endByteLocationTwo = 90830
    elif songNumber == 67:
        startByteLocationOne = 90834
        endByteLocationOne = 9293
        endByteLocationTwo = 90838
    elif songNumber == 68:
        startByteLocationOne = 90842
        endByteLocationOne = 9307
        endByteLocationTwo = 90846
    elif songNumber == 69:
        startByteLocationOne = 90850
        endByteLocationOne = 9321
        endByteLocationTwo = 90854
    elif songNumber == 70:
        startByteLocationOne = 90858
        startByteLocationTwo = 90866
        endByteLocationOne = 9335
        endByteLocationTwo = 9349
        endByteLocationThree = 90862
        endByteLocationFour = 90870
    elif songNumber == 71:
        startByteLocationOne = 90858
        startByteLocationTwo = 90866
        endByteLocationOne = 9335
        endByteLocationTwo = 9349
        endByteLocationThree = 90862
        endByteLocationFour = 90870
    elif songNumber == 72:
        startByteLocationOne = 90874
        startByteLocationTwo = 90882
        endByteLocationOne = 9363
        endByteLocationTwo = 9377
        endByteLocationThree = 90878
        endByteLocationFour = 90886
    elif songNumber == 73:
        startByteLocationOne = 90874
        startByteLocationTwo = 90882
        endByteLocationOne = 9363
        endByteLocationTwo = 9377
        endByteLocationThree = 90878
        endByteLocationFour = 90886
    elif songNumber == 74:
        pass
    elif songNumber == 75:
        pass
    elif songNumber == 76:
        startByteLocationOne = 90890
        endByteLocationOne = 9419
        endByteLocationTwo = 90894
    elif songNumber == 77:
        startByteLocationOne = 90723
        endByteLocationOne = 9041
        endByteLocationTwo = 90726
    elif songNumber == 78:
        startByteLocationOne = 90978
        endByteLocationOne = 9615
        endByteLocationTwo = 90982
    elif songNumber == 79:
        startByteLocationOne = 90986
        endByteLocationOne = 9629
        endByteLocationTwo = 90990
    elif songNumber == 80:
        startByteLocationOne = 44131
        startByteLocationTwo = 58430
        startByteLocationThree = 90995
        endByteLocationOne = 9643
        endByteLocationTwo = 90998
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
            f.seek(startByteLocationThree)
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
    Messagebox.ok("Welcome to Melody Bay!\nStep 1: Obtain the music you'd like to use in game & put it next to Melody Bay\nStep 2: Select the music you'd like to replace\nStep 3:Select the music you'd like to use via the Browse Custom Music File button.\nStep 4: if you need to, check Input Looping Points Manually (a lot of songs don't require this)\nStep 5: click Add My Custom Music!\nWith that you're done and put take the Switch folder from the MusicMod folder and replace it with the one in your Switch Direcotry! (if it isn't there recreate the directory structure to the Switch folder!)\nRequirements for this program to work include FFmpeg & PyMusiclooper. Other requirements are included in package!\nIf you have music that happens to not loop properly I highly encourage inputting the looping points manually in Samples. You can find the samples via an audio app such as Audacity.\nCurrently this application does NOT support combo music, you can look forward to that in a future update!\nFor Emulators same idea, but it goes into your mods folder\nIf you'd like more information you can contact me on Twitter/Discord/GameBanana/Github, Username: Joshua_A_Daniel", "How to")

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