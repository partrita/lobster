# UME를 사용한 강화 학습 훈련

이 가이드는 UME 기반 보상 함수를 사용하여 강화 학습으로 언어 모델을 훈련하는 방법을 보여줍니다. 이 과정은 합성 데이터셋 생성과 UME 보상을 사용한 훈련이라는 두 가지 주요 단계로 이루어집니다.

### 패키지 구조

```
src/lobster/rl_training/
├── __init__.py              # 모듈 내보내기
├── reward_functions.py      # UME 보상 함수 및 유틸리티
├── trainers.py             # 트레이너 생성 및 구성
└── README.md              # 모듈 문서

tests/lobster/rl_training/
├── __init__.py
├── test_reward_functions.py # 보상 함수 단위 테스트
└── test_trainers.py        # 트레이너 단위 테스트

examples/
├── generate_synthetic_dataset.py  # 데이터셋 생성 스크립트
├── train_ume_grpo.py             # 훈련 스크립트
└── test_ume_reward.py            # 보상 함수 테스트 스크립트
```

## 단계별 훈련 과정

## 사전 준비 사항

훈련 과정을 시작하기 전에 TRL extra와 함께 lobster가 설치되어 있는지 확인하십시오.

```bash
# 모든 extra와 함께 lobster 설치
uv sync --all-extras

# 또는 pip를 사용하여 TRL extra와 함께 lobster 설치
pip install "lbster[trl]"

# 또는 소스에서 설치하는 경우
pip install -e ".[trl]"

# uv를 사용한 대체 방법 (개발에 권장)
uv pip install -e ".[trl]"
```

TRL extra에는 다음이 포함됩니다.
- `trl` - 트랜스포머 강화 학습 라이브러리
- `accelerate` - 분산 훈련을 위한 HuggingFace Accelerate

## 0단계: Hugging Face Hub에서 Qwen 모델 다운로드

훈련을 실행하기 전에 Qwen 모델 체크포인트를 다운로드해야 합니다. 훈련 스크립트는 Hugging Face 캐시에서 Qwen 모델을 자동으로 찾아 사용합니다.

### Hugging Face 캐시 디렉토리 설정

먼저 `HF_HUB_CACHE` 환경 변수를 설정하여 모델을 캐시할 위치를 지정합니다.

```bash
# 캐시 디렉토리 설정 (필요에 따라 경로 조정)
export HF_HUB_CACHE="/path/to/your/hf_cache"

# 또는 지속성을 위해 셸 프로필에 추가
echo 'export HF_HUB_CACHE="/path/to/your/hf_cache"' >> ~/.bashrc
source ~/.bashrc
```

### Qwen 모델 다운로드

Hugging Face Hub CLI 또는 Python을 사용하여 Qwen 모델을 다운로드합니다.

```bash
# huggingface-cli 사용
huggingface-cli download Qwen/Qwen2-0.5B-Instruct --local-dir-use-symlinks False

# 또는 Python 사용
python -c "
from huggingface_hub import snapshot_download
snapshot_download(
    repo_id='Qwen/Qwen2-0.5B-Instruct',
    local_dir_use_symlinks=False
)
"
```

### 대안: Python 스크립트를 통한 다운로드

간단한 다운로드 스크립트를 만듭니다.

```python
#!/usr/bin/env python3
"""RL 훈련을 위한 Qwen 모델 다운로드."""

import os
from huggingface_hub import snapshot_download

def download_qwen_model():
    """Qwen 모델을 HF_HUB_CACHE로 다운로드합니다."""
    # HF_HUB_CACHE가 설정되었는지 확인
    hf_cache = os.getenv('HF_HUB_CACHE')
    if not hf_cache:
        print("경고: HF_HUB_CACHE가 설정되지 않았습니다. 기본 캐시 위치를 사용합니다.")

    print("Qwen2-0.5B-Instruct 모델 다운로드 중...")
    snapshot_download(
        repo_id='Qwen/Qwen2-0.5B-Instruct',
        local_dir_use_symlinks=False,
        cache_dir=hf_cache
    )
    print("다운로드 완료!")

if __name__ == "__main__":
    download_qwen_model()
```

이것을 `download_qwen_model.py`로 저장하고 실행합니다.

```bash
python download_qwen_model.py
```

### 모델 다운로드 확인

모델이 올바르게 다운로드되었는지 확인합니다.

```bash
# 캐시 디렉토리 내용 나열
ls -la $HF_HUB_CACHE/models--Qwen--Qwen2-0.5B-Instruct/

# 다음과 같이 표시되어야 합니다.
# drwxr-xr-x 2 user user 4096 date snapshots/
# -rw-r--r-- 1 user user  123 date config.json
# -rw-r--r-- 1 user user  456 date README.md
# ...
```

훈련 스크립트는 이 다운로드된 모델을 자동으로 찾아 사용합니다.

### 1단계: 합성 데이터셋 생성

먼저 분자 및 생물학적 서열의 합성 데이터셋을 생성합니다.

```bash
cd examples
python generate_synthetic_dataset.py
```

이 스크립트는 다음을 수행합니다.
- 100개의 SMILES 문자열(분자 구조) 생성
- 100개의 아미노산 서열(단백질) 생성
- 100개의 DNA 서열 생성
- 훈련/검증/테스트 분할 생성 (90%/5%/5%)
- 데이터셋을 `synthetic_molecular_dataset/` 디렉토리에 저장

**출력:**
- `synthetic_molecular_dataset/` - 훈련/검증/테스트 분할이 있는 HuggingFace 데이터셋
- `synthetic_molecular_dataset.json` - 쉽게 검사할 수 있는 JSON 파일

