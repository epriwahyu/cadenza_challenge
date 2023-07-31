# cadenza_challenge

Step:
1. git clone https://github.com/facebookresearch/demucs/tree/main
2. run code [demix_test-dataset.py]. It will read our music data, then it will demix song into 4 parts: vocals.wav, bass.wav, drums.wav, and other.wav
3. remix song based on our proportions, run [remix.py]
4. run [resample-cadenza.py]. The required output processed music:
   - 16-bit
   - 32 kHz sampling rate
   - Compressed using the lossless FLAC compressor
