from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from reportlab.pdfbase.pdfmetrics import stringWidth
import os

OUT=os.environ.get("RPCNET_GUIDE_OUT","Docs/Guides/RPCNet_Protocol_to_Unreal_Client_Guide.pdf")
os.makedirs(os.path.dirname(OUT), exist_ok=True)
W,H=landscape(A4)

pdfmetrics.registerFont(TTFont('KR','/usr/share/fonts/truetype/nanum/NanumGothic.ttf'))
pdfmetrics.registerFont(TTFont('KRB','/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf'))
pdfmetrics.registerFont(TTFont('MONO','/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'))
pdfmetrics.registerFont(TTFont('MONOB','/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf'))

BG=HexColor('#0B1020'); PANEL=HexColor('#141B2D'); PANEL2=HexColor('#1A2338')
TEXT=HexColor('#F3F6FC'); MUTED=HexColor('#AAB5CC'); CYAN=HexColor('#47D7FF')
BLUE=HexColor('#5B8CFF'); GREEN=HexColor('#6DE3A3'); YELLOW=HexColor('#FFD166')
RED=HexColor('#FF7B7B'); PURPLE=HexColor('#B798FF'); LINE=HexColor('#2B3858')

c=canvas.Canvas(OUT,pagesize=(W,H)); PAGE=0

def bg(title=None,kicker=None):
    global PAGE
    PAGE+=1
    c.setFillColor(BG); c.rect(0,0,W,H,fill=1,stroke=0)
    if kicker:
        c.setFillColor(CYAN); c.setFont('KRB',9); c.drawString(36,H-33,kicker)
    if title:
        c.setFillColor(TEXT); c.setFont('KRB',22); c.drawString(36,H-62,title)
        c.setStrokeColor(LINE); c.line(36,H-76,W-36,H-76)
    c.setFillColor(MUTED); c.setFont('KR',7.5)
    c.drawString(36,20,'Agent Workflow Portfolio  |  ProjectSF / RPCNet  |  2026-10-07')
    c.drawRightString(W-36,20,str(PAGE))

def text(x,y,s,size=10,color=TEXT,font='KR'):
    c.setFillColor(color); c.setFont(font,size); c.drawString(x,y,s)

def para(x,y,s,width,size=10,leading=15,color=TEXT,font='KR'):
    line=''; lines=[]
    for ch in s:
        t=line+ch
        if stringWidth(t,font,size)<=width: line=t
        else:
            if line: lines.append(line.rstrip())
            line=ch.lstrip()
    if line: lines.append(line.rstrip())
    c.setFillColor(color); c.setFont(font,size); yy=y
    for ln in lines:
        c.drawString(x,yy,ln); yy-=leading
    return yy

def box(x,y,w,h,fill=PANEL,stroke=LINE,r=10):
    c.setFillColor(fill); c.setStrokeColor(stroke); c.roundRect(x,y,w,h,r,fill=1,stroke=1)

def label(x,y,s,color=CYAN):
    c.setFillColor(color); c.roundRect(x,y-4,stringWidth(s,'KRB',8)+14,18,6,fill=1,stroke=0)
    c.setFillColor(BG); c.setFont('KRB',8); c.drawString(x+7,y+1,s)

def arrow(x1,y1,x2,y2,color=CYAN,width=2):
    import math
    c.setStrokeColor(color); c.setFillColor(color); c.setLineWidth(width); c.line(x1,y1,x2,y2)
    a=math.atan2(y2-y1,x2-x1)
    for d in (2.65,-2.65):
        c.line(x2,y2,x2+8*math.cos(a+d),y2+8*math.sin(a+d))

def flow(cx,cy,w,h,title,sub='',accent=CYAN):
    x=cx-w/2; y=cy-h/2; box(x,y,w,h,PANEL2,accent,8)
    c.setFillColor(accent); c.rect(x,y,w,4,fill=1,stroke=0)
    c.setFillColor(TEXT); c.setFont('KRB',10); c.drawCentredString(cx,cy+5,title)
    if sub:
        c.setFillColor(MUTED); c.setFont('KR',7.5); c.drawCentredString(cx,cy-10,sub)

