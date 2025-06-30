# SLURM으로 LBSTER 작업 실행하기

이 가이드는 GPU 사용 가능 시스템에서 SLURM을 사용하여 `lobster` 학습 작업을 실행하는 방법을 설명합니다. 또한 작업이 올바르게 실행되기 위해 내보내야 하는 환경 변수에 대해서도 설명합니다.

# SLURM 작업 스크립트
제공된 예제 작업 스크립트 `scripts/train_ume.sh`는 GPU 사용 가능 SLURM 클러스터에서 `UME` 모델을 학습하도록 구성되어 있습니다.

작업을 실행하려면 특정 환경 변수를 설정해야 합니다. 이러한 변수는 `src/lobster/hydra_config/experiment/train_ume.yaml`에 있는 `UME` hydra 구성 파일에서 읽어옵니다.

변수:

* `LOBSTER_DATA_DIR`: 학습 데이터가 포함된 디렉토리 경로입니다. 데이터셋은 이 디렉토리에 다운로드되고 캐시됩니다 (hydra 구성 파일에서 `data.download`가 `True`로 설정된 경우).
* `LOBSTER_RUNS_DIR`: 학습 결과(모델 체크포인트, 로그 등)가 저장될 디렉토리 경로입니다.
* `LOBSTER_USER`: 로거의 사용자 엔티티입니다 (일반적으로 wandb 사용자 이름).
* `WANDB_BASE_URL`: Weights & Biases 서비스의 기본 URL입니다. 선택 사항 - wandb 계정이 기본 wandb 서버에 없는 경우에만 필요합니다.

예시:
```bash
    export LOBSTER_DATA_DIR="/data/lobster/ume/data"
    export LOBSTER_RUNS_DIR="/data/lobster/ume/runs"
    export LOBSTER_USER=$(whoami)
    export WANDB_BASE_URL=https://your_org.wandb.io/
```
