# ProjectSF Structure

## Entry

~~~text
AGENTS.md
└─ resolves Workflow / Rule / Skill / Recipe before mutation
~~~

## Agent behavior

~~~text
AI/
├─ Workflows/
│  ├─ CommonAIWorkflow.md
│  ├─ ContextBudgetPolicy.md
│  ├─ ExecutionObservability.md
│  ├─ ProductionConvergence.md
│  ├─ ProductionEvolution.md
│  └─ TaskExecution.md
├─ Rules/
│  ├─ Programming.md
│  ├─ ResourceProduction.md
│  └─ VerificationDepth.md
└─ Skills/
   ├─ issue-context-sync/
   ├─ terrain-production/
   ├─ landscape-production/
   ├─ road-production/
   ├─ water-terrain-preparation/
   ├─ water-production/
   ├─ world-structure/
   ├─ world-validation/
   ├─ ui-production/
   ├─ ui-architecture/
   ├─ server-feature-production/
   └─ server-bot-verification/
~~~

## Runtime

~~~text
Tools/AgentPipeline/
├─ Config/
├─ Registry/
├─ Schemas/
├─ Scripts/
├─ Templates/
├─ Examples/
├─ Tests/
└─ Runtime.md
~~~

Runtime은 자연어 의미를 소유하지 않습니다.  
Agent가 선택한 Workflow / Step / capability를 구조적으로 검증하고 실제 실행을 지원합니다.

## Production state

~~~text
Production/
├─ Data/
└─ Evidence/
~~~

- Data: 승인된 입력
- Evidence: 실행·검증 근거
- Issue: Goal / Acceptance / current state
- Docs: 장기 제품·기술·제작 계약

## Codex skill discovery

~~~text
.agents/skills/<skill-name>/SKILL.md
            ↓ thin entrypoint
AI/Skills/<skill-name>/SKILL.md
            ↓ source of truth
~~~

Skill의 실제 절차를 두 위치에 복제하지 않는 것이 원칙입니다.
