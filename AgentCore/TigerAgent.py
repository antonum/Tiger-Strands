import os
from mcp import stdio_client, StdioServerParameters
from mcp.client.streamable_http import streamablehttp_client
from strands import Agent
from strands.tools.mcp import MCPClient
from bedrock_agentcore import BedrockAgentCoreApp

app = BedrockAgentCoreApp()
#mcp_client = MCPClient(lambda: stdio_client(StdioServerParameters(command="tiger",args=["mcp", "start"])))
mcp_client = MCPClient(lambda: streamablehttp_client(os.environ.get("TIGER_MCP_URL", "http://localhost:8000/mcp")))
agent = Agent(tools=[mcp_client])
#agent = Agent()

@app.entrypoint
async def agent_invocation(payload):
    """Handler for agent invocation"""
    user_message = payload.get(
        "prompt", "No prompt found in input, please guide customer to create a json payload with prompt key"
    )
    stream = agent.stream_async(user_message)
    async for event in stream:
        print(event)
        yield (event)

def xx_invoke(payload): #use for non-streaming
    """Process user input and return a response"""
    user_message = payload.get("prompt", "Hello")
    result = agent(user_message)
    return {"result": result.message}


if __name__ == "__main__":
    app.run()