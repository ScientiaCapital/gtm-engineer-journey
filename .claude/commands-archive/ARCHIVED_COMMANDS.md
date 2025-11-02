# Archived Commands - Context Optimization

## Archive Date: 2025-11-02

These commands were archived to reduce context overhead from 4.8k tokens to ~600 tokens (87% reduction).

## Archived Directories

### `/tm/*` (30+ commands)
Complex task management system. Restore if needed:
```bash
mv .claude/commands-archive/tm .claude/commands/
```

## Archived Individual Commands

### MCP-Dependent (won't work without MCP servers)
- `team-serena-analyze.md` - Deep code analysis with Serena MCP
- `team-shrimp-plan.md` - Shrimp Task Manager planning
- `team-sync-tasks.md` - Sync tasks across MCPs
- `team-task-master.md` - Task Master AI actions
- `team-think-sequential.md` - Sequential Thinking MCP
- `team-architect-mcp.md` - Architecture with MCP agents
- `team-orchestrate.md` - Multi-agent orchestration
- `project-init-mcp.md` - Initialize MCP servers

### Rarely Used
- `team-memory-save.md` - Save decisions/patterns to memory
- `team-health-check.md` - Check MCP server health
- `performance-workflow.md` - Performance optimization workflow
- `review-workflow.md` - Code review workflow

## Restore Individual Commands

To restore a specific command:
```bash
mv .claude/commands-archive/COMMAND_NAME.md .claude/commands/
```

## Current Active Commands (5 total)
1. `/daily-standup-mcp` - Morning planning
2. `/team-start-advanced` - MCP initialization
3. `/team-research` - Research mode with web search
4. `/workflow:debug-workflow` - Systematic debugging
5. `/workflow:feature-workflow` - Feature development

## Context Savings Summary

**Before Optimization:**
- CLAUDE.md: 373 lines (~2.7k tokens)
- Slash commands: 66 commands (~4.8k tokens)
- **Total overhead: ~7.5k tokens**

**After Optimization:**
- CLAUDE.md: 45 lines (~400 tokens estimated)
- Slash commands: 5 commands (~600 tokens estimated)
- **Total overhead: ~1k tokens**

**Estimated Savings: ~6.5k tokens (87% reduction)**
