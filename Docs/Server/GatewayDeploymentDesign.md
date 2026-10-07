# Gateway LB와 개인 PC 설치·런처 설계안

> Public Design Reference / 2026-10-07 Snapshot. 기존 배포 설계안을 공개 참고본으로 정리했습니다. 아래 Client 관련 상태는 이 설계안의 당시 검증 범위이며, 후속 로컬 UE Client 연동은 [Server Production Case Study](../../CaseStudies/ServerProduction.md)에서 구분해 확인합니다.

상태: 개인 PC 로컬 구현·봇 검증 반영. 실제 인터넷 접속·공유기/방화벽 적용·분산 HA·Client는 NOT_TESTED.
관련: [Server Architecture](ServerArchitecture.md). Client 연동은 별도 후속 작업으로 검증합니다.
기존 Foundation 증거와 Gateway/배포 증거는 별도로 추적한다. 실제 설치·실행은 작업 저장소의 운영 안내를 따른다.

## 목표와 범위

Gateway를 AS/GS보다 먼저 실행하고, 준비된 AS에 새 로그인 연결을 분산한다.
개인 Windows PC에서 설치·시작·종료·업데이트·로그·Bot 검증을 한 런처로 수행한다.
새 서버 간 제어 요청은 기존 RPCNet protobuf와 생성 파이프라인을 사용한다.
Account는 AS, Player/World는 GS가 소유한다. Gateway는 Account 인증이나 DB를 소유하지 않는다.
서버·런처·설치 도구를 구현했다. Client·공유기·방화벽·Windows service 등록은 변경하지 않았다.

## 토폴로지와 배포 프로필

~~~text
Bot / 향후 Client
  -> Gateway :6000 (공개 TLS 진입, AS 연결 LB)
      -> AS public RPC ingress :5100 (개인 PC에서는 loopback)
           -> AS Coordination 모듈 (내부 RPCNet listener, 제어 전용)
           -> Account DB
  -> 배정된 GS :7100 (공개 TLS 진입)
      -> AS Coordination (ticket / registry / reservation / admission lease)
      -> AS internal bootstrap (최초 legacy seed 조회)
      -> 해당 GS의 Player DB

Launcher -> 각 프로세스의 내부 RPCNet lifecycle / readiness
~~~

- Local 프로필: Gateway 1, AS 1, GS 1. Coordination은 AS 안의 논리 모듈로 유지한다.
  Account/Player SQLite를 그대로 사용하고 새 서버 프로세스는 필수가 아니다.
- Pool 프로필: Gateway 1, AS N, GS N. AS 중 명시적으로 지정한 1개가 Coordination authority다.
  다른 AS/GS는 그 authority에 RPCNet으로 요청한다. 개인 PC 초기 Pool은 RpcNetAccountRepository로 지정 AS의 저장소에 접근한다.
  초기 로컬 제작 계약에 따라 운영 RDB를 강제하지 않는다. peer는 SQLite를 열거나 migration을 실행하지 않는다.
  Local SQLite 파일을 여러 AS가 공유하는 방식을 Pool 완료로 인정하지 않는다.
- 단일 Coordination authority는 단일 장애점이다. 개인 PC 단계에서 자동 leader 선출,
  다중 Gateway HA, Coordination 자동 승격은 범위 밖이다.
  나중에 동일 인터페이스 뒤에 공유 저장소/독립 서비스/복제 구조를 붙일 수 있다.
- GS 직접 접속을 유지한다. 모든 GS를 Gateway로 중계하는 별도 토폴로지는 이번 기본안에 포함하지 않는다.

## Gateway 시작과 상태

Gateway는 AS가 없어도 listener를 먼저 연다. Listening을 서비스 Ready로 표시하지 않는다.

