import json

def fibonacci(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)


def response_function(args: str):
    params = json.loads(args)
    if params.get("method") == "fibonacci":
        return fibonacci(int(params.get("value")))
    else:
        return {"string": "Response Here"}