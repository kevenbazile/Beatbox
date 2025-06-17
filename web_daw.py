from flask import Flask, render_template, request, jsonify, send_file
import os
import json
from datetime import datetime
from ai_beat_generator import SmartDrumMachine
import threading
import time

app = Flask(__name__)
drum_machine = SmartDrumMachine()

# Store generated beats
generated_beats = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_beat():
    try:
        data = request.get_json()
        prompt = data.get('prompt', '').strip()
        
        if not prompt:
            return jsonify({'error': 'Please enter a prompt!'}), 400
        
        # Generate the beat
        filename, params = drum_machine.create_beat_from_prompt(prompt)
        
        # Store beat info
        beat_info = {
            'id': len(generated_beats) + 1,
            'prompt': prompt,
            'filename': filename,
            'params': params,
            'timestamp': datetime.now().isoformat(),
            'file_size': os.path.getsize(filename) if os.path.exists(filename) else 0
        }
        generated_beats.append(beat_info)
        
        return jsonify({
            'success': True,
            'beat': beat_info,
            'message': f'Generated {filename} successfully!'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/beats')
def list_beats():
    return jsonify({'beats': generated_beats})

@app.route('/download/<filename>')
def download_file(filename):
    try:
        if os.path.exists(filename):
            return send_file(filename, as_attachment=True)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/examples')
def get_examples():
    examples = [
        "dark trap beat with heavy 808s at 140 BPM",
        "chill lo-fi beat, slow tempo",
        "aggressive drill beat with rapid hi-hats", 
        "boom bap beat with punchy kicks, 90 BPM",
        "melodic trap beat with soft drums",
        "UK drill beat with sliding 808s",
        "relaxing lo-fi beat, 70 BPM, 8 bars",
        "fast trap beat with heavy bass"
    ]
    return jsonify({'examples': examples})

if __name__ == '__main__':
    # Create templates directory
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    print("🌐 AI DAW Web Interface starting...")
    print("🎵 Open your browser to: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
    