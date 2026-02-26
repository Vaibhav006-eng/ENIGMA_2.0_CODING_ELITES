import mne
import numpy as np

def preprocess_eeg(file_path: str):
    """
    Load an EDF file and apply basic preprocessing:
    - Band-pass filter (0.5 - 45 Hz)
    - Notch filter (50/60 Hz)
    - Re-referencing
    - Epoch segmentation
    """
    if file_path.endswith('.edf'):
        raw = mne.io.read_raw_edf(file_path, preload=True)
    elif file_path.endswith('.fif'):
        raw = mne.io.read_raw_fif(file_path, preload=True)
    else:
        raise ValueError("Unsupported file format")
    
    # Basic filtering
    raw.filter(l_freq=0.5, h_freq=45.0, fir_design='firwin')
    
    # Assuming 50Hz line noise for now. Ensure frequencies don't exceed Nyquist.
    nyquist = raw.info['sfreq'] / 2.0
    freqs = np.arange(50, int(nyquist), 50)
    if len(freqs) > 0:
        raw.notch_filter(freqs)
    
    # Re-referencing
    raw.set_eeg_reference('average', projection=True)
    
    # For now, just return the continuous raw data rather than epochs
    # We will segment during feature extraction or later based on events
    return raw
