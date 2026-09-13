---
name: ui-production
description: Plan, create, and validate ProjectSF CommonUI and Unreal MVVM Widget Blueprints through the registered MCP UI tools.
flow_compatibility:
  domains: [programming, ui-ux, qa]
  stages: [analysis, design, production, validation]
  specialties: [client, ui, research, flow, information-architecture, interaction, visual, accessibility]
  intents: [analyze, specify, plan, architecture, implement, create, modify, integrate, review, test, evaluate]
required_capabilities: []
capability_requirements:
  analysis: [UI.Resource.List, UI.WidgetBlueprint.Inspect]
  design: [UI.Resource.List, UI.WidgetBlueprint.Inspect]
  production: [UI.WidgetBlueprint.Create, UI.WidgetTree.Author, UI.MVVM.Binding.Author]
  validation: [UI.WidgetBlueprint.Inspect, UI.MVVM.Binding.Validate, World.PIE.Start, World.PIE.Stop]
---

# UI Production

ProjectSF의 CommonUI + Unreal MVVM UI 제작 요청에 사용한다. 시작 전에 `AI/Workflows/ResourceProduction/UIWorkflow.md`를 읽고, 화면 종류와 ViewModel 소유 방식을 결정한다.

## 선택 기준

- Widget Blueprint Asset은 반드시 `Content/UI/[domain]/WBP_[content]`에 둔다. MCP object path로는 `/Game/UI/[domain]/WBP_[content]`를 사용한다.
- `[domain]`은 화면 기능 단위 PascalCase 폴더, `[content]`는 역할을 나타내는 PascalCase 이름으로 정한다. 예: `Content/UI/Login/WBP_Login`.
- 메뉴, 팝업, 전환 가능한 화면은 `/Script/SF.SFActivatableWidget`을 부모로 사용한다.
- HUD 조각이나 상시 표시 컴포넌트는 `/Script/SF.SFWidgetBase`를 부모로 사용한다.
- Widget은 표시와 입력만 담당하고 게임 상태 읽기·변환은 `UMVVMViewModelBase` 파생 ViewModel에 둔다.
- MVVM ViewModel source를 설정했으면 동일 Widget의 네이티브 `ViewModelClass` 기본값을 별도로 설정하지 않는다. 서로 다른 두 인스턴스가 생길 수 있다.
- 화면 표시값의 Text, Visibility, Enabled 같은 연결은 WBP의 Unreal MVVM Binding 패널에 작성한다. C++에서 FieldNotify 값을 읽어 표시 위젯을 수동 갱신하지 않는다.
- 화면·팝업·HUD content용 C++ Widget 클래스를 새로 만들지 않는다. 화면 WBP는 `SFActivatableWidget` 또는 `SFWidgetBase`를 직접 상속한다.
- C++ Widget은 공용 Button, ListEntry처럼 여러 WBP가 재사용하는 template component에만 만든다. Widget hierarchy, 표시 property, ViewModel binding과 화면 action event는 WBP가 소유한다.

## MCP 도구

- `inspect_widget_blueprint`: 기존 부모, 루트, 트리 이름, ViewModel, binding 수와 compile 상태를 읽는다.
- `create_widget_blueprint`: Widget Blueprint, Designer hierarchy, 선택적 MVVM source와 typed binding을 생성한다. 기본값은 `dry_run: true`, `save: false`다.

도구가 Registry에서 `implemented`가 아니거나 discovery 결과와 다르면 `CAPABILITY_MISSING`으로 중단한다. Python, Editor Utility, Commandlet 또는 직접 HTTP 호출로 Widget Asset을 대신 만들지 않는다.

## 완료 조건

- 부모 클래스가 화면 수명주기와 일치한다.
- Widget Blueprint가 컴파일되고 명명 규칙 `WBP_*`를 따른다.
- Asset 경로가 `/Game/UI/[domain]/WBP_[content]` 규칙을 따른다.
- ViewModel을 지정한 경우 inspector 결과에 정확한 클래스가 한 번 나타난다.
- 표시 상태 binding은 WBP에 존재하고 inspector의 binding 수가 Spec과 일치한다.
- 실제 mutation은 preflight, dry-run, 사용자 승인 뒤 별도 Production Job에서 수행한다.
- binding authoring이 필요하지만 등록된 도구가 없으면 골격 제작까지만 완료하고 후속 Toolset Extension으로 분리한다.

Widget 구조와 ViewModel 책임 판단이 필요하면 [architecture.md](references/architecture.md)를 읽는다.
