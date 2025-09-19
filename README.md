# DataFrame idle_time Processor

이 모듈은 DataFrame에서 'idle_time' 컬럼의 음수 값을 가진 로우와 그 이전 로우를 추출하는 기능을 제공합니다.

## 기능 설명

### `extract_negative_idle_time_rows(df, column_name='idle_time')`

DataFrame에서 지정된 컬럼의 음수 값을 가진 로우와 그 이전 로우를 추출합니다.

#### 파라미터
- `df` (pd.DataFrame): 처리할 데이터프레임
- `column_name` (str): 처리할 컬럼명 (기본값: 'idle_time')

#### 반환값
- `pd.DataFrame`: 음수 값을 가진 로우와 그 이전 로우를 포함하는 새로운 데이터프레임

#### 가정사항
1. 첫 번째 값은 항상 NaN으로 가정
2. 두 번째 값부터는 `pd._libs.tslibs.timedeltas.Timedelta` 타입의 값
3. 음수 값을 가진 로우와 그 이전 로우를 함께 추출

## 사용 예제

```python
import pandas as pd
import numpy as np
from idle_time_processor import extract_negative_idle_time_rows, create_sample_dataframe

# 샘플 데이터프레임 생성
df = create_sample_dataframe()
print("Original DataFrame:")
print(df)

# 음수 idle_time 값을 가진 로우와 이전 로우 추출
result = extract_negative_idle_time_rows(df)
print("\nExtracted rows:")
print(result)
```

## 샘플 데이터

### 입력 데이터
```
   id         idle_time other_data
0   1               NaT          A
1   2   0 days 00:00:10          B
2   3 -1 days +23:59:55          C  <- 음수 값
3   4   0 days 00:00:15          D
4   5 -1 days +23:59:57          E  <- 음수 값
5   6   0 days 00:00:20          F
6   7 -1 days +23:59:59          G  <- 음수 값
7   8   0 days 00:00:08          H
```

### 출력 데이터
```
   id         idle_time other_data
1   2   0 days 00:00:10          B  <- 로우 2의 이전 로우
2   3 -1 days +23:59:55          C  <- 음수 값 로우
3   4   0 days 00:00:15          D  <- 로우 4의 이전 로우
4   5 -1 days +23:59:57          E  <- 음수 값 로우
5   6   0 days 00:00:20          F  <- 로우 6의 이전 로우
6   7 -1 days +23:59:59          G  <- 음수 값 로우
```

## 특징

1. **원본 데이터 보존**: 원본 DataFrame은 수정되지 않음
2. **에러 처리**: 컬럼이 존재하지 않는 경우 ValueError 발생
3. **엣지 케이스 처리**: 빈 DataFrame, 모든 값이 양수인 경우 등 처리
4. **타입 안전성**: Timedelta 타입 검증 및 NaN 값 적절한 처리

## 테스트

전체 테스트 스위트를 실행하려면:

```bash
python3 test_idle_time_processor.py
```

테스트는 다음과 같은 시나리오를 포함합니다:
- 기본 기능 테스트
- 빈 DataFrame 처리
- 음수 값이 없는 경우
- 모든 값이 음수인 경우
- 단일 로우 DataFrame
- 커스텀 컬럼명 사용
- 원본 DataFrame 보존 확인