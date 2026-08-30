import os
from typing import Tuple
from PIL import Image
import torch
from torchvision import transforms

# Standard Medical / ImageNet Normalization values
IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]


def get_inference_transforms(target_size: Tuple[int, int] = (224, 224)) -> transforms.Compose:
    """Prepares standard deterministic preprocessing for inference."""
    return transforms.Compose([
        transforms.Resize(target_size),
        transforms.ToTensor(),
        transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD)
    ])


def get_training_transforms(target_size: Tuple[int, int] = (224, 224)) -> transforms.Compose:
    """Augmentation pipeline for medical image training."""
    return transforms.Compose([
        transforms.Resize((int(target_size[0] * 1.1), int(target_size[1] * 1.1))),
        transforms.RandomCrop(target_size),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomRotation(degrees=15),
        transforms.ColorJitter(brightness=0.1, contrast=0.1),
        transforms.ToTensor(),
        transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD)
    ])


def load_and_preprocess_image(image_path: str, target_size: Tuple[int, int] = (224, 224)) -> torch.Tensor:
    """
    Safely loads an image from disk, converts to RGB, and transforms into a normalized PyTorch tensor [1, 3, 224, 224].
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found at path: {image_path}")

    with Image.open(image_path) as img:
        img_rgb = img.convert("RGB")
        transform = get_inference_transforms(target_size)
        tensor = transform(img_rgb)
        if not isinstance(tensor, torch.Tensor):
            tensor = transforms.ToTensor()(tensor)
        return tensor.unsqueeze(0)  # Shape: [1, 3, 224, 224]
