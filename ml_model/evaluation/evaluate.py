"""
Evaluation script for loading saved Hybrid Model checkpoints and assessing test performance.
"""
import os
import sys
import argparse
import torch
from torch.utils.data import DataLoader
from torchvision.datasets import ImageFolder

# Add root and backend to pythonpath
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, os.path.join(PROJECT_ROOT, "backend"))

from app.ml.hybrid_model import HybridQuantumCareModel
from app.ml.preprocessing import get_inference_transforms
from ml_model.evaluation.metrics import compute_classification_metrics


def run_model_evaluation(checkpoint_path: str, test_dir: str):
    print("================================================================")
    print("QuantumCare – Model Evaluation & Metric Auditor")
    print(f"Checkpoint: {checkpoint_path}")
    print(f"Dataset:    {test_dir}")
    print("================================================================")

    if not os.path.exists(checkpoint_path):
        print(f"[-] Checkpoint not found at: {checkpoint_path}")
        print("    Run `python ml_model/training/train.py` first to train a checkpoint.")
        return

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = HybridQuantumCareModel(n_qubits=4, n_layers=2, num_classes=3).to(device)
    model.load_state_dict(torch.load(checkpoint_path, map_location=device))
    model.eval()

    if os.path.exists(test_dir):
        test_dataset = ImageFolder(test_dir, transform=get_inference_transforms())
    else:
        print(f"[!] Test directory '{test_dir}' not found. Using synthetic medical test set for demonstration.")
        print("    Refer to dataset/README.md for instructions on downloading MedMNIST/ISIC datasets.")
        from ml_model.training.train import SyntheticMedicalDataset
        test_dataset = SyntheticMedicalDataset(num_samples=32)

    test_loader = DataLoader(test_dataset, batch_size=8, shuffle=False)

    all_preds, all_labels, all_probs = [], [], []
    with torch.no_grad():
        for images, labels in test_loader:
            images = images.to(device)
            logits, _, _ = model(images)
            probs = torch.softmax(logits, dim=-1)
            preds = torch.argmax(logits, dim=-1)

            all_preds.extend(preds.cpu().tolist())
            all_labels.extend(labels.tolist())
            all_probs.extend(probs.cpu().tolist())

    metrics = compute_classification_metrics(all_labels, all_preds, all_probs)
    print("\n--- Empirical Performance Metrics ---")
    print(f"Accuracy:  {metrics['accuracy'] * 100:.2f}%")
    print(f"Precision: {metrics['precision_macro']:.4f}")
    print(f"Recall:    {metrics['recall_macro']:.4f}")
    print(f"F1-Score:  {metrics['f1_macro']:.4f}")
    print(f"Confusion Matrix:\n{metrics['confusion_matrix']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", type=str, default="ml_model/saved_models/best_hybrid_model.pth")
    parser.add_argument("--test_dir", type=str, default="dataset/test")
    args = parser.parse_args()

    run_model_evaluation(args.checkpoint, args.test_dir)
