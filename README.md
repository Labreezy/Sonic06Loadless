# Sonic '06 (and others) Loadless LiveSplit Timer

Load times have built-in insane amounts of variation in Sonic '06.  This is a tool that interfaces with LiveSplit that pauses the timer whenever the game is loading.

## How to use
1. After opening LiveSplit, right-click it and hit Control -> Start TCP Server. You will need to do this every time you close and re-open LiveSplit.
1. In your OBS Virtual Camera Settings (the gear to the right of "start virtual camera" at the time of writing), set the Output Type to "Source" and the Output Selection to your capture card.
1. Run the program. It will prompt you to choose a camera, type in the number that corresponds to the OBS Virtual Camera and hit enter. If successful a preview of your capture should appear.
1. Make sure, before starting anything, LiveSplit is set to compare against Game Time, or else nothing will visibly pause. Your timer will now pause in accordance with the footage displayed.
1. To exit the program, click the preview and hit the "Escape" key.

If you just want to use the timer, you're done!  Have fun!

---

## Running from binary release (Windows Only)

1. Download the executable from the [releases section](https://github.com/Labreezy/Sonic06Loadless/releases) of this repository.
1. Run it, and refer to the "How to use" section above.


## Running from source

### Linux & MacOS

Prerequisites: git, python3.11+

1. Open a Terminal window
1. Clone the repository and enter the cloned directory
    ```sh
    git clone https://github.com/Labreezy/Sonic06Loadless && cd Sonic06Loadless
    ```
1. Create a Python virtual environment
    ```sh
    python -m venv venv
    ```
1. Activate the virtual environment
    ```sh
    chmod +x venv/bin/activate && venv/bin/activate
    ```
1. Install dependencies
    ```sh
    pip install -r requirements.txt
    ```
1. Run the script you want (main_06.py / main_sa1.py / retime_06.py)
    ```sh
    python main_sa1.py
    ```
1. (Optional) Build executable
    ```sh
    pyinstaller Sonic06Loadless.spec
    ```
    The resulting executables will be in `./dist/`, you can run them with e.g. `dist/sa1_loadless`

### Windows

Prerequisites: [Git](https://git-scm.com/downloads/win), [Python 3.11+](https://www.python.org/downloads/windows/), [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)

1. Open a PowerShell window
1. Clone the repository and enter the cloned directory
    ```ps1
    git clone https://github.com/Labreezy/Sonic06Loadless && cd Sonic06Loadless
    ```
1. Create a Python virtual environment and activate it
    ```ps1
    python -m venv venv && .\venv\Scripts\Activate.ps1
    ```
    > Note:
    > It may be required to change the execution policy on your system in order to activate the virtual environment
    >
    > `PS C:\> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
1. Install dependencies
    ```ps1
    pip install -r requirements.txt
    ```
1. Run the script you want (main_06.py / main_sa1.py / retime_06.py)
    ```ps1
    python main_sa1.py
    ```
1. (Optional) Build executable
    ```ps1
    pyinstaller Sonic06Loadless.spec
    ```
    The resulting executables will be in `./dist/`, you can run them from there.
