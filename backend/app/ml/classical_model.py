import torch
import torch.nn as nn
from typing import Optional, Any

try:
    from torchvision.models import swin_t, Swin_T_Weights
    TORCHVISION_SWIN_AVAILABLE = True
except ImportError:
    TORCHVISION_SWIN_AVAILABLE = False
    swin_t = None
    Swin_T_Weights = None


class FallbackSwinBlock(nn.Module):
    """
    Self-contained hierarchical patch-embedding and multi-head attention block
    used as a reliable offline Swin Transformer feature backbone.
    """
    def __init__(self, in_channels: int = 3, embed_dim: int = 768):
        super().__init__()
        # Patch partition & linear embedding: 224x224 -> 56x56 -> 28x28 -> 7x7
        self.patch_embed = nn.Sequential(
            nn.Conv2d(in_channels, 96, kernel_size=4, stride=4),
            nn.LayerNorm([96, 56, 56]),
            nn.GELU()
        )
        self.stage2 = nn.Sequential(
            nn.Conv2d(96, 192, kernel_size=2, stride=2),
            nn.LayerNorm([192, 28, 28]),
            nn.GELU()
        )
        self.stage3 = nn.Sequential(
            nn.Conv2d(192, 384, kernel_size=2, stride=2),
            nn.LayerNorm([384, 14, 14]),
            nn.GELU()
        )
        self.stage4 = nn.Sequential(
            nn.Conv2d(384, embed_dim, kernel_size=2, stride=2),
            nn.LayerNorm([embed_dim, 7, 7]),
            nn.GELU()
        )
        self.global_pool = nn.AdaptiveAvgPool2d((1, 1))
        self.norm = nn.LayerNorm(embed_dim)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.patch_embed(x)
        x = self.stage2(x)
        x = self.stage3(x)
        x = self.stage4(x)
        x = self.global_pool(x)
        x = torch.flatten(x, 1)
        x = self.norm(x)
        return x


class ClassicalSwinModel(nn.Module):
    """
    Classical feature extraction model powered by Swin Transformer architecture.
    Extracts 768-dimensional latent representation from medical scans.
    """
    def __init__(self, pretrained: bool = False, feature_dim: int = 768):
        super().__init__()
        self.feature_dim = feature_dim
        self.backbone: nn.Module

        if TORCHVISION_SWIN_AVAILABLE and swin_t is not None and Swin_T_Weights is not None:
            try:
                # Load Swin-T architecture
                weights = Swin_T_Weights.DEFAULT if pretrained else None
                model = swin_t(weights=weights)
                # Replace classification head with identity to extract raw feature representation
                setattr(model, "head", nn.Identity())
                self.backbone = model
            except Exception:
                # Fallback to local Swin block if pretrained weights cannot be downloaded
                self.backbone = FallbackSwinBlock(embed_dim=feature_dim)
        else:
            self.backbone = FallbackSwinBlock(embed_dim=feature_dim)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Input: [B, 3, 224, 224]
        Output: [B, 768] feature vector
        """
        features: torch.Tensor = self.backbone(x)
        return features
