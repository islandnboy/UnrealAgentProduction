# Server Production Case Study

Agent Workflow의 핵심 구조는 Editor mutation만을 위한 것이 아닙니다.

ProjectSF에서는 같은 Workflow / Step / Evidence 모델을 서버 기능 제작에도 적용합니다.

## Current pattern

~~~text
Issue / Goal
→ current SoT restore
→ server-feature-production Skill
→ architecture / contract inspection
→ implementation
→ deterministic test / bot verification
→ evidence
→ Goal evaluation
~~~

## Applied concerns

- feature boundary
- network contract
- deployment / topology impact
- bot-based verification
- persistence of validation evidence
- Issue-driven continuation across sessions

## Why include server work

Agent Workflow가 Unreal Editor Tool 호출에 종속된 구조라면 게임 전체 Production system으로 확장하기 어렵습니다.

현재 구조에서는 **Workflow는 제품 Goal을 소유하고, Skill과 Tool만 도메인에 따라 교체**됩니다.  
따라서 Client, World, UI, Server가 같은 실행 철학을 공유할 수 있습니다.
