import asyncio
from graph_agent import fiscal_pulse_app

async def run_app():
    """
    This is the entry point that actually starts your LangGraph.
    """
    print("--- 🚀 FiscalPulse: Autonomous Audit Started ---")
    
    # We define the initial state to kick off the conversation
    user_input = input("\nWhat would you like to audit today? (e.g., 'Check my hardware expenses')\n> ")
    
    initial_state = {
        "query": user_input,
        "category": "",
        "raw_data": {},
        "audit_report": "",
        "form_prepared": False,
        "final_output": ""
    }

    try:
        # We 'invoke' the graph. It will travel through all your nodes automatically.
        print("\n[*] Engaging AI Agent nodes...")
        final_state = await fiscal_pulse_app.ainvoke(initial_state)

        print("\n" + "="*60)
        print("FISCALPULSE FINAL AUDIT REPORT")
        print("="*60)
        print(final_state["final_output"])
        print("="*60)

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("Tip: Make sure your MCP terminals (Postgres/Filesystem) are running!")

if __name__ == "__main__":
    asyncio.run(run_app())