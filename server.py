from flask import Flask, jsonify
from flask_cors import CORS
import numpy as np
import librosa
import random
import time

app = Flask(__name__)
CORS(app)  # Allow React to talk to this server

# --- RE-USE YOUR CORE ENGINES ---

def generate_ocean_data():
    """Simulates 10 seconds of hydrophone data."""
    sr = 22050
    duration = 10
    
    # 1. Base Ocean Noise
    white = np.random.randn(int(duration * sr))
    pink = np.cumsum(white)
    pink = pink / np.max(np.abs(pink))
    audio = pink * 0.1
    
    # 2. Randomly decide if Megalodon is passing by (30% chance)
    megalodon_present = random.random() < 0.3
    
    if megalodon_present:
        t = np.linspace(0, len(audio)/sr, len(audio))
        pulse = np.sin(2 * np.pi * 15 * t) * np.sin(2 * np.pi * 0.2 * t)
        audio = audio + (pulse * 3.0)
        
    return audio, megalodon_present

def analyze_audio(audio, sr=22050):
    """Runs the FFT analysis."""
    # High-Res FFT
    D = np.abs(librosa.stft(audio, n_fft=16384))
    freqs = librosa.fft_frequencies(sr=sr, n_fft=16384)
    mean_energy = np.mean(D, axis=1)
    
    # Target Indices
    target_idx = np.argmin(np.abs(freqs - 15))
    low_idx = np.argmin(np.abs(freqs - 10))
    high_idx = np.argmin(np.abs(freqs - 20))
    
    # Calculate Ratio
    signal = mean_energy[target_idx]
    noise = (mean_energy[low_idx] + mean_energy[high_idx]) / 2
    ratio = signal / (noise + 0.00001)
    
    return ratio

# --- API ENDPOINT ---

@app.route('/api/scan', methods=['GET'])
def scan_sector():
    # 1. Run the hardware simulation
    audio_data, is_monster_here = generate_ocean_data()
    
    # 2. Run the AI analysis
    snr_ratio = analyze_audio(audio_data)
    
    # 3. Determine Threat Level
    status = "CLEAR"
    if snr_ratio > 10.0:
        status = "ALERT"
    
    # 4. Return JSON to Frontend
    return jsonify({
        "timestamp": time.time(),
        "status": status,
        "snr_ratio": round(snr_ratio, 2),
        "depth": 4000,
        "location": "Point Nemo (Sector 7)"
    })

if __name__ == '__main__':
    print("--- DEEPSCAN SERVER ONLINE (Port 5000) ---")
    app.run(debug=True, port=5000)