### 2단계: UME 기반 GRPO 훈련 실행

데이터셋을 생성한 후 훈련 스크립트를 실행합니다.

```bash
python train_ume_grpo.py
```

이 스크립트는 다음을 수행합니다.
- 생성된 디렉토리에서 합성 데이터셋 로드
- 기본 언어 모델(Qwen2-0.5B-Instruct) 초기화
- 보상 계산을 위한 UME 모델 로드
- UME 기반 보상으로 GRPO 훈련 구성 및 시작
- 지정된 출력 디렉토리에 훈련 결과물 저장

## 주요 구성 요소

### 1. 보상 함수 (`reward_functions.py`)

- **`UmeRewardFunction`**: UME 의사 가능도를 기반으로 보상을 계산하는 주요 보상 함수 클래스
- **`_detect_modality()`**: 서열 양식(SMILES, 아미노산, DNA)을 자동으로 감지합니다 (`lobster.model.utils`에서 사용 가능).
- **`compute_pseudo_likelihood()`**: 가능도 점수 계산을 위한 핵심 함수
- **`create_ume_reward_wrapper()`**: TRL 호환 래퍼 함수 생성

### 2. 트레이너 (`trainers.py`)

- **`create_ume_grpo_trainer()`**: UME 보상을 사용하여 구성된 GRPO 트레이너 생성
- **`train_ume_grpo()`**: 전체 훈련 파이프라인 (모델 로드, 트레이너 생성, 훈련 시작)

### 3. 테스트

- 적절한 테스트 범위를 위한 `tests/lobster/rl_training/`의 **단위 테스트**
- 종단 간 테스트를 위한 `examples/test_ume_reward.py`의 **통합 테스트**

## 사용 예시

### 기본 훈련 파이프라인

```python
# 1단계: 데이터셋 생성
from examples.generate_synthetic_dataset import main as generate_dataset
generate_dataset()

# 2단계: UME 기반 보상으로 훈련
from lobster.rl_training import train_ume_grpo
from datasets import load_from_disk

# 데이터셋 로드
train_dataset = load_from_disk("synthetic_molecular_dataset/train")
val_dataset = load_from_disk("synthetic_molecular_dataset/validation")

# UME 기반 보상으로 훈련
trainer = train_ume_grpo(
    model_path="/path/to/base/model",
    ume_model_path="ume-mini-base-12M",
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    output_dir="./runs",
    reward_temperature=0.1,
    reward_batch_size=8,
)
```

### 사용자 지정 트레이너 구성

```python
from lobster.rl_training import create_ume_grpo_trainer
from lobster.model import Ume

# UME 모델 로드
ume_model = Ume.from_pretrained("ume-mini-base-12M", device="cuda")

# 사용자 지정 트레이너 생성
trainer = create_ume_grpo_trainer(
    model_path="your/model",
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

## 구성 옵션

### 데이터셋 생성 매개변수

`generate_synthetic_dataset.py` 스크립트는 다음을 생성합니다.
- **총 300개 서열** (SMILES, 아미노산, DNA 각각 100개)
- **훈련/검증/테스트 분할**: 90%/5%/5%
- **서열 길이**:
  - SMILES: 10-50자
  - 아미노산: 20-100자
  - DNA: 50-200자

### 보상 함수 매개변수

- **`temperature`**: 보상 스케일링 제어 (낮을수록 극단적인 보상, 기본값: 0.1)
- **`batch_size`**: 보상 계산을 위한 배치 크기 (기본값: 8)

### 훈련 매개변수

- **`output_dir`**: 훈련 결과물 디렉토리
- **`device`**: UME 모델용 장치 (기본값: "cuda")
- **추가 GRPO 매개변수**: 모든 표준 TRL GRPO 매개변수 지원

## 주요 기능

1. **자동 양식 감지**: 다양한 서열 유형을 자동으로 감지하고 처리합니다.
2. **효율적인 배치 처리**: 메모리 효율성을 위해 서열을 배치로 처리합니다.
3. **온도 스케일링**: RL 훈련을 위한 구성 가능한 보상 스케일링
4. **오류 처리**: 0 보상으로 대체하는 강력한 오류 처리
5. **모듈식 설계**: 재사용 가능한 구성 요소로 관심사를 깔끔하게 분리
6. **포괄적인 테스트**: 안정성을 위한 단위 테스트 및 통합 테스트

## 파일

- **`generate_synthetic_dataset.py`**: 합성 분자 및 생물학적 서열 생성
- **`train_ume_grpo.py`**: 새로운 모듈식 구조를 사용하는 깔끔하고 최소한의 훈련 스크립트
- **`test_ume_reward.py`**: 보상 함수 유효성 검사를 위한 테스트 스크립트
- **로컬 모델 캐싱**: 다운로드 시간 초과를 방지하기 위해 Qwen 모델을 로컬에 캐시합니다.

## 문제 해결

### 일반적인 문제

1. **메모리 부족**: `reward_batch_size`를 줄이거나 기울기 누적 사용
2. **느린 훈련**: 메모리가 허용하는 경우 `reward_batch_size` 늘리기
3. **낮은 보상**: `reward_temperature` 조정 (낮을수록 극단적인 보상)
4. **데이터셋을 찾을 수 없음**: `generate_synthetic_dataset.py`가 먼저 실행되었는지 확인

### 성능 팁

- UME 모델 추론에 GPU 사용
- 가능한 경우 보상 계산 일괄 처리
- 훈련 중 메모리 사용량 모니터링
- 사용 사례에 적합한 서열 길이 사용
