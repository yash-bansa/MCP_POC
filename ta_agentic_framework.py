# from mcp.server.fastmcp import FastMCP
# from langchain_groq import ChatGroq
# from langchain.prompts import ChatPromptTemplate
# import os

# # ----------- CONFIGURE GROQ -----------
# GROQ_API_KEY = os.getenv("GROQ_API_KEY", "your-groq-api-key")
# GROQ_MODEL = "llama3-70b-8192"  # or "llama3-70b-8192"

# llm = ChatGroq(
#     groq_api_key=GROQ_API_KEY,
#     model_name=GROQ_MODEL,
#     temperature=0.2
# )

# # ----------- INIT MCP SERVER -----------
# mcp = FastMCP("ta_agentic_framework")


# # ----------- AGENT 1: Summarizer -----------
# @mcp.tool(name="summarizer_agent")
# async def summarize_text(text: str) -> str:
#     """Summarize the input text."""
#     prompt = ChatPromptTemplate.from_messages([
#         ("system", "You are a helpful assistant that summarizes long text."),
#         ("human", "Please summarize the following:\n\n{text}")
#     ])
#     chain = prompt | llm
#     result = chain.invoke({"text": text})
#     return result.content


# # ----------- AGENT 2: SQL Generator -----------
# @mcp.tool(name="sql_generator_agent")
# async def generate_sql(user_query: str, data_dictionary: str) -> str:
#     """Generate an SQL query from user input and schema. Supports dialects like MySQL, PostgreSQL, etc."""
#     prompt = ChatPromptTemplate.from_messages([
#         ("system", "You are an expert SQL query generator."),
#         ("human", "Given the data dictionary:\n{schema}\n\nAnd the user query:\n{query}")
#     ])
#     chain = prompt | llm
#     result = chain.invoke({"schema": data_dictionary, "query": user_query})
#     return result.content


# # ----------- START MCP SERVER -----------
# if __name__ == "__main__":
#     os.environ["MCP_SERVER_PORT"] = "8501" 
#     mcp.run(transport="streamable-http")



from mcp.server.fastmcp import FastMCP
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
import os


# ------------ CONFIGURE GROQ ------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "your-groq-api-key")
GROQ_MODEL = "mixtral-8x7b-32768"

llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name=GROQ_MODEL,
    temperature=0.2
)

# ------------ INIT MCP SERVER ------------
mcp = FastMCP("ta_agentic_framework")


# ------------ AGENT 1: Summarizer ------------
@mcp.tool(name="summarizer_agent")
async def summarize_text(text: str) -> str:
    """Summarize the input text."""
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant that summarizes long text."),
        ("human", "Please summarize the following:\n\n{text}")
    ])
    chain = prompt | llm
    result = chain.invoke({"text": text})
    return result.content


# ------------ AGENT 2: SQL Generator ------------
@mcp.tool(name="sql_generator_agent")
async def generate_sql(user_query: str, data_dictionary: str, dialect: str = "MySQL") -> str:
    """Generate an SQL query from user input and schema. Supports dialects like MySQL, PostgreSQL, etc."""
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert SQL query generator."),
        ("human", "Given the data dictionary:\n{schema}\n\nAnd the user query:\n{query}\n\nWrite a {dialect} SQL query.")
    ])
    chain = prompt | llm
    result = chain.invoke({"schema": data_dictionary, "query": user_query})
    return result.content


# ------------ RUN MCP ON CUSTOM PORT USING UVICORN ------------
if __name__ == "__main__":
     mcp.run(transport="streamable-http")

