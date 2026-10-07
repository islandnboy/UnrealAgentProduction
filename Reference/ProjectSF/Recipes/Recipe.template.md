# Creator Production Recipe — 공통 작성 템플릿

Status: **AUTHORING TEMPLATE / NOT_EXECUTED / NOT A RUNTIME SCHEMA**

ProjectSF의 `Docs/Production/Recipes/RecipeFormat.md` 공통 YAML 작성 양식을 발췌한 공개 참고 자료입니다. 특정 작업의 실제 값·비공개 경로·Issue·실행 Evidence는 포함하지 않습니다.

Creator와 Agent가 무엇을 만들고, 무엇을 보존하며, 어떤 결과를 완료로 인정할지 정리하는 양식입니다. 실제 실행 순서와 Tool 조합은 현재 상태를 관찰한 Agent가 판단합니다.

## 작성 양식

```yaml
Recipe:
  Type: <HeroProduction | MonsterProduction | WorldRegionProduction | DataProduction | ...>
  Name: <작업 이름>

CreatorIntent:
  Goal: <무엇을 만들고 싶은가>
  Experience: <사용자/플레이어가 어떻게 느끼거나 동작해야 하는가>
  Requirements:
    - <핵심 요구사항>

Inputs:
  Required:
    - <반드시 필요한 승인 입력>
  Preferred:
    - <우선 사용하면 좋은 입력>
  Discover:
    - <Agent가 프로젝트에서 찾아 선택할 수 있는 입력>

Preserve:
  - <기존 시스템/데이터/수작업 중 보존할 것>

ExpectedResult:
  - <완성 후 존재해야 하는 결과>

ResultContract:
  RequiredRepresentation:
    - <사람 편집·runtime 동작·후속 공정에 필요한 실제 결과 종류>
  AllowedApproximation:
    - <이번 단계에서 명시적으로 허용한 preview/rough 표현 또는 NONE>
  ForbiddenSubstitutes:
    - <겉모양이 비슷해도 완료로 인정하지 않을 대체물>
  VisibleDelta:
    - <기준 결과와 같은 관점에서 확인되어야 하는 최소 변화>
  PromotionGate:
    - <어떤 기반 결과가 PASS해야 후속 공정을 진척/완료로 인정하는가>

Acceptance:
  - <기계적으로 검증 가능한 완료 조건>
  - <실제 Play/Editor에서 확인할 조건>
  - <Creator 판단이 필요한 조건>

CreatorSurface:                 # optional
  Preferred:
    - Surface: <ExternalSpreadsheet | DataTable | Blueprint | DataAsset | Editor | ...>
      Focus:
        - <완성 후 Creator가 주로 수정·튜닝할 영역>

Constraints:
  - <프로젝트/작업 고유 제약>

Dependencies:
  Hard:
    - <없으면 이 작업 자체가 성립하지 않는 선행 결과>
  DefaultOrder:
    - <일반적으로 먼저 하는 편이 좋은 작업>
  IndependentFrom:
    - <완료되지 않아도 이 작업을 막지 않는 항목>

Capabilities:
  Required:
    - <필요한 효과/능력>
  ExecutionConstraints:
    - <예: Unreal World mutation은 승인된 Official MCP 경계 사용>

DefaultRoute:                   # non-binding
  - INSPECT
  - PASS_OR_REPAIR
  - VERIFY
  - PASS

Evidence:
  - <같은 관점의 유효 baseline과 after>
  - <Artifact identity / hash>
  - <Editor/runtime readback>
  - <Play/visual evidence>
```

## 사용 기준

- `<...>`는 채워 넣을 작성값입니다. 미확인은 `UNKNOWN`, 합의한 범위 밖은 `N/A — 이유`로 표시합니다.
- Goal·Acceptance·Preserve·권한·ResultContract를 유지합니다. DefaultRoute는 현재 상태에 따라 재평가할 기본 경로입니다.
- RequiredRepresentation과 ForbiddenSubstitutes로 필요한 결과와 완료로 인정하지 않을 대체물을 구분합니다.
- CreatorSurface는 사람이 계속 수정할 영역을 안내합니다. 내부 구현 기술을 강제하지 않습니다.
- 작성한 Recipe는 승인된 작업의 계약으로 확정합니다. 템플릿 자체를 실행 상태로 덮어쓰지 않습니다.
- 이 작성 양식은 실행 도구에 직접 넣는 runtime schema가 아닙니다. 실제 적용된 입력·파라미터와 미적용 의도는 Evidence에서 구분합니다.
- 실행 결과는 Acceptance별 기대값·관측·Evidence·PASS/FAIL/NOT_TESTED/N/A로 기록합니다. 빈 양식은 검증이나 승인 근거가 아닙니다.

[Recipe Template Case Study](../../../CaseStudies/RecipeProduction.md)
