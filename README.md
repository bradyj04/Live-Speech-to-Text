# Live Speech-to-Text

## *Internet access is currently required for this to work*
I recommend using the main branch, it is not the default but it is the most stable/up-to-date one, as dev is for me to test some things.

## Installation

There are two installtion methods for the modules needed to run the python file (Windows only)

- Install using the batch file located in the repo, it will install all the modules (as long as there are no errors.)
- Install the modules manually (if you experience issues with PyAudio installation, see the next section)
```bash
pip3 install SpeechRecognition
pip3 install wave
pip3 install PySimpleGUI
pip3 install pyaudio
pip3 install pocketsphinx
```
## Running the program
Find the location of SpeechToText.py, open your command prompt and type:
```bash
python.exe [directory]\SpeechtoText.py
```
The file should open, and save the audio file(s) generated in the same directory as the .py file.

## Windows .exe
If you have windows, you can download the .exe file to run it from:
[here](https://www.mediafire.com/file/qtsh7v8kmc1m7ie/executable.zip/file)

## Issues with PyAudio/PocketSphinx?
Run the following command in your command prompt/ python.exe file:
```python
python --version
```
Then find the corresponding version [here (for PyAudio)](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio) or [here (for PocketSphinx)](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pocketsphinx) and place this in your scripts folder of python (Generally C:\python38\Scripts)
Then run this command, but replace [your file] with what you have downloaded and placed into the scripts folder:
```bash
pip install C:\python38\Scripts\[your file].whl
```
