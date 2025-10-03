# 🚀 나라장터 MCP 서버 - 초보자 가이드

> **MCP가 처음이신가요?** 이 가이드는 MCP(Model Context Protocol)를 처음 접하는 분들을 위해 작성되었습니다.

## 🤔 MCP가 뭔가요?

**MCP(Model Context Protocol)**는 AI가 외부 데이터나 서비스에 접근할 수 있게 해주는 **다리** 역할을 합니다.

```
┌─────────────┐    MCP    ┌─────────────┐    API    ┌─────────────┐
│   AI 모델   │ ◄────────► │ MCP 서버    │ ◄────────► │ 정부조달API │
│  (Claude)   │           │ (이 프로젝트) │           │ (나라장터)   │
└─────────────┘           └─────────────┘           └─────────────┘
```

**쉽게 말하면:**
- AI가 "최근 입찰공고 알려줘"라고 물어보면
- MCP 서버가 정부 API에서 데이터를 가져와서
- AI에게 정리된 정보를 전달해줍니다

## 🎯 이 프로젝트가 하는 일

이 MCP 서버는 **정부조달 데이터**를 AI가 쉽게 사용할 수 있게 해줍니다:

- 📋 **입찰공고 조회** - "최근 컴퓨터 관련 입찰 있어?"
- 🏆 **낙찰정보 확인** - "삼성전자가 따낸 계약 보여줘"
- 📊 **통계 데이터** - "올해 IT 분야 조달 규모는?"
- 🛒 **쇼핑몰 상품** - "나라장터에서 파는 프린터 목록"

## 🚀 빠른 시작 (시각적 확인 가능!)

### 1단계: 환경 준비

```bash
# 1. 가상환경 활성화
.\venv\Scripts\Activate.ps1

# 2. 의존성 설치 확인
pip install -r requirements.txt
```

### 2단계: API 키 설정

`.env` 파일을 만들고 다음 내용 추가:
```env
NARAMARKET_SERVICE_KEY=your_api_key_here
```

### 3단계: 서버 시작 (3가지 방법)

#### 🖥️ 방법 1: STDIO 모드 (기본)
```bash
py -m src.main
```
**결과:** 터미널에 예쁜 ASCII 아트와 함께 서버 시작 메시지가 나타납니다.

#### 🌐 방법 2: HTTP 모드 (웹에서 확인 가능!)
```bash
set FASTMCP_TRANSPORT=http
set PORT=8080
py -m src.main
```

**확인 방법:**
1. 웹 브라우저에서 `http://localhost:8080/health` 접속
2. 다음과 같은 JSON이 보이면 성공! 🎉

```json
{
  "status": "healthy",
  "server": "naramarket-fastmcp-2",
  "version": "2.0.0",
  "available_tools": 15,
  "message": "Server is running successfully!"
}
```

#### ⚡ 방법 3: SSE 모드 (실시간 통신)
```bash
set FASTMCP_TRANSPORT=sse
set PORT=8080
py -m src.main
```

## 🧪 서버 테스트하기

### 웹 브라우저에서 간단 테스트

HTTP 모드로 서버를 시작한 후:

1. **상태 확인:** `http://localhost:8080/health`
2. **API 테스트:** `http://localhost:8080/api`에 POST 요청

### Postman이나 curl로 테스트

```bash
# 서버 상태 확인
curl http://localhost:8080/health

# 간단한 도구 호출 테스트
curl -X POST http://localhost:8080/api \
  -H "Content-Type: application/json" \
  -d '{
    "method": "tools/call",
    "params": {
      "name": "server_info",
      "arguments": {}
    }
  }'
```

## 🎮 실제 사용 예시

### Claude Desktop과 연결하기

1. **Claude Desktop 설정**에서 MCP 서버 추가
2. 서버 경로: `D:\j\cursor\naramarketmcp-main`
3. 실행 명령: `py -m src.main`

### AI와 대화 예시

```
👤 사용자: "최근 일주일간 컴퓨터 관련 입찰공고 알려줘"

🤖 Claude: (MCP 서버를 통해 정부 API 호출)
"최근 7일간 컴퓨터 관련 입찰공고 3건을 찾았습니다:
1. 서울시청 - 업무용 PC 100대 구매 (예산: 5억원)
2. 교육부 - 노트북 50대 임대 (예산: 2억원)
3. 국방부 - 서버 장비 구축 (예산: 10억원)"
```

