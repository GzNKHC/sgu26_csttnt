"""
preprocess.py — Tiền xử lý dữ liệu Thyroid Gland
Dataset: new-thyroid.csv | 215 mẫu | 5 features | 3 classes
Classes: 1=normal, 2=hyper, 3=hypo

Lưu ý quan trọng:
- Không scale toàn bộ dataset trước khi chia train/test.
- Việc chuẩn hóa sẽ được thực hiện sau bước train_test_split,
  tốt nhất là bên trong Pipeline để tránh data leakage.
"""
from pathlib import Path
import pandas as pd

COLS = ['T3_resin', 'Thyroxin', 'Triiodothyronine', 'TSH_basal', 'TSH_diff', 'class']
CLASS_NAMES = {1: 'Normal', 2: 'Hyper', 3: 'Hypo'}


def ensure_parent_dir(path: str) -> None:
    """Tạo thư mục cha nếu chưa tồn tại."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)


def load_raw(path: str) -> pd.DataFrame:
    """Load file CSV gốc, gán tên cột."""
    df = pd.read_csv(path, header=None)
    df.columns = COLS
    return df


def check_data_quality(df: pd.DataFrame) -> None:
    """In thông tin cơ bản: shape, dtypes, missing, class distribution."""
    print(f"Shape       : {df.shape}")
    print(f"Dtypes      :\n{df.dtypes}")
    print(f"\nMissing values:\n{df.isnull().sum()}")
    print(f"\nDuplicate rows: {df.duplicated().sum()}")
    print(f"\nClass distribution:\n{df['class'].value_counts().sort_index()}")
    print(f"\nDescribe:\n{df.describe().round(2)}")


def preprocess(df: pd.DataFrame, save_path: str | None = None):
    """
    Tiền xử lý mức cơ bản:
      - Loại bỏ duplicate (nếu có)
      - Tách X, y
      - Có thể lưu bộ dữ liệu đã làm sạch vào thư mục processed

    Trả về: X (DataFrame), y (Series), clean_df (DataFrame)

    Ghi chú:
      - Không StandardScaler tại đây để tránh data leakage.
      - Việc scale sẽ được làm ở notebook baseline/tuning thông qua Pipeline.
    """
    clean_df = df.drop_duplicates().reset_index(drop=True)
    X = clean_df.drop('class', axis=1)
    y = clean_df['class']

    if save_path:
        ensure_parent_dir(save_path)
        clean_df.to_csv(save_path, index=False)
        print(f"Saved cleaned data → {save_path}")

    return X, y, clean_df
