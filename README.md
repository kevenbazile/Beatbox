# 🎵 AI Music Generator - Docker Edition

Generate full songs like Michael Jackson's "Beat It" and Sleepy Hallow drill tracks using AI!

## 🚀 Quick Start

### Prerequisites
1. **Install Docker Desktop**: https://www.docker.com/products/docker-desktop/
2. **Restart your computer** after Docker installation
3. **Start Docker Desktop** and wait for it to be ready

### Running the Application

#### Option 1: Use the Run Script (Windows)
```bash
# Double-click run.bat or run in command prompt:
run.bat
```

#### Option 2: Manual Commands
```bash
# Create output directory
mkdir generated_songs

# Build and run
docker-compose up --build
```

### First Run
- **First build takes 10-20 minutes** (downloading AI models)
- **Subsequent runs take 1-2 minutes**
- **AI model loading takes 5-10 minutes** after container starts

### Access the Application
Open your browser to: **http://localhost:5000**

## 🎵 What You Can Generate

### Artist Styles Available:
- 🕺 **Michael Jackson Style** - Pop rock like "Beat It"
- 🎤 **Sleepy Hallow Style** - Brooklyn drill beats
- 🎵 **Drake Style** - Melodic hip-hop
- 🔥 **Travis Scott Style** - Psychedelic trap
- 🌙 **The Weeknd Style** - Dark R&B
- 🎯 **Custom** - Any style you describe

### Sample Prompts:
- "upbeat pop rock like Beat It by Michael Jackson with funky bassline"
- "dark drill beat like Sleepy Hallow with heavy 808s"
- "melodic hip hop like Drake with soft piano"
- "electronic dance music with synthesizers and four-on-the-floor beat"

## 📁 File Structure
```
ai-daw-project/
├── Dockerfile              # Container configuration
├── docker-compose.yml      # Service orchestration
├── requirements.txt        # Python dependencies
├── full_song_generator.py  # AI song generation engine
├── web_daw.py              # Web interface
├── run.bat                 # Windows run script
├── generated_songs/        # Output directory (created automatically)
└── README.md               # This file
```

## ⚙️ Technical Details

### Container Specs:
- **Base Image**: Python 3.11 slim
- **AI Model**: Meta's MusicGen-Small
- **Audio Format**: WAV (44.1kHz)
- **Generation Time**: 2-5 minutes per 30-second song
- **Memory Usage**: ~4GB RAM required

### Supported Formats:
- **Audio Output**: WAV files
- **Song Length**: 10-60 seconds
- **Quality**: Professional studio quality

## 🔧 Troubleshooting

### Docker Issues:
```bash
# If container won't start
docker-compose down
docker system prune -f
docker-compose up --build

# Check Docker status
docker --version
docker-compose --version
```

### Performance Issues:
- **Slow generation**: Normal for CPU-only. First song takes longest.
- **Memory errors**: Close other applications, Docker needs 4GB+ RAM
- **Model loading**: Takes 5-10 minutes on first run

### Port Conflicts:
If port 5000 is busy, edit `docker-compose.yml`:
```yaml
ports:
  - "5001:5000"  # Use port 5001 instead
```

## 🎉 Features

### ✅ What Works:
- Full song generation with melody, harmony, and rhythm
- Multiple artist style presets
- Custom text-to-music generation
- Professional audio quality
- Web-based interface
- Automatic file downloads

### 🔄 Generated Content:
- **Duration**: 10-60 seconds per song
- **Instruments**: Drums, bass, melody, harmony
- **Styles**: Pop, rock, hip-hop, drill, R&B, electronic
- **Quality**: Studio-grade audio (44.1kHz WAV)

## 🎵 Usage Tips

1. **First Generation**: Takes longest due to model loading
2. **Shorter Durations**: Generate 15-30 second clips for faster results
3. **Specific Prompts**: More detailed descriptions = better results
4. **Artist Styles**: Use preset buttons for best results
5. **File Management**: Songs saved in `generated_songs/` folder

## 🛠️ Advanced Usage

### Custom Prompts:
Be specific about:
- **Genre**: "trap", "drill", "pop rock", "R&B"
- **Instruments**: "electric guitar", "808 drums", "piano"
- **Mood**: "dark", "upbeat", "melodic", "aggressive"
- **Artist References**: "like Drake", "similar to Beat It"

### Example Advanced Prompts:
```
"cinematic orchestral music with epic drums and strings"
"lo-fi hip hop with jazz samples and vinyl crackle"
"aggressive metal with distorted guitars and double bass drums"
"ambient electronic with atmospheric pads and subtle percussion"
```

## 📞 Support

If you encounter issues:
1. Check Docker Desktop is running
2. Restart the container: `docker-compose restart`
3. Check container logs: `docker-compose logs`
4. Rebuild if needed: `docker-compose up --build`

---

**🎵 Enjoy creating your AI-generated music! 🎵**