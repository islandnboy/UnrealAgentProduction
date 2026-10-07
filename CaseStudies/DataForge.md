# DataForge Case Study

## Creator-facing game data production tool

DataForge는 게임 데이터를 코드나 Unreal Editor에 직접 반복 입력하지 않고, **기획자가 익숙한 authoring source를 유지하면서 Client와 Server 산출물을 같은 데이터 의미에서 생성·검증하는 제작 툴**입니다.

독립 실행형 GUI와 CLI가 같은 Core를 사용합니다.

📄 [DataForge 사용 가이드 (PDF)](../Docs/Guides/DataForgeUserGuide.pdf) — 실제 화면과 DT·DA·Config 작업, 결과 확인·오류 대응·실행 방법을 담은 7페이지 가이드입니다. (2026-10-07 구현 기준)

## Problem

게임 데이터 제작에는 자주 다음 문제가 생깁니다.

- 기획 데이터와 Unreal DataTable이 서로 달라짐
- Server JSON을 별도로 관리하면서 값이 어긋남
- 전체 데이터를 매번 rebuild함
- generated UAsset을 사람이 직접 고쳐 Source of Truth가 모호해짐
- Unreal 고유 DataAsset / Config 의미를 외부 툴이 잘못 재구현함
- invalid source가 기존 정상 artifact를 덮어씀

DataForge는 Source of Truth와 generated artifact의 방향을 명확히 합니다.

## Source of Truth matrix

| Data kind | Authoring SoT | DataForge role |
| --- | --- | --- |
| DataTable | XLSX / XLSM | validate, normalize, build, bake, verify |
| DataAsset / PrimaryDataAsset | Unreal UAsset | native read-only extract / inspect |
| INI Config | Unreal Config | native read-only extract / inspect |

V1에서 Excel authoring은 DataTable에만 적용합니다.

DA / INI를 억지로 Excel로 변환하거나 자동 write-back하지 않습니다.

## DataTable pipeline

~~~text
XLSX / XLSM
    ↓
DataForge
  parse / normalize / validate
    ↓
normalized build artifact
   ↙                 ↘
Server JSON       UE Build JSON
                      ↓
             SFDataBuildCommandlet
                Bake UDataTable
                      ↓
              separate Readback
                      ↓
                 parity verify
                      ↓
                  publish
~~~

Client와 Server가 서로 다른 변환 로직을 가지지 않고 동일 normalized data 의미에서 파생됩니다.

## Native DA / Config pipeline

~~~text
UDataAsset / PrimaryDataAsset
          ↓
SFDataBuildCommandlet Extract
          ↓
       DataForge

Unreal Config
     ↓
GConfig native read
     ↓
DataForge inspect / extract
~~~

DataForge가 `.uasset` binary format이나 Unreal Config merge semantics를 Python으로 다시 구현하지 않습니다.

Unreal이 자신의 데이터를 직접 해석하고 DataForge는 그 결과를 소비합니다.

## Creator-facing GUI

Windows x64에서는 `DataForge.exe`를 직접 실행할 수 있으며 Python 설치가 필요하지 않습니다.

GUI는 다음 작업을 제공합니다.

- DT / DA / Config tabs
- Source / Dataset 목록
- Dirty State
- Schema Status
- Warning / Error
- Last successful build
- Refresh
- Build Selected
- Build Changed
- Rebuild All
- Extract Selected
- Diff / Results / Diagnostics
- Template / Migration support

기획자는 Excel에서 데이터를 작성하고 DataForge에서 변경 대상을 확인한 뒤 필요한 dataset만 build할 수 있습니다.

## Incremental build

Refresh가 전체 rebuild를 의미하지 않습니다.

~~~text
Git changed-file candidates
        ↓
changed sources only
        ↓
dataset normalize
        ↓
semantic fingerprint
        ↓
compare last successful manifest
        ↓
Clean / New / Modified /
SchemaChanged / DependencyDirty /
Removed / Invalid
~~~

Git은 후보 범위를 줄이는 데 사용하고 최종 dirty 판정은 dataset semantic diff로 수행합니다.

같은 workbook 안에서도 dataset 단위로 fingerprint를 계산합니다.

`Build Changed`는 실제 영향받은 dataset과 필수 dependency만 처리합니다.

## Safe publication

Generated 결과는 바로 publish하지 않습니다.

~~~text
Build
→ PENDING_UE_PARITY
→ Unreal Bake
→ separate Readback
→ semantic parity
→ promote Server JSON / baseline
~~~

실패하면 기존 정상 UAsset / Server JSON / last-successful baseline을 보존하거나 복구합니다.

Refresh는 read-only이며 삭제된 source를 발견했다고 기존 artifact를 자동 삭제하지 않습니다.

## First real vertical slice

ProjectSF의 기존 StatGrowth DataTable을 첫 실제 slice로 사용했습니다.

~~~text
Existing UDataTable
→ migration candidate
→ Creator approval
→ XLSX Authoring SoT
→ DataForge build
→ SFDataBuildCommandlet bake
→ UDataTable readback
→ Server JSON
→ parity
~~~

검증 결과:

- migration adoption APPROVED
- original → source → baked UDataTable parity PASS
- baked UDataTable → Server JSON parity PASS
- separate Unreal process readback PASS
- invalid deserialize 시 기존 asset hash 보존
- unused authored field는 warning 처리
- missing Unreal field는 UE default 적용 가능 시 info / warning
- **25 core regression tests PASS**

## Native source verification

같은 DataForge entrypoint에서 추가로 확인했습니다.

- existing DataTable native extraction PASS
- PrimaryDataAsset read-only extraction
- Unreal Config effective values via GConfig
- repeated extraction canonical output identical
- source UAsset / INI bytes preserved

## Current limits

아직 완료된 범위로 주장하지 않는 항목:

- advanced nested / array / GameplayTag / reference adapters
- production consumer switch
- Server runtime load / packaging
- full template / migration feature breadth
- GUI visual usability review

현재 GUI 실제 실행과 기능 경로는 검증했지만 최종 UX 품질 평가는 별도입니다.

## Agent Workflow connection

DataForge 자체도 Agent Workflow의 중요한 예입니다.

처음부터 모든 데이터를 지원하는 거대한 시스템을 만든 것이 아니라:

~~~text
Data Production Goal
→ existing data contract inspect
→ first representative DataTable
→ real vertical slice
→ parity / rollback validation
→ Creator adoption
→ DA / INI native boundary extension
→ GUI / guide
→ reusable Recipe
~~~

실제 제작 결과를 바탕으로 도구와 Recipe를 확장했습니다.

## Portfolio point

DataForge에서 보여주고 싶은 것은 “Excel importer를 만들었다”가 아닙니다.

**기획자 authoring, Unreal runtime artifact, Server data를 하나의 검증 가능한 production pipeline으로 연결하고, incremental build·rollback·native readback까지 포함한 데이터 제작 체계를 만든 것**이 핵심입니다.
