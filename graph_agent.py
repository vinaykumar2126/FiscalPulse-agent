import os
from typing import TypedDict, Annotated, List, Union
from langgraph.graph import StateGraph, END
import ollama
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
# Initialize MCP Manager
mcp = MCPManager(
    db_url="postgresql://localhost:5432/postgres",
    docs_path="/Users/vinaykumargodavarti/tax-docs" 
)
# --- NODES (The Stations) ---

async def router_node(state: AgentState):
    try:
        """Classifies the intent to decide which data to fetch."""
        print("[Node: Router] Classifying intent...")
        prompt = f"Categorize this financial query: '{state['query']}'. Reply with only one word: 'DATABASE', 'FILESYSTEM'"
        response = ollama.chat(model='llama3', messages=[{'role': 'user', 'content': prompt}])
        # print(response)
        return {"category": response["message"]["content"].strip().upper()}

    except Exception as e:
        print(f"[Node: Router] Error: {e}")
        return {"category": "GENERAL"}

async def fetcher_node(state: AgentState):
    if state["category"] == "GENERAL":
        print("[Node: Fetcher] Skipping MCP fetch for GENERAL.")
        return {"raw_data": {}}
    """The Librarian: Fetches data via MCP based on the category."""
    print(f"[Node: Fetcher] Accessing MCP for {state['category']}...")
    # Using our existing MCP Manager
    try:
        def unwrap_textcontent(value):
            if isinstance(value, list):
                return value[0].text
            return value
        data = await mcp.fetch_audit_data()
        # print(f"DEBUG: Transactions found: {bool(data['transactions'])}")
        # print(f"DEBUG: Rules found: {data['rules']}") # See if this is empty!
        # print(data["transactions"])
        return {
    "raw_data": {
        "transactions": unwrap_textcontent(data["transactions"]),
        "rules": unwrap_textcontent(data["rules"])
    }
}
    except Exception as e:
        print(f"[Node: Fetcher] Error fetching data: {e}")
        return {"raw_data": {}}
    
async def auditor_node(state: AgentState):
    print("[Node: Auditor] Performing reasoning against tax rules...")
    
    if not state['raw_data']:        
        return {"audit_report": "No data available for audit."}

    # Enhanced Prompt for specialized auditing
    prompt = f"""
    You are a professional Financial Auditor.
    
    USER QUERY: {state['query']}
    
    DATA PROVIDED:
    1. Transactions (from Database): 
    {state['raw_data']['transactions']}
    
    2. Tax Rules (from Filesystem):
    {state['raw_data']['rules']}
    
    TASK:
    1. Identify all transactions relevant to the user's query.
    2. Compare these transactions against the Tax Rules provided.
    3. Flag any discrepancies (e.g., if a hardware purchase exceeds a limit in the rules).
    4. Provide a summary in a clean Markdown format.
    """
    
    response = ollama.chat(model='llama3', messages=[{'role': 'user', 'content': prompt}])
    analysis = response["message"]["content"]
    return {"audit_report": analysis}

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