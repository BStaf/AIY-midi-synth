import RPi.GPIO as GPIO
import subprocess
import time

SoundFontFile = "/usr/share/sounds/sf2/drumSoundFonts/PremierKit.sf2"
AiyBtnPin = 23
AiyLedPin = 25

def initFluidSynth(soundFont):
    #start fluidsynth in the backround
    subprocess.Popen(["fluidsynth",
        "-is",
        "--audio-driver=alsa",
        "--gain=3",
        soundFont])

def stopFluidSynth():
    subprocess.Popen(["sudo",
        "pkill",
        "fluidsynth"])

def connectMidiToSynth(inputChannel, outputChannel):
    try:
        out = subprocess.check_output(["aconnect",
            inputChannel+":0",
            outputChannel+":0"])
       # if out.contains("Connection Faild"):
        #    return false
    except:
        return False
    return True

def disconnectMidiSynth():
    subprocess.Popen(["aconnect",
        "-x"]);

def lightOn():
    GPIO.output(AiyLedPin, True)

def lightOff():
    GPIO.output(AiyLedPin, False)

def lightBlink(count):
    for x in range(count):
        GPIO.output(AiyLedPin, True)
        time.sleep(0.234)
        GPIO.output(AiyLedPin, False)
        time.sleep(0.234)

def onMidiAttachBtn(channel):
    stopFluidSynth()
    lightOff()
    print("Start FluidSynth")
    initFluidSynth(SoundFontFile)
    time.sleep(7)
    print("Attach Midi Device")
    if connectMidiToSynth("20","128"):
        print("connection ok")
        lightOn()
    else:
        print("connection failed")
        disconnectMidiSynth()
        stopFluidSynth()
        lightBlink(3)
    print("Done")

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(AiyBtnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(AiyLedPin, GPIO.OUT)

lightBlink(2)

#onMidiAttachBtn(0)
GPIO.add_event_detect(AiyBtnPin, GPIO.FALLING, callback=onMidiAttachBtn, bouncetime=12000)

while True:
        time.sleep(0.1)
