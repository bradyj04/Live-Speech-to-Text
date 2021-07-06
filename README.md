# Live Speech-to-Text

## Installation

There are two installtion methods for the modules needed to run the python file (Windows only)

- Install using the batch file located in the repo, it will install all the modules (as long as there are no errors.)
- Install the modules manually (if you experience issues with PyAudio installation, see the next section)
```bash
pip3 install SpeechRecognition
pip3 install wave
pip3 install PySimpleGUI
pip3 install pyaudio
```
## Issues with PyAudio?
Run the following command in your command prompt/ python.exe file:
```python
python --version
```
Then find the corresponding version [here
