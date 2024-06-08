# Audify: a seismic data sonifycation tool.
## Welcome to audify.
Audify is a python program desighned to make seismic data audible to the human ear.
The process of audifycation or sonification envolves infrasound or very low frequency data being turned into sound that we can hear.
The process usually consists of speeding up the data by a given speed factor.
E.G. A seismic trace with a sampling frequency of 100 HZ can be sped up 160 times to give it a new sampling rate of 16000 HZ or 16 KHZ.
## Installation.
To get this script, simpley execute the following from a terminal.
```bash
git clone https://github.com/Donavin97/audify.git
cd audify
```
Make sure that the required libraries are installed:
```bash
pip install obspy argparse
```
###Usage.
To use the script, do the following:
```bash
python audify.py -h
```
This will print a help message to the console, explaining the various parameters of the program.
as a simple example, we will an Mww6.2 earthquake that took place in the Prince Edward Islands Region, South of South Africa on 31 May 2024.
```bash
python audify.py -C iris -n GT -s BOSA -l "*" -c BHZ -S 160 -t "2024-05-31 15:30~2024-05-31 16:30" -f 0.5 -F 20.0 -o output.wav
```
This will creat a WAV audio file of the earthquake in the current directory called output.wav.
The file containes the sped up seismic data for the selected timeframe and any earthquakes that might have been detected by the selected station.
#Contributing.
If you would like to contribute to the project, you are more than welcome to do so.
Any contributions are welcomed.
If you find any issues, please open issues on Github.
Pull requests are also very welcom.