def codebox(x,y,w,h,lines,title=None):
    box(x,y,w,h,HexColor('#0F1525'),LINE,8)
    yy=y+h-20
    if title:
        c.setFillColor(MUTED); c.setFont('KRB',8); c.drawString(x+12,y+h-18,title); yy=y+h-36
    c.setFillColor(HexColor('#D9E3F0')); c.setFont('MONO',7.1)
    for ln in lines:
        c.drawString(x+12,yy,ln[:110]); yy-=11
        if yy<y+10: break

def bullets(x,y,items,width=320,size=9.3,leading=14,accent=CYAN):
    yy=y
    for item in items:
        c.setFillColor(accent); c.circle(x+4,yy+3,2.2,fill=1,stroke=0)
        yy=para(x+14,yy,item,width-14,size,leading,TEXT)-5
    return yy

def tag(x,y,s,color=BLUE):
    w=stringWidth(s,'KRB',7.5)+14
    c.setFillColor(color); c.roundRect(x,y,w,17,6,fill=1,stroke=0)
    c.setFillColor(BG); c.setFont('KRB',7.5); c.drawString(x+7,y+4,s)

bg()
text(48,H-80,'RPCNet',14,CYAN,'KRB')
text(48,H-122,'프로토콜 제작부터',31,TEXT,'KRB')
text(48,H-163,'Unreal Client 구현까지',31,TEXT,'KRB')
para(50,H-205,'ProjectSF의 실제 구조를 기준으로, .proto 정의가 어떻게 생성 코드가 되고 Runtime/Handler/Coordinator/UI까지 연결되는지 설명하는 포트폴리오 가이드입니다.',620,12,20,MUTED)
cy=230; nodes=[('Protocol','Consumer-owned .proto'),('Generator','Manifest + protoc'),('Generated','DTO / Traits / StubBase'),('Client','Proxy / Handler'),('Product','Coordinator / UI')]
xs=[100,260,425,590,750]; colors=[PURPLE,BLUE,CYAN,GREEN,YELLOW]
for i,(t,s) in enumerate(nodes):
    flow(xs[i],cy,125,64,t,s,colors[i])
    if i<len(nodes)-1: arrow(xs[i]+63,cy,xs[i+1]-63,cy,colors[i+1])
tag(50,110,'Portfolio Guide',CYAN); tag(155,110,'Unreal Engine 5.8',BLUE); tag(285,110,'RPCNet',PURPLE); tag(350,110,'Real Client Flow',GREEN)
text(50,78,'핵심: 생성 코드와 수작성 코드를 분리하고, Protocol 변경을 실제 게임 상태로 안전하게 연결한다.',11,TEXT,'KRB')
c.showPage()

bg('1. 먼저 경계를 나눈다','ARCHITECTURE')
para(40,H-105,'RPCNet이 프로토콜의 “의미”까지 소유하지 않는 것이 출발점입니다. Framework는 통신과 생성 인프라를 제공하고, ProjectSF가 실제 게임 Protocol과 Client 동작을 소유합니다.',760,10.5,16,MUTED)
box(45,175,350,300); label(64,447,'RPCNet Framework',CYAN)
bullets(65,415,['Transport abstraction: TCP / WebSocket / Mock / Memory','NetworkSession과 request correlation / timeout','Packet Envelope / Codec','NetworkProxyBase / NetworkStubBase','ProtocolGenerator parser / validation / target emitter','Plugin Installer와 Framework boundary validation'],300,9.3,14,CYAN)
box(447,175,350,300); label(466,447,'ProjectSF Consumer',YELLOW)
bullets(467,415,['.proto schema와 message metadata / direction','GenerationManifest의 target / output / route','Login / World / PlayerScope 같은 Domain 의미','Client Proxy / Stub의 수작성 확장','ConnectionHandler와 Coordinator','UI / Model / Gameplay에 실제 결과 적용'],300,9.3,14,YELLOW)
arrow(395,325,447,325,PURPLE); text(365,345,'contract',8,MUTED,'MONOB')
box(170,92,505,55,HexColor('#10182A'),PURPLE,9)
text(190,125,'RPCNet = communication infrastructure',11,CYAN,'MONOB'); text(190,105,'ProjectSF = protocol semantics + product integration',11,YELLOW,'MONOB')
c.showPage()

