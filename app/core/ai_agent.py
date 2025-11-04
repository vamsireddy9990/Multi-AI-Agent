from langchain_groq import ChatGroq
from langchain_tavily import TavilySearch # Corrected import
from langchain.agents import create_agent
from langchain_core.messages.ai import AIMessage
# Import SystemMessage to correctly handle the system prompt
from langchain_core.messages import SystemMessage

from app.config.settings import settings

def get_response_from_ai_agents(llm_id , query , allow_search ,system_prompt):

    llm = ChatGroq(model=llm_id)

    tools = [TavilySearch(max_results=2)] if allow_search else [] # Corrected usage

    # FIX: Removed the unsupported 'state_modifier' argument.
    # The system prompt is now passed in the 'state' dictionary below.
    agent = create_agent(
        model=llm,
        tools=tools,
    )

    # Prepare the messages list, ensuring the System Prompt is the first message.
    # 'query' is a list of user messages from the frontend (which we assume is just one).
    messages = []
    if system_prompt:
        messages.append(SystemMessage(content=system_prompt))
    
    # Append the user's current query message(s)
    messages.extend(query)
    
    # The state object now includes the correctly structured messages list.
    state = {"messages" : messages}

    response = agent.invoke(state)

    messages = response.get("messages")

    ai_messages = [message.content for message in messages if isinstance(message,AIMessage)]

    return ai_messages[-1]
