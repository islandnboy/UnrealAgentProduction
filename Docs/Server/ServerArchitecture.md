# Project SF Server Architecture

> Status: **Public Architecture Reference / 2026-10-07 Snapshot**
>
> ProjectSF의 기존 ServerArchitecture 문서에서 Topology·책임·Authority·데이터 경계 설계 부분을 발췌한 공개 참고본입니다. 작업 저장소의 단일 원본과 구분하며, 목표 구조·초기 단계 설명은 현재 구현 완료 범위를 의미하지 않습니다.
>
> 현재 구현과 검증 결과: [Server Production Case Study](../../CaseStudies/ServerProduction.md). Gateway 확장·로컬 배포: [Gateway Deployment Design](GatewayDeploymentDesign.md).

## 1. 목표

Project SF의 온라인 서버는 Client의 진입, 계정 인증, 게임 서비스 상태, 영속 데이터, 향후 Unreal Dedicated Server의 실시간 Gameplay Authority를 분리한다.

현재 Foundation은 작게 시작하되, 이후 다중 AS/GS와 Multi-Region으로 확장해도 Client 및 Domain Service 계약을 불필요하게 변경하지 않는 것을 목표로 한다.

## 2. Target Topology

```text
Client
  ↓
Gateway
  ├─ future: Global / Region Routing
  ├─ Load Balancing
  ├─ Health Check / Failover
  ├─ TLS / connection limits; future: Maintenance Routing
  ↓
Account Server Cluster
  ↓
GameServer Directory / Registry
  ↓
Game Server Cluster
  ↓
Repository / Persistence Boundary
  ├─ Cache            (Redis-class, optional)
  └─ Primary DB       (RDB-class, Source of Truth)

future:
Game Server ↔ Unreal Dedicated Server
```

### Multi-Region Expansion

```text
Client
  ↓
Gateway
  ↓
Region Selection
  ├─ KR → Regional AS/GS
  ├─ JP → Regional AS/GS
  └─ US → Regional AS/GS
```

Gateway는 외부 진입 계층의 상위 개념이다. Load Balancing은 Gateway가 제공하는 capability 중 하나이며 별도 제품 계약으로 노출하지 않는다.

초기 구현은 단일 Region / 단일 AS 기준으로 단순화할 수 있다.

```text
Client
  ↓
Gateway
  ↓
Configured AS
```

## 3. Responsibility / Authority

### Gateway

- Client가 아는 public service entry point다.
- 현재는 health-checked AS pool로 연결을 분산한다. 단일 configured AS는 호환 경로로 유지한다.
- Account / Player / World 비즈니스 로직을 소유하지 않는다.
- balancing, health/failover, TLS, connection limits를 제공하며 향후 Region routing과 version/maintenance routing을 확장한다.

### Account Server (AS)

- Account / Authentication
- Login session 또는 handoff credential 발급
- GameServer Directory를 통한 접속 대상 선택
- 로그인 이후의 지속적인 게임 트래픽 중계 서버가 되지 않는다.
- 가능한 한 stateless하게 유지한다.

### GameServer Directory / Registry

- GS registration / heartbeat / health / capacity metadata
- 접속 가능한 GS 선택
- 초기에는 AS 내부 논리 컴포넌트일 수 있다.
- Scale 요구가 생기기 전 별도 서비스 분리를 강제하지 않는다.

### Game Server (GS)

- Player / Character / Inventory / Quest / Party / World State / PlayerScope 등 persistent game content authority
- active player working state
- World 진입 및 persistent content service coordination
- Unreal Dedicated Server의 실시간 Gameplay Authority와 분리한다.

### Dedicated Server (DS, future)

- Unreal Gameplay Framework authority
- movement / combat / GAS / physics 등 실시간 simulation
- persistent content의 최종 SoT가 아니다.

## 4. Persistence

AS/GS의 비즈니스 로직은 Redis/PostgreSQL/MySQL/SQLite 같은 구체 backend를 직접 알지 않는다.

