# 향상된 Wandb 로깅을 사용한 UME GRPO 훈련

이 문서는 상세한 샘플 추적, 보상 분석 및 양식별 메트릭을 포함하여 UME 기반 GRPO 훈련을 위한 향상된 로깅 및 모니터링 기능에 대해 설명합니다.

## 개요

향상된 로깅 시스템은 다음을 통해 UME GRPO 훈련에 대한 포괄적인 모니터링을 제공합니다.

1. **UmeGrpoLoggingCallback**: 훈련 샘플과 보상을 기록하는 사용자 지정 Lightning 콜백
2. **향상된 보상 함수**: 양식 분석을 포함한 상세한 보상 계산 로깅
3. **Wandb 통합**: 자동 wandb 실행 관리 및 메트릭 로깅

## 기능

### 1. 훈련 샘플 로깅

시스템은 개별 훈련 샘플을 다음 정보와 함께 기록합니다.
- **완성**: 생성된 서열 (표시를 위해 잘림)
- **보상**: UME 기반 보상 점수
- **양식**: 감지된 서열 유형 (SMILES, 아미노산, 뉴클레오티드)
- **길이**: 서열 길이

### 2. 보상 통계

다음을 포함한 포괄적인 보상 추적:
- **기본 통계**: 평균, 최소, 최대, 표준 편차
- **양식 분석**: 각 양식 유형에 대한 별도 통계
- **히스토그램**: 시간 경과에 따른 보상 분포
- **누적 메트릭**: 처리된 총 샘플 수, 전체 통계

### 3. 훈련 진행 상황 모니터링

다음에 대한 실시간 모니터링:
- **단계별 메트릭**: 배치별 보상 통계
- **에포크별 요약**: 에포크별 집계 메트릭
- **훈련 구성**: 모델 경로, 하이퍼파라미터 등

## 사용법

### 기본 사용법

```python
from lobster.rl_training import train_ume_grpo

# 향상된 로깅으로 훈련 시작
trainer = train_ume_grpo(
    model_path="your/base/model",
    ume_model_path="ume-mini-base-12M",
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    enable_wandb_logging=True,
    wandb_project="your-project",
    wandb_entity="your-username",
    wandb_run_name="experiment-name",
)
```

### 고급 구성

```python
from lobster.rl_training import create_ume_grpo_trainer
from lobster.callbacks import UmeGrpoLoggingCallback

# 사용자 지정 로깅 콜백 생성
logging_callback = UmeGrpoLoggingCallback(
    log_every_n_steps=50,           # 50단계마다 로그 기록
    max_samples_to_log=15,          # 단계별로 최대 15개 샘플 로그 기록
    log_reward_histogram=True,      # 보상 히스토그램 활성화
    log_sample_examples=True,       # 샘플 로깅 활성화
    log_modality_breakdown=True,    # 양식 분석 활성화
)

# 사용자 지정 콜백으로 트레이너 생성
trainer = create_ume_grpo_trainer(
    model_path="your/base/model",
    ume_model=ume_model,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    enable_wandb_logging=True,
    callbacks=[logging_callback],
)
```

### 환경 변수

wandb 구성을 위해 다음 환경 변수를 설정합니다.

```bash
export WANDB_ENTITY="your-username"
export WANDB_PROJECT="your-project"
export WANDB_API_KEY="your-api-key"
```

## Wandb 대시보드

로깅 시스템은 다음을 포함하는 포괄적인 wandb 대시보드를 생성합니다.

### 1. 훈련 메트릭

- **train/mean_reward**: 배치당 평균 보상
- **train/min_reward**: 배치 내 최소 보상
- **train/max_reward**: 배치 내 최대 보상
- **train/reward_std**: 보상 표준 편차
- **train/batch_size**: 배치당 샘플 수

### 2. 양식별 메트릭

- **train/modality_smiles/mean_reward**: SMILES 서열의 평균 보상
- **train/modality_amino_acid/mean_reward**: 아미노산 서열의 평균 보상
- **train/modality_nucleotide/mean_reward**: 뉴클레오티드 서열의 평균 보상
- **train/modality_*/count**: 양식당 샘플 수

### 3. 샘플 예제

다음을 보여주는 대화형 테이블:
- 샘플 완성 (잘림)
- 개별 보상 점수
- 양식 분류
- 서열 길이

### 4. 보상 히스토그램

