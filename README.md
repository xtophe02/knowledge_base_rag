# Serverless e-Venthone App Using Knowledge Base for Amazon Bedrock

This guide provides step-by-step instructions for setting up a serverless e-Venthone application that utilizes a knowledge base with Amazon Bedrock. The architecture includes AWS services such as API Gateway, Lambda, Amazon Bedrock, OpenSearch, and S3.

## Prerequisites

- **AWS Account**: Ensure you have an AWS account with the necessary permissions to create and manage AWS resources.
- **AWS CLI**: Install and configure the AWS CLI on your local machine.
- **Python and pip**: Install Python and pip if needed for running local scripts.

## Architecture Overview

The architecture of the application includes the following components:

1. **AWS API Gateway**: Provides an endpoint to receive user prompts.
2. **AWS Lambda**: Processes requests from the API Gateway and interacts with the knowledge base.
3. **Amazon Bedrock (Claude FM, Amazon Titan)**: Generates responses based on user prompts.
4. **Knowledge Base**:
   - **AWS OpenSearch**: Acts as a vector store to index and search documents.
   - **Amazon S3**: Stores PDF documents, which are processed and chunked.
   - **RAG (Retrieval-Augmented Generation)**: Integrates document retrieval with model generation.

## Step-by-Step Guide

### 1. Set Up Amazon S3 Bucket

1. Log in to the AWS Management Console.
2. Navigate to **S3** and create a new bucket (e.g., `venthone-pdfs`).
3. Upload your PDF documents to this bucket. These documents will be used to populate the knowledge base.

### 2. Deploy Lambda Function

1. Go to **AWS Lambda** in the AWS Management Console.
2. Create a new function (e.g., `knowledge-base-lambda`).
   - Choose "Author from scratch."
   - Select Python, Node.js, or another runtime of your choice.
3. Implement the Lambda function code to:
   - Receive and process requests from API Gateway.
   - Interact with Amazon Bedrock to retrieve and generate responses based on the user prompt.
   - Optionally, query OpenSearch if required.
   - Return the generated response to the API Gateway.
4. Deploy the function and take note of the function's ARN.

```python
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

```

### 3. Configure Amazon Bedrock and Knowledge Base

#### Set Up the RAG Pipeline

1. Configure the Amazon S3 data source:

   - Use default parsing and chunking strategies for document processing.

2. Set up the **Embeddings Model**:

   - Titan Embeddings G1 - Text v1.2

3. Configure the **Vector Database**:

   - Use **Amazon OpenSearch Serverless**.

4. Ensure that your Lambda function:
   - Uses context retrieved from OpenSearch if necessary.
   - Combines this context with the user prompt.
   - Sends the combined input to Amazon Bedrock for response generation.

### 4. Set Up AWS API Gateway

1. Navigate to **API Gateway** in the AWS Management Console.
2. Create a new REST API.
3. Add a `GET` method and integrate it with the Lambda function you created.
4. Configure the method request:

   - **Request validator**: Validate body, query string parameters, and headers.
   - **URL query string parameters**: Define a parameter named `prompt`, corresponding to the Lambda function input.

5. Configure the Integration Request:
   - **Mapping templates**: Set content type to `application/json`.
   - Define the necessary mappings to pass the query parameters to the Lambda function.

```json
{
  "prompt": "$input.params('prompt')"
}
```

6. Deploy the API.

### 5. Testing

1. Use a REST client like Postman to test the API Gateway endpoint.
2. Send a `GET` request with the `prompt` as a query parameter.
   - Example: `GET https://{api-id}.execute-api.{region}.amazonaws.com/dev/?prompt=Your+Prompt+Here`
3. Verify the response to ensure it is accurate and meets your requirements.

## Conclusion

By following this guide, you will have set up a serverless e-Venthone application that uses Amazon Bedrock and a knowledge base to generate intelligent responses to user prompts.
