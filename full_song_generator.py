import torch
import os
from datetime import datetime
import traceback

class FullSongGenerator:
    def __init__(self):
        print("🎵 Initializing AI Music Generator...")
        self.model = None
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print(f"🔧 Using device: {self.device}")
        
        # Create output directory
        os.makedirs('generated_songs', exist_ok=True)
        
        # Load model
        self.load_model()
    
    def load_model(self):
        """Load AudioCraft MusicGen model"""
        try:
            print("📦 Loading MusicGen model... (this may take 5-10 minutes on first run)")
            
            from audiocraft.models import MusicGen
            
            # Use small model for faster loading and lower memory usage
            self.model = MusicGen.get_pretrained('facebook/musicgen-small')
            
            # Set default generation parameters
            self.model.set_generation_params(
                duration=30,
                top_k=250,
                top_p=0.0,
                temperature=1.0,
                cfg_coef=3.0
            )
            
            print("✅ MusicGen model loaded successfully!")
            
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            traceback.print_exc()
            raise e
    
    def generate_song(self, prompt, duration=30, style_hint=None):
        """Generate a song from text prompt"""
        if self.model is None:
            raise Exception("Model not loaded!")
        
        # Create safe filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_prompt = "".join(c for c in prompt[:30] if c.isalnum() or c in (' ', '-', '_')).strip()
        safe_prompt = safe_prompt.replace(' ', '_')
        
        if style_hint:
            output_filename = f"generated_songs/{style_hint}_{timestamp}"
        else:
            output_filename = f"generated_songs/song_{safe_prompt}_{timestamp}"
        
        print(f"🎵 Generating: '{prompt}'")
        print(f"⏱️ Duration: {duration} seconds")
        print(f"💾 Output: {output_filename}.wav")
        
        try:
            # Set generation parameters for this request
            self.model.set_generation_params(
                duration=duration,
                top_k=250,
                top_p=0.0,
                temperature=1.0,
                cfg_coef=3.0
            )
            
            # Generate the music
            descriptions = [prompt]
            wav = self.model.generate(descriptions)
            
            # Save the audio
            from audiocraft.data.audio import audio_write
            audio_write(output_filename, wav[0].cpu(), self.model.sample_rate,
                       strategy="loudness", loudness_compressor=True)
            
            filename = f"{output_filename}.wav"
            file_size = os.path.getsize(filename) if os.path.exists(filename) else 0
            
            print(f"✅ Generated successfully: {filename}")
            print(f"📊 File size: {file_size/1024/1024:.1f} MB")
            
            return {
                'filename': filename,
                'basename': os.path.basename(filename),
                'duration': duration,
                'prompt': prompt,
                'sample_rate': self.model.sample_rate,
                'file_size': file_size,
                'style': style_hint or 'custom'
            }
            
        except Exception as e:
            print(f"❌ Generation failed: {e}")
            traceback.print_exc()
            raise e
    
    def create_michael_jackson_style(self, duration=30):
        """Generate Michael Jackson 'Beat It' style song"""
        prompts = [
            "upbeat pop rock song with funky bassline and electric guitar, 80s style, danceable rhythm, energetic drums, similar to Beat It by Michael Jackson",
            "energetic pop rock with driving drums, funky bass guitar, electric guitar riffs, upbeat tempo, 1980s production style",
            "pop rock anthem with strong backbeat, electric guitar solo, synth bass, dance pop, 80s style"
        ]
        
        import random
        prompt = random.choice(prompts)
        
        print("🕺 Creating Michael Jackson 'Beat It' style track...")
        return self.generate_song(prompt, duration, "michael_jackson_beat_it")
    
    def create_sleepy_hallow_style(self, duration=30):
        """Generate Sleepy Hallow style drill song"""
        prompts = [
            "dark drill beat with heavy 808s, Brooklyn drill style, aggressive trap drums, menacing piano melody, street vibe, NYC drill rap",
            "UK drill instrumental with sliding 808s, dark piano chords, rapid hi-hats, aggressive drums, drill rap beat, street music",
            "drill rap beat with heavy bass, dark atmosphere, ominous piano, trap drums, Brooklyn drill style, menacing melody"
        ]
        
        import random
        prompt = random.choice(prompts)
        
        print("🎤 Creating Sleepy Hallow style drill track...")
        return self.generate_song(prompt, duration, "sleepy_hallow_drill")
    
    def create_drake_style(self, duration=30):
        """Generate Drake style melodic hip-hop"""
        prompts = [
            "melodic hip hop with atmospheric production, soft piano, 808 drums, ambient pads, emotional and melodic, R&B influence",
            "melodic rap beat with piano chords, atmospheric synths, trap drums, emotional melody, contemporary hip hop, Drake style",
            "melodic hip hop instrumental with lush piano, strings, 808s, atmospheric production, emotional and introspective"
        ]
        
        import random
        prompt = random.choice(prompts)
        
        print("🎵 Creating Drake style melodic hip-hop...")
        return self.generate_song(prompt, duration, "drake_melodic_hiphop")
    
    def create_travis_scott_style(self, duration=30):
        """Generate Travis Scott style psychedelic trap"""
        prompt = "psychedelic trap with autotune vocals, distorted 808s, atmospheric production, reverb-heavy drums, dark and trippy"
        
        print("🔥 Creating Travis Scott style psychedelic trap...")
        return self.generate_song(prompt, duration, "travis_scott_trap")
    
    def create_the_weeknd_style(self, duration=30):
        """Generate The Weeknd style dark R&B"""
        prompt = "dark R&B with atmospheric synths, moody production, electronic elements, sultry and mysterious"
        
        print("🌙 Creating The Weeknd style dark R&B...")
        return self.generate_song(prompt, duration, "weeknd_dark_rnb")
    
    def get_model_info(self):
        """Get model information"""
        if self.model is None:
            return {"status": "Model not loaded", "device": self.device}
        
        return {
            "status": "Model loaded",
            "device": self.device,
            "sample_rate": self.model.sample_rate,
            "model_name": "MusicGen-Small"
        }

# Test script
if __name__ == "__main__":
    print("🎵 Testing AI Music Generator...")
    
    try:
        generator = FullSongGenerator()
        
        # Test generation
        print("\n🎸 Testing Michael Jackson style...")
        result = generator.create_michael_jackson_style(15)  # 15 seconds for quick test
        print(f"✅ Created: {result['basename']}")
        
        print("\n🎤 Testing Sleepy Hallow style...")
        result = generator.create_sleepy_hallow_style(15)
        print(f"✅ Created: {result['basename']}")
        
        print("\n🎉 All tests passed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        traceback.print_exc()