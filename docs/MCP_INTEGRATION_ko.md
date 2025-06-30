# Lobster MCP 통합

이 문서는 Lobster의 모델 컨텍스트 프로토콜(MCP) 통합을 사용하여 MCP 서버를 통해 사전 학습된 모델을 노출하는 방법을 설명합니다.

## 개요

Lobster는 다음과 같은 기능을 위해 사전 학습된 모델을 노출하는 MCP 서버를 제공합니다.

- **서열 표현**: 다양한 Lobster 모델을 사용하여 단백질 서열에서 임베딩 가져오기
- **개념 분석**: 개념 병목 모델을 사용하여 서열에서 생물학적 개념 추출
- **개념 개입**: 특정 생물학적 개념을 기반으로 서열 수정
- **자연스러움 점수 계산**: 서열에 대한 가능도/자연스러움 점수 계산

### 사용 가능한 모델

**마스크 언어 모델 (MLM):**
- `lobster_24M`: UniRef50으로 학습된 2,400만 파라미터 모델
- `lobster_150M`: UniRef50으로 학습된 1억 5,000만 파라미터 모델

**개념 병목 모델 (CBM):**
- `cb_lobster_24M`: 718개의 생물학적 개념을 가진 2,400만 파라미터 모델
- `cb_lobster_150M`: 718개의 생물학적 개념을 가진 1억 5,000만 파라미터 모델
- `cb_lobster_650M`: 718개의 생물학적 개념을 가진 6억 5,000만 파라미터 모델
- `cb_lobster_3B`: 718개의 생물학적 개념을 가진 30억 파라미터 모델

## 설치

### uv를 사용한 빠른 시작 (권장)

1. MCP 지원과 함께 Lobster 설치:
```bash
uv sync --extra mcp
```

2. Claude Desktop 구성을 위한 설정 스크립트 실행:
```bash
uv run lobster_mcp_setup
```

### 대체 설치 방법

pip를 선호하는 경우:
```bash
pip install -e .[mcp]
```

### GPU 지원

GPU 가속을 위해서는 MCP와 flash attention을 모두 사용하여 설치하십시오.
```bash
uv sync --extra mcp --extra flash
```

## Claude Desktop과 함께 사용

설정 스크립트는 Claude Desktop을 자동으로 구성합니다.

```bash
uv run lobster_mcp_setup
```

이 작업은 다음을 수행합니다.
1. 모든 종속성(FastMCP 포함)이 설치되었는지 확인합니다.
2. 적절한 Claude Desktop 구성을 만듭니다.
3. `uv`를 통해 실행되도록 MCP 서버를 설정합니다.

설정 실행 후 Claude Desktop을 다시 시작하면 다음과 같은 명령을 사용할 수 있습니다.
- "사용 가능한 Lobster 모델은 무엇인가요?"
- "lobster_24M을 사용하여 단백질 서열 MKTVRQ에 대한 임베딩을 가져오세요."
- "cb_lobster_24M 모델에서 지원하는 개념은 무엇인가요?"
- "서열 MKTVRQERLKSIVRIL에 개입하여 소수성을 줄일 수 있나요?"

✅ **Claude Desktop에서 FastMCP 구현으로 작동 확인됨!**

## Cursor와 함께 사용

### 자동 설정 (권장)

설정 스크립트를 사용하여 Cursor를 자동으로 구성합니다.

```bash
uv run lobster_mcp_setup
```

메시지가 표시되면 Cursor의 경우 "2"를 선택하거나 Claude Desktop과 Cursor 모두의 경우 "3"을 선택합니다.

### 수동 설정

수동으로 구성하려면 `~/.cursor/mcp.json` 파일을 만들거나 편집합니다.

```json
{
  "mcpServers": {
    "lobster-inference": {
      "command": "uv",
      "args": [
        "run",
        "--project", "/path/to/lobster",
        "--extra", "mcp",
        "lobster_mcp_server"
      ]
    }
  }
}
```

`/path/to/lobster`를 Lobster 리포지토리의 실제 경로로 바꿉니다.

### Cursor에서 서버 사용

Cursor 설정 및 다시 시작 후:

