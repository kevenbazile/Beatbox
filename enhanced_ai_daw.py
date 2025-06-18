import numpy as np
import librosa
import soundfile as sf
import pretty_midi
from pydub import AudioSegment
from pydub.effects import normalize, compress_dynamic_range
import tempfile
import os
from datetime import datetime
from prompt_processor import PromptProcessor

class EnhancedAIDaw:
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
        self.processor = PromptProcessor()
        
    def generate_professional_kick(self, duration=0.5, kick_type='heavy', bass_boost=1.0):
        """Generate professional quality kick using librosa"""
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        
        if kick_type == 'heavy':
            # 808-style kick with sub frequencies
            kick = np.sin(2 * np.pi * 45 * t) * np.exp(-t * 5) * bass_boost
            kick += np.sin(2 * np.pi * 35 * t) * np.exp(-t * 8) * bass_boost * 0.8
            # Add harmonic content
            kick += np.sin(2 * np.pi * 90 * t) * np.exp(-t * 15) * 0.3
        elif kick_type == 'punchy':
            # Punchy kick with more attack
            kick = np.sin(2 * np.pi * 65 * t) * np.exp(-t * 12)
            kick += np.sin(2 * np.pi * 45 * t) * np.exp(-t * 18) * 0.7
            # Add click for punch
            click = np.sin(2 * np.pi * 2000 * t) * np.exp(-t * 200) * 0.1
            kick += click
        else:  # standard
            kick = np.sin(2 * np.pi * 55 * t) * np.exp(-t * 8)
            kick += np.sin(2 * np.pi * 40 * t) * np.exp(-t * 12) * 0.6
            
        return kick * bass_boost
    
    def generate_professional_snare(self, duration=0.3, mood='neutral'):
        """Generate professional snare with realistic character"""
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        
        # Create realistic snare components
        # 1. Noise component (snare buzz)
        noise = np.random.normal(0, 0.15, len(t))
        # Filter the noise to snare frequencies (200-400Hz emphasis)
        noise = librosa.effects.preemphasis(noise)
        
        # 2. Tonal component (drum shell resonance)
        tone1 = np.sin(2 * np.pi * 200 * t) * np.exp(-t * 12)
        tone2 = np.sin(2 * np.pi * 250 * t) * np.exp(-t * 15)
        
        # 3. High frequency crack
        crack = np.sin(2 * np.pi * 1000 * t) * np.exp(-t * 50) * 0.3
        
        # Combine components
        snare = (noise + tone1 + tone2 + crack) * np.exp(-t * 8)
        
        # Apply mood modifications
        if mood == 'aggressive':
            snare = np.tanh(snare * 2) * 1.3  # Add saturation
        elif mood == 'soft':
            snare = snare * 0.7
            
        return snare
    
    def add_audio_effects(self, audio_data, effects=['compression', 'eq']):
        """Add professional audio effects using pydub"""
        # Convert numpy array to pydub AudioSegment
        audio_int = (audio_data * 32767).astype(np.int16)
        audio_segment = AudioSegment(
            audio_int.tobytes(),
            frame_rate=self.sample_rate,
            sample_width=2,
            channels=1
        )
        
        if 'compression' in effects:
            # Add dynamic range compression
            audio_segment = compress_dynamic_range(audio_segment, threshold=-20, ratio=4)
            
        if 'eq' in effects:
            # Simple EQ boost for low end
            audio_segment = audio_segment.low_pass_filter(8000)
            
        if 'normalize' in effects:
            # Normalize audio levels
            audio_segment = normalize(audio_segment)
            
        # Convert back to numpy array
        processed_audio = np.array(audio_segment.get_array_of_samples()).astype(np.float32) / 32767
        return processed_audio
    
    def export_to_midi(self, params, filename):
        """Export beat pattern as MIDI file for use in other DAWs"""
        # Create a new MIDI file
        midi = pretty_midi.PrettyMIDI()
        
        # Create drum track
        drum_program = pretty_midi.instrument_name_to_program('Acoustic Grand Piano')
        drums = pretty_midi.Instrument(program=drum_program, is_drum=True)
        
        bpm = params['bpm']
        bars = params['bars']
        beat_duration = 60.0 / bpm
        
        # MIDI drum mapping (General MIDI)
        kick_note = 36  # C2
        snare_note = 38  # D2
        hihat_note = 42  # F#2
        
        for bar in range(bars):
            bar_start = bar * 4 * beat_duration
            
            # Add kicks based on genre
            if params['genre'] == 'trap':
                # Trap pattern: 1, 2.5, 4
                kick_times = [0, 1.5, 3]
            else:  # boom bap, drill, etc.
                # Standard pattern: 1, 3
                kick_times = [0, 2]
                
            for kick_time in kick_times:
                note_start = bar_start + kick_time * beat_duration
                note = pretty_midi.Note(velocity=100, pitch=kick_note, 
                                      start=note_start, end=note_start + 0.1)
                drums.notes.append(note)
            
            # Add snares on 2 and 4
            for snare_beat in [1, 3]:
                note_start = bar_start + snare_beat * beat_duration
                note = pretty_midi.Note(velocity=80, pitch=snare_note,
                                      start=note_start, end=note_start + 0.1)
                drums.notes.append(note)
            
            # Add hi-hats
            hihat_pattern = 8 if params['hihat_style'] == 'rapid' else 4
            for hihat in range(hihat_pattern):
                note_start = bar_start + hihat * (beat_duration / (hihat_pattern / 4))
                velocity = 60 if hihat % 2 == 0 else 40  # Accent pattern
                note = pretty_midi.Note(velocity=velocity, pitch=hihat_note,
                                      start=note_start, end=note_start + 0.05)
                drums.notes.append(note)
        
        midi.instruments.append(drums)
        midi.write(filename)
        return filename
    
    def create_enhanced_beat(self, prompt):
        """Create professional quality beat with effects and MIDI export"""
        print(f"🎵 Processing prompt: '{prompt}'")
        
        # Parse prompt
        params = self.processor.parse_prompt(prompt)
        description = self.processor.generate_description(params)
        print(f"📝 {description}")
        
        # Generate enhanced beat
        beat = self.generate_enhanced_pattern(params)
        
        # Add professional effects
        print("🎛️ Applying audio effects...")
        beat = self.add_audio_effects(beat, ['compression', 'eq', 'normalize'])
        
        # Export audio
        audio_filename = f"enhanced_beat_{params['genre']}_{params['bpm']}bpm.wav"
        sf.write(audio_filename, beat, self.sample_rate)
        
        # Export MIDI
        midi_filename = f"enhanced_beat_{params['genre']}_{params['bpm']}bpm.mid"
        self.export_to_midi(params, midi_filename)
        
        print(f"✅ Generated: {audio_filename}")
        print(f"🎹 MIDI file: {midi_filename}")
        
        return audio_filename, midi_filename, params
    
    def generate_enhanced_pattern(self, params):
        """Generate enhanced beat pattern with professional drums"""
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
            
            # Generate professional sounds
            kick = self.generate_professional_kick(duration=0.4, 
                                                 kick_type=params['kick_pattern'], 
                                                 bass_boost=params['bass_boost'])
            snare = self.generate_professional_snare(duration=0.3, mood=params['mood'])
            
            # Add pattern based on genre
            if params['genre'] == 'trap':
                self.add_trap_pattern(pattern, bar_start, beat_samples, kick, snare, params)
            elif params['genre'] == 'boom bap':
                self.add_boom_bap_pattern(pattern, bar_start, beat_samples, kick, snare, params)
            # Add other genres...
                
        return pattern
    
    def add_trap_pattern(self, pattern, bar_start, beat_samples, kick, snare, params):
        """Add trap-specific pattern"""
        # Trap kick pattern: 1, 2.5, 4
        kick_positions = [0, int(beat_samples * 1.5), beat_samples * 3]
        
        for pos in kick_positions:
            start_pos = bar_start + pos
            if start_pos + len(kick) < len(pattern):
                pattern[start_pos:start_pos + len(kick)] += kick
        
        # Snare on 2 and 4
        snare_positions = [beat_samples, beat_samples * 3]
        for pos in snare_positions:
            start_pos = bar_start + pos
            if start_pos + len(snare) < len(pattern):
                pattern[start_pos:start_pos + len(snare)] += snare
    
    def add_boom_bap_pattern(self, pattern, bar_start, beat_samples, kick, snare, params):
        """Add boom bap specific pattern"""
        # Boom bap: kick on 1 and 3
        kick_positions = [0, beat_samples * 2]
        
        for pos in kick_positions:
            start_pos = bar_start + pos
            if start_pos + len(kick) < len(pattern):
                pattern[start_pos:start_pos + len(kick)] += kick
        
        # Snare on 2 and 4
        snare_positions = [beat_samples, beat_samples * 3]
        for pos in snare_positions:
            start_pos = bar_start + pos
            if start_pos + len(snare) < len(pattern):
                pattern[start_pos:start_pos + len(snare)] += snare

# Test the enhanced DAW
if __name__ == "__main__":
    print("🎵 Enhanced AI DAW with Professional Libraries")
    daw = EnhancedAIDaw()
    
    test_prompts = [
        "dark trap beat with heavy 808s at 140 BPM",
        "boom bap beat with punchy kicks, 90 BPM"
    ]
    
    for prompt in test_prompts:
        audio_file, midi_file, params = daw.create_enhanced_beat(prompt)
        print(f"Created: {audio_file} and {midi_file}\n")