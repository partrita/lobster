# Lobster 평가 콜백

이 가이드는 `evaluate_model_with_callbacks` 함수를 사용하여 모델 평가를 위한 콜백을 만들고 사용하는 방법을 설명합니다.

## 평가 콜백 만들기

`lightning.Callback`을 하위 클래스로 만들고 `evaluate` 메서드를 구현하여 새 콜백을 만듭니다.

```python
import lightning as L
from pathlib import Path
from typing import Any, dict

class MyEvaluationCallback(L.Callback):
    def __init__(self, param1: str | None = None):
        super().__init__()
        self.param1 = param1

    def evaluate(self, model: L.LightningModule) -> dict[str, Any]:
        """모델을 평가하고 메트릭을 반환합니다.

        매개변수
        ----------
        model : L.LightningModule
            평가할 모델

        반환 값
        -------
        dict[str, Any]
            메트릭 사전
        """
        # 평가 로직 구현
        return {"metric1": 0.95, "metric2": 0.85}
```

## 콜백 요구 사항

1. `lightning.Callback`에서 상속해야 합니다.
2. 모델을 첫 번째 매개변수로 사용하는 `evaluate` 메서드를 구현해야 합니다.
3. 필요한 경우 선택적으로 `dataloader` 매개변수를 받을 수 있습니다.

## 반환 유형

`evaluate` 메서드는 다음을 반환할 수 있습니다.

- **메트릭 사전**: 보고서에 표로 형식이 지정됩니다.
- **파일 경로**: 이미지가 보고서에 포함됩니다.
- **중첩 사전**: 중첩된 표로 형식이 지정됩니다.
- **기타 값**: 텍스트로 포함됩니다.

## 콜백 사용

```python
from lobster.evaluation import evaluate_model_with_callbacks
import lightning as L
from torch.utils.data import DataLoader

# 모델 및 콜백 만들기
model = MyModel()
callbacks = [
    MyEvaluationCallback(),
    AnotherCallback(param="value")
]

# 필요한 콜백을 위한 선택적 데이터 로더
dataloader = DataLoader(...)

# 평가 실행
report_path = evaluate_model_with_callbacks(
    callbacks=callbacks,
    model=model,
    dataloader=dataloader,
    output_dir="results/"
)
```

## 고급: 데이터 로더 종속 콜백

콜백에 데이터 로더가 필요한 경우:

```python
def evaluate(self, model: L.LightningModule, dataloader: DataLoader) -> dict[str, float]:
    """데이터 로더가 필요한 평가를 실행합니다.

    매개변수
    ----------
    model : L.LightningModule
        평가할 모델
    dataloader : DataLoader
        평가에 사용할 데이터 로더

    반환 값
    -------
    dict[str, float]
        메트릭 사전
    """
    results = {}
    for batch in dataloader:
        # 모델로 배치 처리
        # 결과 업데이트
    return results
```

평가 프레임워크는 데이터 로더 매개변수를 자동으로 감지하고 제공합니다.