1. **명령 팔레트**: 명령 팔레트 열기 (Cmd+Shift+P / Ctrl+Shift+P)
2. **MCP 명령**: 사용 가능한 MCP 관련 명령을 보려면 "MCP"를 입력합니다.
3. **채팅 통합**: 채팅에서 `@lobster-inference`를 사용하여 서버를 참조합니다.
4. **사용 가능한 도구**: 서버는 Claude Desktop과 동일한 도구를 제공합니다.
   - `list_available_models` - 사용 가능한 모든 Lobster 모델 나열
   - `get_sequence_representations` - 단백질 서열에 대한 임베딩 가져오기
   - `get_sequence_concepts` - 서열에서 생물학적 개념 추출
   - `intervene_on_sequence` - 개념을 기반으로 서열 수정
   - `get_supported_concepts` - CBM 모델에 대해 지원되는 개념 나열
   - `compute_naturalness` - 서열 자연스러움 점수 계산

### Cursor에서의 예제 사용법

구성 후 Cursor에서 자연어 명령을 사용할 수 있습니다.

```
@lobster-inference 사용 가능한 모델은 무엇인가요?

@lobster-inference lobster_24M을 사용하여 서열 MKTVRQERLKSIVRIL에 대한 임베딩을 가져오세요.

@lobster-inference cb_lobster_24M에서 지원하는 개념은 무엇인가요?

@lobster-inference cb_lobster_24M을 사용하여 MKTVRQERLKSIVRIL에 개입하여 소수성을 줄이세요.
```

✅ **FastMCP 구현으로 작동 확인됨!**

## MCP CLI와 함께 사용

```bash
# MCP 서버 직접 테스트
uv run lobster_mcp_server

# 테스트를 위해 MCP CLI 개발 모드 사용 (호환되는 경우)
uv run mcp dev src/lobster/mcp/inference_server.py:app --with-editable .
```

## 사용 가능한 도구

### get_sequence_representations
단백질 서열에 대한 임베딩 표현을 가져옵니다.

**매개변수:**
- `sequences`: 단백질 서열 목록
- `model_name`: 사용할 모델 이름
- `model_type`: "masked_lm" 또는 "concept_bottleneck"
- `representation_type`: "cls", "pooled" 또는 "full"

**예시:**
```json
{
  "sequences": ["MKTVRQERLKSIVRIL"],
  "model_name": "lobster_24M",
  "model_type": "masked_lm",
  "representation_type": "pooled"
}
```

### get_sequence_concepts
단백질 서열에 대한 개념 예측을 가져옵니다.

**매개변수:**
- `sequences`: 단백질 서열 목록
- `model_name`: 개념 병목 모델의 이름

### intervene_on_sequence
단백질 서열에 대한 개념 개입을 수행합니다.

**매개변수:**
- `sequence`: 수정할 단백질 서열
- `concept`: 개입할 개념 (예: "gravy", "hydrophobicity")
- `model_name`: 개념 병목 모델의 이름
- `edits`: 수행할 편집 횟수 (기본값: 5)
- `intervention_type`: "positive" 또는 "negative" (기본값: "negative")

### get_supported_concepts
개념 병목 모델에 대해 지원되는 개념 목록을 가져옵니다.

**매개변수:**
- `model_name`: 개념 병목 모델의 이름

### compute_naturalness
단백질 서열에 대한 자연스러움/가능도 점수를 계산합니다.

**매개변수:**
- `sequences`: 단백질 서열 목록
- `model_name`: 모델 이름
- `model_type`: "masked_lm" 또는 "concept_bottleneck"

### list_available_models
사용 가능한 모든 사전 학습된 Lobster 모델과 현재 장치를 나열합니다.

## 예제 사용법

Claude Desktop 또는 MCP CLI로 구성한 후 다음과 같이 도구를 사용할 수 있습니다.

```
lobster_24M 모델을 사용하여 단백질 서열 "MKTVRQERLKSIVRIL"에 대한 임베딩을 가져다 주시겠어요?
```

```
cb_lobster_24M 모델에서 지원하는 개념은 무엇인가요?
```

```
cb_lobster_24M 모델을 사용하여 서열 "MKTVRQERLKSIVRIL"에 개입하여 소수성을 줄일 수 있나요?
```

