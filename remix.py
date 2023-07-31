import os
import numpy as np
import librosa
import soundfile as sf

# Function to check if a waveform contains sound based on its energy/amplitude
def has_sound(waveform, threshold=1e-5):
    return waveform.max() > threshold

# Function to adjust the stem proportions based on the presence of sound in each stem
def adjust_proportions(silent_stems):
    total_silent_stems = sum(silent_stems)
    num_stems = len(silent_stems)

    if total_silent_stems == num_stems:
        # All stems are silent, use the original mix (equal proportions)
        proportion = 1.0 / num_stems
        stem_proportions = {stem: proportion for stem in silent_stems}
    else:
        # At least one stem has sound, use the following proportions:
        vocals_proportion = 0.6 if not silent_stems[0] else 0.0
        bass_proportion = 0.15 if not silent_stems[1] else 0.0
        drums_proportion = 0.1 if not silent_stems[2] else 0.0
        other_proportion = 0.15 if not silent_stems[3] else 0.0

        stem_proportions = {
            'vocals.wav': vocals_proportion,
            'bass.wav': bass_proportion,
            'drums.wav': drums_proportion,
            'other.wav': other_proportion,
        }

    return stem_proportions

# Path to the list file
list_path_file = '/home/epri/Downloads/augment_sound/list_demix_test.txt'

# Path to the folder containing subfolders with audio files
folder_path = '/home/epri/Downloads/demucs/separated_test/mdx_q'

# Main output folder for the mix files
output_folder = '/home/epri/Downloads/augment_sound/mix'

# Load the list of audio paths
with open(list_path_file, 'r') as f:
    audio_paths = f.read().splitlines()

# Iterate over the audio paths
for audio_path in audio_paths:
    # Extract the "audio_name" from the audio_path
    audio_name = os.path.basename(os.path.dirname(audio_path))

    # Extract the listener_id from the audio_name (assuming it is in the format "S000000_L0000_fma_000000")
    listener_id = audio_name.split('_')[1]

    # Create a subfolder based on the listener_id under the main output folder
    subfolder_path = os.path.join(output_folder, listener_id)
    os.makedirs(subfolder_path, exist_ok=True)

    # Load the audio files for vocal, bass, drum, and other stems
    audio_files = {
        'vocals.wav': None,
        'bass.wav': None,
        'drums.wav': None,
        'other.wav': None
    }

    # Check if each stem contains sound for the current song
    silent_stems = []
    for stem in audio_files.keys():
        stem_path = os.path.join(folder_path, audio_path, 'mdx_q', audio_path, stem)
        sound, sr = librosa.load(stem_path, sr=None, mono=True)

        audio_files[stem] = sound

        # Check if the stem contains sound
        silent_stems.append(not has_sound(sound))

    # Adjust the proportions based on the presence of sound in each stem
    stem_proportions = adjust_proportions(silent_stems)

    # Apply the updated stem proportions to the remix combination
    for stem, sound in audio_files.items():
        if stem in stem_proportions:
            sound *= stem_proportions[stem]

        # Duplicate the mono sound to create two channels
        sound_stereo = np.stack((sound, sound))

        # Assign the modified stereo sound to the corresponding key in the dictionary
        audio_files[stem] = sound_stereo

    # Combine the modified stereo sounds
    mix = np.sum(list(audio_files.values()), axis=0)

    # Normalize the mix to ensure it doesn't exceed the maximum amplitude
    max_amplitude = np.max(np.abs(mix))
    if max_amplitude > 1.0:
        mix /= max_amplitude

    # Get the filename of the output .wav file
    file_name = f'{audio_name}.wav'

    # Save the mix sound to a file with the specified filename in the output subfolder
    # print(audio_name)
    save_path = os.path.join(subfolder_path, file_name)
    sf.write(save_path, mix.T, sr, format='WAV')
