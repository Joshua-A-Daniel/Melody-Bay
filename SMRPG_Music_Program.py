import sys
import os
import shutil
import time
import pyinputplus as pyip
import subprocess

while True:
    songList = []

    print ("Which song would you like to replace? Enter in the song #")
    with open('SongList.txt') as my_file:
        for line in my_file:
            songList.append(line)

    for i, ele in enumerate(songList):
        songList[i] = ele.replace("\n", '')

    for index, songName in enumerate(songList):
        print(" " + songName)
    songNumber = pyip.inputNum(min=1, max=83) - 1
    print (songNumber)
    print ("You selected " + songList[songNumber])
    print ("Type the directory of your custom song to replace")
    while True:
        VGAudioCliArgs = input()
        if os.path.isfile(VGAudioCliArgs) == False:
            print ("Invalid file path")
            continue
        else:
            try:
                os.rename (VGAudioCliArgs, VGAudioCliArgs.replace(" ", "_"))
                VGAudioCliArgs = VGAudioCliArgs.replace(" ", "_")
                break
            except FileNotFoundError:
                print ("Place your Music files in the directory next to Melody Bay & try again")
                sys.exit()
    userTrack = os.path.split(VGAudioCliArgs)
    FilePath = str(userTrack[0])
    convertedTrack = str(userTrack[1])
    trackNoExt = convertedTrack.replace (".mp3", "")
    newAudio = os.getcwd() + '\\' + trackNoExt + '.wav'
    subprocess.call(['C:\\windows\\system32\\cmd.exe', '/C', 'ffmpeg -i ' + VGAudioCliArgs + " -ar 48000 " + newAudio])
    fileOutput = (f"{songNumber:05}"'_streaming.lopus')
    vgAudioCli = os.getcwd() + '\\vgaudio\\VGAudioCli.exe ' + '"' + newAudio + '" ' + '--bitrate ' + '"' + '96000' +'" ' + '--CBR ' + fileOutput
    os.system (vgAudioCli)
    print ("Converting Audio...")
    time.sleep(1)

    if os.path.isfile(fileOutput) == False:
        print ("Failed to convert audio file")
        sys.exit()
    else:
        try:
            base_file, ext = os.path.splitext(fileOutput)
            os.rename (fileOutput, base_file + ".bin")
            print ("Audio Conversion Sucessful!")
        except FileExistsError:
            os.remove (base_file + '.bin')
            os.rename (fileOutput, base_file + ".bin")

    try:
        os.mkdir(os.getcwd() + "\\MusicMod\\")
    except:
        pass

    if os.path.isfile(os.getcwd() + "\\MusicMod\\BGM2.acb") == False:
        shutil.copy(os.getcwd() + "\\Switch\\BGM2.acb", os.getcwd() + "\\MusicMod\\BGM2.acb")
    if os.path.isfile(os.getcwd() + "\\MusicMod\\BGM2.awb") == False:
        shutil.copy(os.getcwd() + "\\Switch\\BGM2.awb", os.getcwd() + "\\MusicMod\\BGM2.awb")

    customMusic = base_file + '.bin'  
    sonicAudioToolsFolderCreation = os.getcwd() + '\\SonicAudioTools\\AcbEditor.exe ' + os.getcwd() + "\\MusicMod\\BGM2.acb"
    sonicAudioToolsMuiscReplacement = os.getcwd() + '\\SonicAudioTools\\AcbEditor.exe ' + os.getcwd() + "\\MusicMod\\BGM2"

    if os.path.isdir(os.getcwd() + '\\MusicMod\\BGM2\\') == False:
        os.system (sonicAudioToolsFolderCreation)
        time.sleep(1)
        shutil.move(customMusic, os.getcwd() + '\\MusicMod\\BGM2\\' + customMusic)
    else:
        shutil.move(customMusic, os.getcwd() + '\\MusicMod\\BGM2\\' + customMusic)

    os.system (sonicAudioToolsMuiscReplacement)
    shutil.rmtree (os.getcwd() + "\\MusicMod\\BGM2")

    if os.path.isdir(os.getcwd() + '\\CustomMusic') == False:
        os.mkdir (os.getcwd() + '\\CustomMusic')

    trackTuple = os.path.split(VGAudioCliArgs)
    trackName = str(trackTuple[1])
    
    shutil.move(VGAudioCliArgs, os.getcwd() + '\\CustomMusic\\' + trackName)
    trackDirectory = '\\CustomMusic\\' + trackName

    if os.path.isdir(os.getcwd() + '\\CustomMusic\\LooperOutput') == True:
        shutil.rmtree (os.getcwd() + '\\CustomMusic\\LooperOutput')

    subprocess.call(['C:\\windows\\system32\\cmd.exe', '/C', 'pymusiclooper export-points --alt-export-top 0 --export-to txt --path ', os.getcwd() + trackDirectory])

    word_list = open(os.getcwd() + '\\CustomMusic\\LooperOutput\\loops.txt').read().split()

    startingLoopSamples = int(word_list[0])
    startingLoopHex = startingLoopSamples.to_bytes(3, "big")

    startItems = []

    for sValue in startingLoopHex:
        startItems.append( f'\\x{sValue:02x}' )

    startHex = "".join(startItems)

    endingLoopSamples = int(word_list[1])
    endingLoopHex = endingLoopSamples.to_bytes(3, "big")

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

    print ("File Replacement complete!")
    os.remove (newAudio)
   
    while True:
        prompt = 'Would you like to add in another custom song? (yes/no)\n'
        response = pyip.inputYesNo(prompt)
        if response == 'no':
            sys.exit()
        elif response == 'yes':
            break