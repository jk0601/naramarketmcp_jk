# 🚀 나라장터 FastMCP 2.0 서버 - 초보자 가이드

## 📖 이 프로젝트가 무엇인가요?

이 프로젝트는 **한국 정부조달(G2B) 및 나라장터의 복잡한 API들을 쉽게 사용할 수 있게 해주는 중간 서버**입니다.

### 🤔 왜 이런 서버가 필요한가요?

정부에서 제공하는 조달 데이터 API들은:
- 📋 **복잡한 파라미터**: 각 API마다 다른 형식의 파라미터 필요
- 🔐 **복잡한 인증**: API 키와 복잡한 요청 형식
- 📊 **다양한 데이터 형식**: 입찰공고, 낙찰정보, 통계 등 여러 종류의 데이터
- 🌐 **여러 개의 API**: 용도별로 분산된 다양한 API 엔드포인트

**이 서버는 이 모든 복잡함을 숨기고, 간단한 명령어로 데이터를 가져올 수 있게 해줍니다!**

### 🎯 주요 기능

| 기능 분류 | 설명 | 예시 |
|-----------|------|------|
| **📦 상품 정보** | 나라장터 쇼핑몰 상품 목록 및 상세 정보 | 데스크톱컴퓨터, 노트북 등 |
| **📋 입찰 정보** | 정부 입찰공고 및 낙찰 결과 조회 | 최근 30일 입찰공고 |
| **📊 통계 데이터** | 연도별, 기관별 조달 통계 | 2024년 조달 통계 |
| **🔍 검색 기능** | 제품명, 업체명으로 검색 | "삼성" 업체 제품 검색 |

---

## 🛠️ 설치 및 실행 방법

### 📋 준비사항

