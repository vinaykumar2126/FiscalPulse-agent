# FiscalPulse Agent–MCP Execution Flow (End-to-End)

This document captures the **complete execution lifecycle** of your FiscalPulse agent system, from user input to final response. It also **explicitly highlights the pieces you initially missed or blurred**, so you can revisit this later and instantly recall the architecture.

---

## 1. High-Level Goal

The goal of the system is to:

* Interpret **natural language user intent**
* Safely access structured financial data
* Perform reasoning and audits using LLMs
* Do all of this in a **modular, secure, and extensible way** using MCP

---

## 2. Core Components (Who Does What)

### User

* Provides natural language intent

### Lightweight Agent (Router)

* Makes a **coarse-grained decision**
* Selects **which MCP server(s)** are relevant
* Does NOT choose functions or parameters

### Main Agent (Scheduler + Reasoner)

* Discovers available MCP tools
* Maps user intent to **specific function calls + parameters**
* Invokes MCP
* Performs multi-step reasoning (LangGraph)

### MCP Server

* Exposes **self-describing tool schemas**
* Executes function calls safely
* Does NOT reason or infer intent

### Database / Filesystem

* Stores and returns raw data

---

## 3. Full Execution Flow (Start → End)

### Step 1: User Prompt

Example:

> "Find high-risk expenses from last quarter"

---

### Step 2: Lightweight (Router) Agent

**Input:**

* User prompt
* List of available MCP servers

**Output (IMPORTANT):**

```json
{
  "mcp_servers": ["transactions_mcp", "compliance_rules_mcp"]
}
```

🔴 **What you initially missed:**

* The router sends **ONLY MCP server names**
* It does **NOT** send function names
* It does **NOT** send parameters

---

### Step 3: Main Agent – Tool Discovery

Now the main agent takes over.

It asks the MCP client:

```python
mcp_client.list_tools("transactions_mcp")
```

The MCP server responds with **tool schemas**:

```json
[
  {
    "name": "get_transactions",
    "description": "Fetch filtered transactions",
    "parameters": {
      "start_date": "string",
      "end_date": "string",
      "min_amount": "number",
      "type": "string"
    }
  }
]
```

🔴 **What you initially missed:**

* The main agent does NOT magically know functions
* MCP servers are **self-describing**
* Tool schemas are discovered at runtime

---

### Step 4: Main Agent → LLM (Critical Step)

The main agent now sends **two things together** to the LLM:

1. User intent
2. MCP tool schemas

This is **tool / function calling**.

---

### Step 5: LLM Maps Intent → Function + Parameters

LLM output:

```json
{
  "tool_name": "get_transactions",
  "arguments": {
    "start_date": "2024-10-01",
    "end_date": "2024-12-31",
    "min_amount": 10000,
    "type": "expense"
  }
}
```

🔴 **What you initially missed:**

* The LLM does NOT execute anything
* It only performs **mapping and scheduling**

---

### Step 6: Main Agent Invokes MCP

The main agent executes:

```python
transactions_mcp.get_transactions(**arguments)
```

MCP:

* Validates schema
* Executes DB access
* Returns structured data

---

### Step 7: Main Agent Reasoning Loop

The main agent:

* Interprets returned data
* May call additional MCP tools
* Applies audit logic
* Generates explanations

This is typically orchestrated using **LangGraph nodes**.

---

### Step 8: Final Response

User receives:

* Audit results
* Flagged transactions
* Natural language explanation

---

## 4. Key Things You Were Confused About (Now Resolved)

### ❌ Misconception 1

> “If MCP has tools, why does the agent write queries?”

✅ Correction:

* MCP exposes **functions**, not intent
* The agent fills **parameters**

---

### ❌ Misconception 2

> “Router agent should send function names”

✅ Correction:

* Router sends **server names only**
* Main agent handles functions

---

### ❌ Misconception 3

> “Main agent magically knows MCP tools”

✅ Correction:

* MCP servers expose tool schemas
* Main agent discovers tools dynamically

---

## 5. Final Mental Model 

> **Router chooses servers → Main agent discovers tools → LLM maps intent to function + params → MCP executes → Agent reasons**

Or even shorter:

> **Servers → Tools → Parameters → Execution → Reasoning**

---

## 6. One-Sentence Summary 

> “FiscalPulse uses a two-agent architecture where a lightweight router selects relevant MCP servers, and a main agent dynamically discovers exposed tools, maps user intent to specific function calls with parameters, and invokes MCP for safe execution before generating explainable audit results.”



