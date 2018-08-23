import RPi.GPIO as GPIO
import subprocess
import time

SoundFontFile = "/usr/share/sounds/sf2/drumSoundFonts/PremierKit.sf2"
AiyBtnPin = 23
AiyLedPin = 25

def initFluidSynth(soundFonta):
    #start fluidsynth in the backround
    subprocess.Popen(["fluidsynth",
        "-is",
        "--audio-driver=alsa",
        "--gain=3",
        soundFont])

def attaachMidiToSynth(inputChannel, outputChannel):
    subprocess.Popen(["aconnect",
        inputChannel+":0",
        outputChannel+":0"])

def onMidiAttachBtn():
    initFluidSynth(SoundFontFile)
    time.sleep(7)
    attachMidiToSynth("20","128")

GPIO.setmode(GPIO.BCM)
GPIO.setup(AiyBtnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(AiyLedPin, GPIO.OUT)

while True:
    if GPIO.input(AiyBtnPin) == False:
        print("Button")
        GPIO.output(AiyLedPin, True)
        time.sleep(1)
    else:
        GPIO.output(AiyLedPin, False)
