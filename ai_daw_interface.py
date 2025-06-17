import os
import sys
from ai_beat_generator import SmartDrumMachine
import json
from datetime import datetime

class AIDAWInterface:
    def __init__(self):
        self.drum_machine = SmartDrumMachine()
        self.session_beats = []
        self.session_name = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
    def print_banner(self):
        print("\n" + "="*60)
        print("🎵  AI PRODUCER DAW - PROMPT TO BEAT GENERATOR  🎵")
        print("="*60)
        print("Transform your ideas into beats with natural language!")
        print("Examples:")
        print("  • 'dark trap beat with heavy 808s at 140 BPM'")
        print("  • 'chill lo-fi beat, slow tempo'")
        print("  • 'aggressive drill beat with rapid hi-hats'")
        print("  • 'boom bap beat with punchy kicks, 8 bars'")
        print("="*60)
        
    def print_menu(self):
        print("\n🎛️  MAIN MENU:")
        print("1. Generate Beat from Prompt")
        print("2. View Generated Beats")
        print("3. Generate Multiple Beats")
        print("4. Save Session")
        print("5. Load Previous Session")
        print("6. Help & Examples")
        print("7. Exit")
        print("-" * 40)
        
    def generate_single_beat(self):
        print("\n🎹 BEAT GENERATOR")
        print("Enter your prompt (or 'back' to return to menu):")
        
        while True:
            prompt = input("💭 Prompt: ").strip()
            
            if prompt.lower() == 'back':
                return
            elif prompt.lower() == 'help':
                self.show_examples()
                continue
            elif not prompt:
                print("Please enter a prompt!")
                continue
                
            try:
                print(f"\n🚀 Generating beat...")
                filename, params = self.drum_machine.create_beat_from_prompt(prompt)
                
                beat_info = {
                    'prompt': prompt,
                    'filename': filename,
                    'params': params,
                    'timestamp': datetime.now().isoformat()
                }
                self.session_beats.append(beat_info)
                
                print(f"✅ Success! Generated: {filename}")
                print(f"📊 Genre: {params['genre']} | BPM: {params['bpm']} | Bars: {params['bars']}")
                
                # Ask if they want to generate another
                another = input("\n🔄 Generate another beat? (y/n): ").strip().lower()
                if another != 'y':
                    break
                    
            except Exception as e:
                print(f"❌ Error generating beat: {e}")
                print("Please try again with a different prompt.")
                
    def generate_multiple_beats(self):
        print("\n🎼 BATCH BEAT GENERATOR")
        print("Enter multiple prompts (one per line, empty line to finish):")
        
        prompts = []
        while True:
            prompt = input(f"Prompt {len(prompts) + 1}: ").strip()
            if not prompt:
                break
            prompts.append(prompt)
            
        if not prompts:
            print("No prompts entered!")
            return
            
        print(f"\n🚀 Generating {len(prompts)} beats...")
        
        for i, prompt in enumerate(prompts, 1):
            try:
                print(f"\n[{i}/{len(prompts)}] Processing: '{prompt}'")
                filename, params = self.drum_machine.create_beat_from_prompt(prompt)
                
                beat_info = {
                    'prompt': prompt,
                    'filename': filename,
                    'params': params,
                    'timestamp': datetime.now().isoformat()
                }
                self.session_beats.append(beat_info)
                
                print(f"✅ Generated: {filename}")
                
            except Exception as e:
                print(f"❌ Error with prompt '{prompt}': {e}")
                
        print(f"\n🎉 Batch complete! Generated {len([b for b in self.session_beats if any(p == b['prompt'] for p in prompts)])} beats")
        
    def view_generated_beats(self):
        if not self.session_beats:
            print("\n📭 No beats generated in this session yet!")
            return
            
        print(f"\n🎵 GENERATED BEATS ({len(self.session_beats)} total)")
        print("-" * 60)
        
        for i, beat in enumerate(self.session_beats, 1):
            print(f"{i}. {beat['filename']}")
            print(f"   Prompt: '{beat['prompt']}'")
            print(f"   Style: {beat['params']['genre']} | {beat['params']['bpm']} BPM | {beat['params']['bars']} bars")
            print(f"   Created: {beat['timestamp'][:19].replace('T', ' ')}")
            print()
            
    def save_session(self):
        if not self.session_beats:
            print("\n📭 No beats to save!")
            return
            
        session_data = {
            'session_name': self.session_name,
            'created': datetime.now().isoformat(),
            'beats': self.session_beats
        }
        
        filename = f"{self.session_name}.json"
        with open(filename, 'w') as f:
            json.dump(session_data, f, indent=2)
            
        print(f"\n💾 Session saved as: {filename}")
        print(f"📊 Saved {len(self.session_beats)} beats")
        
    def load_session(self):
        # List available sessions
        session_files = [f for f in os.listdir('.') if f.startswith('session_') and f.endswith('.json')]
        
        if not session_files:
            print("\n📭 No saved sessions found!")
            return
            
        print(f"\n📁 AVAILABLE SESSIONS:")
        for i, session_file in enumerate(session_files, 1):
            print(f"{i}. {session_file}")
            
        try:
            choice = int(input(f"\nSelect session (1-{len(session_files)}): ")) - 1
            if 0 <= choice < len(session_files):
                with open(session_files[choice], 'r') as f:
                    session_data = json.load(f)
                    
                self.session_beats = session_data['beats']
                self.session_name = session_data['session_name']
                
                print(f"✅ Loaded session: {self.session_name}")
                print(f"📊 Contains {len(self.session_beats)} beats")
            else:
                print("Invalid selection!")
                
        except (ValueError, FileNotFoundError, json.JSONDecodeError) as e:
            print(f"❌ Error loading session: {e}")
            
    def show_examples(self):
        print("\n📖 PROMPT EXAMPLES:")
        print("\n🎵 Trap/Hip-Hop:")
        print("  • 'dark trap beat with heavy 808s at 140 BPM'")
        print("  • 'aggressive trap beat, fast hi-hats, 8 bars'")
        print("  • 'melodic trap beat with soft drums'")
        
        print("\n🎵 Lo-Fi:")
        print("  • 'chill lo-fi beat, slow tempo'")
        print("  • 'soft lo-fi beat with vinyl texture'")
        print("  • 'relaxing lo-fi beat, 70 BPM'")
        
        print("\n🎵 Boom Bap:")
        print("  • 'boom bap beat with punchy kicks'")
        print("  • 'classic boom bap, 90 BPM, 4 bars'")
        print("  • 'old school boom bap with simple drums'")
        
        print("\n🎵 Drill:")
        print("  • 'UK drill beat with sliding 808s'")
        print("  • 'aggressive drill beat with sparse hi-hats'")
        print("  • 'dark drill beat, 150 BPM'")
        
        print("\n💡 Tips:")
        print("  • Specify BPM: 'at 140 BPM' or 'fast tempo'")
        print("  • Set length: '8 bars' or '4 bars'")
        print("  • Add mood: 'dark', 'aggressive', 'chill', 'soft'")
        print("  • Mention instruments: 'heavy 808s', 'rapid hi-hats', 'punchy kicks'")
        
    def run(self):
        self.print_banner()
        
        while True:
            self.print_menu()
            
            try:
                choice = input("🎛️  Select option (1-7): ").strip()
                
                if choice == '1':
                    self.generate_single_beat()
                elif choice == '2':
                    self.view_generated_beats()
                elif choice == '3':
                    self.generate_multiple_beats()
                elif choice == '4':
                    self.save_session()
                elif choice == '5':
                    self.load_session()
                elif choice == '6':
                    self.show_examples()
                elif choice == '7':
                    print("\n👋 Thanks for using AI Producer DAW!")
                    if self.session_beats:
                        save_prompt = input("💾 Save session before exit? (y/n): ").strip().lower()
                        if save_prompt == 'y':
                            self.save_session()
                    break
                else:
                    print("❌ Invalid option! Please choose 1-7.")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    daw = AIDAWInterface()
    daw.run()