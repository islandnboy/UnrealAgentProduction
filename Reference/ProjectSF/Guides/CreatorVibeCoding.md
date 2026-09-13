# Creator 자연어 Production 실행 가이드

`Creator`는 특정 직군명이 아니다. 기획자, 프로그래머, 아티스트, 테크니컬 아티스트 등 직군과 관계없이 **이번 작업의 목표를 정의하고 Agent에게 제작을 맡기는 작업 담당자**를 뜻한다.

Creator는 내부 구현, Tool ID, Production Spec 형식이나 Execution Mode를 몰라도 자연어로 Production 의도와 관찰 가능한 완료 기준을 요청할 수 있다. 대상은 Unreal Asset뿐 아니라 문서, 데이터, 외부 제작 결과와 그 밖의 승인 가능한 Production 산출물을 포함한다.

## 기본 UX

```text
Creator
  ↓
ChatGPT와 목표 정리
  ↓
Issue / Work Task 생성
  ↓
Issue = Work Spec / Task State / SoT
  ↓
Worker 실행
  ↓
Issue Update / Evidence
  ↓
ChatGPT 결과 회수
  ↓
필요 시 Reviewer
```

## 최소 입력

Creator는 최소한 다음 세 가지를 전달한다.

1. 무엇을 만들고 싶은가
2. 어떤 기능·느낌·목적을 만족해야 하는가
3. 무엇을 보고 완료로 판단할 것인가

경로, Skeleton, Tool ID, Frame 같은 기술 값은 알고 있을 때만 덧붙인다. 모르는 값을 추측해서 채우지 않는다.

## Agent 자동 Intake

자연어 Production 요청을 받으면 Agent는 다음을 자동 수행한다.

1. 공용 Workflow와 Production Rules를 확인한다.
2. 요청 의도와 Domain/Stage를 해석한다.
3. ContextRouter / Resolve-Then-Expand로 필요한 저장소 범위부터 조사한다.
4. 의도, 대상, 필수·금지 요소, 완료 기준을 Atomic Requirement로 정규화한다.
5. 안전하게 확인 가능한 값은 Repository 근거와 함께 채운다.
6. 미확정 값은 `TODO_PROJECT_DECISION`과 확인 방법으로 남긴다.
7. UE 작업이면 공식 Unreal MCP Toolset을 우선 discovery한다.
8. 공식 Tool 하나 또는 공식 Tool/ProgrammaticToolset 조합으로 해결한다.
9. Capability가 부족하면 `CAPABILITY_GAP`으로 중단하고 별도 Framework 작업을 만든다.
10. Production에서는 `preflight → dry-run → approval → mutation → validation → evidence` Gate를 유지한다.

Creator에게 기술 Schema 전체를 다시 작성하게 하지 않는다. 결과를 실질적으로 바꾸는 목표·제약·승인 판단만 요청한다.

## 완료와 Evidence

```text
Requirement → Implementation → Validation → Evidence
```

Build 성공이나 Asset 생성 성공은 그 자체로 전체 완료가 아니다. 검증 상태는 필요에 따라 `PASS / FAIL / BLOCKED / NOT_APPLICABLE / NOT_TESTED`로 구분하고 `NOT_TESTED`를 성공으로 취급하지 않는다.

> Portfolio snapshot. Source of Truth: ProjectSF `AI/Guides/CreatorVibeCoding.md`.