## GPU 지원

서버는 사용 가능한 경우 CUDA를 자동으로 감지하고 사용합니다. 모델은 효율성을 위해 처음 로드된 후 캐시됩니다.

## 문제 해결

1. **가져오기 오류**: Lobster가 MCP 지원과 함께 설치되었는지 확인하십시오: `uv sync --extra mcp`
2. **CUDA 오류**: GPU를 사용하는 경우 PyTorch가 CUDA 지원과 함께 설치되었는지 확인하십시오.
3. **모델 로드 오류**: HuggingFace에서 모델을 다운로드하기 위한 인터넷 연결이 있는지 확인하십시오.
4. **메모리 문제**: 메모리가 부족한 경우 더 작은 모델(24M, 150M)을 사용하십시오.
5. **Claude Desktop 연결 안 됨**: 설정 스크립트가 성공적으로 실행되었는지 확인하고 Claude Desktop을 다시 시작하십시오.

## 개발

### 개발 환경 설정

```bash
# 개발 종속성과 함께 설치
uv sync --all-extras

# 테스트 실행
uv run pytest tests/lobster/mcp/

# 린팅 및 포맷팅 실행
uv run ruff check src/lobster/mcp/
uv run ruff format src/lobster/mcp/

# 유형 검사
uv run mypy src/lobster/mcp/
```

### 새 도구 추가

새 도구나 모델을 추가하려면:

1. `src/lobster/mcp/inference_server.py`의 `handle_list_tools()`에 도구 정의를 추가합니다.
2. `handle_call_tool()`에 구현을 추가합니다.
3. 새 메서드로 `LobsterInferenceServer` 클래스를 업데이트합니다.
4. `tests/lobster/mcp/`에 테스트를 추가합니다.
5. 다음으로 테스트합니다: `uv run lobster_mcp_server`

### 패키지 구조

```
src/lobster/mcp/
├── __init__.py                         # MCP 모듈 초기화
├── inference_server.py                 # FastMCP 기반 MCP 서버
├── setup.py                           # Claude Desktop용 설정 스크립트
├── example_server.py                  # 사용 예제
└── claude_desktop_config.json         # 구성 템플릿

tests/lobster/mcp/
├── __init__.py
├── test_inference_server.py           # 단위 테스트
└── simple_test.py                     # 기본 기능 테스트
```

### MCP 서버 구현

이 패키지는 FastMCP 기반 서버 구현을 제공합니다.

- **lobster_mcp_server** - FastMCP 기반 서버
  - 더 나은 성능과 간단한 디버깅
  - 입력 유효성 검사를 위해 Pydantic 모델 사용
  - 최신 MCP 도구와 호환 가능

## 기술적 세부 정보

### MCP 서버 아키텍처

Lobster MCP 서버는 FastMCP를 사용하여 구축되었으며 다음 원칙을 따릅니다.

- **지연 로딩**: 모델은 처음 요청될 때만 로드됩니다.
- **캐싱**: 로드된 모델은 효율성을 위해 메모리에 남아 있습니다.
- **오류 처리**: 유익한 메시지를 제공하는 포괄적인 오류 처리
- **타입 안전성**: Pydantic을 사용한 전체 타입 힌트 및 유효성 검사
- **테스팅**: CI/CD를 위한 모의(mocking)를 사용한 포괄적인 단위 테스트

### 모델 로딩 전략

- 모델은 처음 사용할 때 HuggingFace Hub에서 다운로드됩니다.
- GPU/CPU 선택은 가용성에 따라 자동으로 이루어집니다.
- 모델 캐싱 및 정리를 통한 메모리 관리
- 통합 인터페이스를 통해 다양한 모델 유형(MLM, CBM) 지원

### Claude와의 통합

MCP 서버는 Claude Desktop 및 기타 MCP 클라이언트와 원활하게 통합됩니다.
- 자동 도구 검색 및 스키마 유효성 검사
- JSON 스키마를 사용한 구조화된 입력/출력
- 비차단 작업을 위한 비동기/대기(async/await) 지원
- 클라이언트에 대한 적절한 오류 전파
