"""
models.py — Định nghĩa 10 classification algorithms (Step 3 đề bài)
Tất cả dùng random_state=42 để reproducible.

Các model nhạy với scale sẽ được gói trong Pipeline(StandardScaler + model)
để tránh data leakage và bảo đảm chuẩn hóa chỉ fit trên tập train.
"""
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (RandomForestClassifier, AdaBoostClassifier,
                               GradientBoostingClassifier)
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

SEED = 42


def get_baseline_models() -> dict:
    """
    Trả về dict {tên: model} của 10 thuật toán theo đề bài.
    Key bắt đầu bằng số thứ tự để dễ sort khi report.
    """
    return {
        '01_kNN':                  make_pipeline(StandardScaler(), KNeighborsClassifier()),
        '02_NaiveBayes':           make_pipeline(StandardScaler(), GaussianNB()),
        '03_SVM':                  make_pipeline(StandardScaler(), SVC(probability=True, random_state=SEED)),
        '04_DecisionTree':         DecisionTreeClassifier(random_state=SEED),
        '05_RandomForest':         RandomForestClassifier(random_state=SEED),
        '06_AdaBoost':             AdaBoostClassifier(random_state=SEED),
        '07_GradientBoosting':     GradientBoostingClassifier(random_state=SEED),
        '08_LDA':                  make_pipeline(StandardScaler(), LinearDiscriminantAnalysis()),
        '09_MLP':                  make_pipeline(StandardScaler(), MLPClassifier(random_state=SEED, max_iter=1000)),
        '10_LogisticRegression':   make_pipeline(StandardScaler(), LogisticRegression(random_state=SEED, max_iter=1000)),
    }
