# WackMan
WackMan is an interactive game, in which the user attempts to collect bloops while
avoiding snakes that are roaming the map.

After each bloop has been collected, the next level (with a unique color scheme) is entered.


WackMan utilizes gamebox.py, an auxiliary program authored by Luther Tychonievich

Sprites were created by Jordan Irwin of OpenGameArt.org


WackMan can be played in the terminal using Python3

PyGame must be installed to play Wackman, which can be installed using the following command:

pip install pygame

if an exception is thrown, try:

brew install sdl sdl_image sdl_mixer sdl_ttf portmidi

and repeat above comand.

Finally, Wackman can be run with:

Python3 run.py

If having trouble with window focus/nonresponse to key input, try instead:

Pythonw run.py


Further plans for WackMan include a more sophisticated algorithm for moving the snakes.
