class ToolsFactory:

    def new_tool_parameter(self, name, description, type = "string", required = False):

        return {
            "name":name,
            "type":type,
            "description": description,
            "required":required
        }


    def new_tool(self, function, description, parameters):

        name = function.__name__

        properties = {}
        required = []

        for parameter in parameters:
            properties[parameter["name"]] = {"type":parameter["type"], "description": parameter["description"]}
            if(parameter["required"] == True): required.append(parameter["name"])

        return {
            "python_fn": function,
            "tool":{
            "type": "function",
            "function": {
            "name": name,
            "description": description,
            "parameters": {
                "type": "object",
                "properties":properties,
                "required": required,
            }},
        },
}
        