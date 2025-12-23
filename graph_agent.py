import os
from typing import TypedDict, Annotated, List, Union
from langgraph.graph import StateGraph, END
import google.generativeai as genai
from dotenv import load_dotenv
from mcp_manager import MCPManager

load_dotenv()

# 1. Define the "State" (The data that flows through the graph)
class AgentState(TypedDict):
    query: str
    category: str
    raw_data: dict
    audit_report: str
    form_prepared: bool
    final_output: str

# 2. Initialize the Specialists
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('models/gemini-1.5-flash')
mcp = MCPManager(
    db_url="postgresql://localhost:5432/finance_db",
    docs_path="D:\\tax-docs"
)

# --- NODES (The Stations) ---

async def router_node(state: AgentState):
    try:
        """Classifies the intent to decide which data to fetch."""
        print("[Node: Router] Classifying intent...")
        prompt = f"Categorize this financial query: '{state['query']}'. Reply with only one word: 'DATABASE', 'FILESYSTEM', or 'GENERAL'."
        response = model.generate_content(prompt)
        return {"category": response.text.strip().upper()}
    except Exception as e:
        print(f"[Node: Router] Error: {e}")
        return {"category": "GENERAL"}

async def fetcher_node(state: AgentState):
    if not state['category']: 
        print("[Node: Fetcher] No data fetch needed for GENERAL category.")
        return {"raw_data": {}}
    """The Librarian: Fetches data via MCP based on the category."""
    print(f"[Node: Fetcher] Accessing MCP for {state['category']}...")
    # Using our existing MCP Manager
    try:
        data = await mcp.fetch_audit_data()
        return {"raw_data": data}
    except Exception as e:
        print(f"[Node: Fetcher] Error fetching data: {e}")
        return {"raw_data": {}}
async def auditor_node(state: AgentState):
    """The Specialist: Compares transactions to rules."""
    print("[Node: Auditor] Performing reasoning...")
    prompt = f"""
    Compare these transactions to the rules:
    Transactions: {state['raw_data']['transactions']}
    Rules: {state['raw_data']['rules']}
    User Question: {state['query']}
    Provide a concise audit summary.
    """
    response = model.generate_content(prompt)
    return {"audit_report": response.text}

async def preparer_node(state: AgentState):
    """The Clerk: Fills the form if needed."""
    if "prepare" in state['query'].lower() or "file" in state['query'].lower():
        print("[Node: Preparer] Generating JSON draft...")
        # In a real app, we'd use mcp.save_filled_form here
        return {"form_prepared": True, "final_output": f"Audit Complete. Form Prepared. \n{state['audit_report']}"}
    return {"final_output": state['audit_report']}

# --- THE GRAPH (The Flowchart) ---

workflow = StateGraph(AgentState)

# Add our stations
workflow.add_node("route_query", router_node)
workflow.add_node("fetch_data", fetcher_node)
workflow.add_node("audit_data", auditor_node)
workflow.add_node("prepare_form", preparer_node)

# Connect the stations (The Edges)
workflow.set_entry_point("route_query")
workflow.add_edge("route_query", "fetch_data")
workflow.add_edge("fetch_data", "audit_data")
workflow.add_edge("audit_data", "prepare_form")
workflow.add_edge("prepare_form", END)

# Compile the Graph
fiscal_pulse_app = workflow.compile()