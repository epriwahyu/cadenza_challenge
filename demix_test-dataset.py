import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
import glob
import demucs.separate

folder_path = "/home/epri/Downloads/cadenza_data/cad1/task2/audio/music/test"  # Replace with the actual folder path

# Read the list of audio files from 'list_train_flac.txt'
with open("/home/epri/Downloads/demucs/list_database_test.txt", "r") as file:
    audio_files = file.read().splitlines()

# Process each audio file
for audio_file in audio_files:
    # Create the file path by joining the folder_path and the audio_file name
    wav_file = os.path.join(folder_path, audio_file)

    # Extract the filename without the extension
    file_name = os.path.splitext(os.path.basename(audio_file))[0]

    # Create the subfolder path
    subfolder_path = os.path.join("separated_test", "mdx_q_test")
    os.makedirs(subfolder_path, exist_ok=True)

    # Define the output filename for the separated stems
    output_file = os.path.join(subfolder_path, file_name)

    # Call the separate.main function with appropriate arguments
    demucs.separate.main(["-n", "mdx_q", wav_file, "-o", output_file])
