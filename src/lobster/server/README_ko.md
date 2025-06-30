# UMEServer

`UMEServer` 클래스는 UME (Universal Model Embedding) 기능을 제공하기 위한 FastMCP 서버 구현을 제공합니다. 이를 통해 표준화된 MCP (Model Control Protocol) 인터페이스를 통해 임베딩 기능을 노출할 수 있습니다.

## 개요

`UMEServer`는 UME 모델 인스턴스를 래핑하고 FastMCP 서버를 통해 임베딩 기능을 노출합니다. 이를 통해 다양한 양식에 걸쳐 서열 임베딩 기능에 대한 표준화된 액세스가 가능합니다.

## 사용법

### 초기화

```python
from lobster.model import UME
from lobster.server import UMEServer

# UME 모델 초기화
model = UME(...)

# 서버 인스턴스 생성
server = UMEServer(model)
```

### 사용 가능한 도구

서버는 다음 도구를 노출합니다.

#### embed_sequences

서열을 잠재 공간에 임베딩합니다.

매개변수:
- `sequences`: 임베딩할 입력 서열
- `modality`: 서열의 양식
- `aggregate` (선택 사항): 임베딩을 집계할지 여부 (기본값: True)

반환 값:
- 잠재 공간에 임베딩된 서열

### 서버 인스턴스 가져오기

구성된 FastMCP 서버 인스턴스를 가져오려면:

```python
mcp_server = server.get_server()
```

## 예제

```python
from lobster.model import UME
from lobster.server import UMEServer

# 모델 및 서버 초기화
model = UME(...)
server = UMEServer(model)

# MCP 서버 인스턴스 가져오기
mcp_server = server.get_server()

# 임베딩할 예제 아미노산 서열
sequences = [
    "MLLAVLYCLAVFALSSRAG",  # 예제 단백질 서열 1
    "MKTVRQERLKSIVRILERSKEPVSGAQLAEELSVSRQVIVQDIAYLRSLGYNIVATPRGYVLAGG"  # 예제 단백질 서열 2
]
modality = "amino_acid"

# 서버 도구를 사용하여 서열 임베딩
embeddings = server.embed_sequences(
    sequences=sequences,
    modality=modality,
    aggregate=True  # 선택 사항, 기본값은 True
)

# 이제 임베딩을 다운스트림 작업에 사용할 수 있습니다.
print(f"생성된 임베딩 형태: {embeddings.shape}")
```

## 종속성

- FastMCP: MCP 서버 구현용
- UME: 기본 임베딩 모델
