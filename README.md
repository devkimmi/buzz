# Sheet Music Transformer

MusicXML 악보를 업로드하면 난이도를 조절해주는 웹 앱.

## 기술 스택

| 영역 | 기술 |
|------|------|
| 백엔드 | Python 3.12 + FastAPI |
| LLM | Google Gemini 2.5 Flash |
| 프론트엔드 | React + Vite (TypeScript) |
| 악보 렌더링 | OpenSheetMusicDisplay (OSMD) |
| 재생 | osmd-audio-player |

## 시작하기

### 사전 요구사항
- Python 3.12 (pyenv 권장)
- Node.js 18+
- Google AI Studio API 키 (aistudio.google.com)

### 백엔드 설정

```bash
# 가상환경 활성화
source .venv/bin/activate

# 패키지 설치
pip install -r backend/requirements.txt

# 환경변수 설정
cp backend/.env.example backend/.env
# backend/.env 에 GOOGLE_API_KEY 입력

# 서버 실행
cd backend
uvicorn app.main:app --reload
```

백엔드: http://localhost:8000

### 프론트엔드 설정

```bash
cd frontend
npm install
npm run dev
```

프론트엔드: http://localhost:5173

## 사용법

1. MusicXML 파일 업로드 (`.xml`, `.musicxml`)
2. 난이도 선택 (쉽게 / 어렵게)
3. 변환하기 클릭
4. 원본과 변환 결과 악보 비교, 재생으로 확인

## 프로젝트 구조

```
buzz/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI 앱
│   │   ├── api/routes/
│   │   │   └── transform.py     # POST /api/transform
│   │   ├── services/
│   │   │   ├── llm.py           # Gemini API 변환 로직
│   │   │   └── musicxml.py      # MusicXML 검증
│   │   └── models/
│   │       └── transform.py     # Pydantic 모델
│   └── tests/
│       └── twinkle.xml          # 테스트용 샘플
├── frontend/
│   └── src/
│       ├── App.tsx              # 메인 UI
│       └── api.ts               # 백엔드 API 호출
└── PLAN.md                      # 개발 계획
```
