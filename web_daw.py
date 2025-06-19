from flask import Flask, render_template_string, request, jsonify, send_file
import os
import json
from datetime import datetime
import traceback
import threading
import time

# Import the song generator
from full_song_generator import FullSongGenerator

app = Flask(__name__)
song_generator = None
generated_songs = []
generator_ready = False

def initialize_generator():
    """Initialize the generator in a background thread"""
    global song_generator, generator_ready
    try:
        print("🎵 Initializing AI Music Generator in background...")
        song_generator = FullSongGenerator()
        generator_ready = True
        print("✅ AI Music Generator ready!")
    except Exception as e:
        print(f"❌ Failed to initialize generator: {e}")
        traceback.print_exc()

# Start generator initialization in background
threading.Thread(target=initialize_generator, daemon=True).start()

# HTML Template with enhanced UI
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎵 AI Music Generator</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: white;
            padding: 20px;
        }
        .container {
            max-width: 1000px;
            margin: 0 auto;
        }
        .header {
            text-align: center;
            margin-bottom: 40px;
        }
        .header h1 {
            font-size: 3em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .card {
            background: rgba(255,255,255,0.1);
            border-radius: 20px;
            padding: 30px;
            backdrop-filter: blur(10px);
            margin-bottom: 30px;
            border: 1px solid rgba(255,255,255,0.2);
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 10px;
            font-weight: bold;
        }
        textarea, input[type="number"] {
            width: 100%;
            padding: 15px;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            background: rgba(255,255,255,0.9);
            color: #333;
        }
        textarea {
            height: 100px;
            resize: vertical;
        }
        .button-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        .btn {
            background: linear-gradient(45deg, #ff6b6b, #ee5a24);
            color: white;
            border: none;
            padding: 15px 25px;
            border-radius: 10px;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
            transition: all 0.3s ease;
            text-align: center;
        }
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(255, 107, 107, 0.3);
        }
        .btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }
        .btn-style {
            background: linear-gradient(45deg, #4CAF50, #45a049);
        }
        .btn-style:hover {
            box-shadow: 0 8px 25px rgba(76, 175, 80, 0.3);
        }
        .status {
            padding: 20px;
            margin: 20px 0;
            border-radius: 10px;
            display: none;
            align-items: center;
            gap: 15px;
        }
        .status.loading {
            background: rgba(52, 152, 219, 0.2);
            border: 1px solid #3498db;
            display: flex;
        }
        .status.success {
            background: rgba(46, 204, 113, 0.2);
            border: 1px solid #2ecc71;
        }
        .status.error {
            background: rgba(231, 76, 60, 0.2);
            border: 1px solid #e74c3c;
        }
        .status.warning {
            background: rgba(255, 193, 7, 0.2);
            border: 1px solid #ffc107;
            color: #856404;
        }
        .spinner {
            width: 24px;
            height: 24px;
            border: 3px solid rgba(255,255,255,0.3);
            border-top: 3px solid white;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .song-item {
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 20px;
            border-left: 5px solid #ff6b6b;
        }
        .song-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            flex-wrap: wrap;
            gap: 15px;
            margin-bottom: 15px;
        }
        .song-title {
            font-size: 1.2em;
            font-weight: bold;
            margin-bottom: 5px;
        }
        .song-meta {
            font-size: 0.9em;
            opacity: 0.8;
        }
        .download-btn {
            background: #2ecc71;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            transition: background 0.2s;
        }
        .download-btn:hover {
            background: #27ae60;
        }
        .ready-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
        }
        .ready { background: #2ecc71; }
        .not-ready { background: #e74c3c; animation: pulse 2s infinite; }
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎵 AI Music Generator</h1>
            <p>Create full songs like Michael Jackson's "Beat It" and Sleepy Hallow drill tracks</p>
            <p><span id="readyIndicator" class="ready-indicator not-ready"></span><span id="readyText">Initializing AI model...</span></p>
        </div>
        
        <div class="card">
            <h3>🎯 Create Your Song</h3>
            <div class="form-group">
                <label for="promptInput">Describe your song:</label>
                <textarea id="promptInput" placeholder="e.g., 'upbeat pop rock like Beat It by Michael Jackson with funky bassline' or 'dark drill beat like Sleepy Hallow'"></textarea>
            </div>
            
            <div class="form-group">
                <label for="duration">Duration (seconds):</label>
                <input type="number" id="duration" value="30" min="10" max="60">
            </div>
            
            <button class="btn" onclick="generateCustom()">🎵 Generate Custom Song</button>
            
            <div class="button-grid">
                <button class="btn btn-style" onclick="generateMJ()">🕺 Michael Jackson Style</button>
                <button class="btn btn-style" onclick="generateDrill()">🎤 Sleepy Hallow Drill</button>
                <button class="btn btn-style" onclick="generateDrake()">🎵 Drake Style</button>
                <button class="btn btn-style" onclick="generateTravis()">🔥 Travis Scott Style</button>
                <button class="btn btn-style" onclick="generateWeeknd()">🌙 The Weeknd Style</button>
            </div>
            
            <div id="status" class="status"></div>
        </div>
        
        <div class="card">
            <h3>🎵 Generated Songs</h3>
            <div id="songsList">
                <p style="opacity: 0.6; text-align: center; padding: 40px;">
                    No songs generated yet. Create your first masterpiece above! 🎼
                </p>
            </div>
        </div>
    </div>

    <script>
        let generatorReady = false;
        
        function checkGeneratorStatus() {
            fetch('/status')
                .then(response => response.json())
                .then(data => {
                    generatorReady = data.ready;
                    const indicator = document.getElementById('readyIndicator');
                    const text = document.getElementById('readyText');
                    
                    if (generatorReady) {
                        indicator.className = 'ready-indicator ready';
                        text.textContent = 'AI Model Ready!';
                    } else {
                        indicator.className = 'ready-indicator not-ready';
                        text.textContent = 'Loading AI Model...';
                        setTimeout(checkGeneratorStatus, 3000); // Check again in 3 seconds
                    }
                })
                .catch(() => {
                    setTimeout(checkGeneratorStatus, 5000); // Retry in 5 seconds
                });
        }
        
        function showStatus(message, type) {
            const status = document.getElementById('status');
            status.innerHTML = type === 'loading' ? 
                `<div class="spinner"></div>${message}` : message;
            status.className = 'status ' + type;
            status.style.display = type === 'loading' ? 'flex' : 'block';
            
            if (type !== 'loading') {
                setTimeout(() => status.style.display = 'none', 5000);
            }
        }
        
        function generateSong(prompt, style) {
            if (!generatorReady) {
                showStatus('⏳ AI model is still loading. Please wait...', 'warning');
                return;
            }
            
            const duration = document.getElementById('duration').value;
            
            showStatus(`🎵 Generating ${style} song... This may take 2-5 minutes...`, 'loading');
            
            fetch('/generate', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({prompt: prompt, duration: parseInt(duration), style: style})
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showStatus(`✅ ${data.message}`, 'success');
                    loadSongs();
                } else {
                    showStatus(`❌ Error: ${data.error}`, 'error');
                }
            })
            .catch(error => {
                showStatus(`❌ Error: ${error}`, 'error');
            });
        }
        
        function generateCustom() {
            const prompt = document.getElementById('promptInput').value.trim();
            if (!prompt) {
                showStatus('Please enter a song description!', 'error');
                return;
            }
            generateSong(prompt, 'custom');
        }
        
        function generateMJ() {
            generateSong('upbeat pop rock like Beat It by Michael Jackson with funky bassline and electric guitar', 'michael_jackson');
        }
        
        function generateDrill() {
            generateSong('dark drill beat like Sleepy Hallow with heavy 808s and menacing melody', 'sleepy_hallow');
        }
        
        function generateDrake() {
            generateSong('melodic hip hop like Drake with atmospheric production and soft piano', 'drake');
        }
        
        function generateTravis() {
            generateSong('psychedelic trap like Travis Scott with autotune and distorted 808s', 'travis_scott');
        }
        
        function generateWeeknd() {
            generateSong('dark R&B like The Weeknd with atmospheric synths and moody production', 'weeknd');
        }
        
        function loadSongs() {
            fetch('/songs')
                .then(response => response.json())
                .then(data => {
                    const list = document.getElementById('songsList');
                    if (data.songs.length === 0) {
                        list.innerHTML = '<p style="opacity: 0.6; text-align: center; padding: 40px;">No songs generated yet. Create your first masterpiece above! 🎼</p>';
                    } else {
                        list.innerHTML = data.songs.map(song => `
                            <div class="song-item">
                                <div class="song-header">
                                    <div>
                                        <div class="song-title">"${song.prompt}"</div>
                                        <div class="song-meta">
                                            Style: ${song.style} | 
                                            Duration: ${song.duration}s | 
                                            Size: ${(song.file_size/1024/1024).toFixed(1)}MB |
                                            Created: ${new Date(song.timestamp).toLocaleString()}
                                        </div>
                                    </div>
                                    <button class="download-btn" onclick="downloadSong('${song.basename}')">
                                        ⬇️ Download
                                    </button>
                                </div>
                            </div>
                        `).reverse().join('');
                    }
                });
        }
        
        function downloadSong(filename) {
            window.location.href = '/download/' + filename;
        }
        
        // Initialize
        checkGeneratorStatus();
        loadSongs();
        setInterval(loadSongs, 10000); // Refresh songs list every 10 seconds
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/status')
def status():
    return jsonify({
        'ready': generator_ready,
        'model_info': song_generator.get_model_info() if song_generator else None
    })

