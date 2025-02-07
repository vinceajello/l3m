
from modules.l3m import L3M
from modules.tool import ToolsFactory

from tools.web_search import web_search

system_prompt = (
            "You are an assistant that can retrieve online informatoins on the web. "
            "When asked about a topic, you can retrieve informations online "
            "and cite information from them. Today is 3 February 2025."
        )

llm = L3M(base_url="http://0.0.0.0:1234/v1", model="llama-3.3-70b-instruct@q4_k_m", system=system_prompt)

user_input = "\nYou: What are the next coming pc games"

response_format_props = [{"name":"response", "type": "string", "required":True}]    
response_format_props = None

tool_factory = ToolsFactory()
search_query_parameter = tool_factory.new_tool_parameter(name="search_query", description="Search query for finding the contents on the search engine", required=True)
tool_parameters = [search_query_parameter]

tool_description = (
        "Search the web and fetch the content of the most relevant pages."
        "Always use this if you dont know something or the user is asking for something that is likely found online."
        "Augment the search query with all the information needed to find content online."
    )
web_search_tool = tool_factory.new_tool(function=web_search, description=tool_description, parameters=tool_parameters)

response = llm.completion(input=user_input, tools=[web_search_tool], response_format_props=response_format_props, stream=True)
collected_content = llm.print_stream(stream=response)