1. **Python 3.10 이상** 설치 필요
2. **나라장터 API 키** 필요 ([data.go.kr](https://www.data.go.kr/)에서 발급)

### 🚀 빠른 시작 (3단계)

#### 1단계: 프로젝트 다운로드
```bash
# 프로젝트 폴더로 이동
cd naramarketmcp-main

# 또는 Git으로 클론한 경우
git clone <repository-url>
cd naramarketmcp
```

#### 2단계: 환경 설정
```bash
# 가상환경 생성 (권장)
python -m venv venv

# 가상환경 활성화
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 필요한 패키지 설치
pip install -r requirements.txt
```

#### 3단계: API 키 설정
```bash
# 환경변수 설정 (Windows)
set NARAMARKET_SERVICE_KEY=여기에_발급받은_API키_입력

# 환경변수 설정 (Mac/Linux)
export NARAMARKET_SERVICE_KEY=여기에_발급받은_API키_입력
```

### ▶️ 서버 실행

#### 방법 1: MCP 모드 (기본)
```bash
python -m src.main
```

#### 방법 2: HTTP 서버 모드 (테스트용)
```bash
# 환경변수 설정
set FASTMCP_TRANSPORT=http
set FASTMCP_HOST=127.0.0.1
set FASTMCP_PORT=8000

# 서버 실행
python -m src.main
```

서버가 성공적으로 시작되면 다음과 같은 메시지가 표시됩니다:
```
✅ CORS configuration ready for Smithery.ai deployment
FastMCP 2.0 initialized: naramarket-fastmcp-2
```

---

## 🎮 사용 방법

### 🔧 HTTP 모드에서 테스트하기

HTTP 서버 모드로 실행한 후, 브라우저에서 `http://localhost:8000/mcp`에 접속하면 서버 정보를 확인할 수 있습니다.

### 📝 주요 기능 사용 예시

#### 1. 나라장터 상품 목록 조회
```json
{
  "method": "tools/call",
  "params": {
    "name": "crawl_list",
    "arguments": {
      "category": "데스크톱컴퓨터",
      "page_no": 1,
      "num_rows": 10,
      "days_back": 30
    }
  }
}
```

#### 2. 최근 입찰공고 조회
```json
{
  "method": "tools/call",
  "params": {
    "name": "get_recent_bid_announcements",
    "arguments": {
      "business_type": "물품",
      "num_rows": 5,
      "days_back": 7
    }
  }
}
```

#### 3. 쇼핑몰 제품 검색
```json
{
  "method": "tools/call",
  "params": {
    "name": "search_shopping_mall_products",
    "arguments": {
      "product_name": "노트북",
      "num_rows": 10
    }
  }
}
```

---

## 🏗️ 프로젝트 구조 이해하기

```
naramarketmcp-main/
├── 📁 src/                    # 메인 소스코드
│   ├── 📄 main.py            # 🚪 서버 시작점 (여기서 모든 것이 시작됩니다)
│   ├── 📁 core/              # 🔧 핵심 설정들
│   │   ├── config.py         # ⚙️ API 키, URL 등 설정
│   │   ├── models.py         # 📊 데이터 구조 정의
│   │   └── client.py         # 🌐 API 호출 담당
│   ├── 📁 tools/             # 🛠️ 실제 기능들
│   │   ├── naramarket.py     # 🛒 나라장터 관련 기능
│   │   └── enhanced_tools.py # ✨ 고급 기능들
│   └── 📁 services/          # 🔄 비즈니스 로직
├── 📄 requirements.txt       # 📦 필요한 패키지 목록
├── 📄 pyproject.toml        # 🔧 프로젝트 설정
├── 📄 Dockerfile           # 🐳 Docker 컨테이너 설정
└── 📄 deploy.sh            # 🚀 배포 스크립트
```

### 🔍 주요 파일 설명

- **`src/main.py`**: 서버의 심장부! 모든 기능들이 여기서 등록되고 시작됩니다
- **`src/core/config.py`**: API 키와 URL 같은 중요한 설정들을 관리합니다
- **`src/tools/naramarket.py`**: 나라장터에서 데이터를 가져오는 실제 기능들
- **`requirements.txt`**: 이 프로젝트가 동작하는데 필요한 Python 패키지들의 목록

---

## 🔧 문제 해결 가이드

### ❌ 자주 발생하는 문제들

#### 1. "Missing or invalid NARAMARKET_SERVICE_KEY" 오류
```
해결방법:
1. data.go.kr에서 API 키를 발급받았는지 확인
2. 환경변수가 올바르게 설정되었는지 확인
3. API 키에 특수문자나 공백이 없는지 확인
```

#### 2. "ModuleNotFoundError: No module named 'fastmcp'" 오류
```
해결방법:
1. 가상환경이 활성화되었는지 확인
2. pip install -r requirements.txt 다시 실행
3. Python 버전이 3.10 이상인지 확인
```

#### 3. 서버가 시작되지 않는 경우
```
해결방법:
1. 포트 8000이 다른 프로그램에서 사용 중인지 확인
2. 방화벽 설정 확인
3. 관리자 권한으로 실행해보기
```

#### 4. API 응답이 없거나 느린 경우
```
해결방법:
1. 인터넷 연결 상태 확인
2. API 키의 사용량 제한 확인
3. 요청하는 데이터 양을 줄여보기 (num_rows 값 감소)
```

### 🔍 로그 확인하기

문제가 발생하면 서버 실행 시 나타나는 로그 메시지를 확인해보세요:

```bash
# 자세한 로그 보기
set LOG_LEVEL=DEBUG
python -m src.main
```

---

## 🌐 배포 방법

### 🐳 Docker로 실행하기

```bash
# Docker 이미지 빌드
docker build -t naramarket-mcp .

# Docker 컨테이너 실행
docker run --rm -p 8000:8000 \
  -e NARAMARKET_SERVICE_KEY=여기에_API키_입력 \
  naramarket-mcp
```

### ☁️ 클라우드 배포 (Smithery.ai)

1. **Smithery CLI 설치**
   ```bash
   npm install -g @smithery/cli
   ```

2. **배포 실행**
   ```bash
   ./deploy.sh
   ```

---

## 📚 사용 가능한 도구들 (총 15개)

### 🏛️ 기본 API 호출 도구 (4개)
- `call_public_data_standard_api`: 입찰공고, 낙찰정보 등
- `call_procurement_statistics_api`: 조달 통계 정보
- `call_product_list_api`: 상품분류, 물품정보
- `call_shopping_mall_api`: MAS 계약 상품정보

### 🤖 AI 친화 간편 도구 (4개)
- `get_recent_bid_announcements`: 최근 입찰공고 (한글로 쉽게!)
- `get_successful_bids_by_business_type`: 업무구분별 낙찰정보
- `get_procurement_statistics_by_year`: 연도별 조달통계
- `search_shopping_mall_products`: 쇼핑몰 제품 검색

### 🧭 고급 분석 도구 (4개)
- `get_all_api_services_info`: 전체 API 서비스 정보
- `get_api_operations`: 서비스별 세부 기능
- `call_api_with_pagination_support`: 대량 데이터 조회
- `get_data_exploration_guide`: 데이터 탐색 가이드

### 📦 기본 기능 도구 (3개)
- `crawl_list`: 나라장터 상품 목록 조회
- `get_detailed_attributes`: 상품 상세 속성 조회
- `server_info`: 서버 정보 확인

---

## 🎓 오늘의 학습 포인트: FastMCP란?

**FastMCP**는 이 프로젝트의 핵심 기술입니다! 

### 🤔 FastMCP가 뭔가요?

**MCP (Model Context Protocol)**는 AI 모델이 외부 도구나 데이터에 접근할 수 있게 해주는 표준 프로토콜입니다. **FastMCP**는 이를 Python으로 쉽게 구현할 수 있게 해주는 프레임워크입니다.

### 🌟 왜 중요한가요?

1. **표준화**: AI가 다양한 도구를 일관된 방식으로 사용할 수 있습니다
2. **확장성**: 새로운 기능을 쉽게 추가할 수 있습니다
3. **호환성**: 다양한 AI 클라이언트와 연동 가능합니다

### 💡 어떻게 작동하나요?

```python
# 이렇게 간단하게 도구를 만들 수 있어요!
@mcp.tool(name="hello_world", description="인사말을 출력합니다")
def hello_world(name: str) -> str:
    return f"안녕하세요, {name}님!"
```

이 한 줄의 데코레이터(`@mcp.tool`)로 Python 함수가 AI가 사용할 수 있는 도구로 변신합니다! 🎭

### 🚀 장점

- **간단함**: 복잡한 API 서버 구축 없이도 AI 도구 제작 가능
- **자동화**: 함수 시그니처를 보고 자동으로 API 문서 생성
- **타입 안전성**: Python의 타입 힌트를 활용한 안전한 개발

이것이 바로 이 프로젝트가 복잡한 정부 API들을 15개의 간단한 도구로 만들 수 있었던 비밀입니다! ✨

---

## 🤝 도움이 필요하시나요?

- 🐛 **버그 발견**: GitHub Issues에 신고해주세요
- 💡 **기능 제안**: 새로운 아이디어를 공유해주세요
- ❓ **사용법 문의**: 언제든 질문해주세요

---

## 📄 라이선스

Apache License 2.0 - 자유롭게 사용하세요! 📜

---

**🎉 축하합니다! 이제 나라장터 FastMCP 서버를 사용할 준비가 되었습니다!**

*"복잡한 정부 데이터도 이제 간단하게!" 🚀*
