import os
import ffmpeg as f
def change_nm():

# Get all .wav files in current folder
    files = [f for f in os.listdir() if f.endswith('.wav')]
    files.sort()


# Rename to 001.wav, 002.wav, ...
    for i, f in enumerate(files, start=1):
        new_name = f"{str(i).zfill(3)}.mp4"
        os.rename(f, new_name)
        print(f"Renamed {f} -> {new_name}")

        print("✅ Done renaming all .wav files.")


def change_ext():
    files = [f for f in os.listdir() if f.endswith('.mp4')]
    files.sort()

    for f in files:
        new_name = f.replace('.mp4', '.wav')
        os.rename(f, new_name)
        print(f"Renamed {f} -> {new_name}")
