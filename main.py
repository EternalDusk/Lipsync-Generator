import os
import montreal_forced_aligner as mfa
import pypar
import tempfile
import soundfile
from pathlib import Path
import shutil


def get_files():
    audio_file_accepted = False
    text_file_accepted = False

    while audio_file_accepted == False:
        audio_file = input("Path to audio file: ")
        if os.path.exists(audio_file):
            # Need to check if it's actually an audio file
            audio_file_accepted = True
        else:
            print("Audio file error: not found")
    
    while text_file_accepted == False:
        text_file = input("Path to text file: ")
        if os.path.exists(text_file):
            # Clean the script and save to new file
            #   Remove the brackets '[]' around text and the emotion tags with content '<**>'
            # Need to check if it's actually a text file
            text_file_accepted = True
        else:
            print("Text file error: not found")

    return audio_file, text_file


def align_files(audio_file, text_file, num_workers = None):

    af_path = Path(audio_file)
    txt_path = Path(text_file)

    # Download english dictionary and acoustic model
    manager = mfa.models.ModelManager()
    manager.download_model('dictionary', 'english_mfa')
    manager.download_model('acoustic', 'english_mfa')

    with tempfile.TemporaryDirectory() as directory:
        directory = Path(directory)
        
        copy_and_convert(directory, text_file, audio_file)
        

        aligner = mfa.alignment.PretrainedAligner(
                    corpus_directory=str(directory),
                    dictionary_path='english_mfa',
                    acoustic_model_path='english_mfa',
                    num_jobs=num_workers,
                    debug=False,
                    verbose=False)

        # Align
        aligner.align()

        # Export alignments
        aligner.export_files(str(directory))

        # Copy alignments to destination
        textgrid_file = (
            directory /
            af_path.parent.name /
            f'{af_path.stem}.TextGrid')

        # The alignment can fail. This typically indicates that the
        # transcript and audio do not match. We skip these files.
        try:
            alignment = pypar.Alignment(textgrid_file)
            alignment.save(f'{af_path.parent}.json')
            print(f'JSON file exported to {af_path.parent}.json')
        except FileNotFoundError:
            warnings.warn('MFA failed to align the given files')

def copy_and_convert(directory, text_file, audio_file):
    af_path = Path(audio_file)
    txt_path = Path(text_file)
    """Prepare text and audio files for MFA alignment"""
    speaker_directory = directory / af_path.parent.name
    speaker_directory.mkdir(exist_ok=True, parents=True)
    print(text_file)
    shutil.copyfile(text_file, speaker_directory / txt_path.name)

    # Aligning fails if the audio is not a 16-bit mono wav file, so
    # we convert instead of copy
    audio, sample_rate = soundfile.read(str(audio_file))
    soundfile.write(
        str(speaker_directory / f'{af_path.stem}.wav'),
        audio.squeeze(),
        sample_rate)

def main():
    # Get input for audio and text
    audio_file, text_file = get_files()
    # Align files to get phoneme timing
    align_files(audio_file, text_file)
    # Animate based on timings and frames


if __name__ == "__main__":
    main()