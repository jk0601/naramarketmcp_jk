# 🚀 나라장터 MCP 서버 배포 가이드

이 가이드는 나라장터 MCP 서버를 다양한 클라우드 플랫폼에 배포하는 방법을 설명합니다.

## 🌐 지원하는 배포 플랫폼

- ✅ **Vercel** - 서버리스 배포 (무료 플랜 가능)
- ✅ **Render** - 컨테이너 기반 배포 (무료 플랜 가능)
- ✅ **Railway** - 간단한 Git 배포
- ✅ **Heroku** - 전통적인 PaaS 배포
- ✅ **Docker** - 어디든 배포 가능

## 🚀 Vercel 배포

### 1. 준비사항
- Vercel 계정
- GitHub 저장소에 코드 업로드
- `NARAMARKET_SERVICE_KEY` 환경변수

### 2. 배포 단계

```bash
# 1. Vercel CLI 설치
npm i -g vercel

# 2. 프로젝트 디렉토리에서 배포
vercel

# 3. 환경변수 설정
vercel env add NARAMARKET_SERVICE_KEY
```

### 3. Vercel 대시보드에서 설정
1. **Settings** → **Environment Variables**
2. `NARAMARKET_SERVICE_KEY` 추가
3. **Deployments** → **Redeploy**

### 4. 접속 확인
- `https://your-project.vercel.app/health`
- `https://your-project.vercel.app/api`

## 🔧 Render 배포

### 1. 준비사항
- Render 계정
- GitHub 저장소에 코드 업로드

### 2. 배포 단계

1. **Render 대시보드**에서 "New Web Service" 선택
2. **GitHub 저장소** 연결
3. **설정값 입력:**
   ```
   Name: naramarket-mcp-server
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: python start_render.py
   ```

### 3. 환경변수 설정
```
FASTMCP_TRANSPORT=http
FASTMCP_HOST=0.0.0.0
NARAMARKET_SERVICE_KEY=your_api_key_here
```

### 4. 접속 확인
- `https://your-app.onrender.com/health`

## 🐳 Docker 배포

### 1. Docker 이미지 빌드
```bash
# 프로덕션 이미지 빌드
docker build -t naramarket-mcp:prod .

# 컨테이너 실행
docker run -d \
  -p 8080:8080 \
  -e NARAMARKET_SERVICE_KEY=your_key \
  -e FASTMCP_TRANSPORT=http \
  -e PORT=8080 \
  naramarket-mcp:prod
```

### 2. Docker Compose 사용
```yaml
# docker-compose.yml
version: '3.8'
services:
  naramarket-mcp:
    build: .
    ports:
      - "8080:8080"
    environment:
      - NARAMARKET_SERVICE_KEY=your_key
      - FASTMCP_TRANSPORT=http
      - PORT=8080
    restart: unless-stopped
```

## 🚄 Railway 배포

### 1. Railway CLI 사용
```bash
# Railway CLI 설치
npm install -g @railway/cli

# 로그인 및 배포
railway login
railway init
railway up
```

### 2. 환경변수 설정
```bash
railway variables set NARAMARKET_SERVICE_KEY=your_key
railway variables set FASTMCP_TRANSPORT=http
```

## 🎯 Heroku 배포

### 1. Procfile 생성
```
web: python start_render.py
```

### 2. Heroku CLI로 배포
```bash
# Heroku 앱 생성
heroku create your-app-name

# 환경변수 설정
heroku config:set NARAMARKET_SERVICE_KEY=your_key
heroku config:set FASTMCP_TRANSPORT=http

# 배포
git push heroku main
```

## 🔐 환경변수 설정

모든 배포에서 다음 환경변수가 필요합니다:

### 필수 환경변수
```env
NARAMARKET_SERVICE_KEY=your_api_key_here
FASTMCP_TRANSPORT=http
FASTMCP_HOST=0.0.0.0
```

### 선택적 환경변수
```env
PORT=8080                    # 포트 번호 (플랫폼에서 자동 설정)
LOG_LEVEL=INFO              # 로그 레벨
CORS_ORIGINS=*              # CORS 허용 도메인
```

## 🧪 배포 후 테스트

### 1. Health Check
```bash
curl https://your-domain.com/health
```

**예상 응답:**
```json
{
  "status": "healthy",
  "server": "naramarket-fastmcp-2",
  "version": "2.0.0",
  "transport": "HTTP",
  "available_tools": 15
}
```

### 2. API 테스트
```bash
curl -X POST https://your-domain.com/api \
  -H "Content-Type: application/json" \
  -d '{
    "method": "tools/call",
    "params": {
      "name": "server_info",
      "arguments": {}
    }
  }'
```

### 3. MCP 프로토콜 테스트
```bash
curl -X POST https://your-domain.com/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/list",
    "params": {}
  }'
```

## 🚨 문제 해결

### 일반적인 오류들

#### 1. "Module not found" 오류
**원인:** Python 경로 설정 문제
**해결:** `sys.path.insert(0, "src")` 확인

#### 2. "API key not found" 오류
**원인:** 환경변수 설정 누락
**해결:** 플랫폼 대시보드에서 `NARAMARKET_SERVICE_KEY` 설정

#### 3. "Port binding failed" 오류
**원인:** 포트 설정 문제
**해결:** `PORT` 환경변수를 플랫폼 기본값으로 설정

#### 4. CORS 오류
**원인:** 브라우저에서 접근 시 CORS 설정 문제
**해결:** 이미 설정되어 있음, 캐시 삭제 후 재시도

### 로그 확인 방법

#### Vercel
```bash
vercel logs
```

#### Render
- 대시보드 → Logs 탭

#### Railway
```bash
railway logs
```

#### Heroku
```bash
heroku logs --tail
```

## 📊 성능 최적화

### 1. 메모리 사용량 최적화
- `num_rows` 기본값을 5로 설정 (이미 적용됨)
- 불필요한 의존성 제거

### 2. 응답 시간 최적화
- API 호출 타임아웃 설정
- 캐싱 구현 (필요시)

### 3. 비용 최적화
- **Vercel**: 서버리스로 사용량 기반 과금
- **Render**: 무료 플랜으로 시작 (월 750시간)
- **Railway**: $5/월 플랜 권장

## 🎉 배포 완료!

배포가 완료되면 다음과 같이 사용할 수 있습니다:

1. **웹 브라우저**에서 직접 테스트
2. **Claude Desktop**에서 MCP 서버로 연결
3. **API 클라이언트**에서 REST API로 호출
4. **다른 AI 도구**에서 MCP 프로토콜로 연결

---

**문의사항이나 배포 중 문제가 발생하면 이슈를 등록해주세요!** 🙋‍♂️
