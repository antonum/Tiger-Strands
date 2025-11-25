import boto3
import json

client = boto3.client('bedrock-agentcore', region_name='us-east-2')
payload = json.dumps({"prompt": "list my tiger services"})

response = client.invoke_agent_runtime(
    agentRuntimeArn='arn:aws:bedrock-agentcore:us-east-2:637423233204:runtime/tigeragent-euLdYk2j7o',
    runtimeSessionId='dfmeoagmreaklgmrkleafremoigrmtesogmtrskhmtkrlshmt',  # Must be 33+ chars
    payload=payload,
    qualifier="DEFAULT" # Optional
)

# Handle streaming response
print("Agent Response (streaming):")
print("-" * 80)

# The response body is a streaming response
response_body = response['response']

# Read and decode the streaming response
accumulated_text = ""
for chunk in response_body.iter_lines():
    if chunk:
        try:
            # Decode the chunk
            chunk_str = chunk.decode('utf-8')

            # Remove 'data: ' prefix if present
            if chunk_str.startswith('data: '):
                chunk_str = chunk_str[6:]

            # Try to parse as JSON
            try:
                chunk_data = json.loads(chunk_str)

                # Check if this is a contentBlockDelta event with text
                if isinstance(chunk_data, dict) and 'event' in chunk_data:
                    event = chunk_data['event']
                    if 'contentBlockDelta' in event:
                        delta = event['contentBlockDelta'].get('delta', {})
                        if 'text' in delta:
                            text = delta['text']
                            print(text, end='', flush=True)
                            accumulated_text += text
            except json.JSONDecodeError:
                # If it's not valid JSON, skip it
                pass

        except Exception as e:
            print(f"\nError processing chunk: {e}")

print("\n" + "-" * 80)
print(f"\nTotal characters received: {len(accumulated_text)}")