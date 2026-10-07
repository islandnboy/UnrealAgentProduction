# UI Production Case Study

## Goal

자연어 UI 요청을 기존 Unreal UI 구조와 연결해 **실제 사용 가능한 Widget / binding / interaction**으로 제작합니다.

## Current flow

~~~text
Request / Issue
→ bootstrap + current SoT
→ inspect existing UI assets and architecture
→ ui-production / ui-architecture Skill
→ derive logical capability
→ live MCP binding
→ create / edit
→ compile / save / readback
→ interaction and intent validation
→ Evidence
~~~

## Production principles

- 새 Widget을 만들기 전에 기존 구조를 조사합니다.
- 표시 책임과 상태 / 명령 책임을 구분합니다.
- reusable component와 ViewModel source를 먼저 검토합니다.
- placeholder를 승인된 결과로 승격하지 않습니다.
- 실제 Tool 이름은 Skill에 고정하지 않고 live discovery로 해결합니다.

## Validation

- Asset / Object identity
- compile
- save / readback
- input / focus / activation
- data binding result
- visual review
- untested items are reported as `NOT_TESTED`

이 사례의 핵심은 “UI를 Agent가 만들었다”가 아니라 **프로젝트의 기존 UI 규칙과 실제 Editor 결과를 같은 계약 안에서 연결했다는 것**입니다.