| 상태 | 의미 |
| --- | --- |
| Starting | 설정 검증 / listener 생성 |
| ListeningNoBackend | 포트는 열렸으나 Ready AS 없음 |
| Ready | Ready AS 1개 이상, 새 로그인 연결 수용 가능 |
| Degraded | 일부 AS 장애 또는 로그인 의존성 미준비 |
| Draining | 신규 연결 거절, 기존 연결 종료 대기 |
| Stopped / Faulted | 정상 종료 / 복구 대상 오류 |

Ready AS가 없으면 연결을 즉시 종료한다. 무한 대기 큐를 만들지 않는다.
opaque relay를 유지하므로 Gateway가 AS 로그인 응답을 위조하지 않는다.
Bot/향후 Client는 연결 종료를 일시적 서비스 미준비로 처리하고 bounded backoff로 재접속한다.
런처는 RPCNet 상태 조회로 미준비 원인을 별도로 보여준다.

## AS Pool과 LB 정책

초기 AS 후보 목록은 설치 설정의 ServerId, private host/port, weight로 명시한다.
Gateway가 DB나 동적 서버 등록 authority를 맡지 않는다.
후보는 TCP connect만으로 Ready가 되지 않으며, 인증된 내부 RPCNet Health 응답으로 검증한다.
Health는 process instance ID, version, readiness, draining, dependency 상태를 반환한다.
AS ingress와 internal listener가 동일 실행 instance인지 확인해 오래된 프로세스를 배제한다.

초기 설계값: health interval 2초, timeout 1초, 성공 2회 후 편입, 실패 3회 후 제외.
Draining / 명시적 NotReady는 즉시 제외한다. 값은 설정 가능하며 장애 시험으로 조정한다.
AS 자체 연결 실패는 즉시 해당 후보의 신규 선택을 차단한다.

선택 정책은 weighted least-connections다. active/weight가 가장 낮은 AS를 고르고,
동률이면 순환한다. 선택과 active reservation은 원자적으로 처리하며 연결 종료 때 반환한다.
로그인 한 TCP 연결은 종료까지 같은 AS를 유지한다. protobuf 요청별 재분산은 하지 않는다.
전체 upstream connect deadline 5초 안에서 서로 다른 후보에 최대 2회 연결을 시도한다.
클라이언트 바이트를 upstream으로 전달하기 전 connect 실패에만 다른 AS를 시도한다.
전달 후 장애는 연결을 닫고 새 로그인으로 복구하며 기존 요청을 자동 replay하지 않는다.

구현 모듈: AsPool(health/selection), AsPassthrough(relay), ServiceLifecycle, LifecycleEndpoint.
연결 수 / per-IP 제한, handshake timeout, 메시지 크기 제한을 둔다.
로그에는 connection ID, backend ID, 상태 전이, 종료 사유를 기록하며 비밀번호/티켓/payload는 제외한다.

## AS 공유 상태와 Coordination

현재 InMemoryTicketStore와 GSRegistry는 각 AS 인스턴스에 묶여 있다.
그 상태로 AS N개를 단순 LB하면 티켓 소비와 GS 선택 결과가 일치하지 않는다.

Coordination authority에 다음 기능을 모은다.

- Directory: ServerId + process instance ID, endpoint, version, health, capacity, draining.
- Handoff: 인증된 AS만 티켓 발급, 대상 GS만 원자적 1회 소비.
- Reservations: 배정 중인 접속을 수용 인원에 포함; 만료/실패/완료 시 회수.
- Admission leases: 계정별 active session의 전역 중복 진입 방지.
- Player owner map: Account/World -> durable GS storage owner의 영속 매핑.

티켓/예약/lease/Directory는 단일 authority 안에서 원자적 상태 전이를 제공한다.
GS heartbeat의 대략적 player count를 admission의 유일한 정합성 근거로 쓰지 않는다.
티켓 소비 시 reservation을 임시 admission lease로 바꾸고, GS가 Player 로드 후 ConfirmEntry한다.
로드/송신 실패는 lease를 반환하고 티켓을 되살리지 않는다. 재로그인이 필요하다.
GS는 lease를 갱신하며 만료된 lease로 새 content mutation을 허용하지 않는다.
authority 재시작 시 generation을 변경하고 이전 티켓/lease를 무효화한다.
GS는 제어 단절 동안 새 진입과 content mutation을 차단하고 읽기만 허용한다.
복구 시 이전 session은 종료하고 재로그인한다. 자동 session 이동을 보장하지 않는다.

