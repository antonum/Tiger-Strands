#!/usr/bin/env python3
import sys
import os
from pathlib import Path
from mcp import stdio_client, StdioServerParameters
from strands import Agent
from strands.models import BedrockModel
from strands.tools.mcp import MCPClient
from strands_tools import file_write, file_read, shell
from constants import SESSION_ID
from rich.console import Console
from rich.markdown import Markdown

console = Console()

# Show rich UI for tools in CLI
os.environ["STRANDS_TOOL_CONSOLE_MODE"] = "enabled"

def main():
    # Initialize agent
    mcp_client = MCPClient(lambda: stdio_client(
        StdioServerParameters(command="tiger", args=["mcp", "start"])
    ))

    model = BedrockModel(
        model_id="us.anthropic.claude-sonnet-4-20250514-v1:0",
    )
    #read text from the file TIGER-CLI.md
    system_prompt = Path("TIGER-CLI.md").read_text()
    agent = Agent(
        tools=[mcp_client, file_write, file_read, shell],
        model=model,
        system_prompt=system_prompt,
        trace_attributes={"session.id": SESSION_ID}
        #/quit, callback_handler=None
    )
    banner = r"""
▀█▀ █ ▄▀  █▀▀ █▀▄   ▄▀▀ ▀█▀ █▀▄ ▄▀▄ █▄ █ █▀▄ ▄▀▀
 █  █ ▀▄█ ██▄ █▀▄   ▄█▀  █  █▀▄ █▀█ █ ▀█ █▄▀ ▄█▀
        
      ╔═══════════════════════════════════╗
      ║  Powered by TigerCLI  &  Strands  ║
      ╚═══════════════════════════════════╝
    """
    print(banner)
    print("CLI Agent (type /quit to exit)")

    try:
        while True:
            try:
                user_input = input("> ").strip()

                if not user_input:
                    continue

                # Handle commands
                if user_input.startswith("/"):
                    cmd = user_input[1:].lower()
                    if cmd == "quit":
                        break
                    elif cmd == "help":
                        print("Commands: /quit, /help")
                    else:
                        print(f"Unknown command: /{cmd}")
                    continue

                # Send to agent
                response = agent(user_input)
                #print(f"\n{response}\n")
                console.print(Markdown(str(response)))

            except KeyboardInterrupt:
                print("\nUse /quit to exit")
            except EOFError:
                break
            except Exception as e:
                print(f"Error: {e}")
    finally:
        # Explicit cleanup before interpreter shutdown
        try:
            agent.cleanup()
        except Exception:
            pass  # Suppress cleanup errors
        try:
            mcp_client.stop(None, None, None)
        except Exception:
            pass  # Suppress cleanup errors


if __name__ == "__main__":
    main()
