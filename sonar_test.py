import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display

def generate_ocean_noise(duration_sec, sr=22050):
    """
    Generates 'Pink Noise' to simulate background ocean static
    (waves, distant ships, seismic activity).
    """
    # White noise
    white = np.random.randn(int(duration_sec * sr))
    # Filter to make it 'Pink' (deeper, rumbling noise)
    # Simple approximation using Cumulative Sum
    pink = np.cumsum(white) 
    # Normalize to range -1 to 1
    pink = pink / np.max(np.abs(pink))
    return pink * 0.1  # Reduce volume to 30%

def inject_megalodon_signal(audio, sr=22050):
    """
    Injects a 'Ghost Signal': Ultra-low frequency pulses (10-15 Hz).
    This mimics a massive biological heart beat or vocalization.
    """
    t = np.linspace(0, len(audio)/sr, len(audio))
    
    # Create a 15Hz pulse (Infrasound - barely audible)
    # It pulses every 5 seconds
    pulse = np.sin(2 * np.pi * 15 * t) * np.sin(2 * np.pi * 0.2 * t)
    
    # Add to background noise
    return audio + (pulse * 3.0)

# --- EXECUTION ---

# 1. Simulate 30 seconds of ocean audio
sr = 22050
duration = 30
print("Generating ocean background noise...")
ocean_noise = generate_ocean_noise(duration, sr)

# 2. Hide the monster in the noise
print("Injecting biological anomaly (15Hz Infrasound)...")
mixed_signal = inject_megalodon_signal(ocean_noise, sr)

# 3. VISUALIZE: The Spectrogram
# This is how we "see" sound.
plt.figure(figsize=(12, 6))

# Compute Short-Time Fourier Transform (STFT)
D = librosa.stft(mixed_signal)
S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)

# Plot
librosa.display.specshow(S_db, sr=sr, x_axis='time', y_axis='hz')
plt.colorbar(format='%+2.0f dB')
plt.ylim(0, 100) # ZOOM IN: Only show low frequencies (0-100Hz)
plt.title('Simulated Sonar Scan: Can you see the anomaly at 15Hz?')
plt.xlabel('Time (seconds)')
plt.ylabel('Frequency (Hz)')
plt.show()

print("Spectrogram generated. Look at the bottom of the graph (15Hz line).")