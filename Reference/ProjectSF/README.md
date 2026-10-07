# ProjectSF current workflow snapshot

이 디렉터리는 비공개 working repository인 ProjectSF의 **현재 Agent Production 구조를 포트폴리오용으로 선별 정리한 Snapshot**입니다.

전체 게임 코드, 콘텐츠, Issue, Production Data/Evidence는 공개하지 않습니다.

## Current source structure

~~~text
AGENTS.md
.agents/skills/
AI/
├─ Workflows/
├─ Rules/
└─ Skills/

Docs/
├─ Project/
├─ Design/
├─ Technical/
├─ Production/
└─ Development/

Tools/AgentPipeline/
├─ Config/
├─ Registry/
├─ Schemas/
├─ Scripts/
├─ Templates/
├─ Examples/
└─ Tests/

Production/
├─ Data/
└─ Evidence/
~~~

## Included here

- [Structure](Structure.md)
- [Current Context Budget Policy](ContextBudgetPolicy.md)
- [Current Execution Observability](ExecutionObservability.md)
- [UI production Skill snapshot](Skills/ui-production/SKILL.md)
- [Road production Skill snapshot](Skills/road-production/SKILL.md)

포트폴리오 설명은 상위 `Docs/`가 담당하고, 이 폴더는 실제 ProjectSF 구조가 어떤 형태로 운영되는지 확인하기 위한 선택적 Snapshot입니다.
