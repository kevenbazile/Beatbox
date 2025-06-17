import torch 
import numpy as np 
from scipy.io import wavfile 
import matplotlib.pyplot as plt 
 
print("Creating simple beat generator...") 
 
# Generate a simple drum pattern 
sample_rate = 44100 
duration = 4  # 4 seconds 
t = np.linspace(0, duration, int(sample_rate * duration)) 
 
# Create a simple kick drum sound 
kick = np.sin(2 * np.pi * 60 * t) * np.exp(-t * 5) 
print("Simple music generator created successfully!") 