## 🛠️ 사용 가능한 도구들

이 MCP 서버는 **15개의 도구**를 제공합니다:

### 📋 기본 조회 도구
- `server_info` - 서버 상태 확인
- `crawl_list` - 카테고리별 상품 목록
- `get_detailed_attributes` - 상품 상세 정보

### 🎯 AI 친화적 간단 도구
- `get_recent_bid_announcements` - 최근 입찰공고
- `get_successful_bids_by_business_type` - 업종별 낙찰정보
- `search_shopping_mall_products` - 쇼핑몰 상품 검색

### 📊 고급 분석 도구
- `call_public_data_standard_api` - 공공데이터 표준 API
- `call_procurement_statistics_api` - 조달 통계 API
- `call_product_list_api` - 물품 목록 API
- `call_shopping_mall_api` - 쇼핑몰 API

## 🔍 문제 해결

### 자주 발생하는 오류들

#### 1. `ImportError: attempted relative import`
**해결:** `py src/main.py` 대신 `py -m src.main` 사용

#### 2. `API key not found`
**해결:** `.env` 파일에 `NARAMARKET_SERVICE_KEY` 설정 확인

#### 3. `Port already in use`
**해결:** 다른 포트 사용 (`set PORT=8081`)

### 로그 확인하기

서버 실행 시 나타나는 로그 메시지들:

```
✅ 성공 메시지들:
[INFO] API service key loaded successfully (length: 64)
[INFO] FastMCP 2.0 initialized: naramarket-fastmcp-2
[INFO] Starting STDIO transport

❌ 오류 메시지들:
[ERROR] Configuration error: Invalid API key
[ERROR] Server startup failed: Port 8080 already in use
```

## 🎨 시각적 확인 방법들

### 1. 터미널에서 ASCII 아트 확인
서버가 시작되면 예쁜 로고가 나타납니다:

```
╭────────────────────────────────────────────────────────────────────────────╮
│                                                                            │
│        _ __ ___  _____           __  __  _____________    ____    ____     │
│       _ __ ___ .'____/___ ______/ /_/  |/  / ____/ __ \  |___ \  / __ \    │
│      _ __ ___ / /_  / __ `/ ___/ __/ /|_/ / /   / /_/ /  ___/ / / / / /    │
│     _ __ ___ / __/ / /_/ (__  ) /_/ /  / / /___/ ____/  /  __/_/ /_/ /     │
│    _ __ ___ /_/    \____/____/\__/_/  /_/\____/_/      /_____(*)____/      │
│                                                                            │
│                                FastMCP  2.0                                │
│                                                                            │
│                 🖥️  Server name:     naramarket-fastmcp-2                   │
│                 📦 Transport:       STDIO                                  │
╰────────────────────────────────────────────────────────────────────────────╯
```

### 2. 웹 브라우저에서 JSON 응답 확인
HTTP 모드에서 `/health` 엔드포인트 접속 시 깔끔한 JSON 응답

### 3. 개발자 도구에서 네트워크 탭 확인
브라우저 F12 → Network 탭에서 API 호출 과정 실시간 확인

## 🚀 다음 단계

1. **Claude Desktop 연결** - AI와 실제 대화해보기
2. **커스텀 도구 추가** - 필요한 기능 직접 만들어보기
3. **웹 인터페이스 구축** - React나 Vue로 예쁜 UI 만들기
4. **클라우드 배포** - Smithery.ai나 Docker로 배포하기

## 💡 팁과 요령

### 개발 시 유용한 명령어들

```bash
# 서버 재시작 (Ctrl+C 후)
py -m src.main

# 다른 포트로 HTTP 서버 시작
set PORT=8081 && set FASTMCP_TRANSPORT=http && py -m src.main

# 로그 레벨 변경
set LOG_LEVEL=DEBUG && py -m src.main
```

### 성능 최적화

- **num_rows=5**: 기본값으로 빠른 응답
- **days_back=7**: 최근 일주일 데이터로 제한
- **HTTP 모드**: 웹에서 직접 테스트 가능

## 🎉 축하합니다!

이제 여러분은 MCP 서버를 성공적으로 실행하고 테스트할 수 있습니다! 

**다음에 해볼 만한 것들:**
- Claude와 실제 대화해보기
- 다른 정부 API 연결해보기
- 나만의 MCP 서버 만들어보기

---

**문의사항이나 문제가 있으시면 이슈를 등록해주세요!** 🙋‍♂️

