import boto3
import json

# Claude requires prompt to start exactly with: "\n\nHuman:"
prompt_text = "\n\nHuman: Act as Shakespeare and write a poem on Generative AI\n\nAssistant:"


bedrock = boto3.client(service_name = "bedrock-runtime")

payload = {
    "prompt": prompt_text,
    "max_tokens_to_sample": 512,
    "temperature": 0.7,
    "top_p": 0.9,
    "stop_sequences": ["\n\nHuman:"]
}

body =json.dumps(payload)
model_id = "anthropic.claude-v2"
response = bedrock.invoke_model(
    body = body,
    modelId = model_id,
    accept = "application/json",
    contentType = "application/json",
)

## filtering only the output
response_body = json.loads(response.get("body").read())
generated_text = response_body.get("completion", "").strip()

print(generated_text)