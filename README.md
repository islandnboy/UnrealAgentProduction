# Agent Workflow

**Production-grade AI Agent workflow for Unreal Engine**

Agent Workflow는 AI에게 Unreal Engine 작업을 단순히 “시켜 보는” 데모가 아니라, **실제 게임 제작 안에서 사람과 AI가 같은 제작 계약을 공유하고 결과를 반복 개선하도록 설계한 Agent Workflow R&D**입니다.

현재 구조는 개인 프로젝트 **ProjectSF**에서 실제 Production을 수행하며 검증한 운영 모델을 기준으로 정리되어 있습니다.

> Applied project: ProjectSF — Unreal Engine 5.8 기반 게임 프로젝트  
> Working repository는 비공개이며, 포트폴리오에 필요한 구조와 일부 계약만 이 저장소에 선별 공개합니다.

## What this solves

게임 제작에서 Agent의 문제는 코드 생성 자체보다 다음에 있습니다.

- 시작 전에 현재 프로젝트 규칙과 작업 범위를 제대로 읽는가
- 이전 대화가 아니라 최신 Repository / Issue / Workflow를 기준으로 재개하는가
- 어떤 전문 Skill과 제작 Recipe가 필요한지 판단하는가
- Tool 성공과 제품 완료를 구분하는가
- Unreal Editor 변경을 안전하게 실행하고 검증하는가
- 사람이 수정한 결과를 보존하면서 다음 Agent가 이어갈 수 있는가
- 반복되는 작업을 Skill / Tool / Recipe로 승격할 수 있는가

이 프로젝트는 이 문제를 **Workflow, Rule, Skill, Recipe, Runtime, Evidence**의 책임 분리로 해결합니다.

## Current architecture

~~~text
Natural-language request / GitHub Issue
                ↓
          AGENTS.md bootstrap
                ↓
 Current Source of Truth Gate
 Repository + Issue + Workflow
                ↓
      Workflow / current Step
                ↓
 Rule + Skill + Recipe resolution
                ↓
 Agent decides required capability
                ↓
 AgentPipeline validates execution contract
                ↓
 Official Unreal MCP / deterministic tools
                ↓
 Validation + Evidence
                ↓
 Goal evaluation
   ├─ next Step / next Cycle
   ├─ ProductionEvolution
   └─ Acceptance complete
~~~

### The key separation

**Agent decides meaning. Runtime validates execution.**

Agent는 요청의 의미, 현재 Step, 필요한 전문성, 요구 capability를 판단합니다.  
AgentPipeline은 그 판단을 대신하는 키워드 Router가 아니라 **schema, binding, preflight, execution, evidence를 검증하는 실행 계층**입니다.

## Source of Truth

| Source | Responsibility |
| --- | --- |
| GitHub Issue | 지속 Goal, Scope, Acceptance, 결정, 현재 상태 |
| `AGENTS.md` | 저장소 공통 진입점과 routing |
| `AI/Workflows` | 실행·재개·전환·검증 계약 |
| `AI/Rules` | 공통 안전·품질 불변 조건 |
| `AI/Skills` | 전문 제작 판단과 절차 |
| `Docs/Production/Recipes` | 검증된 반복 제작 계약 |
| `Tools/AgentPipeline` | Runtime, schema, registry, scripts, tests |
| `Production/Data` | 승인된 제작 입력 |
| `Production/Evidence` | 실제 실행·검증 증거 |
| `Docs` | 사람이 읽는 제품·기술·제작 설계 |

## Design principles

1. **Bootstrap before mutation**  
   실제 변경 전에 적용 Workflow / Rule / Skill / Recipe를 먼저 resolve합니다.

2. **Latest state, not conversation memory**  
   Issue 작업 재개 시 이전 세션이 아니라 현재 Repository + Issue + Workflow를 기준으로 판단합니다.

3. **Goal-oriented execution**  
   직군별 hand-off보다 하나의 Goal과 Acceptance를 중심으로 필요한 전문 Skill을 조합합니다.

4. **Human and AI share the same production pipeline**  
   사람이 Editor에서 수정한 결과도 정상 Production 입력이며, AI는 이를 덮어쓰지 않고 관측·보존·계속합니다.

5. **Evidence over tool success**  
   MCP 호출, Build, Compile, Asset 생성 성공만으로 완료 처리하지 않습니다.

6. **Progressive convergence**  
   Make → Observe → Evaluate → Refine을 반복하며 연결된 결과물을 개선합니다.

7. **Systematize only after evidence**  
   반복이 확인된 방법만 Skill / Tool / Recipe로 승격합니다.

## Repository guide

- [Architecture](Docs/Architecture.md)
- [Execution Model](Docs/ExecutionModel.md)
- [Production Model](Docs/ProductionModel.md)
- [Unreal MCP Execution](Docs/MCPExecution.md)
- [Implementation Status](Docs/ImplementationStatus.md)
- [World Production Case Study](CaseStudies/WorldProduction.md)
- [UI Production Case Study](CaseStudies/UIProduction.md)
- [Server Production Case Study](CaseStudies/ServerProduction.md)
- [ProjectSF structure snapshot](Reference/ProjectSF/README.md)

## Applied domains

현재 ProjectSF에서 이 구조는 다음과 같은 실제 작업에 적용되고 있습니다.

- Terrain / Landscape production
- Road batch production
- Water / river / lake production
- World structure and validation
- UI production and UI architecture
- Server feature production and bot verification
- Issue-driven task execution
- Production input / evidence management
- Agent workflow regression and maintenance

## Status

**Portfolio / active R&D**

이 저장소는 완성된 범용 Agent SDK를 주장하지 않습니다.  
실제 ProjectSF 제작에서 검증된 구조와 현재 R&D 범위를 구분해 공개합니다.