```text
AS / GS
  ↓
Service
  ↓
Repository / Persistence Boundary
  ↓
Cache (optional)
  ↓
Primary DB
```

일반적인 cache-aside 방향을 기본으로 한다.

```text
Read:
Repository
  → Cache hit: return
  → Cache miss: DB read → cache fill → return

Write:
Repository
  → DB write
  → cache invalidate/update
```

원칙:

- Primary DB가 persistent data의 최종 Source of Truth다.
- Cache 장애가 영구 Player Data 유실로 이어져서는 안 된다.
- 초기 개발은 InMemory / File / SQLite 등 lightweight backend를 사용할 수 있다.
- Redis와 운영 RDB 도입은 Repository/Persistence 경계 뒤에서 교체한다.
- 별도의 custom “DB Cache Server”를 선행 구축하지 않는다. 실제 scale/ownership 요구가 생길 때만 Data Service 분리를 검토한다.

## 5. Network / Protocol Boundary

```text
Transport
  ↓
Connection
  ↓
Session
  ↓
Protocol / Dispatch
  ↓
Handwritten Endpoint
  ↓
Domain Service
  ↓
Repository
```

- Transport와 authenticated Session을 구분한다.
- Endpoint/Service는 특정 socket 구현을 직접 참조하지 않는다.
- protobuf schema와 generation configuration은 Project SF protocol contract의 Source다.
- Generated code와 handwritten Final Endpoint/Service의 ownership을 분리한다.
- RPCNet Framework는 Project SF의 Login/Inventory/World 같은 Domain 의미를 소유하지 않는다.

관련 RPCNet 경계는 [RPCNet Case Study](../../CaseStudies/RPCNet.md)를 따른다.

## 6. Initial Foundation Scope

초기 Server Foundation의 제품 목표는 **서버 프로세스를 실행하고 Client/Bot이 Gateway를 통해 AS Login을 성공시키는 것**이다.

```text
Client/Bot
  ↓
Gateway
  ↓
AS
  ↓
Login Result
```

이 단계에서 필요한 기반:

- Gateway / AS 실행
- 향후 GS를 수용할 buildable boundary
- protobuf / RPCNet protocol runtime
- Connection / Session / Dispatch
- Account persistence boundary
- 실제 Login success/failure verification

다음 항목은 Server Foundation Login 완료의 필수 조건이 아니다.

- World Entry
- PlayerScope initial sync
- Inventory / Quest / Party content
- Unreal Dedicated Server gameplay
- Multi-Region production deployment
- 실제 Redis / production RDB deployment

World Entry와 PlayerScope는 후속 Game Session / Content 단계에서 이 문서를 확장하지 않고 소비한다.

## 7. Local vs Production

### Local / Early Development

```text
Bot or Client
  ↓
Gateway (single AS passthrough)
  ↓
AS
  ↓
optional GS
  ↓
lightweight persistence
```

### Future Production

```text
Client
  ↓
Gateway
  ↓
Region Routing / Load Balancing
  ↓
AS Cluster
  ↓
GS Directory
  ↓
GS Cluster
  ↓
Cache + Primary DB
  ↕
DS fleet as required
```

운영 확장 요구가 생기기 전에 microservice, Redis, orchestration, 별도 Registry service를 강제하지 않는다.


## 공개 참고본의 범위

원본의 Topology·Authority·Persistence·Protocol 경계와 단계별 설계를 선별했습니다. 비공개 Issue·원본 Evidence·세부 구현 추적은 포함하지 않습니다.

원본의 Local / Early Development와 Initial Foundation Scope는 초기 단계 설명입니다. 현재 공개 사례에는 Gateway AS pool·Coordination·로컬 UE Client 연동까지의 후속 검증을 별도로 정리합니다. Multi-Region·Unreal Dedicated Server·운영 HA 등은 향후 범위로 구분합니다.
