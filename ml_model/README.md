# Classical Machine Learning & Hybrid Model Subsystem

This module contains the preprocessing, training, and evaluation pipelines for the **QuantumCare** Hybrid Platform.

---

## 1. Architecture Overview

1. **Vision Backbone**:
   - **Swin Transformer** (Hierarchical Vision Transformer with Shifted Windows).
   - Patches are linearly embedded and processed through successive attention stages, outputting a high-level 768-dimensional latent vector.

2. **Feature Projection & Reduction**:
   - Reduces 768 visual dimensions down to 4 target quantum feature channels using batch-normalized dense projections.

3. **Hybrid Coupling**:
   - The 4 classical features are converted to quantum rotational angles in \([0, \pi]\), passed through the PennyLane Variational Quantum Circuit, and re-concatenated with classical representations for final decision boundary learning.

---

## 2. Directory Structure

```
ml_model/
├── preprocessing/
│   └── augmentations.py     # Random crop, flip, rotation, and ImageNet normalization
├── training/
│   └── train.py             # Full PyTorch training loop with train/val/test split
├── evaluation/
│   ├── metrics.py           # Precision, Recall, F1, Confusion Matrix, ROC-AUC
│   └── evaluate.py          # Standalone checkpoint auditor
├── saved_models/            # Checkpoints (.pth)
└── README.md
```

---

## 3. How to Train

```bash
# Training with default synthetic tensors (for demonstration):
python ml_model/training/train.py --epochs 5 --batch_size 8

# Training on a real downloaded medical dataset:
python ml_model/training/train.py --data_dir /path/to/dataset --epochs 10 --batch_size 16
```

---

## 4. Evaluation Metrics Computed

- **Accuracy**: Overall classification accuracy across classes.
- **Precision (Macro)**: Unweighted mean precision across classes.
- **Recall (Macro)**: Unweighted mean recall across classes.
- **F1-Score (Macro)**: Harmonic mean of precision and recall.
- **Confusion Matrix**: Multi-class misclassification distribution.
- **ROC-AUC (OVR)**: Area under the Receiver Operating Characteristic curve.

---

## 5. Medical Safety Statement
No clinical validation or diagnostic guarantees are implied. This model is purely for scientific experimentation.
