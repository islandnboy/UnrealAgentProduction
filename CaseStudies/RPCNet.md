# RPCNet Case Study

## Reusable network framework inside a game project

RPCNet은 ProjectSF의 Client / Server 통신을 위해 개발했지만, 게임의 Login·Inventory·World 같은 Domain 의미와 분리한 **재사용 가능한 Network Framework**입니다.

핵심 목표는 프로젝트 코드에 socket / packet boilerplate를 반복해서 만들지 않고, **Runtime + Protocol Code Generation + Consumer Integration**의 경계를 명확히 하는 것입니다.

## Problem

게임 네트워크 구현이 프로젝트 전용 코드와 강하게 결합되면 다음 문제가 생깁니다.

- Client와 Server protocol boilerplate가 반복됨
- transport 변경이 gameplay 코드에 전파됨
- generated code와 handwritten code의 ownership이 섞임
- 테스트를 위해 항상 실제 Server가 필요함
- 다른 프로젝트에 framework를 재사용하기 어려움

RPCNet은 이 경계를 분리합니다.

## Architecture

~~~text
RPCNet/
├─ Runtime/
│  └─ Unreal/RPCNet
│     ├─ Runtime
│     ├─ Session
│     ├─ Transport
│     ├─ Packet Codec / Envelope
│     └─ Proxy / Stub base
│
├─ Toolchain/
│  ├─ ProtocolGenerator
│  └─ PluginInstaller
│
└─ Integration/
   └─ ProjectSF
      ├─ Protocol Schema
      ├─ Generation Configuration
      └─ Consumer Targets
~~~

### Runtime

~~~text
NetworkRuntimeSubsystem
        ↓
NetworkRuntime
        ↓
NetworkSession
        ↓
INetworkTransport
   ├─ TCP
   ├─ WebSocket
   ├─ Mock
   └─ Memory
        ↓
Packet Codec / Envelope
~~~

Mock / Memory Transport를 Framework 내부에 두어 실제 서버 없이도 상위 Network 흐름을 검증할 수 있습니다.

### Protocol Generator

Protocol Generator는 ProjectSF의 protocol 의미를 직접 알지 않습니다.

~~~text
Consumer Schema + Generation Config
              ↓
      RPCNet ProtocolGenerator
              ↓
      Generated Consumer Code
          ↙             ↘
       Client          Server
~~~

Generator Core가 Login / Inventory / C2AS 같은 프로젝트 Domain을 하드코딩하지 않고, Consumer Integration이 실제 schema와 target을 선택합니다.

## Ownership boundary

### RPCNet owns

- transport abstraction
- connection / session lifecycle
- packet envelope / codec
- Proxy / Stub extension base
- protocol parser / validation / emitter infrastructure
- Unreal runtime plugin
- plugin installer
- framework boundary validation

### ProjectSF owns

- protobuf schema
- message IDs
- Login / Game / Inventory semantics
- endpoint policy
- generated target selection
- handwritten Endpoint / Service
- gameplay integration

핵심 규칙:

~~~text
RPCNet = communication infrastructure
ProjectSF = product protocol semantics
~~~

## Generated vs handwritten code

Generated code를 최종 business implementation으로 사용하지 않습니다.

~~~text
Protocol Schema
→ Generated DTO / Proxy / Stub
→ Handwritten Final Endpoint
→ Domain Service
~~~

이 구조를 통해 protocol 재생성 시 handwritten logic을 보존합니다.

## Framework extraction boundary

RPCNet은 현재 ProjectSF monorepo 안에 있지만 `RPCNet/`을 독립적인 Framework Boundary로 유지합니다.

- canonical Unreal plugin source는 하나
- Client plugin copy는 installer output
- framework source에서 Client / Server gameplay code 역참조 금지
- Project-specific integration은 별도 디렉터리
- `Validate-Boundary.ps1`로 boundary 검사

따라서 필요하면 Runtime / Toolchain을 별도 repository나 SDK로 추출할 수 있는 구조를 유지합니다.

## Validation evidence

ProjectSF server foundation의 RPCNet 관련 검증 checkpoint에서 다음을 확인했습니다.

- stable code regeneration
- generated Stub → handwritten Final Endpoint routing
- route / kind / direction rejection
- invalid input / replay / epoch / length handling
- real TCP connection / session cleanup
- Client-like packets through Gateway / AS / independent GS
- **37 tests PASS**
- **actual Unreal Client interoperability PASS**

이 수치는 해당 validation checkpoint의 결과이며 이후 모든 기능을 포괄하는 숫자로 사용하지 않습니다.

## Agent Workflow connection

RPCNet 작업도 일반 코드 생성과 다르게 다음 계약을 따릅니다.

~~~text
Issue Goal
→ current RPCNet / consumer boundary inspection
→ required protocol effect
→ schema / generator / runtime impact
→ implementation
→ regeneration
→ boundary validation
→ Client / Server interoperability
→ Evidence
~~~

Agent가 새 기능을 구현할 때 Runtime에 Project-specific 의미를 밀어 넣지 않는지까지 Acceptance로 검증합니다.

## Portfolio point

RPCNet에서 보여주고 싶은 것은 “TCP를 구현했다”가 아닙니다.

**게임 프로젝트에서 반복되는 네트워크 코드를 Framework와 Consumer 계약으로 분리하고, 코드 생성·Runtime·Mock·실제 Client/Server interop까지 하나의 검증 가능한 개발 체계로 만든 것**이 핵심입니다.
