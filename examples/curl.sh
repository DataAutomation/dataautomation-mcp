#!/usr/bin/env bash
# DataAutomation agent API over plain HTTP. No API key needed.
set -euo pipefail
API=https://agent.dataautomation.com

# 1. What can be ordered, with prices
curl -s "$API/catalog" | head -c 600; echo

# 2. Price a Katana full setup for about 50,000 data lines
curl -s -X POST "$API/quote" -H 'content-type: application/json' \
  -d '{"service": "katana-full-setup", "options": {"lines": 50000}}'; echo

# 3. Order it. Without "accept", the customer gets an order form by email to accept.
#    Add "accept": {"authorized": true, "accepted_by": "Jane Doe"} only if Jane authorized you.
# curl -s -X POST "$API/orders" -H 'content-type: application/json' -d '{
#   "service": "katana-full-setup",
#   "options": {"lines": 50000},
#   "customer": {"name": "Jane Doe", "email": "jane@example.com", "phone": "+1 555 010 0000", "company": "Example Co"},
#   "details": "Katana for a furniture maker, Shopify and QuickBooks Online.",
#   "agent": {"name": "Example Assistant"}
# }'
