# Unreal Agent Production

**AI Agent & MCP based production workflow for Unreal Engine**

개인 Unreal Engine 프로젝트를 개발하면서 반복되는 개발·콘텐츠 제작 업무를 AI Agent가 실제 Production 과정 안에서 수행할 수 있도록 설계하고 있는 개인 R&D입니다.

목표는 AI에게 코드를 작성시키는 것에 그치지 않고, 자연어 요청을 프로젝트의 현재 구조와 제작 규칙에 맞는 실행 계획으로 변환하고 Unreal Editor 작업과 검증까지 연결하는 것입니다.

> Applied project: **Project SF** — Unreal Engine 5 기반 개인 게임 프로젝트에서 실제 제작 작업을 통해 Workflow를 검증하고 있습니다.

## Why

AI Coding Agent는 코드 작성에는 강하지만 실제 게임 제작에서는 프로젝트 구조 확인, 제작 규칙 준수, Unreal Asset 변경, 검증, 재사용 가능한 공정 축적이 함께 필요합니다.

이 프로젝트는 **Agent Workflow와 Production Framework를 분리**하고, Agent가 실제 제작 절차와 검증 계약을 따라 작업하도록 만드는 방식으로 접근합니다.

## Architecture

```text
Creator / Natural Language Request
        ↓
Intent Interpretation
        ↓
Execution Mode Routing
        ↓
Context Scope Resolution
        ↓
Focused Repository Inspection
        ↓
Production Framework
Flow → Domain → Stage
        ↓
Skill / Guideline Resolution
        ↓
Prompt Compilation
        ↓
Execution Plan
        ↓
Unreal MCP / Tool Pipeline
        ↓
Validation / Evidence
        ↓
Focused Correction
```

### Agent Workflow

Agent가 **어떻게 작업할 것인가**를 담당합니다.

### Production Framework

게임을 **어떤 절차로 만들 것인가**를 담당합니다.

```text
Domain → Stage → Dependency → Artifact → Review → Integration
```

## Natural Language → Compiled Execution Prompt

사용자는 Tool 이름이나 내부 Schema를 알 필요 없이 자연어로 작업을 요청합니다.

```text
"레벨업 보상 UI 만들어줘.
레벨별 보상을 리스트로 보여주고 현재 레벨은 강조해줘."
```

이 요청을 바로 Unreal Tool 호출로 연결하지 않습니다.

```text
Natural Language
→ Intent Interpretation
→ Context Scope Resolution
→ Existing Pattern / Repository Inspection
→ Flow / Domain / Stage Resolution
→ Skill / Guideline Binding
→ Compiled Execution Prompt
→ Execution Plan
→ MCP Preflight / Execution
→ Intent-based Validation
```

## Context Budget — Resolve Then Expand

Repository 전체를 먼저 읽지 않고 필요한 범위를 우선 조사하고, 근거가 부족할 때만 탐색 범위를 확장합니다.

## Execution Modes

| Mode | Purpose |
| --- | --- |
| `/PRODUCTION` | 실제 게임 코드, 데이터, UI, Asset, 콘텐츠 제작 |
| `/FRAMEWORK` | Agent Workflow, Skill, Script, MCP Tool 및 Production Framework 개선 |
| `/FRIDAY_GOD` | Production 문제를 적절한 계층에서 해결하고 검증 후 제작 공정에 환원 |
| `/PLAN` | 설계 Artifact 작성 |
| `/RESEARCH` | 조사와 근거 수집 |

## Unreal MCP Execution Boundary

```text
MCP Discovery
↓
Capability / Registry Check
↓
Preflight
↓
Dry Run / Preview
↓
Approval
↓
Mutation
↓
Validation
↓
Evidence
```

필요 Capability가 없으면 임시 우회로 계속 진행하지 않고 Capability Gap으로 중단한 뒤 Framework 작업으로 분리합니다.

## Validation

Asset 생성이나 Blueprint Compile만으로 완료 처리하지 않습니다.

```text
Requirement
↓
Implementation
↓
Technical Validation
↓
Intent Validation
↓
Evidence
```

## Current Implementation

- Agent Workflow / Production Framework 책임 분리
- Natural Language Intent / Domain 해석
- Prompt Compilation 및 Trace
- Focused Repository Context Resolution
- Skill / Guideline Resolution
- Production Spec / Job / Capability / Manifest 계약
- MCP Registry / Discovery / Preflight / Dry-run
- UI 자연어 요청 E2E 회귀 Test
- CommonUI / UMG / MVVM MCP 제작 기능
- Terrain / World Production Skill 및 일부 MCP Tool
- Node / PowerShell 기반 Workflow Regression Test
- Production ↔ Framework 개선 루프

## Current R&D

아래 영역은 현재 진행 중이며 완료된 기능으로 표시하지 않습니다.

- 승인 이후 MCP Mutation부터 PIE 시각 검증까지의 완전한 자동 실행 Loop
- World / Region Production Orchestration과 영속 Job State
- 범용 PCG Graph / Placement / Navigation Capability
- 서울 공공 GIS 데이터를 이용한 World Production Pipeline
- 전체 저해상도 World + 대표 상세 Region Vertical Slice
- 실제 Production 반복 실행 기반 비용 / Token / 재사용 효과 측정

## Case Studies

- UI Production
- World Production

## Project SF

이 Workflow는 별도 AI Demo가 아니라 개인 게임 프로젝트 **Project SF**를 실제로 개발하면서 구축하고 있습니다.

- https://github.com/islandnboy/ProjectSF

## Status

**Portfolio / R&D v0.1**