bg('2. .proto -> Unreal Client 생성물','PROTOCOL GENERATION')
text(42,H-104,'실제 ProjectSF generation manifest',10,CYAN,'KRB')
xs=[95,250,420,600,755]; labels=[('Proto','Schema'),('Manifest','Route/Target'),('Generator','C# Tool'),('GeneratedFiles','Unreal C++'),('Server','Generated')]
for i,(t,s) in enumerate(labels):
    flow(xs[i],420,120,60,t,s,[PURPLE,BLUE,CYAN,GREEN,YELLOW][i])
    if i<4: arrow(xs[i]+60,420,xs[i+1]-60,420,[BLUE,CYAN,GREEN,YELLOW][i])
codebox(42,205,360,175,['GenerationManifest.json','  target: UnrealClient','  output: Client/Source/SF/Network/GeneratedFiles','  includePrefix: Network/GeneratedFiles','','routes:','  C2AS  -> AS2C','  C2GS  -> GS2C','  GS2AS -> AS2GS','  Control2Server -> Server2Control'],'Consumer-owned configuration')
codebox(425,205,372,175,['Generate-Protocols.ps1 -Target Client','','dotnet run --project ProtocolGenerator.csproj -- generate','  --config GenerationManifest.json','  --protoc <UE protobuf protoc.exe>','  --protobuf-include <UE protobuf include>','','Output examples:','  C2ASProtocol.pb.h / .cc','  AS2CAccountStubBase.h / .cpp','  ProtocolTraits.generated.h'],'Generation entrypoint')
box(42,112,755,63,HexColor('#11192B'),LINE,8); text(58,150,'Generated source는 “소유권이 명확한 산출물”이다.',11,TEXT,'KRB')
para(58,130,'State/ClientGeneratedFiles.json이 생성기가 소유하는 파일을 추적하고, stale cleanup도 그 범위 안에서만 수행합니다. 생성물을 직접 수정하지 않습니다.',700,9.2,14,MUTED)
c.showPage()

bg('3. 생성 코드와 수작성 코드의 경계','OWNERSHIP')
box(42,155,360,335); label(60,462,'GENERATED - 수정 금지',RED); text(60,428,'GeneratedFiles/',12,TEXT,'KRB')
bullets(60,400,['protobuf message classes (.pb.h / .pb.cc)','ProtocolTraits.generated.h','AS2CAccountStubBase / GS2CGameStubBase','Generator가 소유하는 metadata / dispatch glue'],310,9.2,14,RED)
codebox(62,190,320,140,['class FAS2CAccountStubBase : ...','{','  // generated dispatch','  virtual void OnRecvAccountStatus(...) = 0;','};','','// Regenerate instead of editing this file.'],'예시 역할')
box(442,155,355,335); label(460,462,'HANDWRITTEN - 제품 코드',GREEN); text(460,428,'Client/Source/SF/Network/',12,TEXT,'KRB')
bullets(460,400,['Proxy: 제품 친화적 request API','Stub: notify 수신을 delegate / model event로 변환','ConnectionHandler: Session / Proxy / Stub lifecycle','Coordinator: 여러 연결과 제품 Flow를 orchestration'],305,9.2,14,GREEN)
codebox(462,190,315,140,['class FAS2CAccountStub final','  : public FAS2CAccountStubBase','{','protected:','  void OnRecvAccountStatus(...) override;','};','','// Stable handwritten extension point.'],'예시 역할')
arrow(405,320,440,320,PURPLE); text(390,340,'extends',8,MUTED,'MONOB')
c.showPage()

