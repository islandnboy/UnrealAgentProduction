---
name: ui-production
description: Produce and validate Unreal UI assets and connected UI behavior from an approved UI goal.
---

# UI Production

UI 화면·Widget·binding·interaction을 실제 사용 가능한 결과로 제작하는 Skill이다.

## 판단

- 기존 UI asset과 공용 component를 먼저 조사한다.
- 화면의 표시/입력 책임과 상태/명령 책임을 구분한다.
- 새 Widget, ViewModel, binding 또는 asset을 만들기 전에 재사용 가능한 기존 구조를 확인한다.
- placeholder는 승인된 preview가 아니면 완료 결과로 승격하지 않는다.
- UI mutation은 필요한 logical capability를 먼저 정의하고 현재 binding을 live discovery로 확인한다.

## Logical Capability

작업에 따라 다음과 같은 능력을 요구할 수 있다.

- Widget/UI asset inspect
- Widget create/edit
- ViewModel source/binding configure
- compile/save/readback
- runtime/PIE validation

실제 Tool 이름과 ProjectSF class/path는 이 Skill에 고정하지 않는다.

## Validation

- 생성·수정 Asset/Object identity
- compile/save/readback
- 입력·focus·activation 등 요청한 interaction
- ViewModel/model과 표시 결과의 연결
- 필요한 visual/human review
- 미검증 항목은 `NOT_TESTED`

ProjectSF Unreal 구현 규칙은 Client 영역의 UI 문서를 따른다.
