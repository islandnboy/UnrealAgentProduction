# Execution Observability

작업자가 Workflow를 따라 정상적으로 진행되는지 확인할 수 있도록 화면 Trace의 표현을 정의한다.

## Screen trace

~~~text
Request / Issue
→ WorkType
→ Workflow / Step
→ Skill
→ required capability
→ actual Toolset / Tool
→ execution
→ Artifact
→ validation
→ next action
~~~

## Rules

- 시작·재개에는 현재 WorkType / Workflow / Step / Status를 표시한다.
- discovery 후보와 실제 호출을 구분한다.
- 미확인은 `UNRESOLVED`, 비해당은 `NOT_APPLICABLE`, 선택만 한 Tool은 `NOT_CALLED`이다.
- Tool success, preflight, product validation, Goal Acceptance를 서로 다른 판정으로 표시한다.
- Artifact와 Evidence를 검증 상태에 연결한다.
- 선택 경로가 바뀌면 변경 내용과 관측 가능한 이유를 짧게 알린다.
- 비밀정보, 대용량 원문, 숨은 추론은 출력하지 않는다.

## Progress header

~~~text
Task: <Issue or task>
[WorkType: ... | Workflow: ... | Step: ... | Status: ...]
Progress: ...
Skills(applied): ...
Tools(actual): ...
~~~

매 Tool 호출마다 별도 메시지를 만들지는 않는다.  
실제 진행 상태와 다음 행동을 판단할 수 있는 의미 있는 checkpoint를 보여주는 것이 목적이다.

## Final execution summary

최종 전달에는 다음을 짧게 남긴다.

- actual Workflow / Step order
- applied Skills
- actual Tools
- Artifact / Evidence
- validation result