bg('4. Unreal Client에서는 계층별로 책임을 올린다','CLIENT LAYERS')
para(40,H-102,'Protocol이 생성됐다고 UI가 바로 protobuf를 호출하지 않습니다. Wire-level API를 제품 흐름으로 단계적으로 끌어올립니다.',760,10,15,MUTED)
items=[('WBP_Login / LoginViewModel','입력과 표시. 네트워크 세션을 소유하지 않음',YELLOW),('SFLoginFlowCoordinator','다음 연결 / RPC / Travel을 결정하는 유일한 orchestration',GREEN),('SFASConnectionHandler / SFGSConnectionHandler','Session, Proxy, Stub lifecycle과 typed event',CYAN),('C2ASAccountProxy / C2GSGameProxy + handwritten Stub','제품 친화적 request / notify adapter',BLUE),('Generated DTO / Traits / StubBase','Protocol metadata와 protobuf type',PURPLE),('RPCNet Session / Transport','request correlation, packet dispatch, TCP/WebSocket/Mock',HexColor('#8BA6FF'))]
y=445
for i,(t,s,col) in enumerate(items):
    box(150,y-48,545,55,PANEL2,col,8); c.setFillColor(col); c.rect(150,y-48,6,55,fill=1,stroke=0)
    text(170,y-22,t,10.4,TEXT,'KRB'); text(170,y-39,s,8.3,MUTED)
    if i<len(items)-1: arrow(422,y-49,422,y-66,col,1.7)
    y-=72
box(715,210,90,230,HexColor('#10182A'),LINE,8); text(728,414,'금지',9,RED,'KRB')
para(728,392,'UI가 Socket을 직접 소유',62,8.2,12,MUTED); para(728,330,'Coordinator가 protobuf encode 수행',62,8.2,12,MUTED); para(728,250,'Generated 파일에 제품 로직 삽입',62,8.2,12,MUTED)
c.showPage()

bg('5. Request / Notify를 제품 API로 감싼다','IMPLEMENTATION')
text(42,H-105,'Request: Proxy',11,CYAN,'KRB')
codebox(42,300,370,190,['FPacketRequestHandle FC2ASAccountProxy::LoginAsync(','  const FString& AccountId, const FString& Password,','  FLoginCompletion&& Completion, double Timeout) const','{','  LoginRequest Request;','  Request.set_account_id(...);','  Request.set_password(...);','  return SendRequest<LoginRequest, LoginResponse>(', '    Request, Timeout, MoveTemp(Completion));','}'],'Handwritten product-facing request wrapper')
text(435,H-105,'Notify: Stub',11,GREEN,'KRB')
codebox(435,300,362,190,['class FGS2CGameStub final','  : public FGS2CGameStubBase','{','public:','  FSFWorldStateReceived OnWorldState;','protected:','  void OnRecvWorldState(','    const WorldStateNotify& Data) override;','};'],'Generated dispatch -> handwritten event')
text(42,260,'Handler는 연결별 Runtime을 소유한다',11,TEXT,'KRB')
flow(105,195,125,56,'USFASHandler','SendLogin',CYAN); flow(285,195,125,56,'Proxy','LoginAsync',BLUE); flow(465,195,125,56,'Session','Request/Response',PURPLE); flow(645,195,125,56,'OnLoginResponse','typed event',GREEN)
arrow(168,195,222,195,BLUE); arrow(348,195,402,195,PURPLE); arrow(528,195,582,195,GREEN)
box(42,95,755,55,HexColor('#11192B'),LINE,8); para(58,128,'핵심은 protobuf 타입을 숨기는 것이 아니라 “어디까지가 wire contract이고 어디부터가 product behavior인지” 책임을 고정하는 것입니다.',705,9.5,14,MUTED)
c.showPage()

