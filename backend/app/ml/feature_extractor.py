import torch
import torch.nn as nn
from typing import Optional, Dict, Any


class MultimodalFeatureProjector(nn.Module):
    """
    Projects high-dimensional classical visual features down to the quantum Hilbert space
    input dimension (n_qubits) and optionally encodes clinical biomarkers & genomic markers.
    """
    def __init__(self, visual_dim: int = 768, quantum_dim: int = 4, biomarker_dim: int = 3, genomic_dim: int = 2):
        super().__init__()
        self.quantum_dim = quantum_dim

        # Dimensionality reduction from Swin 768 -> quantum_dim (e.g., 4)
        self.visual_to_quantum = nn.Sequential(
            nn.Linear(visual_dim, 128),
            nn.LayerNorm(128),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(128, 32),
            nn.ReLU(),
            nn.Linear(32, quantum_dim)
        )

        # Optional biomarker dense encoder (e.g. CA125, PSA, CEA)
        self.biomarker_encoder = nn.Sequential(
            nn.Linear(biomarker_dim, 16),
            nn.ReLU(),
            nn.Linear(16, 8)
        )

        # Optional genomic dense encoder (e.g. BRCA1, EGFR)
        self.genomic_encoder = nn.Sequential(
            nn.Linear(genomic_dim, 16),
            nn.ReLU(),
            nn.Linear(16, 8)
        )

    def project_visual(self, visual_features: torch.Tensor) -> torch.Tensor:
        """Projects [B, 768] -> [B, 4]"""
        return self.visual_to_quantum(visual_features)

    def encode_clinical(
        self,
        biomarkers: Optional[torch.Tensor] = None,
        genomics: Optional[torch.Tensor] = None
    ) -> Optional[torch.Tensor]:
        """
        Encodes available clinical features. Returns None if neither is provided.
        Never fabricates values for absent modalities.
        """
        embeddings = []
        if biomarkers is not None:
            embeddings.append(self.biomarker_encoder(biomarkers))
        if genomics is not None:
            embeddings.append(self.genomic_encoder(genomics))

        if not embeddings:
            return None

        return torch.cat(embeddings, dim=-1)
