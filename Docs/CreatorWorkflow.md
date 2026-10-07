# Creator Workflow

이 문서는 **기획자 / 디자이너가 Agent Workflow를 실제 제작 도구로 사용하는 과정**을 설명합니다.

Creator는 특정 직군명이 아닙니다. 기획자, 프로그래머, 아티스트 누구든 현재 Goal을 정의하고 결과를 판단하는 사람이 Creator가 될 수 있습니다.

## The designer does not operate the framework

기획자가 알아야 하는 것은 Tool ID, MCP schema, Skill 이름이 아닙니다.

기획자는 다음을 전달합니다.

- 무엇을 만들고 싶은가
- 어디까지 바꿔도 되는가
- 무엇은 보존해야 하는가
- 어떤 상태를 완료로 볼 것인가
- 현재 결과에서 무엇이 마음에 들지 않는가

예:

~~~text
한강은 단순한 정적 수면이 아니라
빠졌을 때 하류로 떠내려가는 느낌이 있어야 한다.

러프 단계에서는 실제 유체 시뮬레이션까지 필요하지 않지만,
후속 Gameplay가 위치별 흐름 방향과 속도를 조회할 수 있어야 한다.
~~~

이 요구는 Agent가 현재 프로젝트 상태와 Production 계약에 맞게 실행 가능한 Step으로 해석합니다.

## Working loop

~~~text
1. 기획 의도
   ↓
2. Goal / Scope / Acceptance
   ↓
3. Issue / Recipe
   ↓
4. Codex Agent 실행
   ↓
5. Unreal 결과물 + Evidence
   ↓
6. 기획자 검수
   ├─ 승인
   ├─ 자연어 수정 지시
   └─ 직접 Editor 수정
   ↓
7. 다음 Agent가 현재 결과를 읽고 계속
~~~

## What the designer sees

Agent 내부의 모든 로그를 읽게 하지 않습니다.

기획자가 확인해야 할 핵심은 다음입니다.

### Before production

- Goal
- Scope
- protected content
- Acceptance
- 현재 선택된 제작 방향

### During production

- 현재 Step
- 적용된 전문 Skill
- 실제 실행한 Tool
- 현재 결과와 검증 상태
- 다음 행동

### After production

- Unreal에서 만들어진 실제 결과
- before / after
- 기술적으로 검증된 항목
- 아직 미검증인 항목
- 사람이 판단해야 하는 시각·경험 품질
- 다음 수정 지점

## Designer artifacts

기획자의 작업 역시 Production의 중요한 산출물입니다.

~~~text
Design Intent
├─ Issue
│  ├─ Goal
│  ├─ Scope
│  ├─ Requirements
│  └─ Acceptance
├─ Recipe, when reusable
├─ Review notes
├─ Owner decisions
└─ Result acceptance / correction
~~~

이 정보는 Agent용 Prompt에만 존재하지 않고 GitHub Issue와 Docs에 남습니다.

## Human edit is first-class production

기획자가 Unreal Editor에서 직접 값을 수정하는 것도 정상 작업입니다.

예:

- spline 위치 조정
- road width / lane parameter 수정
- Material 선택
- PCG parameter 조정
- water depth / shoreline 조정
- UI 위치·크기·레이아웃 수정

사람이 저장한 결과는 다음 Agent에게 단순한 “외부 변경”이 아니라 **현재 Production state**입니다.

~~~text
Agent result
→ Designer edits in Unreal
→ Save
→ Production state / Evidence
→ Next Agent observes current state
→ preserves or extends the edit
~~~

AI가 이전 generation을 무조건 다시 실행해 사람의 수정 내용을 지우는 방식은 피합니다.

## What belongs in a portfolio

Agent Workflow 포트폴리오에서는 다음 세 종류를 같이 보여주는 것이 중요합니다.

### 1. Intent

기획자가 실제로 어떤 요구를 했는지.

### 2. Process

Issue / Recipe / Agent Step / Unreal MCP가 어떻게 연결됐는지.

### 3. Result

Unreal 결과 화면, 구조적 결과, 검증 Evidence, 그리고 사람이 남긴 최종 판단.

즉 포트폴리오의 단위는 “Agent 기능”보다 다음 형태에 가깝습니다.

~~~text
Problem
→ Designer Intent
→ Production Contract
→ Agent Execution
→ Unreal Result
→ Validation
→ Human Review
→ Iteration
~~~

이 구조를 통해 기획자가 개발자의 구현 세부를 알지 않아도 실제 제작 Loop에 참여할 수 있다는 점을 보여줍니다.