bg('6. 실제 로그인은 두 연결을 Coordinator가 이어 붙인다','REAL PRODUCT FLOW')
actors=[('UI / VM',65,YELLOW),('Coordinator',200,GREEN),('AS Handler',345,CYAN),('Gateway / AS',485,BLUE),('GS Handler',630,CYAN),('Game Server',755,PURPLE)]
for name,x,col in actors:
    c.setFillColor(col); c.setFont('KRB',8.4); c.drawCentredString(x,470,name); c.setStrokeColor(LINE); c.line(x,455,x,115)
def msg(y,x1,x2,s,col=TEXT):
    arrow(x1,y,x2,y,col,1.3); c.setFillColor(col); c.setFont('KR',7.2); c.drawCentredString((x1+x2)/2,y+6,s)
msg(430,65,200,'BeginLogin(account, password)',YELLOW); msg(400,200,345,'Connect Gateway',GREEN); msg(370,345,485,'LoginRequest',CYAN); msg(340,485,345,'LoginResponse + GS endpoint + ticket',BLUE); msg(310,345,200,'OnLoginResponse',CYAN); msg(280,200,630,'Connect selected GS',GREEN); msg(250,630,755,'EnterWorldRequest(ticket)',CYAN); msg(220,755,630,'EnterWorldResponse',PURPLE); msg(190,755,630,'WorldStateNotify(PlayerScope)',PURPLE); msg(160,630,200,'Scope event',CYAN); msg(130,200,65,'InWorld -> close UI / travel NeoSeoul',GREEN)
box(68,78,685,26,HexColor('#11192B'),LINE,7); text(82,87,'AS는 handoff 후 종료 가능 / GS는 World 진입 이후 유지 / initial PlayerScope가 적용된 뒤에만 Travel',8.2,TEXT,'KRB')
c.showPage()

bg('7. 네트워크는 “성공 경로”보다 수명주기가 중요하다','LIFECYCLE & FAILURE')
cards=[(42,315,365,165,'Correlation','AttemptId / ConnectionId / RequestId를 구분하고 과거 callback은 무시한다.',CYAN),(435,315,362,165,'Timeout','Connect 5s / Login·EnterWorld RPC 10s / Initial Scope 12s. 무한 대기하지 않는다.',YELLOW),(42,125,365,165,'Cleanup','dispatch 중 session을 즉시 파괴하지 않고 event 처리 뒤 정리한다. Disconnect는 수렴 가능해야 한다.',GREEN),(435,125,362,165,'Security / Handoff','Password·ticket·session id를 Evidence에 출력하지 않는다. GS ticket은 일회용으로 취급한다.',PURPLE)]
for x,y,w,h,t,s,col in cards:
    box(x,y,w,h); label(x+16,y+h-30,t,col); para(x+18,y+h-60,s,w-36,9.6,15,TEXT)
text(55,92,'실패/단절 -> AuthModel + Scope + owned connection reset -> 새 Login 필요',9.3,RED,'KRB'); text(455,92,'nonzero ResultCode -> ProtocolError / 중복 EnterWorld -> reject',9.3,RED,'KRB')
c.showPage()

bg('8. 새 Client Protocol을 추가하는 실제 순서','HOW TO EXTEND')
steps=[('01','Schema','Proto에 message / id / direction / response metadata 정의',PURPLE),('02','Generate','Generate-Protocols.ps1 -Target Client 실행',BLUE),('03','Review generated','pb + Traits + StubBase 변경을 확인. 직접 수정 금지',CYAN),('04','Proxy / Stub','request wrapper와 notify adapter를 handwritten layer에 추가',GREEN),('05','Handler','연결별 Session / Proxy / Stub lifecycle과 typed event 연결',YELLOW),('06','Product flow','Coordinator / Domain Service / ViewModel에서 실제 제품 동작 연결',GREEN),('07','Build & tests','반복 생성 hash, C++ build, failure / lifecycle test',BLUE),('08','Real interop','실제 Server process + UE Client readback으로 Acceptance 확인',CYAN)]
y=455
for num,t,s,col in steps:
    c.setFillColor(col); c.circle(67,y,15,fill=1,stroke=0); text(58,y-4,num,8,BG,'MONOB'); text(95,y+2,t,10,TEXT,'KRB'); para(215,y+2,s,560,9,13,MUTED)
    if num!='08': c.setStrokeColor(LINE); c.line(67,y-15,67,y-38)
    y-=47
