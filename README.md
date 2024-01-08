
# Lip Synced Character Generator

Automate the creation of lip synced characters easily utilizing only a transcript and an audio file.

Created as an updated version of [the old version](github.com/EternalDusk/LipSyncVideoGenerator) meant to clean the code and dependencies required

### Dependencies
* Required python libraries
    ```
    pypar
    tempfile
    soundfile
    pathlib2
    montreal-forced-aligner
    ```
All of these can be installed with the following commands
```shell
pip install -r requirements.txt
conda install -c conda-forge montreal-forced-aligner
```

### Executing program
1. Clone the repo
```shell
git clone https://github.com/EternalDusk/LipSyncVideoGenerator.git
```

2. Install the required libraries
```shell
pip install -r requirements.txt
conda install -c conda-forge montreal-forced-aligner
```

3. Place the required character and background images into the "assets" folder

4. Run main.py. It will prompt you to enter the full path to your text and audio files.


## Version History

* 0.1
    * Initial Release

## Acknowledgments

* [Thanks to CaryKH for creating the 2 programs that inspired this project](https://www.youtube.com/watch?v=y3B8YqeLCpY)


## To Do
- [ ] Generate animated lipsynced character from output json
- [ ] Check if the filetypes passed in are correct filetypes
- [ ] Clean text scripts and save to new file
- [ ] Add functionality for inputting only an audio file and using Whisper to generate a transcript
- [ ] Check for all required character images on start
