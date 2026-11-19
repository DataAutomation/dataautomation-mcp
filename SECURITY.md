# Security

## Reporting a vulnerability

Email [support@dataautomation.com](mailto:support@dataautomation.com) with "Security" in the subject. Please include steps to reproduce. We reply within two business days and ask that you give us a reasonable time to fix the issue before disclosing it.

## How the server handles data

- No authentication is required to read the catalog or request quotes. Nothing about the caller is stored for those calls.
- `create_order` stores the customer details you send (name, email, phone, company, website, and what they need) so DataAutomation can deliver the order. It does not take or store card numbers; payment happens on Stripe Checkout.
- Order status needs both the order id and the secret `status_key` returned when the order was created.
- Order and cancel links are signed. Stripe webhooks are verified with Stripe's signature.
- Orders are rate limited per IP and per customer email.

DataAutomation has been audited by Deloitte and PwC and completed Amazon's SP-API security assessment. See <https://dataautomation.com/audits/>.