다음을 보여주는 분포도:
- 전체 보상 분포
- 양식별 분포
- 훈련 단계에 따른 변화

### 5. 에포크 요약

- **epoch/mean_reward**: 에포크당 평균 보상
- **epoch/min_reward**: 에포크당 최소 보상
- **epoch/max_reward**: 에포크당 최대 보상
- **epoch/total_samples**: 처리된 총 샘플 수

## 구성 파일

### Hydra 구성

```yaml
# src/lobster/hydra_config/callbacks/ume_grpo_logging.yaml
_target_: lobster.callbacks.UmeGrpoLoggingCallback

# 로깅 빈도
log_every_n_steps: 100

# 단계별로 기록할 최대 샘플 예제 수
max_samples_to_log: 10

# 보상 히스토그램 기록 여부
log_reward_histogram: true

# 개별 샘플 예제 기록 여부
log_sample_examples: true

# 양식별 보상 분석 기록 여부
log_modality_breakdown: true
```

### 훈련 구성

```yaml
# 예제 훈련 구성
model_path: "your/base/model"
ume_model_path: "ume-mini-base-12M"
output_dir: "./ume_grpo_runs"
reward_temperature: 0.1
reward_batch_size: 8
enable_wandb_logging: true
wandb_project: "lobster-ume-grpo"
wandb_entity: "your-username"
wandb_run_name: "experiment-001"
```

## 테스트

테스트 스크립트를 실행하여 로깅 기능을 확인합니다.

```bash
python examples/test_ume_grpo_logging.py
```

다음 사항을 테스트합니다.
- 콜백 초기화 및 실행
- 보상 함수 로깅
- 로깅을 사용한 트레이너 생성
- Wandb 통합

## 문제 해결

### 일반적인 문제

1. **Wandb가 로깅하지 않음**: `enable_wandb_logging=True`인지 확인하고 wandb가 올바르게 구성되었는지 확인합니다.
2. **기록된 샘플 없음**: 배치에 완성 및 보상이 포함되어 있는지 확인합니다.
3. **양식 감지 실패**: 서열 형식이 예상 패턴과 일치하는지 확인합니다.

### 디버그 모드

상세 정보를 위해 디버그 로깅을 활성화합니다.

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 성능 고려 사항

- **로깅 빈도**: 더 자주 업데이트하려면 `log_every_n_steps`를 줄입니다.
- **샘플 수**: wandb가 과부하되지 않도록 `max_samples_to_log`를 제한합니다.
- **히스토그램 구간**: 필요에 따라 히스토그램 해상도를 조정합니다.

## 예제 출력

### Wandb 실행 구성

```json
{
  "model_path": "your/base/model",
  "reward_temperature": 0.1,
  "reward_batch_size": 8,
  "output_dir": "./ume_grpo_runs",
  "logging/log_every_n_steps": 100,
  "logging/max_samples_to_log": 10
}
```

### 샘플 메트릭

```
train/mean_reward: 0.75
train/min_reward: 0.23
train/max_reward: 0.98
train/reward_std: 0.15
train/modality_smiles/mean_reward: 0.82
train/modality_amino_acid/mean_reward: 0.71
train/modality_nucleotide/mean_reward: 0.68
```

### 샘플 테이블

| 완성 | 보상 | 양식 | 길이 |
|------------|--------|----------|--------|
| CC(C)CC1=CC=C(C=C1)C(C)C(=O)O... | 0.82 | smiles | 25 |
| MKTVRQERLKSIVRILERSKEPVSGAQLAE... | 0.71 | amino_acid | 60 |
| ATGCGATCGATCGATCGATCGATCGATCG... | 0.68 | nucleotide | 64 |

## 기존 코드와의 통합

향상된 로깅은 이전 버전과 호환됩니다. 기존 코드는 변경 없이 작동하며 `enable_wandb_logging=True`로 설정하여 로깅을 활성화할 수 있습니다.

기존 훈련 스크립트의 경우 wandb 매개변수를 추가하기만 하면 됩니다.

```python
# 이전
trainer = train_ume_grpo(
    model_path=model_path,
    ume_model_path=ume_model_path,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
)

# 이후 (로깅 사용)
trainer = train_ume_grpo(
    model_path=model_path,
    ume_model_path=ume_model_path,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    enable_wandb_logging=True,
    wandb_project="your-project",
    wandb_entity="your-username",
)
```
