# AI security incidents

`ai-security-incidents.json` feeds the banner and the incident log at https://dataautomation.com/ai-security/. It is refreshed daily.

Format: `updated` (YYYY-MM-DD), `stats` (IBM Cost of a Data Breach figures), and `incidents`, newest first, each with `date`, `title`, `category`, `summary` (our own words), `source`, and `url` (the original report).

The list is a permanent archive: incidents are added, never removed. Each incident has exactly one `category`:

- `Leaked AI chats`: what people typed into AI tools was exposed
- `AI vendor breach`: an AI company or its supplier was breached
- `AI agent misuse`: an AI agent used access it should not have
- `Stolen AI keys`: AI API keys or credentials were stolen or abused
- `AI tool vulnerability`: a serious flaw in an AI tool or MCP server
- `Poisoned AI software`: a tampered AI package, extension, or model
- `AI-powered attack`: attackers used AI tools to break in
