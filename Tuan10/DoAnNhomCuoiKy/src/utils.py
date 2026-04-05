"""
utils.py — Hàm hỗ trợ: vẽ biểu đồ, lưu model, load model
"""
from pathlib import Path
import joblib
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, roc_curve, auc
from sklearn.preprocessing import label_binarize

CLASS_LABELS = ['Normal', 'Hyper', 'Hypo']
CLASSES = [1, 2, 3]


def ensure_dir(path: str | Path) -> Path:
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def save_model(model, name: str, folder: str) -> None:
    folder = ensure_dir(folder)
    path = folder / f"{name}.pkl"
    joblib.dump(model, path)
    print(f"Saved → {path}")


def load_model(name: str, folder: str):
    path = Path(folder) / f"{name}.pkl"
    return joblib.load(path)


def plot_confusion_matrix(model, X_test, y_test, model_name: str, save_dir: str = None) -> None:
    y_pred = model.predict(X_test)
    cm = confusion_matrix(y_test, y_pred, labels=CLASSES)
    fig, ax = plt.subplots(figsize=(5, 4))
    disp = ConfusionMatrixDisplay(cm, display_labels=CLASS_LABELS)
    disp.plot(ax=ax, colorbar=False, cmap='Blues')
    ax.set_title(f'Confusion Matrix — {model_name}', fontsize=11)
    plt.tight_layout()
    if save_dir:
        save_dir = ensure_dir(save_dir)
        fig.savefig(save_dir / f"cm_{model_name}.png", dpi=150)
    plt.show()
    plt.close()


def plot_all_confusion_matrices(models: dict, X_test, y_test, save_dir: str = None) -> None:
    for name, model in models.items():
        short = name.split('_', 1)[1]
        plot_confusion_matrix(model, X_test, y_test, short, save_dir)


def plot_roc_curves(model, X_test, y_test, model_name: str, save_dir: str = None) -> None:
    y_bin = label_binarize(y_test, classes=CLASSES)
    if hasattr(model, 'predict_proba'):
        y_score = model.predict_proba(X_test)
    else:
        y_score = model.decision_function(X_test)

    fig, ax = plt.subplots(figsize=(6, 5))
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
    for i, label in enumerate(CLASS_LABELS):
        fpr, tpr, _ = roc_curve(y_bin[:, i], y_score[:, i])
        roc_auc = auc(fpr, tpr)
        ax.plot(fpr, tpr, color=colors[i], lw=1.8, label=f'{label} (AUC = {roc_auc:.2f})')
    ax.plot([0, 1], [0, 1], 'k--', lw=1)
    ax.set_xlim([0, 1]); ax.set_ylim([0, 1.02])
    ax.set_xlabel('False Positive Rate')
    ax.set_ylabel('True Positive Rate')
    ax.set_title(f'ROC Curves (OvR) — {model_name}', fontsize=11)
    ax.legend(loc='lower right', fontsize=9)
    plt.tight_layout()
    if save_dir:
        save_dir = ensure_dir(save_dir)
        fig.savefig(save_dir / f"roc_{model_name}.png", dpi=150)
    plt.show()
    plt.close()


def plot_metrics_comparison(df: pd.DataFrame, save_path: str = None) -> None:
    metrics = ['Accuracy', 'Precision', 'Recall', 'F1-Score', 'AUC']
    fig, axes = plt.subplots(1, 5, figsize=(22, 5))
    for ax, m in zip(axes, metrics):
        df.sort_values(m).plot(kind='barh', x='Model', y=m, ax=ax, legend=False, color='#4C72B0')
        ax.set_xlim(0.5, 1.02)
        ax.set_title(m, fontsize=11)
        ax.set_xlabel(''); ax.set_ylabel('')
        for bar in ax.patches:
            ax.text(bar.get_width() + 0.005, bar.get_y() + bar.get_height() / 2, f'{bar.get_width():.2f}', va='center', fontsize=8)
    plt.suptitle('Baseline Models — Metric Comparison', fontsize=13, y=1.01)
    plt.tight_layout()
    if save_path:
        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.show()
    plt.close()
