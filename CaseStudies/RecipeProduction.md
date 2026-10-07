# Creator Recipe Template Case Study

## 제작 문제와 해결

기획 의도를 자연어 요청으로만 전달하면, 제작자가 바뀌거나 다른 세션에서 작업을 재개할 때 보존 범위·기대 결과·완료 기준을 다시 해석해야 합니다. ProjectSF는 **공통 Recipe Format과 작업별 작성 템플릿**으로 이 계약을 명시합니다.

템플릿은 Creator와 GPT가 제작 의도를 다듬고, 사람이 확정한 Issue를 실행 Agent가 현재 상태와 대조해 수행하도록 연결하는 작성 도구입니다.

```text
Creator Intent → 작업별 Recipe 작성 → 사람의 계약 확정 / Issue
→ Agent의 현재 상태 판단 → Skill·Tool·MCP 실행
→ 실제 결과·검증 근거 → Creator Review / 수정
```

## 실제 템플릿 구성

다음은 ProjectSF의 `Docs/Production/Recipes/`에서 확인한 작성 양식입니다. 아래 범위는 양식의 구성과 목적을 보여주며, 각 유형의 제작 완료를 주장하지 않습니다.

| 템플릿 | 작성하는 계약 |
| --- | --- |
| `HeroProduction.template.md` | 플레이어 입력·Stat·공격/Ability·외형·피격/사망·사람 편집 왕복 |
| `MonsterProduction.template.md` | Stat·인지/추적/공격·피격/사망·외형·사람 편집 왕복 |
| `WorldRegionProduction.template.md` | 지형·수계·도로·건물, 제작 pass와 공간 품질 |
| `RoadProduction.template.md` | 승인 source·Road Design Input·표현 선택·부분 재생성 |
| `WaterProduction.template.md` | 수계 프리셋·개별 override·지형 인계·Native 물 생성/재사용 |
| `DataProduction.template.md` | DT Excel 원천 빌드·DA/INI native 원천 조회·Server JSON·migration |
| `ServerFramework.template.md` | topology·authority·내부 구조·통신/저장/소비자 검증 |
| `Issue.template.md` | 확정한 Recipe, 결과 계약, Acceptance와 재개 문맥을 Issue로 정리 |

[공통 작성 템플릿 보기](../Reference/ProjectSF/Recipes/Recipe.template.md)

## 템플릿이 고정하는 것

| 항목 | 역할 |
| --- | --- |
| CreatorIntent | 목표·플레이 경험·핵심 요구사항 |
| Inputs / Preserve | 승인 입력·탐색 가능한 입력·보존할 기존 결과 |
| ExpectedResult / ResultContract | 필요한 결과 표현·허용 preview·금지 대체물·관측할 변화·후속 공정 Gate |
| Acceptance | 기계 검증·실제 Play/Editor 확인·Creator 판단 기준 |
| CreatorSurface | 사람이 계속 수정할 표·Blueprint·DataAsset·Editor 영역 |
| Dependencies / Capabilities | 실제 선행 조건·필요한 효과·실행 권한 경계 |
| DefaultRoute / Evidence | 기본 진행 방향과 검증할 근거 |

**Goal·Acceptance·보존·권한·결과 계약은 유지하고, 실제 순서와 Tool 조합은 현재 상태를 본 Agent가 판단합니다.** 템플릿은 고정 Tool 명령열이나 실행 도구의 runtime schema가 아닙니다.

## 대표 사례: 결과 계약과 사람 편집 지점

월드 템플릿은 현재 제작 pass와 이번 통과 기준을 명시합니다. 수계에 실제 수위·수심·충돌·편집 동작이 필요하다면 일반 평면 Mesh를 완료 결과로 인정하지 않는 식으로 `RequiredRepresentation`과 `ForbiddenSubstitutes`를 구분합니다. preview를 허용한 경우에도 그 결과를 최종 Production이나 후속 공정의 기반 PASS로 자동 승격하지 않습니다.

영웅·몬스터 템플릿은 사람이 조정할 Stat·Ability 구성·외형 파라미터와 실제 저장 위치를 연결합니다. `CreatorSurface`는 이 접근성을 요구하면서 내부 C++·GAS·Asset 구현 선택은 Agent가 프로젝트 계약에 맞춰 판단하도록 둡니다.

데이터 템플릿은 DT의 XLSX/XLSM 원천과 DA/INI의 Unreal-native 원천을 구분합니다. 모든 데이터를 Excel로 통일하거나 자동 양방향 동기화한다고 가정하지 않습니다.

## 작성과 검증

1. 필요한 작업별 템플릿 하나를 선택하고 현재 기준 결과와 이번 변경을 작성합니다.
2. 미확인은 `UNKNOWN`, 합의한 범위 밖은 `N/A — 이유`로 표시합니다.
3. 사람이 확정한 계약을 Issue로 연결하고 실행 Agent가 저장소·Issue·현재 결과를 대조합니다.
4. Acceptance별 기대값 → 관측 → Evidence → PASS/FAIL/NOT_TESTED/N/A를 기록합니다.
5. Creator가 직접 값을 편집·저장한 뒤 Agent가 재조회·보존·반영했는지 확인합니다.

Agent가 대신 값을 바꾼 것은 도구 검증이며, 사람 편집 왕복의 증거로 처리하지 않습니다. 유효한 기존 결과가 계약을 만족하면 재제작 없이 재사용할 수 있습니다.

## 공개 범위와 검증 상태

이 사례는 현재 저장소의 Recipe 안내·공통 형식·작업별 템플릿에서 확인한 **작성 구조**를 정리한 것입니다. 공개 참고 양식에는 공통 작성 필드와 사용 기준을 담고, 비공개 클래스·에셋 경로·작업별 값·Issue·원본 Evidence는 포함하지 않습니다.

템플릿 존재와 실제 제작 성공은 구분합니다. 특정 Hero·Monster·World 작업의 전체 PASS나 Creator 최종 승인을 이 문서에서 주장하지 않습니다.

## 관련 자료

- [공통 Recipe 작성 템플릿](../Reference/ProjectSF/Recipes/Recipe.template.md)
- [Creator Workflow](../Docs/CreatorWorkflow.md)
- [Production Model](../Docs/ProductionModel.md)
- [World Production](WorldProduction.md)
- [DataForge](DataForge.md)
