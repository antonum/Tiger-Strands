import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from mcp import stdio_client, StdioServerParameters
from strands import Agent
from strands.tools.mcp import MCPClient
#from rich.markdown import Markdown

# Create MCP client
mcp_client = MCPClient(lambda: stdio_client(StdioServerParameters(command="tiger", args=["mcp", "start"])))
agent = Agent(tools=[mcp_client])


# Initialize the app with your bot token
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

# Respond when the bot is mentioned
@app.event("app_mention")
def handle_mention(event, say, client):
    user = event['user']
    text = event['text']
    channel = event['channel']
    timestamp = event['ts']

    # Add "working" emoji reaction
    client.reactions_add(
        channel=channel,
        timestamp=timestamp,
        name="hourglass_flowing_sand"
    )

    try:
        # Process the message
        response = agent(text)
        say(text=str(response), thread_ts=timestamp)
        #say(text=Markdown(str(response)), thread_ts=timestamp)

    finally:
        # Remove "working" emoji and add "done" emoji
        client.reactions_remove(
            channel=channel,
            timestamp=timestamp,
            name="hourglass_flowing_sand"
        )
        client.reactions_add(
            channel=channel,
            timestamp=timestamp,
            name="white_check_mark"
        )

# Respond to messages in channels (without needing @mention)
@app.event("message")
def handle_message(event, say):
    # Avoid responding to bot's own messages
    if event.get('bot_id') is None:
        text = event.get('text', '').lower()
        
        # Example: respond to specific keywords
        if 'hello' in text:
            say("Hello! How can I help you?")
        elif 'help' in text:
            say("I'm here to assist! Try saying 'hello' or mentioning me.")

if __name__ == "__main__":
    # Socket Mode is easiest for development (no public URL needed)
    handler = SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN"))
    handler.start()