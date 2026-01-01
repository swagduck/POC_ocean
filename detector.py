import numpy as np
import librosa

# --- PART 1: THE GENERATORS (Create the Data) ---

def generate_ocean_noise(duration_sec, sr=22050):
    """Generates 'Pink Noise' to simulate background ocean static."""
    # Create white noise
    white = np.random.randn(int(duration_sec * sr))
    # Turn it into pink noise (deeper sound)
    pink = np.cumsum(white) 
    # Normalize volume
    pink = pink / np.max(np.abs(pink))
    return pink * 0.1  # Low volume background

def inject_megalodon_signal(audio, sr=22050):
    """Injects a 15Hz pulsing 'Ghost Signal'."""
    t = np.linspace(0, len(audio)/sr, len(audio))
    # Create a 15Hz pulse that beats every 5 seconds
    pulse = np.sin(2 * np.pi * 15 * t) * np.sin(2 * np.pi * 0.2 * t)
    return audio + (pulse * 3.0) # High volume signal

# --- PART 2: THE DETECTOR (The AI Brain) ---

def analyze_sector(audio_segment, sr=22050):
    """
    HIGH-RES BRAIN: Uses n_fft=16384 to create ultra-narrow frequency bins (~1.3Hz).
    This stops the massive 15Hz signal from 'bleeding' into the 20Hz neighbor.
    """
    # 1. Convert Audio -> Frequency (High Resolution)
    # We increase n_fft to 16384 to get finer detail at low frequencies
    D = np.abs(librosa.stft(audio_segment, n_fft=16384))
    
    # 2. Average energy for each frequency
    freqs = librosa.fft_frequencies(sr=sr, n_fft=16384)
    mean_energy = np.mean(D, axis=1)
    
    # 3. Define Targets
    target_hz = 15
    lower_neighbor_hz = 10
    upper_neighbor_hz = 20
    
    # 4. Find Indices
    target_idx = np.argmin(np.abs(freqs - target_hz))
    low_idx = np.argmin(np.abs(freqs - lower_neighbor_hz))
    high_idx = np.argmin(np.abs(freqs - upper_neighbor_hz))
    
    # 5. Calculate Energy
    signal_strength = mean_energy[target_idx]
    
    # We take a slightly wider average for background to be safe
    background_noise = (mean_energy[low_idx] + mean_energy[high_idx]) / 2
    
    # 6. Calculate Ratio
    ratio = signal_strength / (background_noise + 0.00001)
    
    print(f"   [METRICS] 15Hz: {signal_strength:.2f} | Neighbors: {background_noise:.2f} | Spike Ratio: {ratio:.1f}")
    
    # If signal is 3x louder than its neighbors
    if ratio > 3.0: 
        return True
    return False

# --- PART 3: MAIN EXECUTION (Run the Test) ---

if __name__ == "__main__":
    # Setup variables
    sr = 22050
    duration = 10
    
    print("--- INITIALIZING DEEPSCAN SYSTEM ---\n")

    # TEST 1: Generate Empty Ocean Data
    print("1. Scanning Sector A (Empty Ocean)...")
    ocean_noise = generate_ocean_noise(duration, sr) # <--- THIS DEFINES THE VARIABLE
    alert = analyze_sector(ocean_noise, sr)
    
    if alert:
        print(">>> RESULT: FALSE POSITIVE. (System Error)")
    else:
        print(">>> RESULT: CLEAR. No biologicals detected.")

    print("-" * 40)

    # TEST 2: Generate Megalodon Data
    print("2. Scanning Sector B (Anomaly Present)...")
    mixed_signal = inject_megalodon_signal(ocean_noise, sr)
    alert = analyze_sector(mixed_signal, sr)
    
    if alert:
        print(">>> RESULT: ALERT! TARGET ACQUIRED AT 15HZ!")
        print(">>> STATUS: Deploying camera drone...")
    else:
        print(">>> RESULT: FAILED. Signal missed.")