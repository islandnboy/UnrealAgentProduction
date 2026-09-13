# Natural Language Prompt Compilation Workflow

사용자의 자연어는 최종 Tool 명령이나 Production Spec이 아니다. Agent는 현재 Production Context 안에서 Intent를 해석하고 저장소 근거, Skill, Guideline과 검증 조건을 결합한 Compiled Execution Prompt를 만든 뒤에만 실행한다.

```text
Natural Language
  → Intent Interpretation
  → Execution Mode / Agent Role Resolution
  → Context Scope Resolution
  → Focused Repository Inspection
  → Production Framework Routing (Production Mode only)
  → Flow → Domain → Stage
  → Skill Binding
  → Guideline Resolution
  → Prompt Compilation
  → Execution Plan
  → Tool / MCP Execution
  → Intent-based Validation
  → Focused Correction
```

## 강제 순서

1. `git status`는 1회 확인하고 `ContextBudgetPolicy.md`에 따라 Mode·Domain·Stage·Intent에서 초기 Context Scope를 결정한다.
2. 선택된 Scope 안에서만 관련 코드, Asset 이름, 공용 Framework, 기존 구현을 읽기 전용으로 조사한다. Evidence가 충분하면 즉시 중단하고 부족할 때만 Expansion Reason을 기록한 뒤 다음 범위를 연다.
3. `/PRODUCTION`, `/FRAMEWORK`, `/FRIDAY_GOD`, `/PLAN`, `/RESEARCH` Mode와 Agent 역할을 판정한다.
4. `/PRODUCTION`이면 Production Framework의 Flow·Domain·Stage를 결정한다.
5. Stage·Specialty·Intent에 맞는 Skill과 연결 Guideline을 읽는다.
6. 실행이 필요한 경우 Registry와 실제 MCP discovery에서 Tool 상태와 Capability를 대조한다.
7. 모르는 값은 Repository → Guideline → Skill → 기존 Pattern → 안전한 기본값 순으로 해결한다.
8. 결과를 바꾸는 Blocking Ambiguity만 사용자에게 질문한다.
9. 근거, 가정, Mode·역할 경계, 실행 계획과 Validation Contract를 포함한 Prompt를 컴파일한다.
10. Production Agent는 제품 작업만, Framework Agent는 플랫폼 작업만 수행한다.
11. 실행 Mode별 승인·Preflight·Dry Run Gate를 적용한다.
12. 생성 여부가 아니라 원래 Intent의 관찰 가능한 완료 조건으로 검증한다.
13. 실패 시 Handoff의 Revision Target 또는 Framework 요청으로 해당 부분만 보정한다.

Focused Repository Inspection 없이 Asset 생성이나 Tool mutation을 시작하면 Workflow 실패다. Repository Inspection은 저장소 전체 스캔을 뜻하지 않으며, 선택된 Context Scope 밖의 탐색은 명시적인 확장 근거 없이 수행하지 않는다.

## 논리적 역할

- Intent Interpreter: 목적, 필수·금지 요소와 완료 기준을 해석한다.
- Mode Router: Execution Mode와 Framework/Production Agent 경계를 결정한다.
- Context Resolver: Mode·Domain·Stage·Intent에서 Context Scope를 결정하고, 선택된 범위의 현재 변경사항·기존 구현·재사용 후보·Architecture 근거만 수집한다. Evidence가 부족할 때만 범위를 확장한다.
- Production Framework Router: Production Mode의 Flow·Domain·Stage와 Dependency를 결정한다.
- Skill Resolver: Domain Skill과 그 Skill이 요구하는 Guideline을 선택한다.
- Prompt Compiler: 수집한 근거를 실행 가능한 작업 지시서와 Validation Contract로 결합한다.
- Execution Agent: Compiled Prompt와 분리된 Job Plan을 따라 Tool/MCP를 실행한다.
- Validator: 기술 성공과 사용자 Intent 충족을 각각 판정한다.

## Trace와 대화형 보정

Trace는 최소한 Original User Intent, Resolved Domain, Context Scope, Selected/Deferred Areas, Expansion Reason/Round, Stop Reason, Selected Skills, Loaded Guidelines, Inspected Repository Areas, Existing Patterns, Reuse Candidates, Assumptions, Blocking Ambiguities, Compiled Prompt, Execution Result, Validation Result를 기록한다.

후속 요청은 기존 Trace의 `effectiveUserIntent`, Domain과 Repository Context를 유지한 채 추가 요구사항을 합친다. 변경된 부분을 다시 조사·컴파일하고 영향 범위만 실행한다.

## 표준 명령

```powershell
node Tools/AgentPipeline/Scripts/AgentPipeline.mjs compile-request --request "보상 리스트 만들어줘."
node Tools/AgentPipeline/Scripts/AgentPipeline.mjs route-request --request "레벨업 보상 UI 만들어줘."
node Tools/AgentPipeline/Scripts/AgentPipeline.mjs run-request --request-file Tools/AgentPipeline/Tests/Fixtures/PromptCompilation/UILevelRewardRequest.txt
node Tools/AgentPipeline/Scripts/AgentPipeline.mjs compile-request --request "현재 레벨을 더 강조해줘." --context Production/Jobs/Local/Current/trace.json
```

`compile-request`는 read-only다. `run-request`도 compile, discovery, preflight까지만 자동 진행하며 실제 Unreal mutation은 기존 dry-run과 승인 이후 Execution Agent가 수행한다.
