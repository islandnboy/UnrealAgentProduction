# Creator Workflow

Creator Workflow는 **제작자와 Agent가 같은 제작 흐름을 공유하는 방식**을 설명합니다.

여기서 Creator는 특정 직군을 뜻하지 않습니다.  
기획, 프로그래밍, 아트 등 어떤 역할이든 **직접 결과물을 만들고 판단하는 사람**을 의미합니다.

핵심 원칙은 단순합니다.

> Creator는 제품 의도와 완료 기준을 정의하고, Agent는 현재 프로젝트 상태를 읽어 실행 방법을 판단합니다.

Creator가 Tool ID, MCP schema, Skill 이름, 내부 Runtime 구조를 직접 운영할 필요는 없습니다.

---

## 1. Creator가 정의하는 것

Creator는 다음을 전달합니다.

- **Goal** — 무엇을 만들고 싶은가
- **Scope** — 어디까지 변경해도 되는가
- **Protection** — 무엇은 보존해야 하는가
- **Acceptance** — 어떤 상태를 완료로 볼 것인가
- **Feedback** — 현재 결과에서 무엇을 수정해야 하는가

예:

~~~text
한강은 단순한 정적 수면이 아니라
빠졌을 때 하류로 떠내려가는 느낌이 있어야 한다.

러프 단계에서는 실제 유체 시뮬레이션까지 필요하지 않지만,
후속 Gameplay가 위치별 흐름 방향과 속도를 조회할 수 있어야 한다.
~~~

Agent는 이 요구를 현재 Repository / Issue / Workflow와 대조해 실행 가능한 작업으로 해석합니다.

---

## 2. 공용 제작 Loop

사람과 Agent는 서로 다른 공정을 쓰지 않습니다.

~~~text
Creator Intent
   ↓
Goal / Scope / Acceptance
   ↓
Issue / Recipe
   ↓
Agent 또는 Creator Tool 실행
   ↓
Game / Unreal 결과
   ↓
Validation / Evidence
   ↓
Creator Review
   ├─ 승인
   ├─ 수정 요청
   └─ 직접 수정
   ↓
현재 결과를 기준으로 다음 작업
~~~

중요한 점은 **사람의 직접 수정도 정상 Production 과정에 포함된다는 것**입니다.

Agent가 만든 결과를 사람이 Editor에서 수정한 뒤 저장하면, 다음 Agent는 그 결과를 현재 상태로 읽고 이어서 작업합니다.

---

## 3. Creator의 책임

Creator가 판단하는 것은 제품 결과입니다.

### 작업 전

- 무엇을 만들 것인가
- 어떤 결과를 기대하는가
- 어디까지 변경 가능한가
- 어떤 기존 결과를 보존해야 하는가

### 작업 중

- 현재 결과가 의도와 맞는가
- 방향을 바꿔야 하는가
- 직접 수정하는 편이 빠른가
- 추가 제작이 필요한가

### 작업 후

- 실제 결과가 Acceptance를 만족하는가
- 기술 검증과 별개로 시각·경험 품질이 충분한가
- 다음 Iteration이 필요한가

Creator는 모든 내부 실행 로그를 읽을 필요가 없습니다.

필요한 것은 **현재 결과, 검증 상태, 남은 문제, 다음 행동**입니다.

---

## 4. Agent의 책임

Agent는 Creator의 의도를 구현 가능한 작업으로 연결합니다.

~~~text
Creator Request
→ Current Source of Truth 확인
→ Workflow / Step 판단
→ Rule / Skill / Recipe 선택
→ 필요한 Capability 판단
→ Tool 실행
→ 결과 검증
→ Evidence
→ Goal 평가
~~~

Agent는 다음을 대신 판단합니다.

- 어떤 Skill이 필요한가
- 어떤 Tool을 사용할 것인가
- 기존 결과를 재사용할 것인가
- 부분 수정할 것인가
- 반복 작업을 Recipe나 Tool로 승격할 가치가 있는가

단, **기술적인 PASS가 Creator의 최종 승인까지 의미하지는 않습니다.**

---

## 5. 직접 제작도 같은 Workflow다

Creator가 Unreal Editor나 외부 Tool에서 직접 수정하는 것도 예외 경로가 아닙니다.

예:

- Spline 위치 수정
- Road width / lane parameter 조정
- Material 선택
- PCG parameter 수정
- Water depth / shoreline 조정
- UI 배치·크기·레이아웃 수정
- Excel 기반 밸런스 데이터 편집

~~~text
Agent Result
→ Creator 직접 수정
→ Save
→ 현재 Production State
→ 다음 Agent가 상태 확인
→ 기존 수정 보존
→ 필요한 부분만 계속 제작
~~~

이전 generation을 무조건 다시 실행해 사람의 수정 내용을 덮어쓰지 않습니다.

---

## 6. Creator-facing Tool

모든 반복 작업을 자연어 Agent 요청으로 처리할 필요는 없습니다.

반복성과 입력·출력이 명확한 작업은 Creator가 직접 사용할 수 있는 Tool로 승격합니다.

대표 사례가 **DataForge**입니다.

~~~text
Creator edits XLSX
→ DataForge Refresh
→ 변경 Dataset 확인
→ Build Selected / Build Changed
→ Unreal DataTable Bake
→ Readback / Parity
→ Server JSON
→ Result / Warning / Diff 확인
~~~

Creator는 Unreal asset binary나 Server JSON을 직접 관리하지 않고 **Authoring Source와 결과 검수**에 집중합니다.

DataAsset과 Config는 각각 Unreal native source를 유지하며 DataForge에서는 read-only inspect / extract 경로를 사용합니다.

---

## 7. Production Artifact

Creator와 Agent가 공유하는 제작 정보는 대화에만 남지 않습니다.

~~~text
Production
├─ Issue
│  ├─ Goal
│  ├─ Scope
│  ├─ Requirements
│  └─ Acceptance
├─ Recipe
├─ Authoring Data
├─ Result Artifact
├─ Validation Evidence
├─ Creator Review
└─ Final Decision
~~~

지속되는 Goal과 판단은 Issue에, 반복 가능한 제작 계약은 Recipe에, 실제 입력과 결과 검증은 Data / Evidence에 남깁니다.

---

## 8. 완료 판정

다음 세 단계는 서로 다릅니다.

~~~text
Tool Success
   ↓
Technical Validation
   ↓
Creator Acceptance
~~~

예를 들어 Unreal Asset이 정상 생성되고 저장됐더라도:

- 화면 품질이 부족할 수 있고
- 플레이 경험이 의도와 다를 수 있고
- 후속 수정이 필요할 수 있습니다.

따라서 Agent는 Tool 성공만으로 제품 완료를 선언하지 않습니다.

최종적으로 제품 결과를 승인하는 것은 Creator입니다.

---

## 9. Portfolio에서 보여주는 것

Creator Workflow의 포트폴리오 단위는 “Agent 기능”이 아닙니다.

~~~text
Problem
→ Creator Intent
→ Production Contract
→ Agent / Creator Tool Execution
→ Actual Result
→ Validation
→ Creator Review
→ Iteration
~~~

각 Case Study에서는 가능한 한 다음을 함께 보여줍니다.

- Creator의 실제 요구
- Issue / Acceptance
- 제작 과정
- Unreal / Game 결과
- Before / After
- 기술 검증
- Creator의 수정 또는 승인
- 다음 Iteration

이를 통해 **사람과 AI가 별도의 작업자가 아니라 같은 Production Workflow 안에서 결과를 반복 개선한다는 것**을 보여줍니다.
