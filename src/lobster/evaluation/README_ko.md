# Lobster 모델 평가

이 모듈은 특수 콜백을 사용하여 모델을 평가하고 포괄적인 평가 보고서를 생성하기 위한 도구를 제공합니다.

## 평가 작동 방식

`evaluate_model_with_callbacks` 함수는 모델에서 각 콜백의 `evaluate` 메서드를 실행하고 결과를 수집한 다음 마크다운 보고서를 생성합니다. 프로세스는 다음 단계를 따릅니다.

1. 출력 디렉토리 초기화
2. 각 콜백에 대해:
   - 모델(필요한 경우 데이터 로더 포함)을 사용하여 `evaluate` 메서드 호출
   - 결과 수집 또는 문제 기록
3. 모든 결과가 포함된 마크다운 보고서 생성
4. 보고서 경로 반환

## 평가 프레임워크 사용

명령줄에서 평가를 실행하려면:

```bash
lobster_eval model.model_path=여러분의_체크포인트.ckpt_경로
```

코드에서 평가를 실행하려면:
```python
from lobster.evaluation import evaluate_model_with_callbacks
from lobster.callbacks import LinearProbeCallback, UMAPVisualizationCallback
import lightning as L
import torch

# 모델 및 평가 데이터셋 준비
model = L.LightningModule.load_from_checkpoint("체크포인트_경로/checkpoint.ckpt")
dataloader = torch.utils.data.DataLoader(dataset, batch_size=32)

# 다양한 평가 작업을 위한 콜백 정의
callbacks = [
    LinearProbeCallback(num_classes=10),
    UMAPVisualizationCallback(n_components=2),
]

# 평가 실행
report_path = evaluate_model_with_callbacks(
    callbacks=callbacks,
    model=model,
    dataloader=dataloader,
    output_dir="evaluation_results"
)

# 보고서는 report_path에 저장됩니다.
print(f"평가 보고서는 다음에서 사용할 수 있습니다: {report_path}")
```

## 평가 보고서 형식

생성된 보고서는 다음 구조를 가진 마크다운 파일입니다.

- 제목 및 평가 날짜
- 각 콜백에 대한 하위 섹션이 있는 평가 결과 섹션
- 각 콜백의 결과는 유형에 따라 형식이 지정됩니다.
  - 사전은 표로 표시됩니다.
  - 중첩된 사전은 중첩된 표를 만듭니다.
  - 파일 경로(이미지 등)는 포함됩니다.
  - 기타 결과는 일반 텍스트로 포함됩니다.
- 평가 중에 발생한 모든 문제를 나열하는 섹션

## 예제 보고서

```markdown
# 모델 평가 보고서

평가 날짜: 2023-08-15 14:30:22

## 평가 결과

### LinearProbeCallback

| 메트릭 | 값 |
|--------|-------|
| 정확도 | 0.8750 |
| f1_점수 | 0.8523 |
| 정밀도 | 0.8912 |
| 재현율 | 0.8157 |

### UMAPVisualizationCallback

![UMAPVisualizationCallback 시각화](/umap_plot.png_경로)

### TokensPerSecondCallback

| 메트릭 | 값 |
|--------|-------|
| 초당_토큰_수 | 1256.3400 |
| 배치_크기 | 32 |

### PeerEvaluationCallback

### ResNet50

| 메트릭 | 값 |
|--------|-------|
| 복잡도 | *아래 참조* |

**복잡도에 대한 중첩 메트릭:**

| 하위 메트릭 | 값 |
|-----------|-------|
| 평균 | 4.2100 |
| 최소 | 1.0500 |
| 최대 | 12.3600 |

## 발생한 문제

- CalmLinearProbeCallback: 프로빙 작업에 적합한 데이터를 찾을 수 없습니다.
```

## 고급: 사용자 지정 평가 로직 추가

평가 프레임워크를 확장하려면 `lobster.callbacks` 모듈에서 사용자 지정 평가 로직을 사용하여 콜백을 만듭니다. 호환되는 콜백 만들기에 대한 자세한 내용은 [콜백 README](../callbacks/README.md)를 참조하십시오.
