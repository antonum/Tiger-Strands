# Tiger-Strands

This repo contains examples of using Tiger-CLI MCP agent with AgentCore Strands Agents

- https://github.com/timescale/tiger-cli
- https://strandsagents.com/latest/

## agent.py

Bare minimum 3 lines Strands agent

```python
from strands import Agent

agent = Agent()
agent("What is LLM?") 
```

## agent-tiger

Bare minimum Strands agent with Tiger MCP server

You need to have tiger-cli installed locally for the following examples to work.

```bash
curl -fsSL https://cli.tigerdata.com | sh
```

```python
from mcp import stdio_client, StdioServerParameters
from strands.tools.mcp import MCPClient
from strands import Agent

# Create MCP client
mcp_client = MCPClient(lambda: stdio_client(StdioServerParameters(command="tiger", args=["mcp", "start"])))
agent = Agent(tools=[mcp_client])


agent("list my tiger services") 
```

## cli.py

Interactive coding assistent powered by Tiger CLI, Strands Agent and Strands tools

You can use it as an alternative to Claude Code, Kiro-CLI etc.

`cli.py` combines Strands Agent, Tiger MCP and Strands build-in tools `file_write`, `file_read`, `shell`.

Interact with it in the same way as you would with Claude code. Give it tasks, ask to examine files, create file, runn shell commands.

## SlackBot 

SlackBot wit access to Tiger-CLI. 

Slack application need to be configured in https://api.slack.com/

To run:

```
export SLACK_BOT_TOKEN="xoxb-99...."
export SLACK_APP_TOKEN="xapp-1-A0..."

python SlackBot/tiger-bot.py
```
## AgentCore

TigerAgent deployable to Amazon Bedrock AgentCore

requires:

```
export TIGER_MCP_URL="https://<your-tiger-mcp-url>/mcp"
```

### Deployment to AgentCore local:

```
cd AgentCore
agentcore launch --local 
```
In another terminal:
```
curl -X POST http://localhost:8080/invocations \
-H "Content-Type: application/json" \
-d '{"prompt": "hello"}'
```

### Deployment to AgentCore runtime on AWS:
```
agentcore launch
```

```
agentcore invoke '{"prompt": "Hello"}' 
```