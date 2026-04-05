"""
evaluate.py — Tính 5 metrics theo yêu cầu đề bài (multiclass)
  Accuracy, Precision, Recall, F1-Score, AUC (OvR weighted)
Có hỗ trợ thêm 5-fold cross validation trên tập train.
"""
import time
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.model_selection import cross_validate
from sklearn.preprocessing import label_binarize

CLASSES = [1, 2, 3]


def get_prediction_scores(model, X):
    """Lấy xác suất/score cho AUC một cách an toàn."""
    if hasattr(model, 'predict_proba'):
        return model.predict_proba(X)
    if hasattr(model, 'decision_function'):
        scores = model.decision_function(X)
        if scores.ndim == 1:
            scores = np.column_stack([-scores, scores])
        return scores
    raise AttributeError('Model không hỗ trợ predict_proba hoặc decision_function.')


def evaluate_model(model, X_test, y_test) -> dict:
    """Tính metrics cho 1 model đã fit."""
    y_pred = model.predict(X_test)
    y_score = get_prediction_scores(model, X_test)

    if y_score.ndim == 1 or (y_score.ndim == 2 and y_score.shape[1] == 1):
        y_score = label_binarize(y_score, classes=CLASSES)

    return {
        'Accuracy': round(accuracy_score(y_test, y_pred), 2),
        'Precision': round(precision_score(y_test, y_pred, average='weighted', zero_division=0), 2),
        'Recall': round(recall_score(y_test, y_pred, average='weighted', zero_division=0), 2),
        'F1-Score': round(f1_score(y_test, y_pred, average='weighted', zero_division=0), 2),
        'AUC': round(roc_auc_score(y_test, y_score, multi_class='ovr', average='weighted'), 2),
    }


def compute_cv_scores(model, X_train, y_train, cv) -> dict:
    """Tính CV score trên tập train theo đúng yêu cầu k=5."""
    scoring = {
        'accuracy': 'accuracy',
        'precision': 'precision_weighted',
        'recall': 'recall_weighted',
        'f1': 'f1_weighted',
        'auc': 'roc_auc_ovr_weighted',
    }
    cv_result = cross_validate(
        clone(model), X_train, y_train,
        cv=cv, scoring=scoring, n_jobs=1, error_score='raise'
    )
    return {
        'CV Accuracy': round(cv_result['test_accuracy'].mean(), 2),
        'CV Precision': round(cv_result['test_precision'].mean(), 2),
        'CV Recall': round(cv_result['test_recall'].mean(), 2),
        'CV F1-Score': round(cv_result['test_f1'].mean(), 2),
        'CV AUC': round(cv_result['test_auc'].mean(), 2),
    }


def train_and_evaluate(models: dict, X_train, y_train, X_test, y_test, cv=None) -> pd.DataFrame:
    """Fit tất cả models, trả về DataFrame kết quả + execution time."""
    rows = []
    for name, model in models.items():
        cv_metrics = compute_cv_scores(model, X_train, y_train, cv) if cv is not None else {}

        t0 = time.time()
        model.fit(X_train, y_train)
        elapsed = round(time.time() - t0, 4)

        metrics = evaluate_model(model, X_test, y_test)
        row = {
            'Model': name.split('_', 1)[1],
            **cv_metrics,
            **metrics,
            'Time(s)': elapsed,
        }
        rows.append(row)

        print(
            f"{name:30s}  cv_f1={row.get('CV F1-Score', np.nan):.2f}  "
            f"test_f1={metrics['F1-Score']:.2f}  auc={metrics['AUC']:.2f}  time={elapsed}s"
        )

    preferred = [
        'Model', 'CV Accuracy', 'CV Precision', 'CV Recall', 'CV F1-Score', 'CV AUC',
        'Accuracy', 'Precision', 'Recall', 'F1-Score', 'AUC', 'Time(s)'
    ]
    df = pd.DataFrame(rows)
    return df[[c for c in preferred if c in df.columns]]


def find_top2(df: pd.DataFrame) -> None:
    """In top 2 models theo từng metric test-set."""
    for metric in ['Accuracy', 'Precision', 'Recall', 'F1-Score', 'AUC']:
        top2 = df.nlargest(2, metric)[['Model', metric]]
        print(f"\nTop 2 — {metric}:")
        print(top2.to_string(index=False))
