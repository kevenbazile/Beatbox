import torch
import numpy as np
from scipy.io import wavfile
import json
import os
from datetime import datetime

class AIProducerDAW:
    def __init__(self):
        self.sample_rate = 44100
        self.projects = {}
        self.current_project = None
        print("?? AI Producer DAW initialized!")

    def create_project(self, name):
        self.projects[name] = {'tracks': [], 'tempo': 120}
        self.current_project = name
        print(f"?? Created project: {name}")

    def prompt_to_beat(self, prompt):
        print(f"?? Generating beat from: '{prompt}'")
        # Simple beat generation for now
        duration = 4
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        beat = np.sin(2 * np.pi * 60 * t) * np.exp(-t * 3)
        filename = f"beat_{len(self.projects[self.current_project]['tracks'])}.wav"
        wavfile.write(filename, self.sample_rate, (beat * 32767).astype(np.int16))
        self.projects[self.current_project]['tracks'].append(filename)
        print(f"? Generated: {filename}")
        return filename

# Test the DAW
if __name__ == "__main__":
    daw = AIProducerDAW()
    daw.create_project("My_First_Beat")
    daw.prompt_to_beat("dark trap beat with heavy 808s")
    print("?? DAW test complete!")
