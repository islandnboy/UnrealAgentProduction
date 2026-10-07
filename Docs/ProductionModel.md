# Production Model

## Human + AI shared production

ProjectSF에서는 사람과 AI를 서로 다른 제작 파이프라인으로 분리하지 않습니다.

사람이 Unreal Editor에서 직접 수정한 결과도 정상 Production이며, 다음 Agent는 이를 기존 입력으로 관측하고 보호합니다.

~~~text
Approved Input
→ Human or AI Production
→ Saved Product State
→ Evidence
→ Human or AI continues
~~~

## Data / Recipe / Tool / Evidence

### Production Data

`Production/Data`는 현재 제작이 실제 사용하는 승인 입력을 소유합니다.

예:

- authored parameters
- canonical source references
- production rules
- source identity / revision

### Recipe

Recipe는 반복 검증된 **제작 계약**입니다.

Recipe는 특정 작업의 로그가 아니며 다음을 설명합니다.

- expected input
- reusable procedure
- required representation
- validation
- regeneration boundary

한 번 성공한 즉흥 절차를 바로 Recipe로 승격하지 않습니다.

### Tool

반복 실행은 deterministic Tool 또는 Unreal MCP capability가 담당합니다.

AI는 방법을 판단하고, 반복 가능한 기계적 실행은 Tool에 넘깁니다.

### Evidence

`Production/Evidence`는 실행 결과의 관측 가능한 근거를 보관합니다.

- manifest
- measurements
- validation
- screenshots / preview references
- input revision
- tool / parameter provenance

Goal과 Current State를 Evidence 폴더에 복제하지 않습니다. 업무 상태는 Issue가 소유합니다.

## Progressive convergence

제품 제작은 가능한 한 연결된 전체를 유지하며 반복 개선합니다.

~~~text
Goal
→ Make
→ Observe
→ Evaluate
→ Refine
→ next Cycle
~~~

매 Cycle마다 새 Issue, 새 문서, 새 framework를 만드는 것이 목표가 아닙니다.

## ProductionEvolution

실제 제작 중 다음 문제가 발견될 수 있습니다.

- Tool capability gap
- Recipe가 현재 대상에 맞지 않음
- 검증 수단 부족
- Skill 책임 경계가 잘못됨
- 반복 작업인데 수작업이 과도함

이때 Production을 포기하거나 임시 우회로를 고착시키지 않고 필요한 제작 기반을 최소 범위에서 개선한 뒤 원래 Step으로 복귀합니다.

## Promotion rule

반복 제작을 시스템화하는 기준은 “두 번 나왔다” 같은 횟수 자체가 아닙니다.

다음이 확인되어야 합니다.

- 실제 반복 비용이 존재함
- 입력과 결과 계약을 분리할 수 있음
- 재사용 시 품질이 유지됨
- 검증 방법이 존재함
- 특정 Goal 고유 값이 공용 규칙에 섞이지 않음

그 후 Skill / Tool / Recipe / Test 중 적절한 계층으로 승격합니다.
