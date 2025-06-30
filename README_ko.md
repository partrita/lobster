# LBSTER 🦞
**L**anguage models for **B**iological **S**equence **T**ransformation and **E**volutionary **R**epresentation
**(생물학적 서열 변형 및 진화적 표현을 위한 언어 모델)**


`lobster`는 단백질 및 기타 생물학적 서열을 위한 "모든 기능이 포함된(batteries included)" 언어 모델 라이브러리입니다. [Nathan Frey](https://github.com/ncfrey), [Karina Zadorozhny](https://github.com/karinazad), [Taylor Joren](https://github.com/taylormjs), [Sidney Lisanza](https://github.com/Sidney-Lisanza), [Aya Abdlesalam Ismail](https://github.com/ayaabdelsalam91), [Joseph Kleinhenz](https://github.com/kleinhenz), [Allen Goodman](https://github.com/0x00b1)이 주도하고 있으며, [Prescient Design, Genentech](https://www.gene.com/scientists/our-scientists/prescient-design)의 [기여자들](docs/CONTRIBUTORS.md)로부터 많은 귀중한 기여를 받았습니다.

이 리포지토리에는 생물학적 서열 데이터를 위한 학습 코드와 사전 학습된 언어 모델에 대한 액세스가 포함되어 있습니다.

## 사용법


<!---
이미지 출처: Amy Wang
-->
<p align="center">
<img src="https://raw.githubusercontent.com/prescient-design/lobster/refs/heads/main/assets/lobster.png" width=200px>
</p>


<details open><summary><b>목차</b></summary>

- [LBSTER를 사용해야 하는 이유](#why-use)
- [인용](#citations)
- [설치 지침](#install)
- [모델](#main-models)
- [노트북](#notebooks)
- [MCP 서버](#mcp-integration)
- [학습 및 추론](#training)
- [UME를 사용한 강화 학습](#rl-training)
- [기여](#contributing)
</details>

## LBSTER를 사용해야 하는 이유 <a name="why-use"></a>
* LBSTER는 모델을 처음부터 빠르게 사전 학습할 수 있도록 구축되었습니다. "모든 기능이 포함되어 있습니다." 이는 사전 학습 데이터 혼합 및 임베딩 공간을 제어해야 하거나 새로운 사전 학습 목표 및 미세 조정 전략을 실험하려는 경우에 가장 유용합니다.
* LBSTER는 살아있는 오픈 소스 라이브러리로, [Prescient Design, Genentech](https://www.gene.com/scientists/our-scientists/prescient-design)의 [Frey Lab](https://ncfrey.github.io/)에서 새로운 코드와 사전 학습된 모델로 주기적으로 업데이트될 예정입니다. Frey Lab은 실제 치료용 분자 설계 문제를 다루며, LBSTER 모델과 기능은 실제 신약 개발 캠페인의 요구 사항을 반영합니다.
* LBSTER는 생물학 연구를 위한 표준 라이브러리인 [beignet](https://github.com/Genentech/beignet/tree/main)으로 구축되었으며, 멀티태스크 모델링, 유도 생성 및 멀티모달 모델을 위한 모듈식 프레임워크인 [cortex](https://github.com/prescient-design/cortex/tree/main)와 통합되어 있습니다.
* LBSTER는 개념을 지원합니다. 718개의 개념을 지원하는 개념 병목 단백질 언어 모델인 CB-LBSTER가 있습니다.

## 인용 <a name="citations"></a>
코드 및/또는 모델을 사용하는 경우 관련 논문을 인용해 주십시오.
`lbster` 코드 베이스의 경우 다음을 인용하십시오: [Cramming Protein Language Model Training in 24 GPU Hours](https://www.biorxiv.org/content/early/2024/05/15/2024.05.14.594108)
```bibtex
@article{Frey2024.05.14.594108,
	author = {Frey, Nathan C. and Joren, Taylor and Ismail, Aya Abdelsalam and Goodman, Allen and Bonneau, Richard and Cho, Kyunghyun and Gligorijevi{\'c}, Vladimir},
	title = {Cramming Protein Language Model Training in 24 GPU Hours},
	elocation-id = {2024.05.14.594108},
	year = {2024},
	doi = {10.1101/2024.05.14.594108},
	publisher = {Cold Spring Harbor Laboratory},
	URL = {https://www.biorxiv.org/content/early/2024/05/15/2024.05.14.594108},
	eprint = {https://www.biorxiv.org/content/early/2024/05/15/2024.05.14.594108.full.pdf},
	journal = {bioRxiv}
}

```


`cb-lbster` 코드 베이스의 경우 다음을 인용하십시오: [Concept Bottleneck Language Models for Protein Design](https://arxiv.org/abs/2411.06090)
```bibtex
@article{ismail2024conceptbottlenecklanguagemodels,
      title={Concept Bottleneck Language Models For protein design},
      author={Aya Abdelsalam Ismail and Tuomas Oikarinen and Amy Wang and Julius Adebayo and Samuel Stanton and Taylor Joren and Joseph Kleinhenz and Allen Goodman and H{\'e}ctor Corrada Bravo and Kyunghyun Cho and Nathan C. Frey},
      year={2024},
      eprint={2411.06090},
      archivePrefix={arXiv},
      primaryClass={cs.LG},
      url={https://arxiv.org/abs/2411.06090},
}

```

## 설치 <a name="install"></a>

### `uv` 사용
[uv](https://github.com/astral-sh/uv)를 설치하고 새 가상 환경을 만듭니다:


```bash
uv venv --python 3.12  # `lobster` 디렉토리에 새 가상 환경 만들기
source .venv/bin/activate
uv pip install -e .
```

또는 `uv sync`로 직접 설치를 실행합니다:
```bash
uv sync
```
그런 다음 모든 명령어 앞에 `uv run`을 붙입니다. 예를 들어,

```bash
uv run lobster_train data.path_to_fasta="test_data/query.fasta"
```

### flash attention
[flash attention](https://github.com/Dao-AILab/flash-attention)을 사용하려면 `flash` extra와 함께 설치하십시오.
```bash
uv sync --extra flash
```

### `mamba` 사용
리포지토리를 복제하고 해당 디렉토리로 이동한 후 `mamba env create -f env.yml`을 실행합니다.
그런 다음 리포지토리의 루트에서 다음을 수행합니다.
```bash
pip install -e .
```

## 사용해야 할 주요 모델 <a name="main-models"></a>

### 사전 학습된 모델

#### 마스크 언어 모델 (Masked LMs)
| 약칭 | 파라미터 수 | 데이터셋 | 설명 | 모델 체크포인트 |
|---------|------------|---------|------------------------------------------------------------|-------------|
Lobster_24M | 2,400만 | uniref50 | uniref50으로 학습된 2,400만 파라미터 단백질 마스크 언어 모델 | [lobster_24M](https://huggingface.co/asalam91/lobster_24M)
Lobster_150M | 1억 5,000만 | uniref50 | uniref50으로 학습된 1억 5,000만 파라미터 단백질 마스크 언어 모델 |[lobster_150M](https://huggingface.co/asalam91/lobster_150M)


#### 개념 병목 언어 모델 (CB LMs)
| 약칭 | 파라미터 수 | 데이터셋 | 설명 | 모델 체크포인트 |
|---------|------------|---------|------------------------------------------------------------|-------------|
cb_Lobster_24M | 2,400만 | uniref50+SwissProt | 718개 개념을 가진 2,400만 파라미터 단백질 개념 병목 모델 | [cb_lobster_24M](https://huggingface.co/asalam91/cb_lobster_24M)
cb_Lobster_150M | 1억 5,000만 | uniref50+SwissProt | 718개 개념을 가진 1억 5,000만 파라미터 단백질 개념 병목 모델 |[cb_lobster_150M](https://huggingface.co/asalam91/cb_lobster_150M)
cb_Lobster_650M | 6억 5,000만 | uniref50+SwissProt | 718개 개념을 가진 6억 5,000만 파라미터 단백질 개념 병목 모델 |[cb_lobster_650M](https://huggingface.co/asalam91/cb_lobster_650M)
cb_Lobster_3B | 30억 | uniref50+SwissProt | 718개 개념을 가진 30억 파라미터 단백질 개념 병목 모델 |[cb_lobster_3B](https://huggingface.co/asalam91/cb_lobster_3B)

### 사전 학습된 모델 로드하기
```python
from lobster.model import LobsterPMLM, LobsterPCLM, LobsterCBMPMLM
masked_language_model = LobsterPMLM("asalam91/lobster_24M")
concept_bottleneck_masked_language_model = LobsterCBMPMLM("asalam91/cb_lobster_24M")
causal_language_model = LobsterPCLM.load_from_checkpoint(<ckpt 경로>)
```
3D, cDNA 및 동적 모델은 동일한 클래스를 사용합니다.

**모델**
* LobsterPMLM: 마스크 언어 모델 (BERT 스타일 인코더 전용 아키텍처)
* LobsterCBMPMLM: 개념 병목 마스크 언어 모델 (개념 병목 및 선형 디코더가 있는 BERT 스타일 인코더 전용 아키텍처)
* LobsterPCLM: 인과적 언어 모델 (Llama 스타일 디코더 전용 아키텍처)
* LobsterPLMFold: 구조 예측 언어 모델 (사전 학습된 인코더 + 구조 헤드)


## 노트북 <a name="notebooks"></a>

### 표현 학습

다양한 모델에서 임베딩 표현을 추출하는 방법에 대한 예제는 이 [jupyter 노트북 튜토리얼](notebooks/01-inference.ipynb)을 확인하십시오.


### 개념 개입

개념 병목 모델 클래스에 대해 다양한 개념에 개입하는 방법에 대한 예제는 이 [jupyter 노트북 튜토리얼](notebooks/02-intervention.ipynb)을 확인하십시오.

## MCP 통합

Lobster는 Claude Desktop 및 기타 AI 도구와의 원활한 통합을 위해 [모델 컨텍스트 프로토콜(MCP)](https://modelcontextprotocol.io/)을 지원합니다:

```bash
# MCP 지원과 함께 설치
uv sync --extra mcp

# Claude Desktop 통합 설정
uv run lobster_mcp_setup
```

<!-- ### Cursor용 원클릭 설치 -->
<!-- TODO -->
<!-- [![Cursor에 Lobster MCP 서버 추가](https://cursor.com/deeplink/mcp-install-dark.svg)](cursor://anysphere.cursor-deeplink/mcp/install?name=lobster-inference&config=eyJjb21tYW5kIjoidXYiLCJhcmdzIjpbInJ1biIsIi0tZXh0cmEiLCJtY3AiLCJsb2JzdGVyX21jcF9zZXJ2ZXIiXX0=) -->

설정 후 Cursor 또는 Claude Desktop에서 다음과 같은 자연어 명령으로 Lobster 모델을 직접 사용할 수 있습니다:
- "lobster_24M을 사용하여 이 단백질 서열에 대한 임베딩 가져오기"
- "cb_lobster_24M 모델에서 지원하는 개념은 무엇인가?"
- "소수성을 줄이기 위해 이 서열에 개입하기"

전체 문서는 [MCP 통합 가이드](docs/MCP_INTEGRATION.md)를 참조하십시오.

## 예제 스크립트

추론 및 개입을 수행하는 방법을 보여주는 스크립트는 [examples](examples/)를 확인하십시오.

## 학습 및 추론 <a name="training"></a>

### 임베딩
`lobster_embed` 진입점은 서열 임베딩을 위한 주요 드라이버이며 Hydra 구문을 사용하여 매개변수를 허용합니다. 사용 가능한 구성 매개변수는 `lobster_embed --help`를 실행하거나 src/lobster/hydra_config 디렉토리를 참조하여 찾을 수 있습니다.

대화형 GPU 노드에서 사전 학습된 모델을 사용하여 fasta 파일의 서열을 임베딩하려면 이 리포지토리의 루트 디렉토리로 이동한 후 다음을 수행하십시오.
```bash
lobster_embed data.path_to_fasta="test_data/query.fasta" checkpoint="path_to_checkpoint.ckpt"
```

이렇게 하면 임베딩 데이터프레임이 생성되고 wandb에도 기록됩니다.

### 회귀 및 분류
강력한 멀티태스크 모델링을 위해서는 `lobster`를 [cortex]((https://github.com/prescient-design/cortex/tree/main))와 함께 사용하는 것이 좋습니다. `lobster` 임베딩을 사용하는 간단한 기준선에는 `lobster.model.LinearProbe` 및 `lobster.model.LobsterMLP`를 사용하십시오.

### 가능도
자기 회귀 `LobsterCLM`의 가능도 또는 `LobsterPMLM`의 의사 로그 가능도("자연스러움")는 다음을 사용하여 `sequences` 목록에 대해 계산할 수 있습니다.

```python
model.naturalness(sequences)
model.likelihood(sequences)
```

### 처음부터 학습하기
`lobster_train` 진입점은 학습을 위한 주요 드라이버이며 Hydra 구문을 사용하여 매개변수를 허용합니다. 사용 가능한 구성 매개변수는 `lobster_train --help`를 실행하거나 src/lobster/hydra_config 디렉토리를 참조하여 찾을 수 있습니다.

대화형 GPU 노드에서 fasta 파일의 서열에 대해 MLM을 학습하려면 이 리포지토리의 루트 디렉토리로 이동한 후 다음을 수행하십시오.
```bash
lobster_train data.path_to_fasta="test_data/query.fasta" logger=csv paths.root_dir="."
```

### UME 보상 함수를 사용한 강화 학습 <a name="rl-training"></a>

Lobster는 사전 학습된 언어 모델의 사후 학습을 위해 UME 기반 보상 함수를 사용하는 강화 학습을 지원합니다. 이 접근 방식은 UME 의사 가능도 점수를 보상으로 사용하여 모델이 생물학적으로 더 타당한 서열을 생성하도록 유도합니다.

**빠른 시작:**
```bash
# 1단계: 합성 데이터셋 생성
cd examples
python generate_synthetic_dataset.py

# 2단계: UME 기반 GRPO 학습 실행
python train_ume_grpo.py
```

**주요 특징:**
- SMILES, 아미노산 및 DNA 서열에 대한 **자동 양식 감지**
- 의사 가능도 점수를 사용하는 **UME 기반 보상 함수**
- TRL 통합을 통한 **GRPO 학습**
- 재사용 가능한 구성 요소가 있는 **모듈식 설계**

자세한 지침 및 고급 사용법은 [RL 학습 가이드](docs/RL_TRAINING.md)를 참조하십시오.

## 기여 <a name="contributing"></a>
기여를 환영합니다! 모든 사용자와 기여자는 LBSTER 팀이 모두 풀타임 신약 개발자이며, 우리의 오픈 소스 노력은 우리가 오픈 사이언스와 과학적 진보에 깊이 관심을 갖고 있기 때문에 사랑으로 하는 일이라는 점을 기억해 주시기 바랍니다.

### 기여 시작하기
단위 테스트 범위, 독스트링 및 유형 힌트를 확장하는 것은 언제나 환영하며 코드 베이스에 익숙해지는 좋은 시작점입니다. 🐛버그🐛를 식별하고 수정하는 것도 마찬가지입니다. 더 복잡한 프로젝트 아이디어는 [좋은 첫 번째 이슈](https://github.com/prescient-design/lobster/issues?q=is%3Aissue%20state%3Aopen%20label%3A%22good%20first%20issue%22)를 확인하십시오. 모든 신규 또는 수정된 코드는 유지 관리자가 검토하기 전에 *반드시* 단위 테스트를 거쳐야 합니다.

### 개발 요구 사항 및 pre-commit 훅 설치

```bash
pre-commit install
```

### 환경용 lockfile 생성
```bash
uv pip compile requirements.in -o requirements.txt
```

### 테스트

```bash
python -m pytest -v --cov-report term-missing --cov=./lobster ./tests
```
