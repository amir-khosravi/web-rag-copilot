import os
from typing import List
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import AIMessage
from app.common.logger import get_logger
from app.config.settings import settings

logger = get_logger(__name__)

def retrieve_knowledge_base(query: str) -> str:
    """Placeholder for Vector Database Retrieval (Pinecone/Milvus)."""
    return ""

def get_response_from_ai_agents(
    model_id: str, 
    query: List[str], 
    allow_search: bool, 
    system_prompt: str
) -> str:
    try:
        # 1. Setup LLM (Groq)
        llm = ChatGroq(model=model_id, api_key=settings.GROQ_API_KEY)
        
        # 2. Setup Tools (Web RAG)
        tools = []
        if allow_search:
            # Explicitly pass the key for Tavily
            os.environ["TAVILY_API_KEY"] = settings.TAVILY_API_KEY
            tools.append(TavilySearchResults(max_results=2))

        # 3. RAG Context Injection
        internal_context = retrieve_knowledge_base(query[-1] if query else "")
        enhanced_system_prompt = f"""{system_prompt}\n\nCONTEXT FROM INTERNAL KB:\n{internal_context}"""

        # 4. Create Agent
        agent = create_react_agent(model=llm, tools=tools, state_modifier=enhanced_system_prompt)

        # 5. Execute
        state = {"messages": query}
        response = agent.invoke(state)
        messages = response.get("messages", [])
        ai_messages = [msg.content for msg in messages if isinstance(msg, AIMessage)]
        
        return ai_messages[-1] if ai_messages else "No response generated."

    except Exception as e:
        logger.error(f"Error in RAG pipeline: {str(e)}")
        raise e