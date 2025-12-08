# Testing Guide for LangChain Deep Agent

## Prerequisites

✓ You've added your `OPENAI_API_KEY` to `.env`  
✓ (Optional) Added `LANGSMITH_API_KEY` for observability

## Quick Test

Run the full system test with interactive selection:

```bash
cd /Users/jg/Documents/github/LangChain-DeepAgent
python3 tests/test_full_system.py
```

This will:
1. Verify your API key is configured
2. Show you 3 test scenarios
3. Let you select which to run
4. Display the complete agent response

## Test Scenarios

**Test 1: Simple Equipment List**
- Tests: Data retrieval subagent + HighByte MCP server
- Shows: Available equipment catalog

**Test 2: Equipment Status**
- Tests: Multi-tool usage (real-time data + status)
- Shows: Current equipment health and metrics

**Test 3: Production Analysis**
- Tests: Complex pipeline (data → analysis → report)
- Shows: Full subagent orchestration

## Interactive Mode

For conversational testing (run from project root):

```bash
python3 -m src.main --mode interactive
```

Example queries to try:
- "What equipment do we have?"
- "Show me the status of CNC-Machine-1"
- "Analyze production metrics for the last week"
- "Are there any work orders that need attention?"
- "What inventory items are low in stock?"

Type `exit` or `quit` to end the session.

## Single Query Mode

For one-off queries:

```bash
python3 -m src.main --mode single --query "What is the status of CNC-Machine-1?"
```

## Viewing LangSmith Traces

If you enabled LangSmith:
1. Visit https://smith.langchain.com
2. Select your project: `langchain-deepagent-manufacturing`
3. View detailed traces of agent execution
4. See tool calls, subagent spawning, and LLM reasoning

## What to Look For

✅ **Success indicators:**
- Agent responds with coherent answers
- MCP tools are being called (you'll see data in responses)
- Subagents are spawned when appropriate
- Structured logging shows the pipeline

⚠️ **Potential issues:**
- Rate limits: Wait a moment and try again
- If agent seems confused: Query might need more context
- Long delays: LLM is thinking through complex workflows

## Troubleshooting

**Error: "No valid OPENAI_API_KEY"**
- Open `.env` file
- Ensure `OPENAI_API_KEY=sk-...` is set correctly
- No quotes needed around the key

**Error: Module not found**
- Run: `pip3 install -r requirements.txt`
- Ensure you are running from project root: `python3 tests/test_full_system.py`

**Agent not using tools**
- This is expected for very simple queries
- Try more specific queries that require data

## Next Steps

After successful testing:
- Phase 5: Add RAG (ChromaDB) for documentation search
- Phase 6: Create example scenarios and full documentation
