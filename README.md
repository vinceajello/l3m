# L3M

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)  

L3M is a little LLM client for Python that keeps things simple while packing some powerful features like structured output, tool use, and more... 🚀🐍🦙

~~~bash  
# READY TO GO EXAMPLE
git clone https://github.com/vinceajello/l3m.git
cd l3m
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python example.py
~~~

L3M allow to connect to local api that are compliant with the OpenAI standard

LM Studio server has been used during development so it has been extensively tested

~~~bash  
from modules.l3m import L3M

llm = L3M(base_url="http://0.0.0.0:1234/v1", model="your_local_model")
~~~

If you prefer to use remote models you have just to define a **model_name** and an **api_key**

~~~bash  
llm = L3M(model="your_local_model", api_key="your_api_key")
~~~

You can simply define a system prompt using **system** parameter
~~~bash  
llm = L3M(model="your_local_model", api_key="your_api_key", system="You are a medieval knight.")
~~~

You can change system prompt at any time before generation using:

~~~bash  
llm.set_system_prompt(system="now you are a pirate")
~~~

Start the generation calling the completion method:

~~~bash  
response = llm.completion(input="Hello")
~~~

Set **stream=True** if you need to stream the response

~~~bash  
generator = llm.completion(input="Hello", stream=True)
response = llm.print_stream(stream=generator)
~~~

If you you need to **structure** the output following a defined **schema** you can do:

Note: to use structured output you need to use a model that have that feature 

~~~bash
props = [{"name":"answer", "type": "string", "required":True}]    
response = llm.completion(input="Hello", response_format_props=props)
~~~

You can pass one or more python function/s to the llm as tools

The following example shows the use of a tool:

Note: as with structured output to use tools you need to use a model that have that feature 

~~~bash
from tools.web_search import web_search_tool
input = "You: What are the next coming medieval pc games"
generator = llm.completion(input=input, tools=[web_search_tool], stream=True)
response = llm.print_stream(stream=generator)
~~~

And here is how to define you own tools:

~~~bash
def your_python_function(parameter_name):

    # Where magic things happen

    return "must return some text"

tool_factory = ToolsFactory()
search_query_parameter = tool_factory.new_tool_parameter(name="search_query", description="Search query for finding the contents on the search engine", required=True)
tool_parameters = [search_query_parameter]

tool_description = (
        "Search the web and fetch the content of the most relevant pages."
        "Always use this if you dont know something or the user is asking for something that is likely found online."
        "Augment the search query with all the information needed to find content online."
    )
web_search_tool = tool_factory.new_tool(function=your_python_function, description=tool_description, parameters=tool_parameters)
~~~

~~~bash
input = "A prompt that require the use of your tool"
response = llm.completion(input=input, tools=[your_tool])
~~~

# Happy generation!

## Futures (just don't bet on it)

- Return info about the used tool
- Return conversation
- Memory management  
- Include a simple RAG

## Feedback  

If you have any feedback, please reach me out at vince.ajello@themailwithg.com 😉

## License  

[MIT](https://choosealicense.com/licenses/mit/)
