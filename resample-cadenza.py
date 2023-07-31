import os
import librosa
import soundfile as sf
from scipy.signal import resample
import numpy as np

# Function to resample audio to 32000 Hz and save as stereo in the target directory
def resample_and_save_stereo(input_folder, output_folder):
    # Get the listener name from the input folder path
    listener_name = os.path.basename(os.path.normpath(input_folder))  # Extract the listener name from the path

    # Create a subfolder with the listener name inside the output folder
    listener_folder = os.path.join(output_folder, listener_name)
    os.makedirs(listener_folder, exist_ok=True)

    # List all files in the input folder
    audio_files = os.listdir(input_folder)

    for audio_file in audio_files:
        # Get the full path of the audio file
        audio_path = os.path.join(input_folder, audio_file)

        # Check if the file is in WAV format
        if audio_file.lower().endswith('.wav'):
            # Load the audio using librosa
            y, sr = librosa.load(audio_path, sr=None)

            # Resample to 32000 Hz
            target_sr = 32000
            y_resampled = resample(y, int(len(y) * target_sr / sr))

            # Convert the mono audio to stereo by stacking the resampled audio into two channels
            y_stereo = np.vstack((y_resampled, y_resampled))

            # Save the stereo audio as .flac in the listener's subfolder
            output_file = os.path.splitext(audio_file)[0] + '.flac'
            output_path = os.path.join(listener_folder, output_file)
            sf.write(output_path, y_stereo.T, target_sr)

# Read the list of folder paths from the provided file
with open('/home/epri/Downloads/augment_sound/list_mix5.txt', 'r') as file:
    folder_paths = file.read().splitlines()

# Define the output folder where the resampled stereo files will be saved
output_folder = '/home/epri/Downloads/augment_sound/mix-demix5-resample-stereo'

# Process each folder and resample the audio files
for folder_path in folder_paths:
    resample_and_save_stereo(folder_path, output_folder)
