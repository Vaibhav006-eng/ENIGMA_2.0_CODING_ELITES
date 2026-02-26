# ENIGMA_2.0_CODING_ELITES
# EEG-Based Schizophrenia Detection (ENIGMA 2.0 - Coding Elites)

## Problem Statement
Schizophrenia diagnosis is often **subjective and delayed** because it depends heavily on behavioral observation rather than measurable biomarkers.

This project proposes an **EEG-based AI system** to detect abnormal brain signal patterns associated with schizophrenia and support early risk assessment.

## The Challenge
Build an AI pipeline and interface that can:

- Process EEG recordings and extract clinically meaningful signal features.
- Identify patterns associated with schizophrenia risk.
- Generate interpretable outputs for clinicians and researchers.

## Deliverables

### 1) EEG Analysis Interface
- Upload/select EEG recordings.
- Preprocessing controls (artifact filtering, normalization, segmentation).
- Interactive plots for channel-wise signal inspection.

### 2) Early Schizophrenia Risk Scoring
- ML/DL-based inference on processed EEG segments.
- Patient-level risk score with confidence indicator.
- Threshold-based triage categories (Low / Medium / High Risk).

### 3) Explainable Brain Activity Visualization
- Explainability maps (feature/channel contribution over time).
- Visualization of abnormal activity bands and regions.
- Human-readable rationale accompanying the model output.

### 4) Research Dataset Pipeline
- Dataset ingestion and metadata validation.
- Standardized preprocessing workflow for reproducibility.
- Train/validation/test splitting and experiment tracking support.

## Suggested High-Level Workflow
1. Data Collection & Validation
2. Signal Preprocessing
3. Feature Engineering / Representation Learning
4. Model Training & Evaluation
5. Explainability & Visualization
6. Deployment in EEG Analysis Interface

## Expected Impact
- Earlier screening support for schizophrenia risk.
- More objective decision support using EEG biomarkers.
- Better clinician trust through explainable AI outputs.
