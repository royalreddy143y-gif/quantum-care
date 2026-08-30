# Medical Datasets Reference & Setup Guide

**QuantumCare** is designed to work with standardized, openly licensed medical imaging benchmarks. To adhere to research ethics, copyright regulations, and patient privacy standards (HIPAA/GDPR), no raw patient datasets are bundled within this repository without explicit licensing.

The platform operates out-of-the-box in **DEMO Mode** (`MODEL_MODE=demo`). When you are ready to train on a real dataset, follow the instructions below.

---

## 1. Supported Open Research Datasets

### A. MedMNIST v2 (Recommended for College & Academic Demonstrations)
- **Dataset Name**: MedMNIST v2 (specifically **PathMNIST** or **ChestMNIST**)
- **Source**: [https://medmnist.com](https://medmnist.com) / [Nature Scientific Data Paper](https://www.nature.com/articles/s41597-022-01721-8)
- **License**: Creative Commons Attribution 4.0 International (CC BY 4.0)
- **Number of Classes**: 
  - PathMNIST: 9 tissue types (colorectal cancer histology)
  - ChestMNIST: Binary/Multi-label (thoracic diseases)
- **Intended Use**: Educational benchmarks for biomedical image classification and quantum machine learning experimentation.
- **How to Download**:
  ```bash
  pip install medmnist
  python -c "import medmnist; from medmnist import PathMNIST; PathMNIST(split='train', download=True)"
  ```

### B. ISIC Archive (Skin Lesion Dermoscopy)
- **Dataset Name**: International Skin Imaging Collaboration (ISIC) Benchmark
- **Source**: [https://www.isic-archive.com](https://www.isic-archive.com)
- **License**: CC-BY-NC (Non-commercial educational research)
- **Number of Classes**: 2 or 7 classes (Benign Nevus, Melanoma, Basal Cell Carcinoma, etc.)
- **Intended Use**: Dermoscopic feature analysis and lesion segmentation.

### C. CBIS-DDSM (Curated Breast Imaging Subset of DDSM)
- **Dataset Name**: CBIS-DDSM Mammography
- **Source**: The Cancer Imaging Archive (TCIA) / [TCIA CBIS-DDSM](https://wiki.cancerimagingarchive.net/display/Public/CBIS-DDSM)
- **License**: TCIA Data Usage Policy (Open Academic Research)
- **Number of Classes**: 2 classes (Benign vs Malignant calcification/mass)
- **Intended Use**: Mammographic lesion classification.

---

## 2. Expected Dataset Directory Structure

When organizing your dataset for training, format it into standard `ImageFolder` structure:

```
dataset/
├── train/
│   ├── normal/
│   │   ├── scan_001.png
│   │   └── scan_002.png
│   ├── suspicious/
│   │   ├── scan_003.png
│   │   └── scan_004.png
│   └── neoplasm/
│       ├── scan_005.png
│       └── scan_006.png
├── val/
│   ├── normal/
│   ├── suspicious/
│   └── neoplasm/
└── test/
    ├── normal/
    ├── suspicious/
    └── neoplasm/
```

---

## 3. Data Preparation & Ingestion Script

To prepare any custom images into normalized 224x224 RGB scans for QuantumCare:

```python
from PIL import Image
import os

def prepare_image(src_path, dest_path):
    with Image.open(src_path) as img:
        rgb = img.convert('RGB')
        resized = rgb.resize((224, 224), Image.Resampling.LANCZOS)
        resized.save(dest_path, format='PNG')
```

---

## 4. Configuring Real Model Mode

Once your dataset is prepared and trained:
1. Place the saved model checkpoint in `ml_model/saved_models/best_hybrid_model.pth`.
2. In your `.env` file, change:
   ```env
   MODEL_MODE=research
   ```
3. Restart the FastAPI backend server.

---

## 5. Critical Research & Safety Reminder
All datasets cited here are strictly for non-clinical research. Predictions generated from these models are experimental computational outputs and **MUST NOT** be used for clinical diagnoses or patient care.
