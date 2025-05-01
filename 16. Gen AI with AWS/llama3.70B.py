import boto3
import json

# Your prompt text
prompt_text = "Act as Shakespeare and write a poem on machine learning"

# Payload to send to Meta LLaMA 3 via the API
payload = {
    "modelId": "meta.llama3-70b-instruct-v1:0",
    "contentType": "application/json",
    "accept": "application/json",
    "body": json.dumps({
        "prompt": f"[INST] {prompt_text} [/INST]",  # Using the correct prompt format
        "max_gen_len": 512,  # Max tokens to generate
        "temperature": 0.5,  # Sampling temperature
        "top_p": 0.9         # Top-p sampling (nucleus sampling)
    })
}

# Creating the Bedrock client (replace 'your_region' with the appropriate AWS region)
bedrock = boto3.client(service_name="bedrock-runtime", region_name="us-east-1")

try:
    # Sending the request to invoke the model
    response = bedrock.invoke_model(
        modelId=payload["modelId"],  # Model ID
        contentType=payload["contentType"],  # Content type (JSON)
        accept=payload["accept"],  # Acceptable response type (JSON)
        body=payload["body"]  # The JSON body (converted to a string)
    )

    # Parsing the response body to extract the generated text
    response_body = json.loads(response["body"].read())
    generated_text = response_body.get("generation", "").strip()

    # Output the generated text
    print("Generated text:", generated_text)

except Exception as e:
    print("Error:", str(e))
