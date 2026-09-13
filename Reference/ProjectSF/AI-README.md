# ProjectSF Agent Workflow

`AI/`는 Agent가 읽는 **Agent Workflow, Production Framework 지침과 Skill의 Git Source of Truth**다. 실행 코드, Registry, Schema, Template, Fixture, Job 데이터는 소유하지 않는다.

생성형 AI는 선택 가능한 하위 도구다. Agent 제품별 폴더와 세션 handoff 문서는 이곳에 두지 않는다. 운영 Context와 인수인계는 `D:/AI/SF_Context`에서 관리한다.

ProjectSF는 다음 두 축을 분리한다.

| 축 | 목적 | 소유하지 않는 것 |
| --- | --- | --- |
| Agent Workflow | Agent 역할, Execution Mode, Prompt Routing, Skill·Script·MCP 실행, Validation, Human Review와 Handoff | 게임 제작 Flow 자체 |
| Production Framework | 게임 제작 Flow, 직군 Domain, Stage, Dependency, Review와 Integration | Agent 종류, Prompt 작성법, Skill·MCP 구현법 |

Agent Workflow가 Production Framework를 읽고 실행한다. Production Framework는 Agent Workflow를 설명하거나 제어하지 않는다.

## 프로그래밍 지침과의 경계

이 디렉터리는 공통 Workflow와 Production Flow, 실행·검증 절차에 집중한다.
공통 구현 원칙은 [공통 프로그래밍 원칙](Rules/Programming.md), Unreal 구현 규칙은
[Client/.AI](../Client/.AI/README.md), 서버 구현 규칙은
[Server/.AI](../Server/.AI/README.md)가 소유한다.
프로그래밍 Stage의 절차는 이곳에서 유지하고 구체적인 코딩 규칙은 해당 지침을 참조한다.
기존 Workflow·Skill·계약 경로는 유지하며 같은 규칙을 양쪽에 복제하지 않는다.

## 시작점

| 목적 | 읽을 문서 |
| --- | --- |
| Agent Workflow 전체 구조 | `AI/Docs/AgentProductionPipeline.md` |
| Execution Mode·Agent 역할·공통 순서 | `AI/Workflows/CommonAIWorkflow.md` |
| 자연어 요청 Prompt Compilation | `AI/Workflows/PromptCompilation.md` |
| Context/Token Budget·탐색 범위 정책 | `AI/Workflows/ContextBudgetPolicy.md` |
| Production Flow·Domain·Stage | `AI/Flows/README.md` |
| 새 제작 요청 작성 | `AI/Docs/PlannerGuide.md` |
| 자연어로 Production 요청 | `AI/Guides/DesignerVibeCoding.md` |
| 작업 실행 | `AI/Rules/ResourceProduction.md`, `AI/Workflows/README.md` |
| 로컬 환경 설정 | `AI/Docs/LocalEnvironmentSetup.md` |
| 새 Skill·Tool 추가 | `AI/Docs/AddingAProductionSkill.md`, `AI/Workflows/MCPToolLifecycle.md` |
| World Production 설계와 Capability 경계 | `AI/Docs/WorldProductionCapabilityMap.md` |
| MCP 사용 원칙 | `AI/Docs/MCP/README.md`, `AI/Docs/MCP/Contracts.md` |
| 현재 구현 범위 | `AI/Docs/CurrentState.md` |

## 디렉터리 책임

| 디렉터리 | 책임 | 주요 입력 | 주요 산출물 |
| --- | --- | --- | --- |
| `Docs/` | 구조·환경·확장·유지보수 안내 | 실제 계약과 구현 상태 | 재현 가능한 운영 문서 |
| `Guides/` | 기획자와 제작 요청자를 위한 역할별 안내 | 제작 의도 | 정형 요청과 검수 기준 |
| `Rules/` | 승인·안전·Source·SCM 강제 정책 | 조직 결정 | Workflow와 Tool의 공통 제약 |
| `Skills/` | Stage에 바인딩되는 전문 실행 지침과 Capability 요구 | Work Node의 Domain·Stage·Specialty·Intent | 실행 절차·중단 조건 |
| `Flows/` | Production Framework: 게임 제작 Flow, 직군 Domain, 공통 Stage | 제작 목표와 승인된 입력 | Dependency·Artifact·Review·Integration·Handoff |
| `Workflows/` | Agent Workflow: 실행 모드, Prompt Routing, 공통 Gate와 Tool 수명주기 | 자연어 요청·Framework Node·Capability | 실행 계획과 Evidence 요구사항 |

각 폴더의 상세 책임과 파일 배치 기준은 해당 폴더의 `README.md`를 따른다.

## Execution Mode

Agent는 Production Framework의 Flow·Domain·Stage를 결정하기 전에 실행 모드를 먼저 고른다.

- `/PRODUCTION`: 게임 코드·데이터·UI·에셋·콘텐츠 제작
- `/FRAMEWORK`: Agent Workflow, Production Framework, Skill, Script, Prompt, MCP Tool과 실행 계약 수정
- `/FRIDAY_GOD`: Production의 실패/비효율을 적절한 계층에서 해결하고 검증된 방법을 Production에 환원한다. 기본 제작은 `/PRODUCTION`이다.
- `/PLAN`: 설계 Artifact만 작성
- `/RESEARCH`: 조사와 근거 수집만 수행

Execution Mode는 `programming.production` 같은 `domain.stage`와 별개다.

## MCP 강제 실행 경계

- Unreal Asset 변경 전에는 UE 5.8 공식 MCP discovery, `Tools/AgentPipeline/Registry/OfficialCapabilityMap.json`, `Tools/AgentPipeline/Scripts/AgentPipeline.mjs preflight`를 사용한다.
- 미구현 Capability는 `CAPABILITY_MISSING`으로 중단하며 Python·Commandlet·Editor Utility·Native Helper로 우회하지 않는다.
- `PRODUCTION`, `MCP_TOOLSET_EXTENSION`, `ENGINEERING_CHANGE`는 서로 다른 Job으로 분리한다.
- 모든 Asset 변경 Manifest에는 MCP Tool·Adapter·Dry Run·승인·변경 전후 상태를 추적하는 `mutationProvenance`가 있어야 한다.
