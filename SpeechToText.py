import os.path
import time
import PySimpleGUI as sg
import pyaudio
pa = pyaudio.PyAudio()
import wave
import speech_recognition as sr

# Button Fonts/Settings
RecordButton = sg.Button('Record', key='Record', button_color="dark red", font=("Sans Serif", 12, "bold"), size=(15, 2))
SubmitLength = sg.Button('Submit Length', key='Submit', button_color='grey', font=("Sans Serif", 10, "bold"), size=(15, 1))
ExitButton = sg.Button('Exit', key='Exit', button_color='red', font=("Sans Serif", 12, "bold"), size=(15, 2))
TranscriptText = sg.Multiline(size=(50,15), key='Transcript', justification='center')
# Defines function FileLabel, and sets text as what's defined to the right in ()
def FileLabel(text):
    return sg.Text(text + ':', justification="center", size=(10, 1))
def TimeElapsed(text):
    return sg.Text(text, justification='left',font=("Sans Serif", 10, "bold"))
#Configures speech recognition audio file
def AudioFilePath(filepath):
    global r
    global audiosource
    r = sr.Recognizer()
    with sr.AudioFile(filepath) as source:
        audiosource = r.record(source)
        return r, source, audiosource
WIT_KEY = "3LOWRYZO6UQ7JWONLAVWHN3DT7TU2ZXJ"

# Configures layout of window
layout = [[sg.Text("Speech-to-Text", font=('Calibri', 13, 'bold'))],
          [sg.Text('                                                                            ', key = 'Status', justification='center', font=('Sans Serif', 10, 'italic'))],
          [TimeElapsed('Time Set: '), sg.Text('0', key='TimeRemaining',size=(5, 1), justification='center',font=("Sans Serif", 10, "bold")), TimeElapsed('seconds')],
          [FileLabel('Audio File'), sg.Input(key='InputFolder', size=(40, 1))],
          [sg.Text('Recording Length:', justification='left'), sg.Input(key='AudioLengthInput', size=(30, 1), justification='left'), sg.Text('seconds', justification='left')],
          [SubmitLength],
          [RecordButton, ExitButton],
          [TranscriptText]]
# Creates the window
window = sg.Window('Speech-to-Text by Brady', layout, element_justification="center", finalize=True)
# Display and interact with the Window

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == 'Exit':
        break
    if event == 'Submit':
        try:
            AFlength = int(values['AudioLengthInput'])
            window['Status'].update('Length Updated')
            window['TimeRemaining'].update(AFlength)
        except:
            window['Status'].update('Length needed')

    # Changes what each Button Displays, depending on if audio is recording or not
    try:
        if event == 'Record':
            # Setup PyAudio and Wave
            CHUNK = 1024
            FORMAT = pyaudio.paInt16
            CHANNELS = 2
            RATE = 44100
            RECORD_SECONDS = AFlength
            WAVE_OUTPUT_FILENAME = "recorded.wav"
            stream = pa.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
            frames = []
            # Updates text to match status Recording
            window['Record'].update('Recording')
            window['Status'].update('Recording...')
            # Record function goes here
            RangeValue = RATE / CHUNK * RECORD_SECONDS
            for recording in range(0, int(RangeValue)):
                data = stream.read(CHUNK)
                frames.append(data)
                window.refresh()
            window['TimeRemaining'].update('0')
            window['AudioLengthInput'].update('0')
            window['Status'].update('Stopped')
            #Changes state after time limit
            # Updates text to match status Stop
            window['Record'].update('Record')
            window.refresh()
            # Stop record function goes here
            try:
                # Stops recording the audio stream
                stream.stop_stream()
                stream.close()
                pa.terminate()
                wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(pa.get_sample_size(FORMAT))
                wf.setframerate(RATE)
                wf.writeframes(b''.join(frames))
                wf.close()
                # Gets the path to recorded file and updates the file input
                filepath = os.path.abspath('recorded.wav')
                window['InputFolder'].update(filepath)
                #Updates TextBox with transcribed audio
                AudioFilePath(filepath)
                try:
                    window['Status'].update('Processing...')
                    window.refresh()
                    #Pastes transcribed text in text box and updates status
                    TranscribedText = r.recognize_wit(audiosource, key=WIT_KEY)
                    window.refresh()
                    window['Transcript'].update(TranscribedText)
                    time.sleep(1)
                    window['Status'].update('Audio Transcribed')
                except sr.UnknownValueError:
                    window['Status'].update('Wit.ai could not understand')
                except sr.RequestError as re:
                    window['Status'].update('Request Error: {}'.format(re))
            except:
                    window['Status'].update('Error, not recording')
    except:
        window['Status'].update('Length needed')
# Closes Window
window.close()