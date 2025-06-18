# Sonic '06 (and others) Loadless LiveSplit Timer

Load times have built-in insane amounts of variation in Sonic '06.  This is a tool that interfaces with LiveSplit that pauses the timer whenever the game is loading.

## How to use
1. After opening LiveSplit, right-click it and hit Control -> Start TCP Server. You will need to do this every time you close and re-open LiveSplit.
2. In your OBS Virtual Camera Settings (the gear to the right of "start virtual camera" at the time of writing), set the Output Type to "Source" and the Output Selection to your capture card.
3. Run the program. It will prompt you to choose a camera, type in the number that corresponds to the OBS Virtual Camera and hit enter. If successful a preview of your capture should appear.
4. Make sure, before starting anything, LiveSplit is set to compare against Game Time, or else nothing will visibly pause. Your timer will now pause in accordance with the footage displayed.
5. To exit the program, click the preview and hit the "Escape" key.

If you just want to use the timer, you're done!  Have fun!

---

## Building
Required: Python 3.11+ (i think)


To install the requirements:

``pip install -r requiements.txt``

To build the standalone executable for a game:

``pyinstaller -F -n Sonic06Loadless main_06.py``

or

``pyinstaller -F -n SonicAdveture1Loadless main_sa1.py``
