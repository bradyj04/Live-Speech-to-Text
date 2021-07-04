import os.path
import PySimpleGUI as sg
import pyaudio
pa = pyaudio.PyAudio()
import wave

# Button Fonts/Settings
RecordButton = sg.Button('Record', key='Record', button_color="dark red", font=("Sans Serif", 12, "bold"), size=(10, 2))
StopButton = sg.Button('Stop', key='Stop', button_color='black', font=("Sans Serif", 12, "bold"), size=(10, 2))
ExitButton = sg.Button('Exit', key='Exit', button_color='red', font=("Sans Serif", 12, "bold"), size=(10, 2))
# Test loading icon - RecordingIcon = sg.popup_animated("LoadingIcon.gif")

# Defines function FileLabel, and sets text as what's defined to the right in ()
def FileLabel(text):
    return sg.Text(text + ':', justification="center", size=(10, 1))

# Configures layout of window
layout = [[sg.Text("Speech-to-Text", font=('Calibri', 13, 'bold'))],
          [sg.Text('                            ', key = 'Status', font=('Sans Serif', 10, 'italic'))],
          [FileLabel('Audio File'), sg.Input(key='InputFolder'), sg.FileBrowse(target='InputFolder')],
          [sg.Text('Recording Length:'), sg.Input]
          [RecordButton, StopButton, ExitButton]]
# Creates the window
window = sg.Window('Speech-to-Text by Brady', layout, element_justification="center", finalize=True)

#Setup PyAudio and Wave
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 1
WAVE_OUTPUT_FILENAME = "recorded.wav"
stream = pa.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
frames = []

# Display and interact with the Window
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == 'Exit':
        break
    # Changes what each Button Displays, depending on if audio is recording or not
    if event == 'Record':
        # Updates text to match status Recording
        window['Record'].update('Recording')
        window['Status'].update('Recording...')
        # Record function goes here
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            RECORD_SECONDS += 1
            data = stream.read(CHUNK)
            frames.append(data)

    if event == 'Stop':
        # Updates text to match status Stop
        window["Record"].update('Record')
        window['Status'].update('Stopped')
        # Stop record function goes here
        try:
        #Stops recording the audio stream
            stream.stop_stream()
            stream.close()
            pa.terminate()
            wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(pa.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            wf.close()
        #Gets the path to recorded file and updates the file input
            filepath = os.path.abspath('recorded.wav')
            window['InputFolder'].update(filepath)
        finally:
            window['Status'].update('Stopped')

# Closes Window
window.close()
