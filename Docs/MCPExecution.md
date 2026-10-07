# Unreal MCP Execution

ProjectSF의 Unreal mutation은 **UE 5.8 Official Unreal MCP 우선**입니다.

## Execution boundary

~~~text
Required production effect
↓
Live MCP discovery
↓
Toolset / schema confirmation
↓
Capability / binding check
↓
Preflight / preview when applicable
↓
Mutation
↓
Readback / product validation
↓
Evidence
~~~

## Principles

- 과거 Tool ID를 Skill에 장기 고정하지 않습니다.
- 현재 live schema에서 실제 capability를 확인합니다.
- 세션에 namespace가 보이지 않는 것만으로 capability 부재를 선언하지 않습니다.
- MCP 호출 성공과 제품 성공을 분리합니다.
- 현재 입력과 대상이 명확하지 않으면 mutation하지 않습니다.
- 기존 사람 편집과 source-derived 결과를 보호합니다.

## Capability gap

필요한 Unreal 효과가 없을 때 작업 전용 Python, legacy localhost bridge, Editor Utility, Commandlet, 직접 HTTP, binary patch를 임시 mutation fallback으로 사용하지 않습니다.

재사용 가능한 capability가 실제로 필요하면 ProductionEvolution을 통해 최소 확장으로 다룹니다.

## Observation

관측도 가능한 한 Official MCP를 먼저 사용합니다.

- actor / component readback
- world / geometry validation
- save / reload state
- editor / viewport capture
- PIE or runtime checks where required

MCP로 얻을 수 없는 UI 관측이나 입력만 별도 interaction 수단을 검토하며, 관측 fallback을 mutation 우회로로 확대하지 않습니다.

## Validation

대표적인 검증 계층:

1. Tool execution
2. Asset / object identity
3. compile / save / readback
4. structural correctness
5. runtime / PIE behavior
6. visual / intent quality
7. Owner acceptance when required

각 계층은 서로 대체하지 않습니다.
