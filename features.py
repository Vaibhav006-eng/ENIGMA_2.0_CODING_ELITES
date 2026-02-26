import numpy as np

def extract_features(raw_eeg):
    """
    Extract frequency-domain, time-domain, and non-linear features.
    For this prototype, we'll extract simple frequency band powers 
    (Delta, Theta, Alpha, Beta, Gamma) from a predefined epoch.
    """
    # Sample Mock feature extraction logic for baseline
    # Assume 64 channels, extracting 5 bands per channel = 320 features
    features = {
        'delta_power': np.random.normal(0.5, 0.1, 64), # 0.5-4 Hz
        'theta_power': np.random.normal(0.4, 0.1, 64), # 4-8 Hz
        'alpha_power': np.random.normal(0.3, 0.1, 64), # 8-13 Hz
        'beta_power':  np.random.normal(0.2, 0.1, 64), # 13-30 Hz
        'gamma_power': np.random.normal(0.1, 0.05, 64) # >30 Hz
    }
    
    # Flatten into a single feature vector
    feature_vector = np.concatenate([v for v in features.values()])
    return feature_vector

def extract_bands(raw_eeg):
    """
    For frontend summary dashboard
    """
    # mock summary data
    return {
        'Delta': float(round(np.random.uniform(10, 30), 2)),
        'Theta': float(round(np.random.uniform(15, 40), 2)),
        'Alpha': float(round(np.random.uniform(20, 50), 2)),
        'Beta': float(round(np.random.uniform(10, 30), 2)),
        'Gamma': float(round(np.random.uniform(5, 20), 2)), # Gamma decreases in SZ
    }
