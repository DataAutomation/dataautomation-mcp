"""List, quote, and (optionally) order from DataAutomation over MCP, using only the standard library."""
import json
import urllib.request

MCP = "https://agent.dataautomation.com/mcp"


def call(method, params=None, _id=[0]):
    _id[0] += 1
    body = json.dumps({"jsonrpc": "2.0", "id": _id[0], "method": method, "params": params or {}}).encode()
    req = urllib.request.Request(MCP, data=body, headers={"content-type": "application/json", "accept": "application/json, text/event-stream"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())["result"]


def tool(name, **arguments):
    return call("tools/call", {"name": name, "arguments": arguments})["structuredContent"]


if __name__ == "__main__":
    call("initialize", {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "example", "version": "1.0"}})
    services = tool("list_services")
    print(json.dumps(services, indent=1)[:800], "...")
    print(tool("get_quote", service="integration", options={"flows": [{"source": "Shopify", "destination": "Katana", "data": "orders"}]}))
    # To place a real order, uncomment and use real customer details:
    # print(tool("create_order", service="integration",
    #            options={"flows": [{"source": "Shopify", "destination": "Katana", "data": "orders"}]},
    #            customer={"name": "Jane Doe", "email": "jane@example.com", "phone": "+1 555 010 0000"},
    #            agent={"name": "Example Assistant"}))
