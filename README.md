# CitizenParticipation

현재 제공된 정적 HTML을 유지하면서 다음 구조로 배포할 수 있도록 정리한 프로젝트입니다.

- `frontend/`: Vercel에 올릴 정적 사이트
- `backend/`: Render에 배포할 FastAPI API

## 로컬 실행

### 1. 백엔드

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

기본 API 주소는 `http://127.0.0.1:8000` 입니다.
환경변수는 `backend/.env.example`을 참고하면 됩니다.

### 2. 프론트엔드

정적 파일이므로 `frontend/index.html`을 직접 열거나 정적 서버로 실행하면 됩니다.

## 실제 배포 순서

1. GitHub에 새 리포지토리를 만들고 이 프로젝트를 push 합니다.
2. Render에서 PostgreSQL을 생성합니다.
3. Render에서 저장소 루트의 [`render.yaml`](/c:/Users/heedou/.vscode/dualbrain/CitizenParticipation/render.yaml) 기준으로 웹 서비스를 배포합니다.
4. 배포가 끝나면 Render 백엔드 URL을 확인합니다.
5. `frontend/config.js`의 `API_BASE_URL`을 Render URL로 변경합니다.
6. Render의 `FRONTEND_ORIGIN` 환경변수도 실제 Vercel 도메인으로 바꿉니다.
7. Vercel에서 `frontend/`를 배포합니다.
8. 폼 제출 후 Render DB에 데이터가 저장되는지 확인합니다.

## GitHub 연결

이 폴더는 이미 로컬 Git 저장소로 초기화되어 있습니다. GitHub에서 빈 저장소를 만든 뒤 아래처럼 연결하면 됩니다.

```bash
git remote add origin <YOUR_GITHUB_REPO_URL>
git add .
git commit -m "Initial deployment-ready structure"
git push -u origin main
```

## 주요 API

- `GET /health`
- `POST /api/applications`

## Email Delivery

Application submissions are stored in the database and then emailed to the administrator from the backend.

Set these environment variables before using the apply form:

- `SMTP_HOST`
- `SMTP_PORT`
- `SMTP_USERNAME`
- `SMTP_PASSWORD`
- `SMTP_USE_TLS`
- `MAIL_FROM`
- `ADMIN_EMAIL`

For Gmail, use an App Password rather than your normal account password.
