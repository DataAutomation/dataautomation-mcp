"""Refresh tools.json, the README tool table, and server.json from the live MCP server. Usage: python3 scripts/sync_from_live.py <version> ["description"]"""
import json, re, subprocess, sys
req = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/list"})
out = subprocess.run(['curl', '-s', '-m', '20', '-X', 'POST', 'https://agent.dataautomation.com/mcp', '-H', 'Content-Type: application/json',
                      '-H', 'Accept: application/json, text/event-stream', '-d', req], capture_output=True, text=True).stdout
tools = json.loads(out)['result']['tools']
keep = [{k: t[k] for k in ('name', 'title', 'description', 'inputSchema', 'annotations', '_meta') if k in t} for t in tools]
open('tools.json', 'w').write(json.dumps(keep, indent=2, ensure_ascii=False) + '\n')
def effect(t):
    a = t.get('annotations', {})
    if a.get('readOnlyHint'): return 'None (read only)'
    return {'create_order': 'Creates an order and emails the user', 'map_workflow': 'Starts a mapping job; emails the result only with consent',
            'start_app_signup': 'Emails the person a setup link; creates an unconfirmed login until they click it'}.get(t['name'], 'Writes data')
OVR = {'map_workflow': 'Map a described workflow to the systems, steps, and DataAutomation services it needs, before buying.'}
def short(d):
    d = re.sub(r'\s+', ' ', d).strip()
    m = re.match(r'(.+?\.)\s', d + ' ')
    return (m.group(1) if m else d).replace('|', '/')
rows = '\n'.join(f"| `{t['name']}` | {OVR.get(t['name']) or short(t['description'])} | {effect(t)} |" for t in tools)
r = open('README.md').read()
r = re.sub(r'(\| Tool \| What it does \| Side effects \|\n\| --- \| --- \| --- \|\n)(?:\|.*\|\n)+', lambda m: m.group(1) + rows + '\n', r, count=1)
open('README.md', 'w').write(r)
s = json.load(open('server.json'))
s['description'] = sys.argv[2] if len(sys.argv) > 2 else s['description']
s['version'] = sys.argv[1]
open('server.json', 'w').write(json.dumps(s, indent=2, ensure_ascii=False) + '\n')
print(len(tools), 'tools;', s['version'], len(s['description']), 'chars')
