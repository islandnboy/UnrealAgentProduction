# Context Budget Policy

Agent의 Context는 많이 읽는 것이 아니라 **현재 결정을 내리는 데 필요한 근거만 읽는 것**을 기본으로 한다. 이 정책은 Codex/CLI의 Repository 탐색, Prompt Compilation, Tool/MCP discovery와 후속 요청에 공통 적용한다. 실행 코드의 강제 구현은 `Tools/AgentPipeline/Scripts/ContextRouter.mjs`가 담당한다.

## 핵심 원칙: Resolve, then Expand

```text
Intent
  → Execution Mode
  → Domain / Stage
  → Initial Context Scope
  → Focused Inspection
  → Evidence sufficient? ─ yes → STOP
                       └─ no  → expand one scope → inspect → STOP/expand
```

저장소 전체를 먼저 읽고 관련성을 판단하지 않는다. 먼저 요청을 분류하고, 그 분류 결과로 읽을 범위를 결정한다.

## Context Scope

초기 Scope는 다음 정보만으로 결정한다.

1. 현재 사용자 Intent와 명시된 대상/경로
2. `/PRODUCTION`, `/FRAMEWORK`, `/FRIDAY_GOD`, `/PLAN`, `/RESEARCH` Execution Mode
3. Production인 경우 Flow·Domain·Stage
4. 해당 Domain의 Skill/Guideline과 `prompt-domains.json` inspection area
5. 후속 요청인 경우 이전 Trace의 검증된 Context Scope

`/FRAMEWORK` 작업은 게임 Content를 기본 Scope에 포함하지 않는다. Production 작업도 관련 없는 Domain의 Skill, Source, Content, MCP Tool을 선행 로딩하지 않는다.

## 탐색 규칙

- `git status` 같은 전역 상태는 작업 시작 시 한 번 확인하고 상태 변화가 예상될 때만 다시 읽는다.
- 디렉터리 전체 출력보다 이름/키워드 검색으로 후보를 좁힌 뒤 필요한 파일만 읽는다.
- 대형 디렉터리는 무제한 재귀 스캔하지 않는다. ContextRouter의 area/file budget을 따른다.
- Registry와 MCP discovery는 실제 Capability 판단이 필요한 시점에만 읽는다.
- 같은 파일·Registry·로그를 같은 단계에서 반복해서 읽지 않는다. 이미 확보한 Evidence와 Trace를 재사용한다.
- 빌드·테스트·터미널 출력은 성공 시 요약을 우선하고, 실패 시 원인 판정에 필요한 구간만 Context에 유지한다.
- 독립적인 read-only 조사는 가능한 경우 한 planning cycle에서 묶고, 결과만 통합한다.

## Stop Rule

다음 조건이 충족되면 Repository 탐색을 중단한다.

- 요청 대상과 기존 구현/재사용 후보를 판단할 Evidence가 확보됨
- 필요한 Skill/Guideline과 Capability 경계가 결정됨
- Blocking Ambiguity가 없거나 안전한 기본값으로 해결 가능함
- 다음 실행/검증 단계가 결정됨

더 읽으면 결론이 달라질 구체적인 이유가 없는 상태에서 '혹시 모르니' 탐색을 계속하지 않는다.

## Expansion Rule

Evidence가 부족할 때만 Scope를 확장한다. 확장은 한 번에 하나의 다음 우선순위 영역을 추가하고 다음을 Trace에 남긴다.

- `selectedAreas` / `deferredAreas`
- `expansionRound`
- `expansionReason`
- `evidenceCount`
- `stopReason`

확장 예산을 소진했는데도 근거가 부족하면 저장소 전체 스캔으로 자동 전환하지 않는다. 필요한 결정 또는 추가 입력을 명시한다.

## Follow-up Context Reuse

후속 요청은 이전 Trace의 Domain과 검증된 Context Scope를 우선 유지한다. 사용자가 바꾼 차원만 다시 해석하고 영향 범위만 재조사한다.

예: '현재 레벨 강조를 더 세게'는 UI 전체, Content 전체, MCP Registry 전체를 처음부터 다시 읽는 요청이 아니다. 기존 UI Context에서 Style/State 관련 범위만 보정한다.

## Instruction Loading

`AGENTS.md`는 진입 계약만 유지하고 상세 규칙은 이 문서와 Domain Skill에 둔다. 모든 Skill/Guide를 선행 로딩하지 않는다. Mode·Domain·Stage에서 선택된 문서만 읽고, 연결된 세부 reference는 실제 결정에 필요할 때 연다.

## Tool / MCP Context

Tool 이름을 전부 Context에 넣지 않는다. 필요한 Capability를 먼저 결정한 뒤 Registry/Discovery에서 후보 Tool만 선택한다. `/RESEARCH`나 `/PLAN`처럼 mutation이 없는 작업은 실행 Capability가 필요하지 않으면 MCP discovery를 생략할 수 있다.

## Sub-agent / Parallel Work

Sub-agent가 필요한 경우 부모의 전체 대화·탐색 history를 복제하는 것을 기본값으로 삼지 않는다. 독립 작업에는 목표, 허용 Scope, 필요한 계약, 산출 형식만 전달하고 결과 요약을 부모 Context로 반환한다. 단순 작업에는 sub-agent를 만들지 않는다.

## 금지 패턴

- 작업 시작마다 `AI/`, `Docs/`, `Client/Source/`, `Client/Content/` 전체를 읽기
- 관련성 확인 전 대형 빌드 로그/디렉터리 트리를 그대로 Context에 적재
- 후속 요청마다 전체 Prompt Compilation Context를 처음부터 재구축
- 동일 Registry/파일/명령 출력을 이유 없이 반복 조회
- Evidence가 충분한데도 탐색을 계속하는 것
- Context 부족을 이유로 무제한 Scope 확장

## 구현 계약

`ContextRouter.mjs`와 `PromptCompiler.mjs`는 이 정책의 기계적 강제 계층이다. 문서와 코드의 기본값이 다르면 더 좁은 Scope를 우선하되, Validation에 필요한 Evidence가 사라지지 않도록 테스트로 조정한다. 정책 변경 시 `ContextRouter.Tests.mjs`, `PromptCompiler.Tests.mjs`, `AgentPipeline.Tests.mjs`를 함께 검증한다.
