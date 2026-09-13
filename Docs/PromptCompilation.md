# Prompt Compilation

사용자의 자연어를 Tool 호출이나 Production Spec으로 직접 취급하지 않습니다.

```text
Natural Language
→ Intent Interpretation
→ Execution Mode / Agent Role Resolution
→ Context Scope Resolution
→ Focused Repository Inspection
→ Production Framework Routing
→ Flow → Domain → Stage
→ Skill Binding
→ Guideline Resolution
→ Prompt Compilation
→ Execution Plan
→ Tool / MCP Execution
→ Intent-based Validation
→ Focused Correction
```

## Principles

- Repository evidence first
- Blocking ambiguity only
- Focused Repository Inspection 이전에는 mutation을 시작하지 않음
- Asset 생성이나 Compile 성공만으로 완료 판정하지 않음
- 후속 요청에서는 가능한 범위에서 이전 Production Context를 재사용
