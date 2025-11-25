from mcp import stdio_client, StdioServerParameters
from strands.tools.mcp import MCPClient
from strands import Agent

# Create MCP client
mcp_client = MCPClient(lambda: stdio_client(StdioServerParameters(command="tiger", args=["mcp", "start"])))
agent = Agent(tools=[mcp_client])


agent("list my tiger services") 

