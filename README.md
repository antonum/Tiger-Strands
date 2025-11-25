# Tiger-Strands

A collection of examples demonstrating how to integrate [Tiger-CLI MCP](https://github.com/timescale/tiger-cli) with [Strands Agents](https://strandsagents.com/latest/) for building AI-powered database management and automation tools.

## Overview

Tiger-Strands showcases various implementations of AI agents that can interact with TimescaleDB/Tiger services through the Tiger CLI's MCP (Model Context Protocol) server. These examples range from simple 3-line agents to production-ready Slack bots and AWS deployments.

## Prerequisites

- Python 3.12+
- Tiger CLI installed locally (required for most examples)
- TimescaleDB/Tiger account (for database operations)

## Installation

### Install Tiger CLI

```bash
curl -fsSL https://cli.tigerdata.com | sh
```

### Install Python Dependencies

```bash
pip  install -r requirements.txt
```

## Examples

### 1. agent.py

**Basic Strands Agent** - A minimal 3-line example to get started with Strands agents.

```python
from strands import Agent

agent = Agent()
agent("What is LLM?")
```

This demonstrates the simplest possible Strands agent without any external tools or MCP integration.

### 2. agent-tiger

**Strands Agent with Tiger MCP Integration** - Connects a Strands agent to Tiger CLI's MCP server for database operations.

**Requirements:** Tiger CLI must be installed (see Installation section above).

```python
from mcp import stdio_client, StdioServerParameters
from strands.tools.mcp import MCPClient
from strands import Agent

# Create MCP client that connects to Tiger CLI
mcp_client = MCPClient(
    lambda: stdio_client(
        StdioServerParameters(command="tiger", args=["mcp", "start"])
    )
)
agent = Agent(tools=[mcp_client])

# Now the agent can interact with Tiger services
agent("list my tiger services")
```

This example shows how to give your agent access to Tiger CLI capabilities, enabling it to manage TimescaleDB services, run queries, and more.

### 3. cli.py

**Interactive Coding Assistant** - A full-featured AI coding assistant powered by Tiger CLI, Strands Agent, and Strands tools.

This is an alternative to tools like Claude Code, Kiro-CLI, etc.

**Features:**
- Tiger MCP integration for database operations
- Built-in Strands tools: `file_write`, `file_read`, `shell`
- Interactive command-line interface

**Usage:**

```bash
python cli.py
```

Interact with it like Claude Code: give it tasks, ask it to examine files, create files, and run shell commands.

**Example commands:**
- "list my tiger services"
- "using timescaledb best practices create DB schema for Solana blockchain and write it to schema.sql file"
- "pause my tiger-test service"
- "create fork of tiger-test service and implement test data retention policy of 1 week there"

### 4. SlackBot

**Slack Bot with Tiger MCP Access** - A Slack bot that can manage Tiger/TimescaleDB services directly from Slack channels.

**Setup:**

1. Configure a Slack application at https://api.slack.com/
2. Obtain your bot tokens (Bot Token and App Token)
3. Set up the required environment variables

**Environment Variables:**

```bash
export SLACK_BOT_TOKEN="xoxb-99...."
export SLACK_APP_TOKEN="xapp-1-A0..."
```

**Run the bot:**

```bash
python SlackBot/tiger-bot.py
```

**Usage in Slack:**
Once running, you can interact with the bot in your Slack workspace to manage Tiger services, run queries, and get database insights directly from your team's chat.

### 5. AgentCore

**AWS Bedrock AgentCore Deployment** - Deploy a Tiger-powered agent to Amazon Bedrock AgentCore for production-scale AI operations.

**Requirements:**

Set the Tiger MCP URL environment variable:

```bash
export TIGER_MCP_URL="https://<your-tiger-mcp-url>/mcp"
```

#### Local Development

Test your agent locally before deploying to AWS:

```bash
cd AgentCore
agentcore launch --local
```

In another terminal, test the agent:

```bash
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "hello"}'
```

#### Production Deployment to AWS

Deploy to AgentCore runtime on AWS:

```bash
agentcore launch
```

Invoke your deployed agent:

```bash
agentcore invoke '{"prompt": "Hello"}'
```

## Resources

- [Tiger CLI Documentation](https://github.com/timescale/tiger-cli)
- [Strands Agents Documentation](https://strandsagents.com/latest/)
- [TimescaleDB Documentation](https://www.tigerdata.com/docs/)
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

Please refer to the repository license file for licensing information.