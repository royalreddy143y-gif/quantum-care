from typing import Dict, Any, List, Optional, cast
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, roc_auc_score


def compute_classification_metrics(
    y_true: List[int],
    y_pred: List[int],
    y_prob: Optional[List[List[float]]] = None,
    class_names: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Computes rigorous classification metrics using scikit-learn.
    Does not invent or extrapolate outcomes.
    """
    y_true_arr = np.array(y_true)
    y_pred_arr = np.array(y_pred)

    acc = float(accuracy_score(y_true_arr, y_pred_arr))
    precision = float(precision_score(y_true_arr, y_pred_arr, average="macro", zero_division=cast(Any, 0)))
    recall = float(recall_score(y_true_arr, y_pred_arr, average="macro", zero_division=cast(Any, 0)))
    f1 = float(f1_score(y_true_arr, y_pred_arr, average="macro", zero_division=cast(Any, 0)))
    cm = confusion_matrix(y_true_arr, y_pred_arr).tolist()

    metrics = {
        "accuracy": round(acc, 4),
        "precision_macro": round(precision, 4),
        "recall_macro": round(recall, 4),
        "f1_macro": round(f1, 4),
        "confusion_matrix": cm,
        "class_names": class_names or ["Class 0", "Class 1", "Class 2"]
    }

    if y_prob is not None:
        try:
            prob_arr = np.array(y_prob)
            if prob_arr.shape[1] > 2:
                roc_auc = float(roc_auc_score(y_true_arr, prob_arr, multi_class="ovr"))
            else:
                roc_auc = float(roc_auc_score(y_true_arr, prob_arr[:, 1]))
            metrics["roc_auc"] = round(roc_auc, 4)
        except Exception:
            metrics["roc_auc"] = None

    return metrics
