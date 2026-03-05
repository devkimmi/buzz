# Sheet Music Transformer

음악 악보를 LLM으로 변환해주는 웹 앱.

## 최종 목표
MusicXML 악보를 업로드하면 LLM이 난이도·톤·악기 등을 변환해서 새 악보를 돌려주는 반응형 웹 앱.

---

## 현재 단계: Phase 1 - E2E MVP

### 목표
MusicXML 업로드 → 난이도 조절(쉽게) → 결과 악보 렌더링 + 재생

### 진행 상황
- [ ] 1. 프로젝트 셋업 (백엔드 + 프론트엔드)
- [ ] 2. MusicXML 업로드 및 파싱
- [ ] 3. LLM으로 난이도 조절 변환
- [ ] 4. 결과 MusicXML 렌더링 (악보로 표시)
- [ ] 5. MIDI 재생 (귀로 검증)
- [ ] 6. E2E 테스트 통과

---

## Phase 2 (예정)
- 난이도 올리기, 조옮김, 악기 변환 등 변환 종류 확장
- 변환 품질 개선

## Phase 3 (예정)
- PDF / 이미지 입력 지원 (OMR)
- 다양한 출력 포맷

## Phase 4 (예정)
- 태블릿 UX 최적화
- 사용자 계정 / 악보 저장

---

## 기술 스택 (가정, 변경 가능)

| 영역 | 선택 | 이유 |
|------|------|------|
| 백엔드 | Python + FastAPI | music21 라이브러리 활용 |
| MusicXML 처리 | music21 | 파싱, 검증, MIDI 변환 |
| LLM | Claude API | MusicXML은 XML 텍스트라 직접 처리 가능 |
| 프론트엔드 | React + Vite | 심플, FastAPI와 역할 분리 명확 |
| 악보 렌더링 | OpenSheetMusicDisplay (OSMD) | MusicXML 직접 렌더링 |
| MIDI 재생 | MIDI.js or Tone.js | 브라우저 내 재생 |

---

## 핵심 결정 사항
- 입력: MusicXML (PDF는 Phase 3)
- 첫 변환: 난이도 조절 (쉽게 만들기)
- 멜로디 검증: 사람이 직접 재생해서 귀로 확인
- 플랫폼: 반응형 웹 (네이티브 앱 없음)

---

## 메모 / 미결 사항
- LLM에게 MusicXML 전체를 넘길지 vs 파싱 후 구조화된 데이터를 넘길지 → 실험 필요
- "난이도 쉽게"의 정의 명확화 필요 (리듬 단순화? 음표 수 감소? 장식음 제거?)
