# Architecture

## Separation of Concerns

### Agent Workflow

Agent가 작업을 수행하는 방법을 정의합니다.

- Intent interpretation
- Execution mode routing
- Context resolution
- Skill / Guideline binding
- Prompt compilation
- Tool / MCP execution boundary
- Validation / Evidence

### Production Framework

게임 제작 절차를 정의합니다.

- Domain
- Stage
- Dependency
- Artifact
- Review
- Integration

Agent Workflow는 Production Framework를 읽고 실행하지만, 게임 제작 Flow 자체를 소유하지 않습니다.

## High-level Flow

```text
Natural Language Request
→ Execution Mode
→ Context Scope
→ Focused Repository Inspection
→ Production Flow / Domain / Stage
→ Skill / Guideline
→ Compiled Prompt
→ Execution Plan
→ MCP / Tool
→ Validation / Evidence
```