box(42,72,755,50,HexColor('#11192B'),RED,8); text(58,101,'Regression rule',9,RED,'KRB'); para(150,100,'Protocol generation PASS != Client behavior PASS. 최소한 build, handler lifecycle, 실제 request/notify, product state 적용을 분리해서 검증합니다.',620,8.6,13,TEXT)
c.showPage()

bg('9. ProjectSF에서 실제로 확인한 것','VERIFICATION')
metrics=[('Stable regeneration','동일 protocol 재생성 hash 확인',CYAN),('SFEditor build','UHT / C++ / DLL PASS',BLUE),('Real widget flow','입력/버튼 -> Gateway -> GS -> Model readback',GREEN),('Entry travel','Entry -> PlayerScope -> NeoSeoul',YELLOW)]
for (title,sub,col),x in zip(metrics,[125,325,525,725]):
    box(x-88,375,176,100,PANEL,col,10); text(x-72,438,title,10,col,'KRB'); para(x-72,415,sub,145,8.1,12,MUTED)
text(42,335,'Failure / lifecycle cases',11,TEXT,'KRB')
bullets(45,310,['잘못된 비밀번호, login failure, GS disconnect','cancel 이후 늦게 도착한 callback 무시','중복 world entry 거절, relogin과 server restart','PlayerScope identity / session / revision correlation','UI teardown과 Handler / Coordinator 수명 분리'],350,9.1,14,RED)
text(430,335,'현재 명시적으로 미검증',11,TEXT,'KRB')
bullets(433,310,['Public TLS / WAN Unreal Client','Packaged Game end-to-end','사람이 직접 입력하는 최종 화면 UX','GS의 Unreal gameplay replication','Production multi-region / HA'],330,9.1,14,YELLOW)
box(42,86,755,55,HexColor('#11192B'),LINE,8); text(58,119,'완료 판정 원칙',9,CYAN,'KRB'); para(150,118,'Generated file 존재나 RPC 호출 성공을 제품 완료로 보지 않고, 실제 Client state와 사용자 경험에 필요한 Acceptance까지 분리해 Evidence로 남깁니다.',620,8.8,13,TEXT)
c.showPage()

bg('10. 이 구조가 포트폴리오에서 보여주는 것','PORTFOLIO TAKEAWAY')
text(50,H-120,'Protocol 변경을 “파일 생성”으로 끝내지 않는다.',24,TEXT,'KRB')
para(52,H-162,'Schema에서 출발한 변경이 Generated boundary, Runtime session, Handler lifecycle, Product Coordinator, UI/Model 적용, 실제 Server interoperability까지 이어지는 전체 경로를 설계하고 검증합니다.',720,11,18,MUTED)
for x,title,sub,col in [(55,'Generate','반복 boilerplate를 자동화하되 generated ownership을 명확히 한다.',PURPLE),(300,'Integrate','wire-level contract를 Handler / Coordinator를 통해 제품 흐름으로 올린다.',GREEN),(545,'Verify','실제 Server + Unreal Client까지 end-to-end Evidence를 남긴다.',CYAN)]:
    box(x,190,220,170,PANEL,col,12); label(x+18,330,title,col); para(x+18,295,sub,184,10,16,TEXT)
text(52,145,'핵심 설계 문장',10,CYAN,'KRB'); box(52,75,710,52,HexColor('#10182A'),PURPLE,8)
text(70,105,'Generated code is replaceable. Product behavior is handwritten and testable.',11,TEXT,'MONOB'); text(70,87,'Protocol -> Runtime -> Handler -> Coordinator -> Product State',10,CYAN,'MONOB')
c.showPage()

c.save()
print(OUT)
