class ResponseFormatFactory:

    def __init__(self):
        pass

    def new_json_schema(self, properties):

        props = {}
        required = []

        for property in properties:
            props[property["name"]] = {"type":property["type"]}
            if(property["required"] == True): required.append(property["name"])

        return {

            "type": "json_schema",
            "json_schema": {
                "name": "schema",
                "strict": "true",
                "schema": {
                    "type": "object",
                    "properties": props,
                    "required": required
                }
            }
        }
        

if __name__ == "__main__":

    r = ResponseFormatFactory()
    p = {"name":"arg_title", "type":"string", "required":True}
    a = r.new_json_schema(properties=[p])

    print(a)