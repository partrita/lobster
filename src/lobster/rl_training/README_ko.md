# 강화 학습 훈련 모듈

이 모듈은 강화 학습 기법, 특히 UME 모델 기반의 보상 함수를 사용하여 모델을 훈련하기 위한 유틸리티를 제공합니다.

## 개요

`rl_training` 모듈에는 다음이 포함됩니다.

- **보상 함수**: RL 훈련을 위한 UME 기반 보상 함수
- **훈련기**: RL 훈련기 생성 및 구성을 위한 유틸리티

## 빠른 시작

### 기본 사용법

```python
from lobster.rl_training import train_ume_grpo
from datasets import load_from_disk

# 데이터셋 로드
train_dataset = load_from_disk("경로/train")
val_dataset = load_from_disk("경로/val")

# UME 기반 보상으로 훈련
trainer = train_ume_grpo(
    model_path="사용자/기본/모델",
    ume_model_path="ume-mini-base-12M",
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    output_dir="./runs",
)
```

### 사용자 지정 훈련기 구성

```python
from lobster.rl_training import create_ume_grpo_trainer
from lobster.model import Ume

# UME 모델 로드
ume_model = Ume.from_pretrained("ume-mini-base-12M", device="cuda")

# 사용자 지정 훈련기 생성
trainer = create_ume_grpo_trainer(
    model_path="사용자/모델",
    ume_model=ume_model,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    output_dir="./custom_runs",
    reward_temperature=0.2,
    reward_batch_size=16,
    learning_rate=1e-5,
    batch_size=4,
    max_steps=1000,
)
```

### 보상 함수 테스트

```python
from lobster.rl_training import UmeRewardFunction
from lobster.model.utils import _detect_modality
from lobster.model import Ume

# 양식 감지 테스트
sequence = "CC(C)CC1=CC=C(C=C1)C(C)C(=O)O"
modality = _detect_modality(sequence)  # Modality.SMILES 반환

# 보상 함수 테스트
ume_model = Ume.from_pretrained("ume-mini-base-12M", device="cuda")
reward_func = UmeRewardFunction(ume_model, temperature=0.1)
rewards = reward_func(["CC(C)CC1=CC=C(C=C1)C(C)C(=O)O"])
```

## 구성 요소

### 보상 함수 (`reward_functions.py`)

- `UmeRewardFunction`: UME 의사 가능도에 기반하여 보상을 계산하는 주요 보상 함수 클래스
- `_detect_modality()`: 서열 양식(SMILES, 아미노산, DNA)을 자동으로 감지 (`lobster.model.utils`에서 사용 가능)
- `compute_pseudo_likelihood()`: 가능도 점수 계산을 위한 핵심 함수
- `create_ume_reward_wrapper()`: TRL 호환 래퍼 함수 생성

### 훈련기 (`trainers.py`)

- `create_ume_grpo_trainer()`: UME 보상으로 구성된 GRPO 훈련기 생성
- `train_ume_grpo()`: 전체 훈련 파이프라인 (모델 로드, 훈련기 생성, 훈련 시작)

## 구성

### 보상 함수 매개변수

- `reward_temperature`: 보상 스케일링 제어 (낮을수록 더 극단적인 보상, 기본값: 0.1)
- `reward_batch_size`: 보상 계산을 위한 배치 크기 (기본값: 8)

### 훈련 매개변수

- `output_dir`: 훈련 결과물 디렉토리
- `device`: UME 모델용 장치 (기본값: "cuda")
- **추가 GRPO 매개변수**: 모든 표준 TRL GRPO 매개변수 지원

## 주요 기능

1. **자동 양식 감지**: 다양한 서열 유형을 자동으로 감지하고 처리
2. **효율적인 배치 처리**: 메모리 효율성을 위해 서열을 배치로 처리
3. **온도 스케일링**: RL 훈련을 위한 구성 가능한 보상 스케일링
4. **오류 처리**: 0 보상으로 대체하는 강력한 오류 처리
5. **모듈식 설계**: 재사용 가능한 구성 요소로 관심사를 깔끔하게 분리

## 테스트

단위 테스트는 `tests/lobster/rl_training/`에 있습니다.

- `test_reward_functions.py`: 보상 함수 및 양식 감지 테스트
- `test_trainers.py`: 훈련기 생성 및 구성 테스트

통합 테스트는 `examples/test_ume_reward.py`를 참조하십시오.

## 예제

완전히 작동하는 예제는 `examples/` 디렉토리를 참조하십시오.

- `train_ume_grpo.py`: 모듈식 구조를 사용하는 깔끔하고 최소한의 훈련 스크립트
- `test_ume_reward.py`: 보상 함수 유효성 검사를 위한 테스트 스크립트
- `README_RL_TRAINING.md`: 포괄적인 문서 및 사용 예제
