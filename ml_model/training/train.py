"""
Training pipeline for the QuantumCare Hybrid Classical-Quantum Model.
Integrates Swin Transformer backbone with PennyLane Variational Quantum Circuit.
"""
import os
import sys
import argparse
from typing import Tuple, Optional

import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset, random_split
from torchvision.datasets import ImageFolder
from PIL import Image

# Add root and backend to pythonpath
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, os.path.join(PROJECT_ROOT, "backend"))

from app.ml.hybrid_model import HybridQuantumCareModel
from app.ml.preprocessing import get_training_transforms, get_inference_transforms
from ml_model.evaluation.metrics import compute_classification_metrics


class SyntheticMedicalDataset(Dataset):
    """Fallback synthetic dataset for demonstrating pipeline mechanics when no external dataset is downloaded."""
    def __init__(self, num_samples: int = 120, image_size: Tuple[int, int] = (224, 224), num_classes: int = 3):
        self.num_samples = num_samples
        self.image_size = image_size
        self.num_classes = num_classes
        torch.manual_seed(42)
        self.images = torch.randn(num_samples, 3, image_size[0], image_size[1])
        self.labels = torch.randint(0, num_classes, (num_samples,))

    def __len__(self):
        return self.num_samples

    def __getitem__(self, index):
        return self.images[index], self.labels[index]


def train_hybrid_system(
    data_dir: Optional[str] = None,
    epochs: int = 5,
    batch_size: int = 8,
    lr: float = 1e-4,
    save_dir: str = "ml_model/saved_models"
):
    print("=================================================================")
    print("QuantumCare – Hybrid Swin Transformer + PennyLane QML Training")
    print(f"Epochs: {epochs} | Batch Size: {batch_size} | Learning Rate: {lr}")
    print("=================================================================")

    os.makedirs(save_dir, exist_ok=True)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Execution Device: {device}")

    # 1. Dataset Loading
    if data_dir and os.path.exists(data_dir):
        print(f"Loading medical dataset from folder: {data_dir}")
        full_dataset = ImageFolder(data_dir, transform=get_training_transforms())
    else:
        print("[!] No external dataset directory specified. Using synthetic medical tensors for demonstration.")
        print("    Refer to dataset/README.md for instructions on downloading MedMNIST/ISIC datasets.")
        full_dataset = SyntheticMedicalDataset(num_samples=96)

    # 2. Train / Val / Test Splits (70% / 15% / 15%)
    n_total = len(full_dataset)
    n_train = int(0.70 * n_total)
    n_val = int(0.15 * n_total)
    n_test = n_total - n_train - n_val

    train_set, val_set, test_set = random_split(full_dataset, [n_train, n_val, n_test])

    train_loader = DataLoader(train_set, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_set, batch_size=batch_size, shuffle=False)
    test_loader = DataLoader(test_set, batch_size=batch_size, shuffle=False)

    print(f"Dataset split: Train={n_train}, Val={n_val}, Test={n_test}")

    # 3. Model Initialization
    model = HybridQuantumCareModel(n_qubits=4, n_layers=2, num_classes=3).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-2)

    best_val_loss = float("inf")

    # 4. Training Loop
    for epoch in range(epochs):
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0

        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)
            optimizer.zero_grad()

            logits, _, _ = model(images)
            loss = criterion(logits, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item() * images.size(0)
            preds = torch.argmax(logits, dim=-1)
            correct += (preds == labels).sum().item()
            total += labels.size(0)

        epoch_loss = running_loss / max(total, 1)
        epoch_acc = (correct / max(total, 1)) * 100

        # Validation Step
        model.eval()
        val_loss = 0.0
        val_correct = 0
        val_total = 0
        with torch.no_grad():
            for images, labels in val_loader:
                images, labels = images.to(device), labels.to(device)
                logits, _, _ = model(images)
                loss = criterion(logits, labels)
                val_loss += loss.item() * images.size(0)
                preds = torch.argmax(logits, dim=-1)
                val_correct += (preds == labels).sum().item()
                val_total += labels.size(0)

        epoch_val_loss = val_loss / max(val_total, 1)
        epoch_val_acc = (val_correct / max(val_total, 1)) * 100

        print(
            f"Epoch [{epoch+1:02d}/{epochs:02d}] "
            f"Train Loss: {epoch_loss:.4f}, Acc: {epoch_acc:.1f}% | "
            f"Val Loss: {epoch_val_loss:.4f}, Acc: {epoch_val_acc:.1f}%"
        )

        # Checkpoint Best Model
        if epoch_val_loss < best_val_loss:
            best_val_loss = epoch_val_loss
            ckpt_path = os.path.join(save_dir, "best_hybrid_model.pth")
            torch.save(model.state_dict(), ckpt_path)
            print(f"  [+] Saved new optimal checkpoint: {ckpt_path}")

    # 5. Final Test Evaluation
    print("\n--- Running Final Evaluation on Unseen Test Split ---")
    model.eval()
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
    print(f"Final Test Accuracy:  {metrics['accuracy'] * 100:.2f}%")
    print(f"Final Test Precision: {metrics['precision_macro']:.4f}")
    print(f"Final Test Recall:    {metrics['recall_macro']:.4f}")
    print(f"Final Test F1-Score:  {metrics['f1_macro']:.4f}")
    print(f"Confusion Matrix:     {metrics['confusion_matrix']}")
    print("\n[+] Training & Evaluation completed successfully.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train Hybrid QuantumCare Model")
    parser.add_argument("--data_dir", type=str, default=None, help="Path to medical dataset folder")
    parser.add_argument("--epochs", type=int, default=3, help="Training epochs")
    parser.add_argument("--batch_size", type=int, default=4, help="Batch size")
    parser.add_argument("--lr", type=float, default=1e-4, help="Learning rate")
    args = parser.parse_args()

    train_hybrid_system(
        data_dir=args.data_dir,
        epochs=args.epochs,
        batch_size=args.batch_size,
        lr=args.lr
    )
