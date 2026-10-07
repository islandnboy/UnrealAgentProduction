# Execution Model

## 1. Mandatory bootstrap gate

실제 조사·진단·변경·제작 작업은 mutation 전에 실행 문맥을 먼저 확정합니다.

최소 문맥:

- Workflow
- Step
- Skill
- Recipe, if applicable
- Goal
- Acceptance
- Planned Evidence

필수 지침을 읽기 전에 구현을 먼저 시작하고 나중에 정당화하는 방식은 허용하지 않습니다.

## 2. Current Source of Truth Gate

Issue 작업의 기준은 이전 세션이 아니라 **현재 시점의 실제 상태**입니다.

~~~text
Repository
+ Issue
+ Workflow
= Current Source of Truth
~~~

확인 범위는 작업에 필요한 만큼만 확장합니다.

### Repository

- branch / HEAD
- dirty diff
- 대상 구현과 입력
- 관련 Evidence
- 필요한 경우 실제 Unreal Editor 저장 상태

### Issue

- Goal
- Scope
- Acceptance
- 최신 Owner decision
- current state
- relevant recent evidence

### Workflow

- 현재 checkout의 `AGENTS.md`
- 적용 Workflow / Rule / Skill / Recipe

이전 대화와 handoff는 위치를 찾는 참고 자료일 뿐, 현재 계약을 대체하지 않습니다.

## 3. Resolve then expand

Repository 전체를 먼저 읽지 않습니다.

1. 현재 Step의 질문을 정의합니다.
2. 해당 질문에 필요한 문서와 코드를 읽습니다.
3. 근거가 확보되면 탐색을 멈춥니다.
4. 충돌이나 근거 부족이 있을 때만 확장합니다.
5. 유효한 결과는 revision / identity와 함께 재사용합니다.

이 방식은 단순 token 절약이 아니라 **판단에 불필요한 context가 오히려 품질을 떨어뜨리는 문제**를 줄이기 위한 정책입니다.

## 4. Issue / Recipe partition gate

작업을 잘게 나누기 전에 먼저 기존 계약을 확인합니다.

- 기존 Recipe
- Parent / Child Issue
- 같은 영역의 기존 Issue
- Architecture / Production 문서의 책임 경계

기본값은 하나의 Goal과 Acceptance를 공유하면 같은 Issue의 Step으로 유지하는 것입니다.

새 Issue나 Recipe는 “작업량이 많다”는 이유가 아니라 **독립적인 Goal, Acceptance, lifecycle 또는 재사용 계약이 존재할 때**만 분리합니다.

## 5. Step execution

~~~text
Restore current state
→ choose next Step
→ load required Skill / Recipe
→ derive required capability
→ discover actual tool
→ execute in approved scope
→ validate actual result
→ record evidence
→ evaluate next action
~~~

Tool 호출 성공과 Step PASS는 별도입니다.

## 6. Observability

진행 화면에서는 다음 연결이 보여야 합니다.

~~~text
Issue / Request
→ WorkType
→ Workflow / Step
→ Skill
→ required capability
→ actual Toolset / Tool
→ Artifact
→ Validation
→ Next action
~~~

발견한 Tool 후보와 실제 호출한 Tool을 구분하고, 미확인 상태를 성공처럼 표현하지 않습니다.

## 7. Task outcome

대표 상태:

- continue
- wait for user decision
- blocked
- complete
- not tested
- capability gap

Build 성공, Compile 성공, MCP 호출 성공만으로 `complete`가 되지 않습니다.

완료는 **Acceptance에 필요한 실제 제품 결과와 검증 Evidence가 충족됐을 때** 판정합니다.
