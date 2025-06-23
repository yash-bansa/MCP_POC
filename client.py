from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq

from dotenv import load_dotenv
load_dotenv()

import asyncio

async def main():
    client=MultiServerMCPClient(
        {
            "math":{
                "command":"python",
                "args":["mathserver.py"], ## Ensure correct absolute path
                "transport":"stdio",
            
            },
            # "weather": {
            #     "url": "http://localhost:8000/mcp",  # Ensure server is running here
            #     "transport": "streamable_http",
            # },
            "ta_agentic_framework" : {
                "url": "http://localhost:8000/mcp",  # Ensure server is running here
                "transport": "streamable_http",
            }

        }
    )

    import os
    os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")

    tools=await client.get_tools()
    model=ChatGroq(model="llama3-70b-8192")
    agent=create_react_agent(
        model,tools
    )

    math_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "what's (3 + 5) x 12?"}]}
    )

    print("Math response:", math_response['messages'][-1].content)

    # weather_response = await agent.ainvoke(
    #     {"messages": [{"role": "user", "content": "what is the weather in California?"}]}
    # )
    # print("Weather response:", weather_response['messages'][-1].content)

    ta_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "Summarize this: To instantiate AutoCodeRover as a Unified Software Engineering Agent (USEagent), the process involves several key steps:\n\n1. **Decompose Existing Workflow**: The first step is to break down the fixed workflow of AutoCodeRover into distinct components or phases. This allows for a more modular approach, where each phase can be addressed individually.\n\n2. **Implement Orchestration**: After decomposing the workflow, orchestration needs to be added. This orchestration will determine which component to invoke based on the type of task and the current state of the task. This decision-making capability is crucial for adapting to various software engineering tasks effectively.\n\n3. **Test Generation Tasks**: In scenarios where AutoCodeRover may not be directly applicable, the USEagent has shown versatility with a reported efficacy of 31.8% in test generation tasks. This indicates that the USEagent can adapt and perform effectively even in cases where traditional methods may fall short.\n\n4. **Integration with USEbench**: The development of USEbench, a benchmark for evaluating the performance of software engineering agents, plays a significant role. AutoCodeRover is expanded upon to participate in solving tasks defined within USEbench, thus enhancing its capabilities as a USEagent.\n\nBy following these steps, AutoCodeRover can be effectively instantiated as a Unified Software Engineering Agent, capable of handling a variety of tasks within the software engineering domain.'"}]}
    )
    print("🧠 Summarizer response:", ta_response['messages'][-1].content)

    sql_response = await agent.ainvoke({
    "messages": [{
        "role": "user",
        "content": (
            "Using this schema:\n"
            "Table: employees(id INT, name TEXT, department TEXT, salary INT, join_date DATE)\n\n"
            "Write a query to get the average salary of employees who joined after 2020, "
            "grouped by department, in PostgreSQL."
            "dileact : PostgreSQL "
        )
        }]
    })

    print("🛠️ SQL response:", sql_response['messages'][-1].content)

asyncio.run(main())
