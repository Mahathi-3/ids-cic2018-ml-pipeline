<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/scikit--learn-1.3%2B-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white" alt="scikit-learn"/>
  <img src="https://img.shields.io/badge/XGBoost-2.0%2B-006600?style=for-the-badge&logo=xgboost&logoColor=white" alt="XGBoost"/>
  <img src="https://img.shields.io/badge/LightGBM-4.0%2B-9B59B6?style=for-the-badge" alt="LightGBM"/>
  <img src="https://img.shields.io/badge/SHAP-Explainability-E74C3C?style=for-the-badge" alt="SHAP"/>
</p>

<h1 align="center">🛡️ Network Intrusion Detection System</h1>
<h3 align="center">Machine Learning Pipeline on CSE-CIC-IDS2018</h3>

<p align="center">
  <em>A production-grade, leak-free ML pipeline for binary network intrusion detection using ensemble tree models, SMOTE-Tomek resampling, and stratified cross-validation — built to minimize false alarm rate without sacrificing recall.</em>
</p>

---

## 📋 Project Summary

This project implements an end-to-end **Network Intrusion Detection System (IDS)** that classifies network flows as **Benign** or **Attack** using the [CSE-CIC-IDS2018](https://www.unb.ca/cic/datasets/ids-2018.html) dataset. The pipeline evaluates three gradient-boosted / ensemble models — **Random Forest**, **XGBoost**, and **LightGBM** — under rigorous 5-fold stratified cross-validation with **SMOTETomek** resampling applied *inside* each fold to prevent data leakage. Nine domain-informed engineered features augment the original 80 CICFlowMeter features, and **SHAP** analysis provides global model explainability. The primary optimization target is **False Alarm Rate (FAR)**, because in real-world SOC environments, excessive false positives cause alert fatigue and erode analyst trust.

---

## 🏗️ Pipeline Architecture

```
┌──────────────┐     ┌─────────┐     ┌────────────────┐     ┌─────────────────────┐
│  Data Loading│────▶│   EDA   │────▶│ Preprocessing  │────▶│ Feature Engineering │
│ (10 Parquet) │     │ & Viz   │     │ Clean + Prune  │     │  (9 new features)   │
└──────────────┘     └─────────┘     └────────────────┘     └──────────┬──────────┘
                                                                       │
                                                                       ▼
                                                          ┌────────────────────────┐
                                                          │  Stratified 5-Fold CV  │
                                                          │  (100k sample, k=5)    │
                                                          └───────────┬────────────┘
                                                                      │
                                          ┌───────────────────────────┼───────────────────────────┐
                                          ▼                           ▼                           ▼
                                  ┌───────────────┐          ┌───────────────┐          ┌───────────────┐
                                  │ Random Forest │          │    XGBoost    │          │   LightGBM    │
                                  └───────┬───────┘          └───────┬───────┘          └───────┬───────┘
                                          │                          │                          │
                                          ▼                          ▼                          ▼
                                ┌─────────────────────────────────────────────────────────────────────┐
                                │              Per-Fold Inner Pipeline (no leakage)                   │
                                │  ┌──────────────┐  ┌─────────────┐  ┌───────────┐  ┌────────────┐  │
                                │  │ StandardScaler│─▶│ SMOTETomek  │─▶│  Train    │─▶│  Evaluate  │  │
                                │  │  (fit on train)│  │ (train only)│  │  Model    │  │  on Test   │  │
                                │  └──────────────┘  └─────────────┘  └───────────┘  └────────────┘  │
                                └─────────────────────────────────────────────────────────────────────┘
                                                              │
                                                              ▼
                                                  ┌─────────────────────┐
                                                  │   Aggregate Results │
                                                  │ Confusion Matrix,   │
                                                  │ ROC, SHAP, FAR      │
                                                  └─────────────────────┘
```

---

## 📊 Key Results

| Metric | Random Forest | XGBoost | LightGBM |
|:---|:---:|:---:|:---:|
| **Accuracy** | 97.52% | 97.79% | _TBD_ |
| **Precision** | 95.68% | 96.90% | _TBD_ |
| **Recall** | 91.72% | 91.88% | _TBD_ |
| **F1-Score** | 93.66% ± 0.17% | 94.32% ± 0.09% | _TBD_ |
| **AUC-ROC** | 0.9848 | 0.9855 | _TBD_ |
| **False Alarm Rate** ⬇️ | 1.04% | **0.73%** | _TBD_ |

> **Takeaway**: XGBoost achieves the best balance with the lowest FAR (0.73%) while maintaining competitive recall, making it the recommended production model.

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- ~4 GB RAM (for 100k sample)

### 1. Clone & Install

```bash
git clone https://github.com/<your-username>/ids-ml-pipeline.git
cd ids-ml-pipeline
pip install -r requirements.txt
```

### 2. Download the Dataset

Download the **CSE-CIC-IDS2018** dataset (Parquet format) from [Kaggle](https://www.kaggle.com/datasets/solarmainframe/ids-intrusion-csv) or the [CIC website](https://www.unb.ca/cic/datasets/ids-2018.html) and place the 10 Parquet files inside:

```
archive (1)/
├── part-00000-...snappy.parquet
├── part-00001-...snappy.parquet
└── ... (10 files total)
```

### 3. Run the Pipeline

```bash
jupyter notebook IDS_CIC2018_Final.ipynb
```

Execute cells sequentially. The notebook handles EDA, preprocessing, feature engineering, model training with CV, evaluation, and SHAP analysis.

---

## 📁 Project Structure

```
cyber_final/
│
├── 📓 IDS_CIC2018_Final.ipynb     # Main pipeline notebook (RF, XGBoost, LightGBM)
├── 📄 requirements.txt            # Python dependencies
├── 📄 README.md                   # This file
│
├── 📂 archive (1)/                # Dataset directory (10 Parquet files)
│   ├── Botnet-Friday-..._CICFlowMeter.parquet
│   ├── Bruteforce-Wednesday-..._CICFlowMeter.parquet
│   └── ... (10 files total)
│
├── 📊 confusion_matrix.png        # Generated by notebook
├── 📊 feature_importance.png      # Generated by notebook
├── 📊 roc_curve.png               # Generated by notebook
├── 📊 plot_01..07_*.png           # Additional visualizations
└── 📄 results_all_models.csv      # Model comparison metrics
```

---

## 🧠 Design Decisions

### 1. Why SMOTETomek Resampling?

The CSE-CIC-IDS2018 dataset is **heavily imbalanced** (~83% Benign, ~17% Attack). Naïve oversampling creates exact duplicates that cause overfitting. **SMOTETomek** combines two complementary techniques:

- **SMOTE** (Synthetic Minority Over-sampling Technique) generates *synthetic* minority samples by interpolating between existing attack flows and their k-nearest neighbors — introducing diversity without duplication.
- **Tomek Links** identifies pairs of samples from opposite classes that are each other's nearest neighbor and removes the majority-class sample. This cleans the decision boundary by eliminating ambiguous borderline instances.

The result: a cleaner, more separable feature space that yields **lower False Alarm Rate** and **higher Precision** compared to SMOTE alone.

### 2. Why Stratified K-Fold Cross-Validation?

Standard random k-fold splitting can produce folds where the minority class is underrepresented or overrepresented, leading to **optimistically biased** or **high-variance** performance estimates. **Stratified K-Fold** guarantees that each fold preserves the original class distribution (~83/17 split), producing:

- More **stable** and **reliable** metric estimates across folds
- Lower standard deviation in F1 (±0.09% for XGBoost)
- Realistic performance expectations for deployment

Critically, **SMOTETomek is applied inside each fold** (only on training data), preventing synthetic samples from leaking into the validation set — a common pitfall that inflates reported metrics.

### 3. Why FAR as the Primary Metric?

In operational Security Operations Centers (SOCs), **False Alarm Rate** (False Positive Rate) directly determines analyst workload and system trust:

| Metric | What It Tells You |
|:---|:---|
| Accuracy | Misleading on imbalanced data — a "predict all benign" model gets ~83% accuracy |
| Recall | Critical (missed attacks are dangerous), but must be balanced against FAR |
| **FAR** | **Directly measures alert fatigue** — every false alarm wastes analyst time |

Our pipeline achieves **FAR as low as 0.73%** (XGBoost), meaning only ~7 out of every 1,000 benign flows trigger a false alert.

### 4. Why Correlation Pruning with Engineered Feature Protection?

CICFlowMeter produces 80+ features, many of which are highly correlated (e.g., `Fwd Packet Length Mean` and `Fwd Packet Length Max`). High multicollinearity:

- Inflates feature importance estimates
- Increases model training time
- Can degrade generalization

We apply **Pearson correlation pruning** (threshold = 0.95) to remove redundant features, but **protect all 9 engineered features** from pruning. This ensures domain-informed features survive the filter while eliminating redundant raw features.

---

## ⚙️ Feature Engineering

Nine domain-informed features were engineered from raw CICFlowMeter fields to capture network traffic behavior patterns:

| # | Feature | Formula | Intuition |
|:---:|:---|:---|:---|
| 1 | `byte_ratio` | `Fwd_Bytes / (Fwd_Bytes + Bwd_Bytes + ε)` | Directional asymmetry — attacks often have skewed upload/download ratios |
| 2 | `packet_ratio` | `Fwd_Packets / (Fwd_Packets + Bwd_Packets + ε)` | Packet-level directionality — e.g., DDoS sends many packets with few responses |
| 3 | `network_bytes` | `Fwd_Bytes + Bwd_Bytes` | Total data volume — large transfers may indicate exfiltration |
| 4 | `duration_per_byte` | `Duration / (network_bytes + ε)` | Transfer efficiency — slow, small transfers suggest C2 beaconing |
| 5 | `bytes_per_packet` | `network_bytes / (Total_Packets + ε)` | Average payload size — small packets may indicate scanning |
| 6 | `load_ratio` | `Fwd_Bytes × Fwd_Packets / (Bwd_Bytes × Bwd_Packets + ε)` | Combined directional load — amplifies byte_ratio signal |
| 7 | `fwd_pkt_size_avg` | `Fwd_Bytes / (Fwd_Packets + ε)` | Average forward packet size — distinguishes bulk transfer from probing |
| 8 | `flow_bytes_per_second` | `network_bytes / (Duration + ε)` | Throughput — high-rate flows may indicate flooding attacks |
| 9 | `header_payload_ratio` | `Header_Length / (Payload_Length + ε)` | Protocol overhead — abnormal ratios indicate crafted packets |

> **Note**: `ε` (epsilon = 1) is added to denominators to prevent division-by-zero errors and maintain numerical stability.

---

## 🔮 Future Improvements

| Priority | Improvement | Description |
|:---:|:---|:---|
| 🔴 High | **Multi-class Classification** | Extend from binary (Benign/Attack) to fine-grained attack-type classification (DDoS, Brute Force, Botnet, etc.) |
| 🔴 High | **Hyperparameter Optimization** | Integrate [Optuna](https://optuna.org/) for Bayesian hyperparameter search with FAR-aware objective functions |
| 🟡 Medium | **Deep Learning Models** | Experiment with 1D-CNN and LSTM architectures for sequential flow analysis |
| 🟡 Medium | **Real-Time Inference** | Build a streaming inference pipeline (e.g., Kafka + FastAPI) for live network monitoring |
| 🟢 Low | **Feature Selection** | Apply mutual-information or Boruta for more principled feature selection |
| 🟢 Low | **Model Stacking** | Ensemble RF + XGBoost + LightGBM via a meta-learner for improved robustness |

---

## 📜 License

This project is for educational and portfolio purposes. The CSE-CIC-IDS2018 dataset is provided by the [Canadian Institute for Cybersecurity](https://www.unb.ca/cic/).

---

<p align="center">
  <strong>Built with 🔬 rigorous ML methodology and ☕ strong coffee</strong>
</p>
