#!/usr/bin/env python
# coding: utf-8

# # Lesson 5: Read the FAQ Manual

# ## Preparation 
# <p style="background-color:#fff6ff; padding:15px; border-width:3px; border-color:#efe6ef; border-style:solid; border-radius:6px"> 💻 &nbsp; <b>Access <code>requirements.txt</code> and <code>helper.py</code> and other files:</b> 1) click on the <em>"File"</em> option on the top menu of the notebook and then 2) click on <em>"Open"</em>. For more help, please see the <em>"Appendix - Tips and Help"</em> Lesson.</p>

# In[1]:


# Before you start, please run the following code to set up your environment.
# This code will reset the environment (if needed) and prepare the resources for the lesson.
# It does this by quickly running through all the code from the previous lessons.

get_ipython().system('sh ./ro_shared_data/reset.sh')
get_ipython().run_line_magic('run', './ro_shared_data/lesson_2_prep.py lesson5')
get_ipython().run_line_magic('run', './ro_shared_data/lesson_3_prep.py lesson5')
get_ipython().run_line_magic('run', './ro_shared_data/lesson_4_prep.py lesson5')
get_ipython().run_line_magic('run', './ro_shared_data/lesson_5_prep.py lesson5')

import os   

agentId = os.environ['BEDROCK_AGENT_ID']
agentAliasId = os.environ['BEDROCK_AGENT_ALIAS_ID']
region_name = 'us-west-2'
knowledgeBaseId = os.environ['KNOWLEDGEBASEID']


# ## Lesson starts here

# In[2]:


import boto3
import uuid, json
from helper import *


# In[3]:


bedrock_agent = boto3.client(service_name='bedrock-agent', region_name='us-west-2')


# In[4]:


describe_agent_response = bedrock_agent.get_agent(
    agentId=agentId
)


# In[5]:


print(json.dumps(describe_agent_response, indent=4, default=str))


# In[6]:


print(describe_agent_response['agent']['instruction'])


# ### Look at the knowledge base

# In[7]:


get_knowledge_base_response = bedrock_agent.get_knowledge_base(
    knowledgeBaseId=knowledgeBaseId
)


# In[ ]:


print(json.dumps(get_knowledge_base_response, indent=4, default=str))


# ### Connect the knowledge base

# In[11]:


associate_agent_knowledge_base_response = bedrock_agent.associate_agent_knowledge_base(
    agentId=agentId,
    knowledgeBaseId=knowledgeBaseId,
    agentVersion='DRAFT',
    description='my-kb'
)


# In[ ]:


associate_agent_knowledge_base_response


# ### Prepare agent and alias

# In[ ]:


bedrock_agent.prepare_agent(
    agentId=agentId
)

wait_for_agent_status(
    agentId=agentId,
    targetStatus='PREPARED'
)

bedrock_agent.update_agent_alias(
    agentId=agentId,
    agentAliasId=agentAliasId,
    agentAliasName='MyAgentAlias',
)

wait_for_agent_alias_status(
    agentId=agentId,
    agentAliasId=agentAliasId,
    targetStatus='PREPARED'
)


# ### Try it out

# In[16]:


sessionId = str(uuid.uuid4())
message=""""mike@mike.com - I bought a mug 10 weeks ago and now it's broken. I want a refund."""


# In[ ]:


invoke_agent_and_print(
    agentId=agentId,
    agentAliasId=agentAliasId,
    inputText=message,  
    sessionId=sessionId,
    enableTrace=False
)


# In[ ]:


message=""""It's just a minor crack.  What can I do?"""


# In[ ]:


invoke_agent_and_print(
    agentId=agentId,
    agentAliasId=agentAliasId,
    inputText=message,  
    sessionId=sessionId,
    enableTrace=True
)


# ### Another Question, new session

# In[19]:


sessionId = str(uuid.uuid4())
message=""""My mug is chipped, what can I do?"""


# In[ ]:


invoke_agent_and_print(
    agentId=agentId,
    agentAliasId=agentAliasId,
    inputText=message,  
    sessionId=sessionId,
    enableTrace=True
)


# In[21]:


message=""""mike@mike.com - I am not happy.  I bought this mug yesterday. I want a refund."""


# In[ ]:


invoke_agent_and_print(
    agentId=agentId,
    agentAliasId=agentAliasId,
    inputText=message,  
    sessionId=sessionId,
    enableTrace=True
)


# In[ ]:





# In[ ]:


sessionId = str(uuid.uuid4())
message=""""Try your own message"""

