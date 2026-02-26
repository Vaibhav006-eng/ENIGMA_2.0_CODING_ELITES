import mne
import numpy as np
import datetime
import os

def generate_mock_edf():
    print("Generating mock EEG EDF data...")
    n_channels = 64
    sfreq = 250  # Lowered sampling frequency to reduce file size
    times = np.linspace(0, 10, sfreq * 10)  # 10 seconds of data
    
    # Generate random noise + simple sine waves to mimic brain activity
    data = np.random.randn(n_channels, len(times)) * 1e-6
    
    # Add fake alpha wave (10Hz) to represent waking state
    alpha = np.sin(2 * np.pi * 10 * times) * 2e-6
    for i in range(10, 20):  # Add to occipital/parietal channels
        data[i] += alpha
        
    # Create MNE info structure
    ch_names = [f'EEG_{i:03d}' for i in range(1, 65)]
    ch_types = ['eeg'] * n_channels
    info = mne.create_info(ch_names=ch_names, sfreq=sfreq, ch_types=ch_types)
    
    # Create Raw object
    raw = mne.io.RawArray(data, info)
    
    # Since writing native EDF is tricky without pyedflib, we will export to FIF format.
    # The frontend is already configured to accept .fif files.
    filename = "test_eeg.fif"
    raw.save(filename, overwrite=True)
    print(f"\nSuccess! Saved mock EEG data to: {os.path.abspath(filename)}")
    print("You can now upload this file in the Streamlit web interface.")

if __name__ == "__main__":
    generate_mock_edf()