@app.route('/generate', methods=['POST'])
def generate_song():
    try:
        if not generator_ready:
            return jsonify({'error': 'AI model is still loading. Please wait...'}), 503
        
        data = request.get_json()
        prompt = data.get('prompt', '').strip()
        duration = int(data.get('duration', 30))
        style = data.get('style', 'custom')
        
        if not prompt:
            return jsonify({'error': 'Please enter a prompt!'}), 400
        
        print(f"🎵 Generation request: '{prompt}' ({duration}s, {style} style)")
        
        # Generate based on style
        if style == 'michael_jackson':
            result = song_generator.create_michael_jackson_style(duration)
        elif style == 'sleepy_hallow':
            result = song_generator.create_sleepy_hallow_style(duration)
        elif style == 'drake':
            result = song_generator.create_drake_style(duration)
        elif style == 'travis_scott':
            result = song_generator.create_travis_scott_style(duration)
        elif style == 'weeknd':
            result = song_generator.create_the_weeknd_style(duration)
        else:
            result = song_generator.generate_song(prompt, duration)
        
        # Store song info
        song_info = {
            'prompt': prompt,
            'filename': result['filename'],
            'basename': result['basename'],
            'duration': duration,
            'style': result['style'],
            'file_size': result['file_size'],
            'timestamp': datetime.now().isoformat()
        }
        generated_songs.append(song_info)
        
        return jsonify({
            'success': True,
            'song': song_info,
            'message': f'Generated {result["basename"]} successfully!'
        })
        
    except Exception as e:
        print(f"❌ Generation error: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/songs')
def list_songs():
    return jsonify({'songs': generated_songs})

@app.route('/download/<filename>')
def download_file(filename):
    try:
        filepath = os.path.join('generated_songs', filename)
        if os.path.exists(filepath):
            return send_file(filepath, as_attachment=True)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🌐 Starting AI Music Generator Web Server...")
    print("🎵 Access at: http://localhost:5000")
    print("⏳ AI model will load in background...")
    print("🔄 Docker container will handle all dependencies!")
    
    app.run(debug=False, host='0.0.0.0', port=5000)