# Architecture

현재 Unreal Agent Production의 구조는 ProjectSF에서 실제 운영 중인 Agent Workflow를 기준으로 합니다.

## 1. Repository entry

모든 실제 작업은 저장소 루트의 `AGENTS.md`에서 시작합니다.

`AGENTS.md`는 거대한 정책 문서가 아니라 다음 역할만 가집니다.

- Repository identity
- mandatory bootstrap gate
- Workflow / Rule / Skill routing
- 하위 영역별 지침 연결
- mutation 이전에 확인해야 할 최소 실행 문맥

~~~text
AGENTS.md
  ↓
AI/Workflows
AI/Rules
AI/Skills
Docs/Production/Recipes
  ↓
Tools/AgentPipeline
  ↓
Production/Data + Production/Evidence
~~~

Codex의 repository Skill 자동 발견을 위해 `.agents/skills/<name>/SKILL.md`를 얇은 entrypoint로 두고, 실제 Skill 원본은 `AI/Skills/<name>/SKILL.md`가 소유합니다.

## 2. Responsibility boundaries

| Layer | Owns | Does not own |
| --- | --- | --- |
| `AGENTS.md` | bootstrap, routing | 제품 설계, 도구 구현 |
| `AI/Workflows` | 실행 상태, 재개, Step 전환, 완료 판정 | 제품 고유 규칙 |
| `AI/Rules` | 공통 안전·품질 불변 조건 | 특정 작업 계획 |
| `AI/Skills` | 전문 판단, 입력 확인, 검증 방법 | 실제 프로젝트 class/path 복제 |
| `Docs/Production/Recipes` | 반복 가능한 제작 계약 | 매 실행의 상태 |
| `Tools/AgentPipeline` | schema, registry, binding, preflight, evidence tooling | 자연어 의미 판단 |
| `Production/Data` | 승인된 제작 입력 | workflow policy |
| `Production/Evidence` | 실행 및 검증 증거 | Goal / task state |
| GitHub Issue | Goal, Scope, Acceptance, current state, decisions | raw logs |
| `Docs` | 제품·기술·제작 설계 | Agent runtime state |

## 3. Agent vs Runtime

이 구조에서 가장 중요한 경계입니다.

### Agent

Agent가 판단합니다.

- 요청의 실제 의도
- 현재 Workflow와 Step
- 필요한 Rule / Skill / Recipe
- 미해결 질문
- 요구 capability
- 다음 행동
- Goal Acceptance 충족 여부

### AgentPipeline Runtime

Runtime은 Agent 판단을 실행 가능한 형태로 검증합니다.

- schema validation
- capability / tool binding
- registry lookup
- preflight
- deterministic scripts
- execution support
- evidence / manifest handling
- regression tests

과거의 keyword 기반 Prompt Compiler가 자연어 의미를 대신 판단하는 구조는 현재 모델의 중심이 아닙니다.

## 4. Current workflow set

### CommonAIWorkflow

공통 실행 계약의 단일 원본입니다.

- bootstrap
- current source of truth
- Issue restore / resume
- authority boundary
- Step transition
- Main / Sub delegation
- task outcome

### TaskExecution

조사, 설계, 진단, 수정처럼 일반적인 작업을 수행합니다.

### ProductionConvergence

연결된 제품 결과를 대상으로 반복 제작합니다.

~~~text
Make
→ Observe
→ Evaluate
→ Refine
→ re-evaluate Goal
~~~

### ProductionEvolution

Production 중 드러난 제작 기반 결함을 해결합니다.

예:

- 필요한 reusable Tool 부재
- Recipe 문제
- Skill 경계 문제
- validation path 부족

개선 후 원래 Production Step으로 복귀하는 것이 핵심입니다.

### ExecutionObservability

작업자가 현재 Agent의 선택과 실행 상태를 확인할 수 있도록 화면 Trace를 정의합니다.

## 5. Current Skill model

Skill은 직군 분업 단위가 아니라 **반복 가능한 전문 판단 단위**입니다.

ProjectSF의 현재 예:

- issue-context-sync
- terrain-production
- landscape-production
- road-production
- water-terrain-preparation
- water-production
- world-structure
- world-validation
- ui-production
- ui-architecture
- server-feature-production
- server-bot-verification

하나의 Goal은 여러 Skill을 Step별로 조합할 수 있습니다.

## 6. Persistent context

대화 기억을 장기 상태 저장소로 사용하지 않습니다.

~~~text
GitHub Issue
  ├─ Goal / Scope / Acceptance
  ├─ decisions
  ├─ current state
  └─ next action

Production/Evidence
  ├─ manifest
  ├─ measurements
  ├─ validation
  └─ artifact references
~~~

이 구조 덕분에 GPT, Codex, 다른 세션, 다른 작업자가 동일 Issue와 실제 저장소 상태를 읽고 재개할 수 있습니다.
