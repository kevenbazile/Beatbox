import numpy as np
from scipy.io import wavfile
import json
from prompt_processor import PromptProcessor

class SmartDrumMachine:
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
        self.processor = PromptProcessor()

    def generate_kick(self, duration=0.5, kick_type='standard', bass_boost=1.0):
        """Generate kick drum based on style"""
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        
        if kick_type == 'heavy':
            # Heavy 808-style kick
            kick = np.sin(2 * np.pi * 50 * t) * np.exp(-t * 6) * bass_boost
            kick += np.sin(2 * np.pi * 35 * t) * np.exp(-t * 8) * bass_boost * 0.7
        elif kick_type == 'punchy':
            # Boom bap style punchy kick
            kick = np.sin(2 * np.pi * 70 * t) * np.exp(-t * 12)
            kick += np.sin(2 * np.pi * 45 * t) * np.exp(-t * 15) * 0.6
        elif kick_type == 'soft':
            # Lo-fi soft kick
            kick = np.sin(2 * np.pi * 65 * t) * np.exp(-t * 10) * 0.7
        else:  # standard
            kick = np.sin(2 * np.pi * 60 * t) * np.exp(-t * 8)
            kick += np.sin(2 * np.pi * 40 * t) * np.exp(-t * 12) * 0.5
        
        return kick * bass_boost

    def generate_snare(self, duration=0.3, mood='neutral', distortion=0.3):
        """Generate snare with mood variations"""
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        
        # Base snare
        noise = np.random.normal(0, 0.1, len(t))
        tone = np.sin(2 * np.pi * 200 * t) * np.exp(-t * 15)
        snare = (noise + tone) * np.exp(-t * 10)
        
        # Apply mood modifications
        if mood == 'aggressive':
            # Add more distortion and punch
            snare = np.tanh(snare * 3) * 1.2
        elif mood == 'soft':
            # Softer, less aggressive
            snare = snare * 0.6
        elif mood == 'dark':
            # Lower frequency content
            tone = np.sin(2 * np.pi * 150 * t) * np.exp(-t * 12)
            snare = (noise * 0.7 + tone) * np.exp(-t * 8)
        
        return snare

    def generate_hihat(self, duration=0.1, hihat_style='standard'):
        """Generate hi-hat based on style"""
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        
        if hihat_style == 'rapid':
            # Sharp, quick hi-hats
            hihat = np.random.normal(0, 0.08, len(t)) * np.exp(-t * 80)
        elif hihat_style == 'vinyl':
            # Lo-fi vinyl texture
            hihat = np.random.normal(0, 0.04, len(t)) * np.exp(-t * 30)
            # Add some vinyl crackle
            crackle = np.random.normal(0, 0.01, len(t))
            hihat += crackle
        elif hihat_style == 'sparse':
            # Drill style - less frequent, more space
            hihat = np.random.normal(0, 0.06, len(t)) * np.exp(-t * 60)
        else:  # simple/standard
            hihat = np.random.normal(0, 0.05, len(t)) * np.exp(-t * 50)
        
        return hihat

    def create_beat_from_prompt(self, prompt):
        """Main function: Create beat from natural language prompt"""
        print(f"🎵 Processing prompt: '{prompt}'")
        
        # Parse the prompt
        params = self.processor.parse_prompt(prompt)
        description = self.processor.generate_description(params)
        print(f"📝 {description}")
        
        # Generate the beat
        beat = self.create_parametric_beat(params)
        
        # Save the beat
        filename = f"ai_beat_{params['genre']}_{params['bpm']}bpm.wav"
        volume_scale = params.get('volume', 1.0)
        wavfile.write(filename, self.sample_rate, (beat * 16383 * volume_scale).astype(np.int16))
        
        print(f"✅ Generated: {filename}")
        return filename, params

    def create_parametric_beat(self, params):
        """Create beat based on parsed parameters"""
        bpm = params['bpm']
        bars = params['bars']
        genre = params['genre']
        
        # Generate pattern based on genre
        if genre == 'trap':
            pattern = self.create_trap_pattern_advanced(params)
        elif genre == 'boom bap':
            pattern = self.create_boom_bap_pattern(params)
        elif genre == 'drill':
            pattern = self.create_drill_pattern(params)
        elif genre == 'lo-fi':
            pattern = self.create_lofi_pattern(params)
        else:
            pattern = self.create_trap_pattern_advanced(params)
        
        return pattern

    def create_trap_pattern_advanced(self, params):
        """Advanced trap pattern with parameters - FIXED VERSION"""
        bpm = params['bpm']
        bars = params['bars']
        
        beat_duration = 60.0 / bpm
        bar_duration = beat_duration * 4
        total_duration = bar_duration * bars
        total_samples = int(self.sample_rate * total_duration)
        pattern = np.zeros(total_samples)
        
        for bar in range(bars):
            bar_start = int(bar * bar_duration * self.sample_rate)
            beat_samples = int(beat_duration * self.sample_rate)
            
            # Generate sounds with shorter durations to fit the beat
            kick = self.generate_kick(duration=0.3, kick_type=params['kick_pattern'], bass_boost=params['bass_boost'])
            snare = self.generate_snare(duration=0.2, mood=params['mood'], distortion=params['distortion'])
            hihat = self.generate_hihat(duration=0.1, hihat_style=params['hihat_style'])
            
            # Kick pattern: 1, 2.5, 4 (trap style) - FIXED
            # Kick on beat 1
            kick_pos1 = bar_start
            if kick_pos1 + len(kick) < len(pattern):
                pattern[kick_pos1:kick_pos1 + len(kick)] += kick
            
            # Kick on beat 2.5
            kick_pos2 = bar_start + int(beat_samples * 1.5)
            if kick_pos2 + len(kick) < len(pattern):
                pattern[kick_pos2:kick_pos2 + len(kick)] += kick * 0.8
            
            # Kick on beat 4
            kick_pos3 = bar_start + beat_samples * 3
            if kick_pos3 + len(kick) < len(pattern):
                pattern[kick_pos3:kick_pos3 + len(kick)] += kick
            
            # Snare on 2 and 4 - FIXED
            snare_pos1 = bar_start + beat_samples
            if snare_pos1 + len(snare) < len(pattern):
                pattern[snare_pos1:snare_pos1 + len(snare)] += snare
            
            snare_pos2 = bar_start + beat_samples * 3
            if snare_pos2 + len(snare) < len(pattern):
                pattern[snare_pos2:snare_pos2 + len(snare)] += snare
            
            # Hi-hats - FIXED
            if params['hihat_style'] == 'rapid':
                # Rapid trap hi-hats (16th notes)
                for sixteenth in range(16):
                    hihat_pos = bar_start + int(sixteenth * beat_samples / 4)
                    if hihat_pos + len(hihat) < len(pattern):
                        pattern[hihat_pos:hihat_pos + len(hihat)] += hihat * 0.4
            else:
                # Standard 8th notes
                for eighth in range(8):
                    hihat_pos = bar_start + int(eighth * beat_samples / 2)
                    if hihat_pos + len(hihat) < len(pattern):
                        pattern[hihat_pos:hihat_pos + len(hihat)] += hihat * 0.3
        
        return pattern

    def create_boom_bap_pattern(self, params):
        """Classic boom bap pattern - FIXED VERSION"""
        bpm = params['bpm']
        bars = params['bars']
        
        beat_duration = 60.0 / bpm
        bar_duration = beat_duration * 4
        total_duration = bar_duration * bars
        total_samples = int(self.sample_rate * total_duration)
        pattern = np.zeros(total_samples)
        
        for bar in range(bars):
            bar_start = int(bar * bar_duration * self.sample_rate)
            beat_samples = int(beat_duration * self.sample_rate)
            
            # Generate sounds with appropriate durations
            kick = self.generate_kick(duration=0.4, kick_type=params['kick_pattern'], bass_boost=params['bass_boost'])
            snare = self.generate_snare(duration=0.3, mood=params['mood'])
            hihat = self.generate_hihat(duration=0.2, hihat_style=params['hihat_style'])
            
            # Classic boom bap: kick on 1 and 3 - FIXED
            kick_pos1 = bar_start
            if kick_pos1 + len(kick) < len(pattern):
                pattern[kick_pos1:kick_pos1 + len(kick)] += kick
            
            kick_pos2 = bar_start + beat_samples * 2
            if kick_pos2 + len(kick) < len(pattern):
                pattern[kick_pos2:kick_pos2 + len(kick)] += kick
            
            # Snare on 2 and 4 (the "bap") - FIXED
            snare_pos1 = bar_start + beat_samples
            if snare_pos1 + len(snare) < len(pattern):
                pattern[snare_pos1:snare_pos1 + len(snare)] += snare
            
            snare_pos2 = bar_start + beat_samples * 3
            if snare_pos2 + len(snare) < len(pattern):
                pattern[snare_pos2:snare_pos2 + len(snare)] += snare
            
            # Simple hi-hat pattern - FIXED
            for quarter in range(4):
                hihat_pos = bar_start + int(quarter * beat_samples)
                if hihat_pos + len(hihat) < len(pattern):
                    pattern[hihat_pos:hihat_pos + len(hihat)] += hihat * 0.2
        
        return pattern

    def create_drill_pattern(self, params):
        """UK Drill pattern - similar to trap but with sliding 808s"""
        bpm = params['bpm']
        bars = params['bars']
        
        beat_duration = 60.0 / bpm
        bar_duration = beat_duration * 4
        total_duration = bar_duration * bars
        total_samples = int(self.sample_rate * total_duration)
        pattern = np.zeros(total_samples)
        
        for bar in range(bars):
            bar_start = int(bar * bar_duration * self.sample_rate)
            beat_samples = int(beat_duration * self.sample_rate)
            
            # Generate sounds
            kick = self.generate_kick(duration=0.4, kick_type=params['kick_pattern'], bass_boost=params['bass_boost'])
            snare = self.generate_snare(duration=0.25, mood=params['mood'], distortion=params['distortion'])
            hihat = self.generate_hihat(duration=0.08, hihat_style=params['hihat_style'])
            
            # Drill pattern: sparse kicks with emphasis
            kick_pos1 = bar_start
            if kick_pos1 + len(kick) < len(pattern):
                pattern[kick_pos1:kick_pos1 + len(kick)] += kick
            
            kick_pos2 = bar_start + int(beat_samples * 2.75)  # Slightly off-beat
            if kick_pos2 + len(kick) < len(pattern):
                pattern[kick_pos2:kick_pos2 + len(kick)] += kick * 0.9
            
            # Snare on 2 and 4
            snare_pos1 = bar_start + beat_samples
            if snare_pos1 + len(snare) < len(pattern):
                pattern[snare_pos1:snare_pos1 + len(snare)] += snare
            
            snare_pos2 = bar_start + beat_samples * 3
            if snare_pos2 + len(snare) < len(pattern):
                pattern[snare_pos2:snare_pos2 + len(snare)] += snare
            
            # Sparse hi-hats
            for quarter in range(0, 8, 3):  # Every 3rd eighth note
                hihat_pos = bar_start + int(quarter * beat_samples / 2)
                if hihat_pos + len(hihat) < len(pattern):
                    pattern[hihat_pos:hihat_pos + len(hihat)] += hihat * 0.3
        
        return pattern

    def create_lofi_pattern(self, params):
        """Lo-fi hip hop pattern - laid back and chill"""
        bpm = params['bpm']
        bars = params['bars']
        
        beat_duration = 60.0 / bpm
        bar_duration = beat_duration * 4
        total_duration = bar_duration * bars
        total_samples = int(self.sample_rate * total_duration)
        pattern = np.zeros(total_samples)
        
        for bar in range(bars):
            bar_start = int(bar * bar_duration * self.sample_rate)
            beat_samples = int(beat_duration * self.sample_rate)
            
            # Generate sounds with lo-fi character
            kick = self.generate_kick(duration=0.5, kick_type=params['kick_pattern'], bass_boost=params['bass_boost'])
            snare = self.generate_snare(duration=0.4, mood=params['mood'], distortion=params['distortion'])
            hihat = self.generate_hihat(duration=0.15, hihat_style=params['hihat_style'])
            
            # Lo-fi pattern: simple and laid back
            kick_pos1 = bar_start
            if kick_pos1 + len(kick) < len(pattern):
                pattern[kick_pos1:kick_pos1 + len(kick)] += kick
            
            kick_pos2 = bar_start + beat_samples * 2
            if kick_pos2 + len(kick) < len(pattern):
                pattern[kick_pos2:kick_pos2 + len(kick)] += kick * 0.8
            
            # Snare on 2 and 4
            snare_pos1 = bar_start + beat_samples
            if snare_pos1 + len(snare) < len(pattern):
                pattern[snare_pos1:snare_pos1 + len(snare)] += snare
            
            snare_pos2 = bar_start + beat_samples * 3
            if snare_pos2 + len(snare) < len(pattern):
                pattern[snare_pos2:snare_pos2 + len(snare)] += snare
            
            # Subtle hi-hats with vinyl texture
            for eighth in range(0, 8, 2):  # Every other eighth note
                hihat_pos = bar_start + int(eighth * beat_samples / 2)
                if hihat_pos + len(hihat) < len(pattern):
                    pattern[hihat_pos:hihat_pos + len(hihat)] += hihat * 0.25
        
        return pattern

# Test the smart drum machine
if __name__ == "__main__":
    print("🤖 Starting AI Beat Generator...")
    drum_machine = SmartDrumMachine()
    
    # Test different prompts
    test_prompts = [
        "dark trap beat with heavy 808s at 140 BPM",
        "chill lo-fi beat, slow tempo",
        "boom bap beat with punchy kicks"
    ]
    
    for prompt in test_prompts:
        filename, params = drum_machine.create_beat_from_prompt(prompt)
        print(f"Created: {filename}\n")