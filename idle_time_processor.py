import pandas as pd
import numpy as np
from typing import Optional


def extract_negative_idle_time_rows(df: pd.DataFrame, column_name: str = 'idle_time') -> pd.DataFrame:
    """
    데이터프레임에서 'idle_time' 컬럼의 음수 값을 가진 로우와 그 이전 로우를 추출합니다.
    
    Args:
        df (pd.DataFrame): 처리할 데이터프레임
        column_name (str): 처리할 컬럼명 (기본값: 'idle_time')
    
    Returns:
        pd.DataFrame: 음수 값을 가진 로우와 그 이전 로우를 포함하는 새로운 데이터프레임
    
    Assumptions:
        - 첫 번째 값은 항상 NaN
        - 두 번째 값부터는 pd._libs.tslibs.timedeltas.Timedelta 타입
    """
    # 입력 검증
    if df.empty:
        return pd.DataFrame()
    
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' not found in DataFrame")
    
    # 데이터프레임 복사 (원본 보존)
    result_df = df.copy()
    
    # idle_time 컬럼 추출
    idle_time_series = result_df[column_name]
    
    # 음수 값을 가진 인덱스 찾기 (NaN은 제외)
    # pd.Timedelta 타입의 음수 값 확인
    try:
        # NaN이 아닌 값들 중에서 음수인 값들을 찾기
        valid_mask = ~idle_time_series.isna()
        if valid_mask.any():
            negative_mask = valid_mask & (idle_time_series < pd.Timedelta(0))
        else:
            negative_mask = pd.Series([False] * len(idle_time_series), index=idle_time_series.index)
        negative_indices = idle_time_series[negative_mask].index.tolist()
    except (TypeError, ValueError):
        # 타입 에러가 발생하면 빈 리스트 반환
        negative_indices = []
    
    if not negative_indices:
        # 음수 값이 없으면 빈 데이터프레임 반환
        return pd.DataFrame(columns=df.columns)
    
    # 추출할 인덱스 집합 생성
    indices_to_extract = set()
    
    for neg_idx in negative_indices:
        # 음수 값을 가진 로우 추가
        indices_to_extract.add(neg_idx)
        
        # 이전 로우 추가 (존재하는 경우)
        if neg_idx > 0:
            prev_idx = neg_idx - 1
            indices_to_extract.add(prev_idx)
    
    # 인덱스 정렬하여 결과 반환
    sorted_indices = sorted(list(indices_to_extract))
    
    return result_df.loc[sorted_indices].copy()


def create_sample_dataframe() -> pd.DataFrame:
    """
    테스트용 샘플 데이터프레임을 생성합니다.
    
    Returns:
        pd.DataFrame: 샘플 데이터프레임
    """
    data = {
        'id': [1, 2, 3, 4, 5, 6, 7, 8],
        'idle_time': [
            np.nan,  # 첫 번째 값은 NaN
            pd.Timedelta(seconds=10),    # 양수
            pd.Timedelta(seconds=-5),    # 음수
            pd.Timedelta(seconds=15),    # 양수
            pd.Timedelta(seconds=-3),    # 음수
            pd.Timedelta(seconds=20),    # 양수
            pd.Timedelta(seconds=-1),    # 음수
            pd.Timedelta(seconds=8),     # 양수
        ],
        'other_data': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    }
    
    return pd.DataFrame(data)


if __name__ == "__main__":
    # 샘플 데이터프레임 생성
    sample_df = create_sample_dataframe()
    print("Original DataFrame:")
    print(sample_df)
    print("\nidle_time column details:")
    print(sample_df['idle_time'].dtype)
    print(sample_df['idle_time'])
    
    # 음수 idle_time 값을 가진 로우와 이전 로우 추출
    result = extract_negative_idle_time_rows(sample_df)
    print("\nExtracted rows (negative idle_time and previous rows):")
    print(result)
    
    # 추출된 로우들의 idle_time 값 확인
    print("\nExtracted idle_time values:")
    print(result['idle_time'])