영속 owner map은 Coordination 전용 저장소에 보관하며 ephemeral state와 분리한다.
향후 lease 기반 서버 간 쓰기 이전에는 fencing token을 저장소에서도 강제해야 한다.

## GS 배정과 Player 데이터

GS 선택은 Gateway의 TCP LB와 별개다. AS가 인증 후 Coordination에 배정을 요청한다.

1. 기존 owner map이 있으면 그 저장소를 소유한 GS에 배정한다.
2. 기존 owner가 Offline / Full이면 새 GS에 임의 배정하지 않고 일시적 실패를 반환한다.
3. 신규 Account는 호환 World/version의 Ready GS 중 (active + reserved)/capacity가 가장 낮은 곳을 고른다.
4. owner map 최초 등록은 원자적으로 수행한다. 동시 로그인도 같은 owner로 수렴한다.
5. 안정된 owner ID와 재시작마다 바뀌는 process instance ID를 구분한다.

현재 GS별 SQLite에 Player가 있으므로 단순 GS least-load 재배정은 데이터 분기를 만든다.
owner 변경은 검증된 데이터 이관 또는 공용 Player 저장소 도입 후 별도 작업으로 수행한다.
GS session은 원래 연결에 고정한다. GS 장애 시 다른 GS로 자동 live migration하지 않는다.

## 내부 RPCNet 계약과 보안 경계

기존 message ID / field number를 보존하고 새 계약은 additive하게 생성한다.
상세 ID는 구현 시 GenerationManifest 및 전체 proto 충돌 검사 후 배정한다.
신규 계약: Health/GetStatus, BeginDrain, Register/Heartbeat,
AllocateHandoff, ConsumeHandoff, ConfirmEntry, Release/RenewAdmission.
AS 내부 legacy Player bootstrap은 AS의 authenticated internal ingress로 분리한다.
서버 간 호출은 TLS 및 서버별 credential/role로 보호한다.
Gateway health/launcher lifecycle/AS allocation/GS consumption 권한을 구분한다.
공개 AS router에 서버 제어 route를 등록하지 않는다. Gateway를 거쳐도 접근할 수 없어야 한다.
인터넷 ingress는 표준 TLS transport로 RPCNet 프레임을 보호한다.
현재 envelope의 미지원 encryption flag를 켜서 TLS 구현을 대신하지 않는다.

## 설치와 통합 런처

초기 배포 대상은 Windows x64 self-contained package다. publish 시 지원 런타임/OS를 다시 확인한다.
Installer는 binary/config/data/log를 분리하고 기존 DB를 덮어쓰지 않는다.
설치 때 내부 credential을 생성하고 파일 권한을 제한한다. dev key를 배포 기본값으로 쓰지 않는다.
초기 런처는 상주 supervisor로 child process를 관리한다. 프로세스별 Windows service는 우선 도입하지 않는다.
로그온 자동 시작은 선택 옵션이다. 로그오프 후 무인 운영이 필요하면 별도 service host로 확장한다.

시작 순서:

1. 설정/포트 충돌/DB backup·migration 정책 검증.
2. Gateway 실행, ListeningNoBackend까지 확인.
3. Coordination owner AS 시작; DB와 내부 RPC 응답 준비 확인.
4. 추가 AS와 GS 시작; 등록/heartbeat/readiness 확인.
5. Gateway pool 편입과 전체 LoginReady/WorldReady 판정.
6. 선택적으로 Bot 로그인 -> World -> PlayerScope 적용 검증.

종료 순서:

