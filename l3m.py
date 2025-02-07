
import json

from openai import OpenAI

from modules.response_format import ResponseFormatFactory
from modules.tool import ToolsFactory

class L3M:

    def __init__(self, base_url = None, api_key = "None", model="None", system = None):

        client_args = { "api_key":api_key }

        if base_url:
            client_args["base_url"] = base_url

        self.model_name = model
        self.system_prompt = system
        self.client = OpenAI(**client_args)
        self.response_format_factory = ResponseFormatFactory()
        self.tools_factory = ToolsFactory()
        self.tools_functions = {}

    def set_system_prompt(self, system):

        if len(self.messages)>0:
            if self.messages[0]["role"] == "system":
                self.messages[0]["content"] = system

        self.system_prompt = system

    def completion(self, input, messages = [], response_format_props = None, tools=None, stream=False):

        messages = [] + messages

        if self.system_prompt and len(messages) <= 0:
            messages.append({ "role": "system", "content": self.system_prompt})

        if input:
            messages.append({"role": "user", "content": input})

        args = {
            "model":self.model_name,
            "messages":messages,
            "stream":stream
        }

        if not tools and response_format_props:
            args["response_format"] = self.response_format_factory.new_json_schema(properties=response_format_props)

        if tools:
            TOOLS = []
            for tool in tools: 
                print(tool)
                self.tools_functions = {f"{tool["tool"]["function"]["name"]}":tool["python_fn"]}
                TOOLS.append(tool["tool"])
            args["tools"] = TOOLS
            args["stream"] = False

        completions = self.client.chat.completions.create(**args)

        if not hasattr(completions, 'choices'):
            return completions

        if completions.choices[0].message.tool_calls:

            message_tool_calls = completions.choices[0].message.tool_calls
            
            tool_calls = [ { "id": tool_call.id, "type": tool_call.type, "function": tool_call.function } for tool_call in message_tool_calls ]
            messages.append( {"role": "assistant", "tool_calls": tool_calls})

            for tool_call in message_tool_calls:
                args = json.loads(tool_call.function.arguments)
                function_name = tool_call.function.name
                function = self.tools_functions[function_name]
                docs = function(args)

                if len(docs) <= 0:
                    messages.append({ "role": "tool", "content": json.dumps({"result":"No informations found online"}), "tool_call_id": tool_call.id })
                for doc in docs:
                    messages.append({ "role": "tool", "content": json.dumps({"result":doc["content"]}), "tool_call_id": tool_call.id })

            return self.completion(input=None, messages=messages, response_format_props=response_format_props, stream=stream)

        return completions

    @staticmethod
    def print_stream(stream):
        print()
        collected_content = ""
        for chunk in stream:
            if chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                print(content, end="", flush=True)
                collected_content += content
        print()
        return collected_content