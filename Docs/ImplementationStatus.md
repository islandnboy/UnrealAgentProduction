# Implementation Status

이 문서는 실제 ProjectSF 운영 구조와 공개 포트폴리오 설명을 맞추기 위한 상태표입니다.

## Implemented and actively used

### Workflow

- repository `AGENTS.md` bootstrap gate
- Current Source of Truth Gate
- Issue start / resume contract
- Issue / Recipe partition gate
- TaskExecution
- ProductionConvergence
- ProductionEvolution
- ExecutionObservability
- ContextBudgetPolicy

### Rules and Skills

- common resource production rule
- programming rule
- verification depth rule
- repository-discoverable Skill packages
- thin `.agents/skills` entrypoints
- UI production / architecture
- terrain / landscape
- road production
- water terrain preparation / water production
- world structure / validation
- server feature production / bot verification
- issue context sync

### Runtime

`Tools/AgentPipeline` currently separates:

- Config
- Registry
- Schemas
- Scripts
- Templates
- Examples
- Tests
- Runtime contract

### Production state

- `Production/Data`
- `Production/Evidence`
- Issue-driven persistent task state
- human / AI shared production state
- input revision and validation evidence

## Engineering systems built with the workflow

### RPCNet

- reusable Unreal network Runtime
- TCP / WebSocket / Mock / Memory transport
- Session / Codec / Proxy / Stub boundary
- C# ProtocolGenerator
- generated / handwritten ownership separation
- ProjectSF Consumer Integration boundary
- framework boundary validator
- checkpoint: 37 tests + actual Unreal interoperability PASS

### Online Server

- Gateway / AS / GS topology
- GS Directory / Registry
- Player / World / PlayerScope persistent authority
- Repository / persistence boundary
- weighted Gateway connection balancing
- TLS ingress
- Launcher / Bot verification
- current-phase clean build 0 warnings/errors + 52 tests PASS
- actual UE Entry → Login → GS → PlayerScope → NeoSeoul integration

### DataForge

- standalone Windows GUI + CLI shared Core
- XLSX / XLSM DataTable Authoring SoT
- incremental dataset-level dirty detection
- SFDataBuildCommandlet Bake / Readback
- generated Server JSON parity
- DA / PrimaryDataAsset / INI native read-only extraction
- rollback / last-successful publication gate
- first vertical slice parity PASS
- 25 Core regression tests PASS

### Unreal production

Current applied areas include:

- terrain and landscape
- road batch production
- water / river / lake production
- world structure and validation
- UI production
- server and client-online integration
- data production

## Active R&D

- structured WorkflowSnapshot / execution materialization without restoring the old keyword Prompt Compiler
- larger-scale city production orchestration
- production performance measurement for road / water / world output
- more reusable batch execution around verified Recipes
- stronger human ↔ AI round-trip editing evidence
- DataForge advanced data types and production consumer rollout
- production-grade Server HA / RDB / WAN deployment
- continued reduction of duplicated rules and stale workflow paths

## Not claimed

이 저장소는 다음을 완료된 범용 제품으로 주장하지 않습니다.

- fully autonomous game development
- universal Unreal capability coverage
- zero-review visual production
- arbitrary project portability without project-specific Rules / Skills
- production-grade multi-region Server deployment
- DataForge support for every Unreal data shape
- tool success as proof of product quality
