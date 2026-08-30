import os
import pytest
import torch
from PIL import Image

from app.ml.preprocessing import load_and_preprocess_image, get_inference_transforms
from app.ml.classical_model import ClassicalSwinModel
from app.ml.hybrid_model import HybridQuantumCareModel


@pytest.fixture
def sample_image_path(tmp_path):
    img = Image.new("RGB", (300, 300), color=(120, 150, 180))
    file_path = tmp_path / "test_scan.png"
    img.save(file_path)
    return str(file_path)


def test_image_preprocessing(sample_image_path):
    tensor = load_and_preprocess_image(sample_image_path)
    assert tensor.shape == (1, 3, 224, 224)
    assert isinstance(tensor, torch.Tensor)


def test_classical_swin_feature_extraction():
    model = ClassicalSwinModel(pretrained=False, feature_dim=768)
    model.eval()

    dummy_scan = torch.randn(2, 3, 224, 224)
    with torch.no_grad():
        features = model(dummy_scan)

    assert features.shape == (2, 768)


def test_hybrid_quantum_classical_forward():
    hybrid_model = HybridQuantumCareModel(n_qubits=4, n_layers=2, num_classes=3)
    hybrid_model.eval()

    dummy_input = torch.randn(1, 3, 224, 224)
    with torch.no_grad():
        logits, classical_4d, quantum_exp = hybrid_model(dummy_input)

    assert logits.shape == (1, 3)
    assert classical_4d.shape == (1, 4)
    assert quantum_exp.shape == (1, 4)
