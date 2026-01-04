import asyncio
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class MCPManager:
    """
    Handles the 'Bridges' to your local data.
    This class is responsible for talking to the MCP servers.
    """
    def __init__(self, db_url, docs_path):
        self.db_params = StdioServerParameters(
            command="npx",
            args=["@modelcontextprotocol/server-postgres", db_url],
            env=os.environ.copy()
        )
        self.fs_params = StdioServerParameters(
            command="npx",
            args=["@modelcontextprotocol/server-filesystem", docs_path],
            env=os.environ.copy()
        )
        print("Filesystem root:", docs_path)

    async def fetch_audit_data(self):
        """Connects to both servers and returns the raw data."""
        async with stdio_client(self.fs_params) as (f_read, f_write), \
                   stdio_client(self.db_params) as (d_read, d_write):
            
            async with ClientSession(f_read, f_write) as fs_session, \
                       ClientSession(d_read, d_write) as db_session:
                
                await fs_session.initialize()
                await db_session.initialize()

                # 1. Get Transactions
                db_result = await db_session.call_tool("query", {
                    "sql": "SELECT * FROM business_transactions WHERE is_filled = FALSE;"
                })
                
                # 2. Get Rules
                print("DEBUG read_file path sent to MCP:", "/Users/vinaykumargodavarti/tax-docs/tax_docs.md")
                rules_result = await fs_session.call_tool("read_file", {
                    "path": "/Users/vinaykumargodavarti/tax-docs/tax_docs.md"
                })

                return {
                    "transactions": str(db_result.content),
                    "rules": str(rules_result.content)
                }