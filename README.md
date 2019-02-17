# AIY-midi-syth

I'm writing this to use my existing Google AIY voice kit hardware to make a midi syth that can link an instrument to a a soundfont via FluidSynth. The goal is to use the button to create the midi link and turn on the button light when ink is established.


### Prerequisites

You will need the Google AIY voiice kit for a regular size Raspberry Pi and a 2 B+ or newer board (I used a 2 B+, this could possibly work on older hardware).

### Setup

Follow the AIY voice kit instructions and build the whole deal. The microphone is not used, so that part can be skipped.

Once cloned, run the setup script. This will install fluidsynth, configure the pi to use the AIY hat sound driver,and kick off the midiSynthHandler.py at startup. 

You will also need to acquire a soundfont file and place it in the pi home directory. The midiSynthHandler.py script will need to be modified with the name of that file.

### Authors

* **Bill S** 


