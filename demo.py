#!/usr/bin/env python3
"""
Demo script for idle_time processor functionality.
이 스크립트는 다양한 시나리오에서 idle_time 처리 기능을 보여줍니다.
"""

import pandas as pd
import numpy as np
from idle_time_processor import extract_negative_idle_time_rows


def demo_basic_functionality():
    """기본 기능 데모"""
    print("=" * 60)
    print("1. 기본 기능 데모")
    print("=" * 60)
    
    data = {
        'id': [1, 2, 3, 4, 5],
        'idle_time': [
            np.nan,
            pd.Timedelta(seconds=10),
            pd.Timedelta(seconds=-5),  # 음수
            pd.Timedelta(seconds=15),
            pd.Timedelta(seconds=-3),  # 음수
        ],
        'status': ['init', 'running', 'error', 'running', 'error']
    }
    
    df = pd.DataFrame(data)
    print("입력 DataFrame:")
    print(df)
    print()
    
    result = extract_negative_idle_time_rows(df)
    print("결과 (음수 idle_time과 이전 로우):")
    print(result)
    print()


def demo_no_negative_values():
    """음수 값이 없는 경우 데모"""
    print("=" * 60)
    print("2. 음수 값이 없는 경우")
    print("=" * 60)
    
    data = {
        'id': [1, 2, 3],
        'idle_time': [
            np.nan,
            pd.Timedelta(seconds=10),
            pd.Timedelta(seconds=5),
        ]
    }
    
    df = pd.DataFrame(data)
    print("입력 DataFrame:")
    print(df)
    print()
    
    result = extract_negative_idle_time_rows(df)
    print("결과 (음수 값이 없으므로 빈 DataFrame):")
    print(result)
    print(f"결과 행 수: {len(result)}")
    print()


def demo_first_value_negative():
    """첫 번째 non-NaN 값이 음수인 경우"""
    print("=" * 60)
    print("3. 첫 번째 유효 값이 음수인 경우")
    print("=" * 60)
    
    data = {
        'id': [1, 2, 3],
        'idle_time': [
            np.nan,
            pd.Timedelta(seconds=-10),  # 첫 번째 유효 값이 음수
            pd.Timedelta(seconds=5),
        ],
        'note': ['start', 'error', 'normal']
    }
    
    df = pd.DataFrame(data)
    print("입력 DataFrame:")
    print(df)
    print()
    
    result = extract_negative_idle_time_rows(df)
    print("결과 (NaN 이전 로우와 음수 로우):")
    print(result)
    print()


def demo_consecutive_negative():
    """연속된 음수 값들"""
    print("=" * 60)
    print("4. 연속된 음수 값들")
    print("=" * 60)
    
    data = {
        'id': [1, 2, 3, 4, 5],
        'idle_time': [
            np.nan,
            pd.Timedelta(seconds=10),
            pd.Timedelta(seconds=-5),   # 음수
            pd.Timedelta(seconds=-3),   # 연속 음수
            pd.Timedelta(seconds=8),
        ],
        'event': ['start', 'ok', 'error1', 'error2', 'recovery']
    }
    
    df = pd.DataFrame(data)
    print("입력 DataFrame:")
    print(df)
    print()
    
    result = extract_negative_idle_time_rows(df)
    print("결과 (연속된 음수 값들과 이전 로우들):")
    print(result)
    print()


def demo_custom_column():
    """커스텀 컬럼명 사용"""
    print("=" * 60)
    print("5. 커스텀 컬럼명 사용")
    print("=" * 60)
    
    data = {
        'task_id': [1, 2, 3, 4],
        'waiting_time': [  # idle_time 대신 다른 컬럼명
            np.nan,
            pd.Timedelta(minutes=2),
            pd.Timedelta(minutes=-1),  # 음수
            pd.Timedelta(minutes=3),
        ],
        'description': ['init', 'waiting', 'timeout', 'completed']
    }
    
    df = pd.DataFrame(data)
    print("입력 DataFrame (waiting_time 컬럼):")
    print(df)
    print()
    
    result = extract_negative_idle_time_rows(df, column_name='waiting_time')
    print("결과 (waiting_time 컬럼 기준):")
    print(result)
    print()


def main():
    """메인 데모 함수"""
    print("DataFrame idle_time Processor 데모")
    print("이 스크립트는 다양한 시나리오에서의 기능을 보여줍니다.\n")
    
    demo_basic_functionality()
    demo_no_negative_values()
    demo_first_value_negative()
    demo_consecutive_negative()
    demo_custom_column()
    
    print("=" * 60)
    print("데모 완료!")
    print("=" * 60)


if __name__ == "__main__":
    main()