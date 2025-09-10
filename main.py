from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools import search_tool, wiki_tool, save_tool
from config import google_api_key
import json

class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=google_api_key)
parser = PydanticOutputParser(pydantic_object=ResearchResponse)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a research assistant that will help generate a research paper.
            Answer the user query and use neccessary tools. 
            Wrap the output in this format and provide no other text\n{format_instructions}
            """,
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())

tools = [search_tool, wiki_tool, save_tool]
agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=tools
)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

while True:
    query = input("What can I help you research? (Type 'exit' to quit) ")
    if query.strip().lower() == "exit":
        break
    raw_response = agent_executor.invoke({"query": query})

    try:
        output_str = raw_response.get("output")
        # Remove code block markers if present
        if output_str.startswith("```json"):
            output_str = output_str[len("```json"):]
        if output_str.startswith("```"):
            output_str = output_str[len("```"):]
        output_str = output_str.strip()
        if output_str.endswith("```"):
            output_str = output_str[:-3].strip()
        # Now parse JSON
        response_dict = json.loads(output_str)
        structured_response = ResearchResponse.model_validate(response_dict)
        print("\n" + structured_response.summary)
        print("Sources:", *structured_response.sources, sep="\n- ")
        print("Tools used:", *structured_response.tools_used, sep="\n- ")
        print()
    except Exception as e:
        print("Error parsing response", e, "Raw Response - ", raw_response)