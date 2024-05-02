from vpython import *
import numpy as np
import sounddevice as sd
from fork import TuningFork, SAMPLE_RATE

# Initialize the list with one default tuning fork


def add_fork():
    """Function to add a new tuning fork to the simulation."""
    new_fork = TuningFork(length=0.5, height=0.02, density=3000, shape="cylinder")
    forklist.append(new_fork)
    new_fork.canvas.width = 400
    new_fork.canvas.height = 600
    arrange_canvases()


def play_all_forks():
    """Play sounds from all forks simultaneously."""
    duration = 2  # Duration in seconds for which to play the sound
    sample_rate = SAMPLE_RATE
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    total_wave = None

    # Combine sounds from all forks
    for fork in forklist:
        freq = fork.frequency
        waveform = 0.5 * np.sin(2 * np.pi * freq * t)  # Generate waveform for each fork

        if total_wave is None:
            total_wave = waveform
        else:
            total_wave += waveform

    total_wave /= len(forklist)  # Normalize by number of forks to control amplitude
    sd.play(total_wave, sample_rate)
    sd.wait()


forklist = [TuningFork(length=0.8, height=0.02, density=5800, shape="rectangle")]

# Setup the main canvas and control panel
button(text="Add Tuning Fork", bind=add_fork)
button(text="Play All Forks", bind=play_all_forks)


# def arrange_canvases():
#     """Arrange all fork canvases vertically."""
#     y_offset = 0
#     for fork in forklist:
#         fork.canvas.pos = vec(400, y_offset, 0)
#         y_offset += fork.canvas.height + 10  # Add space between canvases


def main():
    while True:
        rate(24)  # 24 fps
        # for fork in forklist:
        #     pass  # Handle dynamic updates or checks


if __name__ == "__main__":
    main()
