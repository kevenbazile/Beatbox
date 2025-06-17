import re
import random

class PromptProcessor:
    def __init__(self):
        # Define genre keywords and their characteristics
        self.genre_patterns = {
            'trap': {
                'bpm_range': (130, 180),
                'kick_pattern': 'heavy',
                'hihat_style': 'rapid',
                'mood': 'dark'
            },
            'drill': {
                'bpm_range': (130, 160), 
                'kick_pattern': 'sliding',
                'hihat_style': 'sparse',
                'mood': 'dark'
            },
            'boom bap': {
                'bpm_range': (80, 100),
                'kick_pattern': 'punchy',
                'hihat_style': 'simple',
                'mood': 'classic'
            },
            'lo-fi': {
                'bpm_range': (70, 90),
                'kick_pattern': 'soft',
                'hihat_style': 'vinyl',
                'mood': 'chill'
            }
        }
        
        # Tempo keywords
        self.tempo_keywords = {
            'slow': (60, 90),
            'medium': (90, 120),
            'fast': (120, 160),
            'rapid': (160, 200),
            'chill': (70, 95),
            'upbeat': (120, 140)
        }
        
        # Mood keywords
        self.mood_keywords = {
            'dark': {'minor_key': True, 'distortion': 0.8},
            'bright': {'minor_key': False, 'distortion': 0.2},
            'aggressive': {'volume': 1.2, 'distortion': 0.9},
            'soft': {'volume': 0.7, 'distortion': 0.1},
            'heavy': {'bass_boost': 1.5, 'distortion': 0.7},
            'melodic': {'melody': True, 'harmony': True}
        }

    def parse_prompt(self, prompt):
        """
        Parse a natural language prompt into musical parameters
        """
        prompt_lower = prompt.lower()
        
        # Initialize default parameters
        params = {
            'genre': 'trap',  # default
            'bpm': 140,
            'bars': 4,
            'mood': 'neutral',
            'kick_pattern': 'standard',
            'hihat_style': 'standard',
            'bass_boost': 1.0,
            'distortion': 0.3,
            'volume': 1.0
        }
        
        # Extract genre
        for genre, characteristics in self.genre_patterns.items():
            if genre in prompt_lower:
                params['genre'] = genre
                params['bpm'] = random.randint(*characteristics['bpm_range'])
                params['kick_pattern'] = characteristics['kick_pattern']
                params['hihat_style'] = characteristics['hihat_style']
                params['mood'] = characteristics['mood']
                break
        
        # Extract specific tempo mentions
        bpm_match = re.search(r'(\d+)\s*bpm', prompt_lower)
        if bpm_match:
            params['bpm'] = int(bpm_match.group(1))
        else:
            # Check for tempo keywords
            for tempo_word, (min_bpm, max_bpm) in self.tempo_keywords.items():
                if tempo_word in prompt_lower:
                    params['bpm'] = random.randint(min_bpm, max_bpm)
                    break
        
        # Extract mood characteristics
        for mood, characteristics in self.mood_keywords.items():
            if mood in prompt_lower:
                params['mood'] = mood
                params.update(characteristics)
        
        # Extract specific instrument mentions
        if 'heavy 808' in prompt_lower or 'heavy bass' in prompt_lower:
            params['bass_boost'] = 1.8
        
        if 'fast hi-hat' in prompt_lower or 'rapid hi-hat' in prompt_lower:
            params['hihat_style'] = 'rapid'
        
        if 'punchy kick' in prompt_lower:
            params['kick_pattern'] = 'punchy'
        
        # Extract length
        bars_match = re.search(r'(\d+)\s*bar', prompt_lower)
        if bars_match:
            params['bars'] = int(bars_match.group(1))
        
        return params

    def generate_description(self, params):
        """
        Generate a description of what will be created
        """
        description = f"Creating a {params['genre']} beat at {params['bpm']} BPM"
        
        if params['mood'] != 'neutral':
            description += f" with a {params['mood']} mood"
        
        if params['kick_pattern'] != 'standard':
            description += f", {params['kick_pattern']} kick drums"
        
        if params['hihat_style'] != 'standard':
            description += f", {params['hihat_style']} hi-hats"
        
        description += f" for {params['bars']} bars"
        
        return description

# Test the prompt processor
if __name__ == "__main__":
    processor = PromptProcessor()
    
    test_prompts = [
        "dark trap beat with heavy 808s at 140 BPM",
        "chill lo-fi beat, slow tempo, soft drums",
        "aggressive drill beat with rapid hi-hats",
        "boom bap beat with punchy kicks, 90 BPM",
        "fast trap beat, 8 bars, heavy bass"
    ]
    
    print("🎵 Testing Prompt Processor...")
    for prompt in test_prompts:
        params = processor.parse_prompt(prompt)
        description = processor.generate_description(params)
        print(f"\nPrompt: '{prompt}'")
        print(f"Result: {description}")
        print(f"Parameters: {params}")