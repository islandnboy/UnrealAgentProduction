# AI Agent 기반 Unreal Engine 개발·제작 워크플로

**UnrealAgentWorkflow**는 AI Agent와 사람이 같은 제작 계약을 공유하며 Unreal Engine 개발·제작 결과를 반복 개선하는 워크플로 R&D입니다.

개인 프로젝트 **ProjectSF (Unreal Engine 5.8)**에서 실제로 사용한 운영 구조와 제작 사례를 정리합니다. 게임 작업 저장소는 비공개이며, 이 저장소에는 공개용으로 선별한 문서·사례·참고 자료를 담습니다.

## 둘러보기

- [Agent Workflow](#agent-workflow) — 작업 판단, 실행, 검증을 연결하는 운영 구조
- [기획·콘텐츠 제작](#기획콘텐츠-제작) — 사람과 AI가 함께 만드는 월드와 UI
- [개발 시스템](#개발-시스템) — 네트워크, 온라인 서버, 데이터 파이프라인
- [참고 자료·샘플](#참고-자료샘플) — 선별한 운영 문서와 제작 계약 예시

## 핵심 흐름

```text
요청 / Issue → 최신 저장소·Issue·Workflow 확인 → Rule·Skill·Recipe 선택
→ 제작 도구 / Unreal MCP 실행 → 제품 결과 검증·Evidence → 수정 및 다음 Step
```

**Agent는 작업의 의미와 다음 행동을 판단하고, Runtime은 실행과 검증을 담당합니다.**

도구 실행 성공만으로 완료를 판정하지 않습니다. 실제 제품 결과와 목표의 Acceptance를 확인하고, 사람의 검토·직접 편집을 다음 제작 단계에 반영합니다.

## Agent Workflow

작업 진입부터 반복 개선까지의 공통 구조입니다.

| 문서 | 다루는 내용 |
| --- | --- |
| [Architecture](Docs/Architecture.md) | Workflow·Rule·Skill·Recipe·Runtime·Evidence의 책임과 경계 |
| [Execution Model](Docs/ExecutionModel.md) | 최신 상태 확인, 작업 분리, Step 실행과 완료 판정 |
| [Production Model](Docs/ProductionModel.md) | 사람과 AI의 공통 제작 계약, 반복 개선과 재사용 도구 승격 |
| [MCP Execution](Docs/MCPExecution.md) | Unreal Editor 실행과 도구 연결 방식 |
| [Implementation Status](Docs/ImplementationStatus.md) | 실제 적용·검증 범위와 진행 중인 R&D |

## 기획·콘텐츠 제작

자연어 목표를 제작 입력과 결과로 연결하고, 중간 검토와 Editor 수정으로 결과를 다듬는 과정입니다.

| 문서 / 사례 | 다루는 내용 |
| --- | --- |
| [Creator Workflow](Docs/CreatorWorkflow.md) | 기획자·제작자의 요청, 검토, 직접 수정, 다음 작업 연결 |
| [Designer Production](CaseStudies/DesignerProduction.md) | 기획 의도를 제작 계약과 결과 검증으로 연결한 사례 |
| [World Production](CaseStudies/WorldProduction.md) | 지형·도로·수계 등 Unreal 월드 제작 과정 |
| [UI Production](CaseStudies/UIProduction.md) | Unreal UI 제작과 검증 과정 |
| [Designer Artifact Set](Samples/DesignerArtifactSet.md) | 기획자와 Agent가 공유하는 제작 산출물 예시 |

## 개발 시스템

같은 워크플로를 적용해 구현한 게임 개발 시스템입니다. 상세 구조와 검증 시점의 결과는 각 사례 문서에서 확인할 수 있습니다.

| 사례 | 핵심 내용 |
| --- | --- |
| [RPCNet](CaseStudies/RPCNet.md) | Runtime·Session·Transport·Codec 분리, 프로토콜 생성기, Unreal 연동 |
| [Online Server](CaseStudies/ServerProduction.md) | Gateway·Account Server·Game Server, 접속·인증·영속화 흐름 |
| [DataForge](CaseStudies/DataForge.md) | Excel 입력에서 Unreal DataTable·서버 JSON까지의 변환·검증 파이프라인 |

📄 [RPCNet: Protocol → Unreal Client Guide (PDF)](Docs/Guides/RPCNet_Protocol_to_Unreal_Client_Guide.pdf)

## 참고 자료·샘플

공개용으로 선별한 ProjectSF 운영 구조와 예시입니다.

| 자료 | 다루는 내용 |
| --- | --- |
| [ProjectSF Reference](Reference/ProjectSF/README.md) | 공개 참고 자료의 범위와 구성 |
| [Project Structure](Reference/ProjectSF/Structure.md) | 작업 저장소의 디렉터리 구조와 역할 |
| [Execution Observability](Reference/ProjectSF/ExecutionObservability.md) | 실행 상태와 검증 근거를 기록하는 방식 |
| [Context Budget Policy](Reference/ProjectSF/ContextBudgetPolicy.md) | Agent가 필요한 문맥을 선택하고 확장하는 기준 |
| [Samples](Samples/README.md) | 제작 입력·계약·검증 산출물 예시 안내 |

## 현재 상태

**Portfolio / Active R&D.** 실제 프로젝트에서 사용한 구조를 정리하며, 적용·검증된 범위와 연구 중인 항목은 [Implementation Status](Docs/ImplementationStatus.md)에서 구분합니다.

사례에 기록된 테스트·연동 결과는 해당 검증 시점의 근거입니다. 기술 검증, 화면 결과 검토, 최종 제작 승인도 구분해 기록합니다. 비공개 게임 코드·원본 데이터·Issue·Production Evidence 전체는 공개하지 않습니다.
