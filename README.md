# DataAutomation MCP server

[![DataAutomation MCP connector: tool definition quality and endpoint health on Glama](https://glama.ai/mcp/connectors/com.dataautomation/agent/badges/score.svg)](https://glama.ai/mcp/connectors/com.dataautomation/agent) [![mcptry](https://mcptry.com/badge/com.dataautomation/agent)](https://mcptry.com/servers/com.dataautomation/agent)

A remote [Model Context Protocol](https://modelcontextprotocol.io) server that lets AI agents find, price, order, and pay for DataAutomation services on behalf of their user.

DataAutomation has built integrations and implemented business software since 2016: custom integrations between systems like Shopify, Katana MRP, QuickBooks, ShipStation, BigCommerce, Amazon, and EDI; Katana, ShipStation, Sutton, and RepZio implementations; QuickBooks Desktop to Online migrations; AI implementation; custom software; and fractional CAIO or CTO leadership.

- **Endpoint:** `https://agent.dataautomation.com/mcp` (Streamable HTTP, JSON responses)
- **Authentication:** none
- **Registry name:** `com.dataautomation/agent` in the [official MCP Registry](https://registry.modelcontextprotocol.io)
- **Docs for people:** <https://dataautomation.com/agents/>
- **Docs for agents:** <https://dataautomation.com/llms.txt>

## Connect

**Claude Desktop, Claude.ai, and other clients with remote MCP support:** add a custom connector with the URL `https://agent.dataautomation.com/mcp`.

**Claude Code:**

```bash
claude mcp add --transport http dataautomation https://agent.dataautomation.com/mcp
```

**Cursor, Windsurf, VS Code, and other JSON configs:**

```json
{
  "mcpServers": {
    "dataautomation": {
      "url": "https://agent.dataautomation.com/mcp"
    }
  }
}
```

**Clients that only run local (stdio) servers:**

```json
{
  "mcpServers": {
    "dataautomation": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://agent.dataautomation.com/mcp"]
    }
  }
}
```


## Interactive cards (MCP Apps)

`get_quote`, `create_order`, and `get_order_status` declare an MCP Apps UI (`ui://dataautomation/order-card.html`, `text/html;profile=mcp-app`). Hosts that support MCP Apps, such as Claude and VS Code, show quotes and orders as a card with Order, Pay, and Talk to a person buttons. Other hosts get the same JSON as before.

## WebMCP

Every page on dataautomation.com registers `list_services`, `get_quote`, `open_order_form`, `create_order`, and `book_a_call` through `navigator.modelContext` when the browser supports WebMCP. Setup steps for every app: https://dataautomation.com/connect-your-ai/

## Tools

| Tool | What it does | Side effects |
| --- | --- | --- |
| `list_services` | Every service with prices, delivery times, required inputs, and how it is ordered. Optional filters: `category`, `platform` (e.g. Katana), `query`. Call this first. | None (read only) |
| `get_quote` | Exact price for one service with its options. | None (read only) |
| `create_order` | Orders a service for the user. Optionally accepts for them and returns a Stripe payment link. | Creates an order and emails the user |
| `get_order_status` | Whether an order is accepted, paid, or cancelled, the cancel deadline, and a payment link while unpaid. | None (read only) |

Full input schemas, with every argument described, are in [`tools.json`](tools.json).

### Ordering rules for agents

- `customer.name`, `customer.email`, and `customer.phone` are required.
- **Accepting for the user.** Only when your user authorized the order, pass `accept: {"authorized": true, "accepted_by": "<their full name>"}`. The order is accepted at once and the response includes `payment_url` (Stripe Checkout). The user gets a confirmation email and can cancel within 48 hours for a full refund.
- **Without `accept`,** the user gets an order form by email, and the order is binding only after they accept it.
- Apps (SyncPersonalized, TokSync) are self-serve: send the user to the `signup_url` from `list_services`. The free discovery call uses `booking_url`.
- Orders are rate limited per IP and per customer email.

## Examples

- [`examples/curl.sh`](examples/curl.sh): the same flow over plain HTTP
- [`examples/order.py`](examples/order.py): list, quote, and order with the Python standard library

A quote, as an MCP call:

```json
{"jsonrpc": "2.0", "id": 1, "method": "tools/call",
 "params": {"name": "get_quote", "arguments": {"service": "katana-full-setup", "options": {"lines": 50000}}}}
```

returns a $5,000 quote ($0.10 per imported data line, $4,000 minimum).

## REST API

The same functions are available without MCP at `https://agent.dataautomation.com/` (`GET /catalog`, `POST /quote`, `POST /orders`, `GET /orders/{id}?key=`), described in [openapi.json](https://dataautomation.com/openapi.json). Browsing agents can also use the plain order form at <https://dataautomation.com/order/>.

## Prices

Current prices always come from `list_services`. At the time of writing: custom integrations are $100 per flow per month with no setup fee; Katana implementation starts at $2,300, and Katana full setup is $0.10 per imported data line with a $4,000 minimum; QuickBooks Desktop to Online migration is $2,500; training and fractional CAIO or CTO time are $250 per hour. See <https://dataautomation.com/pricing/>.

## Free skills

The [`skills/`](skills) folder has free Claude skills with the rules DataAutomation uses when it sets up [Katana MRP](skills/katana-mrp), [QuickBooks](skills/quickbooks), [Shopify](skills/shopify), and [ShipStation](skills/shipstation). Download them as .zip files at <https://dataautomation.com/skills/>, then upload in Claude under Customize > Skills, or copy a folder into `~/.claude/skills/` for Claude Code.

## Policies

[Store policy](https://agent.dataautomation.com/policy) · [Terms](https://dataautomation.com/terms-and-conditions/) · [Privacy](https://dataautomation.com/privacy-policy/) · [Data handling](https://dataautomation.com/data-handling-policy/) · [Security](SECURITY.md)

## About this repository

This repository documents the hosted server: its listing ([`server.json`](server.json)), tool schemas, and examples. The server itself is operated by DataAutomation; there is nothing to install or self-host.

Questions: [sales@dataautomation.com](mailto:sales@dataautomation.com) · (706) 705-9061
