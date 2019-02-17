import RPi.GPIO as GPIO
import subprocess
import time

SoundFontFile = "/home/pi/PremierKit.sf2"
AiyBtnPin = 23
AiyLedPin = 25

btnPressStart = -1

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

def startAndAttachSynth():
    lightOff()
    stopFluidSynth()
    time.sleep(1)
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

def handleBtnPress(channel):
    global btnPressStart
    if GPIO.input(channel) == 0:
        btnPressStart = time.time()
    if GPIO.input(channel) == 1:
        if btnPressStart < 0:
            return
        lightBlink(1)
        elapsed = time.time() - btnPressStart
        btnPressStart = -1
        print(elapsed)
        if elapsed < 1:
            startAndAttachSynth()
        elif elapsed > 2:
            subprocess.call("sudo shutdown -h now", shell=True)
                    
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(AiyBtnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(AiyLedPin, GPIO.OUT)

lightBlink(2)

#onMidiAttachBtn(0)
#GPIO.add_event_detect(AiyBtnPin, GPIO.FALLING, callback=onMidiAttachBtn, bouncetime=12000)
GPIO.add_event_detect(AiyBtnPin, GPIO.BOTH, callback=handleBtnPress)

while True:
        time.sleep(0.1)
