import torch
import numpy as np
from scipy.io import wavfile
import json

class DrumMachine:
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate

    def generate_kick(self, duration=0.5):
        """Generate a realistic kick drum sound"""
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        # Kick drum: low frequency with quick decay
        kick = np.sin(2 * np.pi * 60 * t) * np.exp(-t * 8)
        kick += np.sin(2 * np.pi * 40 * t) * np.exp(-t * 12) * 0.5
        return kick

    def generate_snare(self, duration=0.3):
        """Generate a snare drum sound"""
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        # Snare: noise + tone
        noise = np.random.normal(0, 0.1, len(t))
        tone = np.sin(2 * np.pi * 200 * t) * np.exp(-t * 15)
        snare = (noise + tone) * np.exp(-t * 10)
        return snare

    def generate_hihat(self, duration=0.1):
        """Generate hi-hat sound"""
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        # Hi-hat: high frequency noise
        hihat = np.random.normal(0, 0.05, len(t)) * np.exp(-t * 50)
        return hihat

    def create_trap_pattern(self, bars=4, bpm=140):
        """Create a trap beat pattern"""
        beat_duration = 60.0 / bpm  # Duration of one beat
        bar_duration = beat_duration * 4  # 4/4 time
        total_duration = bar_duration * bars
        total_samples = int(self.sample_rate * total_duration)
        pattern = np.zeros(total_samples)

        # Trap pattern: Kick on 1 and 3, snare on 2 and 4
        for bar in range(bars):
            bar_start = int(bar * bar_duration * self.sample_rate)
            beat_samples = int(beat_duration * self.sample_rate)

            # Kick drums
            kick = self.generate_kick()
            pattern[bar_start:bar_start + len(kick)] += kick
            pattern[bar_start + beat_samples * 2:bar_start + beat_samples * 2 + len(kick)] += kick

            # Snare drums
            snare = self.generate_snare()
            pattern[bar_start + beat_samples:bar_start + beat_samples + len(snare)] += snare
            pattern[bar_start + beat_samples * 3:bar_start + beat_samples * 3 + len(snare)] += snare

            # Hi-hats (8th notes)
            hihat = self.generate_hihat()
            for eighth in range(8):
                hihat_pos = bar_start + int(eighth * beat_samples / 2)
                if hihat_pos + len(hihat) < len(pattern):
                    pattern[hihat_pos:hihat_pos + len(hihat)] += hihat * 0.3

        return pattern

# Test the drum machine
if __name__ == "__main__":
    print("🥁 Creating advanced drum machine...")
    drums = DrumMachine()
    trap_beat = drums.create_trap_pattern(bars=4, bpm=140)
    wavfile.write("trap_beat.wav", drums.sample_rate, (trap_beat * 16383).astype(np.int16))
    print("✅ Created trap_beat.wav - 4 bars at 140 BPM!")
    