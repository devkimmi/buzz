# Sheet Music Transformer

음악 악보를 변환해주는 웹 앱.

## 최종 목표
MusicXML 악보를 업로드하면 난이도·톤·악기 등을 변환해서 새 악보를 돌려주는 반응형 웹 앱.

---

## 현재 단계: Phase 1 - E2E MVP

### 목표
MusicXML 업로드 → 난이도 조절 → 결과 악보 렌더링 + 재생

### 진행 상황
- [x] 1. 프로젝트 셋업 (백엔드 + 프론트엔드)
- [x] 2. MusicXML 업로드 및 파싱
- [x] 3. 난이도 조절 변환 (3단계 LLM 프롬프트)
- [x] 4. 결과 MusicXML 렌더링 (OSMD)
- [x] 5. MIDI 재생 (osmd-audio-player)
- [ ] 6. 변환 품질 개선 → **music21로 전환 예정** (아래 참고)

### 다음 작업
- [ ] music21로 변환 로직 재구현 (LLM 의존 제거)
- [ ] easier/harder 변환 품질 검증

---

## Phase 2 (예정)
- 조옮김, 악기 변환 등 변환 종류 확장
- 창의적 변환 (스타일 변경 등)에 LLM 재도입

## Phase 3 (예정)
- PDF / 이미지 입력 지원 (OMR)
- 다양한 출력 포맷

## Phase 4 (예정)
- 태블릿 UX 최적화
- 사용자 계정 / 악보 저장

---

## 기술 스택

| 영역 | 선택 | 이유 |
|------|------|------|
| 백엔드 | Python + FastAPI | |
| MusicXML 변환 | music21 | 정확한 음표 조작, LLM보다 신뢰도 높음 |
| LLM | Gemini 2.5 Flash | 창의적 판단에만 사용 (스타일 변환 등) |
| 프론트엔드 | React + Vite | |
| 악보 렌더링 | OpenSheetMusicDisplay (OSMD) | MusicXML 직접 렌더링 |
| 재생 | osmd-audio-player | OSMD와 통합 |

---

## 아키텍처 결정

### 변환 로직: music21 우선, LLM은 보조
```
현재 (문제): MusicXML → LLM → MusicXML
             (LLM이 XML 직접 생성 → grace note 오류, divisions 오계산 등)

개선 방향:
  easier/harder 등 규칙이 명확한 변환 → music21로 구현 (deterministic)
  "재즈 스타일로", "바로크 풍으로" 등 창의적 변환 → LLM이 규칙 결정 → music21이 적용
```

### LLM 역할 분리
- **music21**: 음표 쪼개기, 패싱톤 추가, 장식음 제거 등 구조적 변환
- **LLM**: "어떤 변환을 할지" 고수준 결정 (창의적 판단)
- MCP tool + LLM agent 구조는 창의적 변환 기능 추가 시 고려

---

## 핵심 결정 사항
- 입력: MusicXML (PDF는 Phase 3)
- 멜로디 검증: 사람이 직접 재생해서 귀로 확인
- 플랫폼: 반응형 웹 (네이티브 앱 없음)

---

## 메모 / 미결 사항
- osmd-audio-player가 grace note를 처리 못함 → LLM 후처리로 제거 중 (music21 전환 시 해결)
- OSMD 컨테이너 너비 이슈 → width: 100% 로 해결
- Gemini 2.5 Flash: 3단계 프롬프트로 변환 가능하나 멜로디 보존 품질 불안정
