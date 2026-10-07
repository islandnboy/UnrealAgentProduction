# Context Budget Policy

요청과 현재 Step의 미해결 질문에 따라 필요한 근거를 찾아간다.

1. Issue/자연어에서 Goal, Scope, Acceptance, 기존 결정과 남은 문제를 확인한다.
2. 관련 Docs, 영역별 AGENTS, 선택한 Skill을 읽는다. 저장소 전체를 먼저 순회하지 않는다.
3. 실제 질문에 답하는 코드·계약·관측을 확보하면 해당 탐색을 멈춘다.
4. 근거 부족, 충돌, 입력 변경이 있으면 범위를 확장한다. 파일 수나 검색 결과 수만으로 충분성을 판정하지 않는다.
5. 후속 Step에서 유효한 근거를 재사용하되 최신 Issue/commit/입력 변경을 확인한다.

LLM Context에 큰 데이터셋과 전체 로그를 넣지 않는다. 관련 실패 위치·집계·검증 결과를 사용한다. 기술 구현과 데이터 변환은 승인된 결정론적 도구를 사용한다.

## Issue Working Set

Active Issue를 재개할 때는 이번 Step의 `Goal`, `Scope`, `Acceptance`, `Current State`, `Next Step`과 이전 Step 이후의 변경만 Working Set으로 복구한다. 과거 설계 전문, 종료된 체크리스트, 원시 Tool 출력, 전체 comment 이력은 현재 미해결 질문을 해결할 때만 읽는다.

단, 기존 결과의 재생성·개선·이관 또는 과거 결과 비교에서는 과거 기준선 자체가 현재 질문이다. 이 경우 관련 commit, 당시 validation/evidence를 필요한 범위에서 읽고 Baseline Contract를 확정한 뒤 Context를 다시 축소한다.

## Sub Agent Context

Main은 전체 대화 이력 대신 위임 작업에 필요한 Goal/Scope/Acceptance, Parent Step, 입력 identity/revision, 대상 경로, 필수 지침·참조, 기존 사용자 변경, 검증 방법과 반환 조건을 전달한다.

Sub는 자신에게 적용되는 지침을 직접 읽고 필요한 근거만 확장한다.

## Evidence reuse

- 재사용 단위는 결론과 짧은 근거 참조다.
- 입력·규칙·대상·Owner decision이 바뀌면 영향받는 결론만 다시 검증한다.
- Tool 의미 설명은 재사용할 수 있지만 live session과 mutation 권한은 캐시하지 않는다.
- 압축 후에도 Goal/Acceptance/승인 경계, 현재 input/output identity, PASS와 stale 조건, 다음 행동은 보존한다.
- 큰 Tool 목록은 compact discovery를 사용하고 선택한 Tool만 상세 schema를 확인한다.
