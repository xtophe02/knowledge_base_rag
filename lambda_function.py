import json

# 1. import boto3
import boto3

# 2 create client connection with bedrock
client_bedrock_knowledgebase = boto3.client("bedrock-agent-runtime")


def lambda_handler(event, context):
    # 3 Store the user prompt
    print(event["prompt"])
    user_prompt = event["prompt"]
    # 4. Use retrieve and generate API
    client_knowledgebase = client_bedrock_knowledgebase.retrieve_and_generate(
        input={"text": user_prompt},
        retrieveAndGenerateConfiguration={
            "type": "KNOWLEDGE_BASE",
            "knowledgeBaseConfiguration": {
                "knowledgeBaseId": "YOUR_KNOWLEDGE_BASE_ID",
                "modelArn": "arn:aws:bedrock:us-west-2::foundation-model/anthropic.claude-instant-v1",
            },
        },
    )

    # print(client_knowledgebase)
    # print(client_knowledgebase['output']['text'])
    # print(client_knowledgebase['citations'][0]['generatedResponsePart']['textResponsePart'])
    response_kbase_text = client_knowledgebase["output"]["text"]
    response_kbase_citations = client_knowledgebase["citations"][0][
        "generatedResponsePart"
    ]["textResponsePart"]

    response_body = {"text": response_kbase_text, "citations": response_kbase_citations}
    return {"statusCode": 200, "body": json.dumps(response_body)}
