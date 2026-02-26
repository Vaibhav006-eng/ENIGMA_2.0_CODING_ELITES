import shap
import numpy as np
import plotly.express as px
from .model import load_or_train_model
import matplotlib.pyplot as plt
import io

def generate_shap_values(feature_vector):
    """
    Generates SHAP feature importance for the given prediction.
    """
    model = load_or_train_model()
    # Mocking explainer for speed in this demo, usually TreeExplainer
    # Since model is XGBoost
    explainer = shap.TreeExplainer(model)
    
    # SHAP expected 2d array
    shap_vals = explainer.shap_values(feature_vector.reshape(1, -1))
    
    # Sort and take top 10 features
    feature_importance = np.abs(shap_vals[0]).argsort()[::-1][:10]
    
    return [
        {"feature": f"Feature {i}", "importance": float(shap_vals[0][i])} 
        for i in feature_importance
    ]

def generate_brain_heatmap(feature_vector):
    """
    Generates mock topographic data for plotting in frontend.
    Returns array of objects with coordinates and values.
    """
    return [
        {"x": float(np.random.uniform(-1, 1)), "y": float(np.random.uniform(-1, 1)), "value": float(v)}
        for v in feature_vector[:64]  # Mock values for 64 electrodes
    ]

def generate_waveform_image(raw_eeg):
    """
    Plots a 2s snippet of the raw EEG onto a styled matplotlib chart and returns png bytes.
    """
    try:
        data = raw_eeg.get_data()
        sfreq = raw_eeg.info['sfreq']
        times = np.arange(data.shape[1]) / sfreq
        
        plt.figure(figsize=(10, 3))
        max_idx = min(len(times), int(sfreq * 2)) # Plot 2 seconds
        
        # Neon cyan on navy
        plt.plot(times[:max_idx], data[0, :max_idx], color='#00f0ff', linewidth=1)
        plt.title('EEG Channel 1 - 2s Segment', color='white', fontsize=12)
        plt.xlabel('Time (s)', color='white')
        plt.ylabel('Amplitude', color='white')
        
        ax = plt.gca()
        ax.set_facecolor('#0a1128')
        plt.gcf().patch.set_facecolor('#0a1128')
        ax.tick_params(colors='white')
        for spine in ax.spines.values():
            spine.set_edgecolor('white')
            
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', dpi=150)
        plt.close()
        return buf.getvalue()
    except Exception as e:
        print("Waveform generation failed:", e)
        return None
