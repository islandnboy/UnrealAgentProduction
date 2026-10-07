# Server Production Case Study

## Online game service foundation

ProjectSF 서버는 단일 게임 서버 프로세스에 모든 책임을 넣지 않고 **외부 진입, 인증, 영속 게임 상태, 향후 실시간 Gameplay simulation**을 분리합니다.

Agent Workflow는 이 서버 작업에도 동일한 Issue / Step / Skill / Evidence 모델을 적용합니다.

## Target architecture

~~~text
Client
  ↓
Gateway
  ├─ health / failover
  ├─ connection load balancing
  ├─ TLS ingress
  └─ future region routing
  ↓
Account Server Cluster
  ↓
GameServer Directory / Registry
  ↓
Game Server Cluster
  ↓
Repository / Persistence
  ├─ optional Cache
  └─ Primary DB

future:
Game Server ↔ Unreal Dedicated Server
~~~

## Authority boundaries

### Gateway

- public service entry point
- business-opaque forwarding
- health checked AS pool
- connection load balancing
- TLS / connection limits
- future region / maintenance routing

### Account Server

- account / authentication
- login session and GS handoff ticket
- GS selection
- persistent gameplay traffic relay는 하지 않음

### GameServer Directory

- GS registration
- heartbeat / health
- capacity / version metadata
- routing decision

초기에는 AS 내부 logical component로 유지하고 scale 필요 전 별도 service로 강제 분리하지 않습니다.

### Game Server

- Player
- Character
- Inventory
- Quest / Party
- World persistent state
- PlayerScope

### Unreal Dedicated Server — future

- movement
- combat
- GAS
- physics
- realtime gameplay simulation

Persistent Player / World 데이터의 최종 SoT와 realtime simulation authority를 구분합니다.

## Persistence boundary

~~~text
AS / GS
  ↓
Domain Service
  ↓
Repository
  ↓
Cache optional
  ↓
Primary DB
~~~

현재 local implementation에서는 SQLite 기반 authority를 사용하지만 business logic이 특정 DB 구현에 직접 의존하지 않도록 Repository 경계를 둡니다.

Peer AS가 authority SQLite 파일을 직접 열지 않고 RPCNet을 통해 접근하도록 하여 향후 RDB 교체 경계를 보존합니다.

## RPCNet integration

새 Server 통신은 RPCNet protobuf / generated contract를 사용합니다.

~~~text
Transport
→ Connection
→ Session
→ Protocol / Dispatch
→ Generated Stub
→ Final Endpoint
→ Domain Service
→ Repository
~~~

RPCNet은 통신 infrastructure를 제공하고, Server가 Account / Player / World semantics를 소유합니다.

## Local deployment system

개인 개발 환경에서도 실제 service topology를 검증할 수 있도록 다음 기반을 구성했습니다.

- Gateway
- multiple AS / GS profile
- health / readiness
- weighted connection balancing
- TLS ingress
- Launcher / Supervisor
- account registration
- Bot verification
- log / backup / staged update path
- self-contained win-x64 package

운영 scale이 필요하기 전 Redis, microservice, orchestration을 무조건 도입하지 않는 것이 설계 원칙입니다.

## Verification

### Server foundation current-phase gate

현재 Architecture에 기록된 current-phase server gate:

- Server + external Bot PASS
- clean build **0 warnings / 0 errors**
- **52 tests PASS**

### Gateway deployment checkpoint

Gateway / shared coordination / TLS를 확장한 별도 deployment checkpoint에서는:

- clean Release build PASS
- **58-test clean regression PASS**
- weighted live-connection distribution targeted test PASS
- packaged file integrity PASS

58개 regression + targeted test를 하나의 59-test full-suite 실행으로 과장하지 않고 별도 검증으로 기록합니다.

## Actual Unreal Client flow

후속 Client integration에서는 실제 UE Client가 서버 흐름을 소비합니다.

~~~text
Entry
→ Login UI
→ Gateway
→ Account authentication
→ automatic GS admission
→ initial PlayerScope
→ NeoSeoul OpenLevel
~~~

GameInstance가 LoginFlowCoordinator를 소유하고, AS / GS ConnectionHandler를 분리하며 PlayerScopeSubsystem이 인증/PlayerScope 상태를 맵 이동 동안 유지합니다.

실제 검증에는 다음이 포함됩니다.

- SFEditor UHT / C++ / DLL build PASS
- real Gateway / AS / GS process execution
- login widget submit
- authentication failure
- GS disconnect cleanup
- relogin
- server restart
- initial PlayerScope application
- Entry → NeoSeoul travel

## Explicit limits

현재 포트폴리오에서 완료된 것으로 주장하지 않는 항목:

- public WAN Client
- production HA
- shared production RDB
- production Redis/cache deployment
- packaged-game end-to-end
- Unreal Dedicated Server gameplay replication
- multi-region production deployment

## Agent Workflow connection

~~~text
Issue / Goal
→ Current Source of Truth
→ server-feature-production Skill
→ Architecture / authority inspection
→ RPCNet contract impact
→ implementation
→ build / deterministic tests
→ Bot / real process verification
→ Client integration when required
→ Evidence
~~~

서버 기능이 추가될 때 topology 전체를 매번 다시 설계하지 않고 기존 Authority와 Extension Point 안에서 확장합니다.

## Portfolio point

이 Case Study의 핵심은 단순한 로그인 서버 구현이 아닙니다.

**Gateway / Account / Game persistent authority / future Dedicated Server를 분리하고, 실제 Bot과 Unreal Client가 동일 protocol contract를 통해 끝까지 연결되는 온라인 게임 서버 기반을 단계적으로 구축하고 검증한 것**입니다.