1. Gateway Drain으로 신규 로그인 차단.
2. AS/GS Drain으로 추가 배정과 진입 차단.
3. GS session 종료/DB flush 확인 후 GS 종료.
4. AS 종료, Gateway relay 종료, Gateway 종료.
각 단계에 기한을 두고 강제 종료 발생 시 다음 시작에서 recovery 필요 상태를 표시한다.

Supervisor는 PID와 process instance ID로 자신이 시작한 프로세스만 제어한다.
재시작은 exponential backoff와 circuit breaker를 적용해 crash loop를 보여준다.
계획된 종료/업데이트 중에는 자동 재시작을 억제한다.
Coordination/GS 자동 재시작은 기존 session 보존을 의미하지 않는다.
UI: 전체 시작/종료, 상태와 실패 원인, 서버별 로그, 설정, Bot 검증, 백업/업데이트.
Bot 비밀번호는 입력 시에만 전달하며 설정/명령행/로그에 저장하지 않는다.

업데이트는 전체 Drain -> 종료 -> SQLite 일관 backup -> 단일 migration owner -> 새 binary 전환 -> health/Bot 확인.
binary와 schema의 rollback 호환성을 package manifest에 기록한다.
migration 후 실패했다고 무조건 예전 binary를 실행하지 않는다.
DB restore가 필요하면 발생한 신규 데이터 손실 가능성을 표시하고 운영자가 복구를 선택한다.

## 포트와 외부 접속

| 포트 | 용도 | 초기 노출 |
| --- | --- | --- |
| TCP 6000 | Gateway login TLS | Public 프로필에서 공개 |
| TCP 7100 | GS content TLS | Public 프로필에서 공개 |
| TCP 5100 | AS client ingress | loopback only |
| 설정으로 배정하는 제어 포트 | 내부 health / coordination / lifecycle | loopback only |
| legacy 5000 / 7000 | 기존 gRPC / WebSocket | 배포 기본에서 비활성 |

Local 프로필은 전부 loopback. Public 프로필은 Gateway/GS만 지정 인터페이스에 bind한다.
공유기에는 공개 두 포트만 서버 PC의 고정 LAN IP로 매핑한다.
GS public endpoint는 공인 hostname/port, private endpoint는 내부 주소로 별도 보관한다.
추가 GS는 별도 public port 매핑이 필요하다. listener port와 public NAT port를 혼동하지 않는다.
방화벽 도구는 운영자가 명시적으로 실행할 때 두 공개 포트만 등록한다. Installer는 공유기를 변경하지 않는다.
공인 WAN IP/CGNAT, 같은 LAN에서의 public hostname 접근 여부는 외부 접속 시험으로 확인한다.
PC 한 대/공유기 한 대의 장애를 이 LB가 해결한다고 표시하지 않는다.

## 구현 순서와 수용 기준

| 단계 | 변경 | 검증 |
| --- | --- | --- |
| 1 | public/internal ingress 분리, RPCNet Health/Drain | 공개 control 호출 거절, Gateway-first 상태 전이 |
| 2 | Gateway AS pool/LB 및 bounded relay | 두 AS 분산, 장애 제외/복귀, 전송 후 replay 없음 |
| 3 | Coordination ticket/registry/reservation/owner/lease | cross-AS ticket 소비, 중복/만료/경합, owner 고정 |
| 4 | 지정 AS의 RPCNet Account repository와 관리 AS pool | cross-AS 로그인, peer DB 미생성, migration 단일 owner |
| 5 | self-contained installer/supervisor | 개발 SDK 없는 PC 설치, 재시작, DB 보존/백업 |
| 6 | Public TLS/endpoint/firewall 안내 | 실제 외부 Bot 로그인/World/scope, 내부 포트 차단 |

각 단계는 Server/Bot로 검증한다. Client 생성/빌드/연결은 별도 후속 작업으로 수행한다.
Pool 지원 완료는 단계 2의 TCP 분산만으로 선언하지 않는다.
현재 Foundation 52 PASS는 본 설계의 LB/배포 검증 증거가 아니다.
