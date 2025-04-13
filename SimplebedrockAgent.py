import os
import boto3
from helper import *
# Agent status are creating, NotPrepared, Prepairing, Prepared

roleArn = os.environ['BEDROCKAGENTROLE']

# initialing the bedrock agent using our boto3 library
bedrock_agent = boto3.client(service_name='bedrock-agent', region_name='us-west-2')

# Creating the agent
create_agent_response = bedrock_agent.create_agent(
    agentName='mugs-customer-support-agent',
    foundationModel='anthropic.claude-3-haiku-20240307-v1:0',
    instruction="""You are an advanced AI agent acting as a front line customer support agent.""",
    agentResourceRoleArn=roleArn
)

# Check the response of agent creation, initially it should be creating status
create_agent_response

# Extracting the agentId from response
agentId = create_agent_response['agent']['agentId']

# Waiting for agent to reach status: NOT_PREPARED
wait_for_agent_status(
    agentId=agentId, 
    targetStatus='NOT_PREPARED'
)

# once agent is in NOT_PREPARED status, then we can prepare it
bedrock_agent.prepare_agent(
    agentId=agentId
)

#now waiting for the agent to become PREPARED status
wait_for_agent_status(
    agentId=agentId, 
    targetStatus='PREPARED'
)

# Below steps create a agent alias and bring it till Prepaid status
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
# initialing the bedrock agent runtime using our boto3 library
bedrock_agent_runtime = boto3.client(service_name='bedrock-agent-runtime', region_name='us-west-2')

import uuid


# The below code returns a very  detailed reponse
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


# The below code returns a very readble anc crisp response

message = "Hello, I bought a mug from your store yesterday, and it broke. I want to return it."

sessionId = str(uuid.uuid4())

invoke_agent_and_print(
    agentAliasId=agentAliasId,
    agentId=agentId,
    sessionId=sessionId,
    inputText=message,
    enableTrace=True,
)