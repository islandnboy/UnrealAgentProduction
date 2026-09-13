# World Production Case Study

> Work in progress. 구현된 범위와 R&D 범위를 분리해 기록합니다.

## Implemented / Partial

- Terrain heightmap import / create / reimport
- PCG Region / Spline Road paths
- Partial Water / Streaming tools
- World Validation
- Read-only World Region planning

## Current R&D

- Persistent World / Region Job state
- Seoul GIS canonical data pipeline
- City-wide low-resolution World generation
- Representative detailed Region Vertical Slice

## Target Flow

```text
GIS / World Source
→ Canonical World Data
→ Region / Production Recipe
→ Agent Workflow
→ Unreal MCP
→ Landscape / Road / Building / PCG
→ World Partition
→ Validation
```
