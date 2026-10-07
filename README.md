# AI Agent 기반 Unreal Engine 개발·제작 워크플로

**UnrealAgentWorkflow**는 AI Agent와 사람이 같은 제작 계약을 공유하며 Unreal Engine 개발·제작 결과를 반복 개선하는 워크플로 R&D입니다.

개인 프로젝트 **ProjectSF (Unreal Engine 5.8)**에서 실제로 사용한 운영 구조와 제작 사례를 정리합니다. 게임 작업 저장소는 비공개이며, 이 저장소에는 공개용으로 선별한 문서·사례·참고 자료를 담습니다.

**프로젝트 인원 구성:** 기획 4명 · 프로그래머 1명 · PM 1명. 아트 2명은 합류 예정입니다.

## 둘러보기

| 카테고리 | 내용 |
| --- | --- |
| [Workflow](#workflow) | Agent의 작업 판단·실행·검증과 사람의 검토 흐름 |
| [Framework](#framework) | 공통 제작 기반, Unreal 도구 연결, 월드·UI 제작 사례 |
| [Network](#network) | RPCNet과 프로토콜 생성·Unreal 클라이언트 연동 |
| [Server](#server) | 온라인 서버 구성과 접속·인증·영속화 |
| [Data](#data) | DataForge와 게임 데이터 변환·검증 |

## Workflow

요청을 실행 가능한 작업으로 나누고, 최신 상태와 검증 근거를 바탕으로 다음 행동을 결정합니다.

```text
요청 / Issue → 최신 저장소·Issue·Workflow 확인 → Rule·Skill·Recipe 선택
→ 제작 도구 / Unreal MCP 실행 → 제품 결과 검증·Evidence → 수정 및 다음 Step
```

**Agent는 작업의 의미와 다음 행동을 판단하고, Runtime은 실행과 검증을 담당합니다.** 도구 실행 성공만으로 완료를 판정하지 않고, 실제 제품 결과와 목표의 Acceptance를 확인합니다.

| 문서 | 다루는 내용 |
| --- | --- |
| [Execution Model](Docs/ExecutionModel.md) | 최신 상태 확인, 작업 분리, Step 실행과 완료 판정 |
| [Creator Workflow](Docs/CreatorWorkflow.md) | 기획자·제작자의 요청, 검토, 직접 수정, 다음 작업 연결 |
| [Designer Production](CaseStudies/DesignerProduction.md) | 기획 의도를 제작 계약과 결과 검증으로 연결한 사례 |
| [Execution Observability](Reference/ProjectSF/ExecutionObservability.md) | 실행 상태와 검증 근거를 기록하는 방식 |
| [Context Budget Policy](Reference/ProjectSF/ContextBudgetPolicy.md) | 필요한 문맥을 선택하고 확장하는 기준 |
| [Designer Artifact Set](Samples/DesignerArtifactSet.md) | 기획자와 Agent가 공유하는 제작 산출물 예시 |

## Framework

공통 제작 계약과 실행 도구를 연결하는 기반입니다. 현재 공개 문서는 AgentPipeline·Unreal MCP 연결과 이를 적용한 콘텐츠 제작 사례를 중심으로 구성합니다.

| 문서 / 사례 | 다루는 내용 |
| --- | --- |
| [Architecture](Docs/Architecture.md) | Workflow·Rule·Skill·Recipe·Runtime·Evidence의 책임과 경계 |
| [Production Model](Docs/ProductionModel.md) | 공통 제작 계약, 반복 개선과 재사용 도구 승격 |
| [Recipe Templates](CaseStudies/RecipeProduction.md) | 영웅·몬스터·월드·도로·수계·데이터·서버의 제작 계약 양식과 사용 사례 |
| [MCP Execution](Docs/MCPExecution.md) | Unreal Editor 실행과 도구 연결 방식 |
| [Project Structure](Reference/ProjectSF/Structure.md) | 작업 저장소의 디렉터리 구조와 역할 |
| [World Production](CaseStudies/WorldProduction.md) | 지형·도로·수계 등 Unreal 월드 제작 과정 |
| [UI Production](CaseStudies/UIProduction.md) | Unreal UI 제작과 검증 과정 |

참고: [ProjectSF 공개 자료 범위](Reference/ProjectSF/README.md) · [Samples](Samples/README.md)

## Network

**RPCNet** — Runtime·Session·Transport·Codec을 분리하고, 프로토콜 생성기와 Unreal 런타임 플러그인을 연결하는 네트워크 시스템입니다.

- [RPCNet Case Study](CaseStudies/RPCNet.md) — 구조, Consumer Integration과 실제 Unreal 연동 검증
- [Protocol → Unreal Client Guide (PDF)](Docs/Guides/RPCNet_Protocol_to_Unreal_Client_Guide.pdf) — 프로토콜에서 Unreal 클라이언트까지의 연결 가이드

## Server

**Online Server** — Gateway·Account Server·Game Server를 연결해 접속·인증·게임 진입·영속화 흐름을 구성합니다.

- [Server Production Case Study](CaseStudies/ServerProduction.md) — 서버 구성, Player·World 상태 저장과 클라이언트 연동 검증
- [Server Architecture / Topology](Docs/Server/ServerArchitecture.md) — 서비스 구성, Authority와 데이터·프로토콜 경계
- [Gateway Deployment Design](Docs/Server/GatewayDeploymentDesign.md) — AS 풀·LB·Coordination·로컬 런처·배포 설계

## Data

**DataForge** — Excel 입력에서 Unreal DataTable·서버 JSON까지 게임 데이터를 변환하고 결과의 일치 여부를 검증하는 파이프라인입니다.

- [DataForge Case Study](CaseStudies/DataForge.md) — GUI·CLI 공통 처리, 증분 변환과 Bake·Readback·Parity 검증
- [DataForge 사용 가이드 (PDF)](Docs/Guides/DataForgeUserGuide.pdf) — 화면 안내, DT 빌드, DA·Config 조회와 결과·오류 확인

## 현재 상태

**Portfolio / Active R&D.** 적용·검증된 범위와 연구 중인 항목은 [Implementation Status](Docs/ImplementationStatus.md)에서 구분합니다.

사례에 기록된 테스트·연동 결과는 해당 검증 시점의 근거입니다. 기술 검증, 화면 결과 검토, 최종 제작 승인도 구분해 기록합니다. 비공개 게임 코드·원본 데이터·Issue·Production Evidence 전체는 공개하지 않습니다.
