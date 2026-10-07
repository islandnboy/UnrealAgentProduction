---
name: road-production
description: Produce and repair editable, regenerable road networks from approved road sources.
---

# Road Production

승인된 도로 원천과 현재 작업 조건을 해석해 Road Design Input을 만들고, 현재 Unreal 환경에서 사용할 수 있는 capability를 탐색해 적절한 표현을 선택·생성·검증한다.

## Plan

- 특정 원천 형식이나 표현 방식을 canonical contract로 고정하지 않는다.
- source identity와 연결 관계를 추적할 수 있어야 한다.
- 생성 전에 목표 범위, 보호 대상, 편집 지점, 재생성 경계를 명확히 한다.
- 현재 단계의 형상 기준을 정하고 이미 검증된 Geometry를 불필요하게 다시 원천 파싱하지 않는다.
- 도로명/등급·폭/차선 등 현재 설계에 부족한 의미만 보충한다.

## Select representation

- 현재 Unreal 환경에서 사용할 수 있는 capability와 재사용 가능한 표현을 먼저 탐색한다.
- 입력 호환성, 편집 가능성, 생성 소유권, 재생성 범위와 검증 가능성을 기준으로 표현을 선택한다.
- 특정 Tool, graph, asset 또는 구현 방식을 Skill 계약에 고정하지 않는다.

## Produce

- Road Design Input과 생성 출력을 분리한다.
- 도로 ID/이름·등급·경로·폭/차선·예외 override를 입력으로 유지한다.
- 첫 대표 구간을 실제 도로 결과로 제작하고 형상·접지·연결 검증을 통과한 뒤 확장한다.
- 부분 재생성이 다른 source-derived 결과나 수작업 결과를 덮어쓰지 않게 한다.

## Output and scale

- 편집·재생성 입력과 runtime 출력을 구분한다.
- 넓은 범위로 확장하기 전에 대표 구역에서 Actor / component / geometry / collision / streaming 비용을 관측한다.
- 생성 수단과 최종 저장 표현은 달라도 된다.
- 도시 전체를 하나의 mesh로 합치거나 타일마다 불필요한 고유 asset을 생성하는 구조를 피한다.

## Validate

- technical correctness
- persistence
- visual readability
- regeneration safety
- Owner acceptance

생성 성공이나 일부 수치 검증만으로 전체 품질을 PASS하지 않는다.

## Invariants

- source representation != road production contract
- terrain grounding != road design elevation
- technical validity != visual readability
- generated output != human-editable design input
- partial regeneration must preserve unaffected results
