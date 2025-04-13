import os

roleArn = os.environ['BEDROCKAGENTROLE']

import boto3

bedrock_agent = boto3.client(service_name='bedrock-agent', region_name='us-west-2')

create_agent_response = bedrock_agent.create_agent(
    agentName='mugs-customer-support-agent',
    foundationModel='anthropic.claude-3-haiku-20240307-v1:0',
    instruction="""You are an advanced AI agent acting as a front line customer support agent.""",
    agentResourceRoleArn=roleArn
)

create_agent_response

agentId = create_agent_response['agent']['agentId']

from helper import *

wait_for_agent_status(
    agentId=agentId, 
    targetStatus='NOT_PREPARED'
)

bedrock_agent.prepare_agent(
    agentId=agentId
)

wait_for_agent_status(
    agentId=agentId, 
    targetStatus='PREPARED'
)

create_agent_alias_response = bedrock_agent.create_agent_alias(
    agentId=agentId,
    agentAliasName='MyAgentAlias',
)

agentAliasId = create_agent_alias_response['agentAlias']['agentAliasId']

wait_for_agent_alias_status(
    agentId=agentId,
    agentAliasId=agentAliasId,
    targetStatus='PREPARED'
)

bedrock_agent_runtime = boto3.client(service_name='bedrock-agent-runtime', region_name='us-west-2')

import uuid

message = "Hello, I bought a mug from your store yesterday, and it broke. I want to return it."

sessionId = str(uuid.uuid4())

invoke_agent_response = bedrock_agent_runtime.invoke_agent(
    agentId=agentId,
    agentAliasId=agentAliasId,
    inputText=message,
    sessionId=sessionId,
    endSession=False,
    enableTrace=True,
)

event_stream = invoke_agent_response["completion"]

for event in event_stream:
    print(event)

message = "Hello, I bought a mug from your store yesterday, and it broke. I want to return it."

sessionId = str(uuid.uuid4())


invoke_agent_and_print(
    agentAliasId=agentAliasId,
    agentId=agentId,
    sessionId=sessionId,
    inputText=message,
    enableTrace=True,
)