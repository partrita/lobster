# CLAUDE.md

이 파일은 Claude Code (claude.ai/code)가 이 리포지토리의 코드로 작업할 때 가이드라인을 제공합니다.

## 프로젝트 구조

LBSTER (Lobster)는 PyTorch Lightning과 Hydra 설정 관리를 사용하여 구축된, 단백질 및 생물학적 서열을 위한 "모든 기능이 포함된(batteries included)" 언어 모델 라이브러리입니다. 이 프로젝트는 데이터 처리, 모델 정의, 학습 및 평가 간의 명확한 분리를 통해 모듈식 아키텍처를 사용합니다.

### 주요 디렉토리

- `src/lobster/` - 모든 핵심 기능을 포함하는 메인 패키지
- `src/lobster/model/` - 모델 아키텍처 (MLM, CLM, 컨셉 병목 모델 등)
- `src/lobster/data/` - 다양한 생물학적 데이터셋을 위한 데이터 모듈
- `src/lobster/datasets/` - 다양한 데이터 유형을 위한 데이터셋 구현
- `src/lobster/tokenization/` - 생물학적 서열(아미노산, 뉴클레오티드, SMILES)을 위한 토크나이저
- `src/lobster/transforms/` - 데이터 변환 함수
- `src/lobster/hydra_config/` - 모든 구성 요소를 위한 Hydra 설정 파일
- `src/lobster/cmdline/` - 명령줄 인터페이스 구현
- `tests/` - src 구조를 미러링하는 단위 테스트
- `examples/` - 추론 및 개입을 위한 예제 스크립트
- `notebooks/` - 튜토리얼을 위한 Jupyter 노트북

## 일반적인 명령어

### 설치 및 환경
```bash
# uv를 사용한 기본 설치 방법
uv sync
uv sync --extra flash  # flash attention 포함

# mamba를 사용한 대체 방법
mamba env create -f env.yml
pip install -e .
```

### 테스트
```bash
python -m pytest -v --cov-report term-missing --cov=./lobster ./tests
```

### 코드 품질
```bash
pre-commit install  # pre-commit 훅 설정
pre-commit run --all-files  # 모든 검사 실행
ruff check --fix  # 린트 및 문제 수정
ruff format  # 코드 포맷팅
```

### 학습 및 추론
```bash
# 모델 학습
lobster_train data.path_to_fasta="test_data/query.fasta" logger=csv paths.root_dir="."

# 서열 임베딩
lobster_embed data.path_to_fasta="test_data/query.fasta" checkpoint="path_to_checkpoint.ckpt"

# 기타 CLI 명령어
lobster_predict
lobster_intervene
lobster_perplexity
lobster_eval
```

## 모델 아키텍처

이 라이브러리는 여러 모델 유형을 구현합니다:

1. **LobsterPMLM**: 마스크 언어 모델 (BERT 스타일 인코더 전용)
2. **LobsterCBMPMLM**: 718개의 생물학적 컨셉을 가진 컨셉 병목 마스크 언어 모델
3. **LobsterPCLM**: 인과적 언어 모델 (Llama 스타일 디코더 전용)
4. **LobsterPLMFold**: 구조 예측 모델 (인코더 + 구조 헤드)
5. **최신 BERT 변형**: FlexBERT 및 Hyena 아키텍처 포함

### 주요 기본 클래스
- `LMBaseForMaskedLM` - 마스크 언어 모델을 위한 기본 클래스
- `LMBaseContactPredictionHead` - 구조 예측 작업을 위한 접촉 예측 헤드
- 모델은 학습 관리를 위해 PyTorch Lightning 모듈을 확장합니다.

## 설정 시스템

이 프로젝트는 설정 관리를 위해 Hydra를 사용합니다:

- 모든 설정은 `src/lobster/hydra_config/`에 있습니다.
- 모듈식 설정: `data/`, `model/`, `callbacks/`, `trainer/` 등
- 기본 학습 설정은 `fasta` 데이터와 `mlm` 모델을 사용합니다.
- 명령줄 구문을 사용하여 설정을 재정의합니다: `model=clm data=calm`

## 토큰화

생물학적 서열을 위한 다수의 특수 토크나이저:
- `pmlm_tokenizer` - 기본 단백질 토크나이저
- `amino_acid_tokenizer` - 아미노산 서열
- `nucleotide_tokenizer` - DNA/RNA 서열
- `smiles_tokenizer` - 화학적 SMILES 문자열
- `hyena_tokenizer`, `mgm_tokenizer` - 아키텍처별 토크나이저

모든 토크나이저는 HuggingFace 토크나이저 인터페이스를 따르며 어휘 파일과 특수 토큰을 포함합니다.

## 데이터 파이프라인

데이터 처리는 Lightning의 DataModule 패턴을 따릅니다:
- `FastaDataModule` - FASTA 서열 파일
- `CALMDataModule` - CALM 데이터셋
- `UMEDataModule` - UME 멀티모달 데이터
- `ChemblDataModule` - 화학적 속성 데이터

데이터셋은 분산 학습 및 효율적인 데이터 로딩을 지원하는 PyTorch의 Dataset/IterableDataset 인터페이스를 구현합니다.

## 개발 참고 사항

- 프로젝트는 의존성 관리를 위해 `uv` (선호) 또는 `mamba`를 사용합니다.
- pre-commit 훅은 ruff 린팅 및 포맷팅을 강제합니다.
- 새로운 코드에 대한 테스트 커버리지가 필요합니다.
- 모델은 CPU 및 GPU 실행을 모두 지원합니다.
- 분산 학습은 Lightning을 통해 지원됩니다.
- 실험 추적을 위해 Weights & Biases와 통합됩니다.

## Git 커밋 가이드라인

git 커밋을 생성할 때, 커밋 메시지에 다음 텍스트를 포함하지 마십시오:
```
🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

커밋 메시지는 간결하고 실제 변경 사항에 초점을 맞춰 작성하십시오.

## 이 파일 업데이트

다음 사항 변경 시 CLAUDE.md를 업데이트하십시오:
- CLI 명령어 또는 진입점
- 프로젝트 구조 또는 주요 디렉토리
- 설치 방법 또는 의존성
- 핵심 모델 아키텍처
- 설정 패턴 또는 데이터 파이프라인
