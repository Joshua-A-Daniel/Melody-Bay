# MelodyBay Alpha v1.0

This tool allows you to very quickly and easily switch the music in Super Mario RPG Remake.

A short tutorial will be provided in the near future but it's a fairly simple program. Just download and run the Exe and you'll be given instructions. Modded files will be in the MusicMod folder while your custom music that you selected will move to the Custom Music folder

This program relys on FFMpeg (Which you'll need to install if you don't have it. Google + Youtube is your friend here), SonicAudioTools & VGAudioCli which are included within the package.

It also relys on another program made in python called "PyMusicLooper" which detects loop points for music files. It needs to be downloaded via python for automatic looping to work. It can be found here: https://github.com/arkrow/PyMusicLooper

Songs will attempt to automatically loop but there is an option to manually put in the looping points of a song via samples. Most songs from my testing loop seamlessly.

Only requirements from the user are:
1. A song you'd like to loop
2. FFMpeg being properly installed
3. A folder structure that doesn't contain spaces

This is my first ever program so the code likely need work and will be updated as I continue to learn more. 
