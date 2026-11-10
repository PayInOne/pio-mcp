# PIO MCP

Connect a compatible AI client to your existing PIO account to read the team records you are permitted to access: workspace and tasks, payroll, bills and payments, contracts, company cards, expenses and incentives, employees and time off, onboarding and company verification. Team tools are read-only: they cannot pay, approve or recalculate payroll, edit employees, sign contracts or send messages.

This repository provides PIO's hosted MCP connection details, reusable workflow skills and client-specific setup guides. The MCP endpoints are shared across compatible clients. Plugin packaging, installation, authentication support and marketplace review depend on the client; one plugin package is not a universal installer.

A separate public connection provides published PIO product information and hypothetical employment-cost estimates without an account. Its cost tool creates a calculation job, without creating a business record.

The two hosted servers are listed in the [official MCP Registry](https://registry.modelcontextprotocol.io/?q=io.github.PayInOne). Registry listing publishes server metadata; it does not imply approval or publication in any client's marketplace.

## Choose a connection

| Connection | Purpose | Authentication |
| --- | --- | --- |
| `pio` | Read the connected team's permitted data | PIO OAuth in a compatible client, or a PIO personal access token |
| `pio-public` | Published product information and hypothetical employment cost estimates | None |

Both connections use hosted Streamable HTTP. The team URL remains `https://app.pioinc.com/gateway/foundation/mcp`; the public URL is `https://app.pioinc.com/gateway/foundation/mcpPublic`.

## Connect from your AI client

1. Open the client's remote MCP or connector settings and add the team URL above using Streamable HTTP.
2. Complete its supported PIO OAuth flow, or configure a PIO personal access token in protected credential settings if the client supports that method.
3. Confirm the selected team and available tools, then make an explicit read request for records you are authorized to share.

Some platforms require a publisher-managed connector or their own plugin package before users can connect. Follow that platform's setup requirements rather than uploading this repository unchanged.

### Client-specific guides

- [Claude: hosted MCP connection](docs/claude.md)
- [Rakazo: GitHub plugin installation and connection settings](docs/rakazo.md)

The root [`plugin.json`](plugin.json) and [`mcp.json`](mcp.json) use Agent Plugins 1.1.0 for clients that accept that format. The `skills/` directory currently includes three workflow skills. Other client packages may expose the same PIO service through a different manifest or skill bundle. A setup guide or installable package does not establish marketplace approval or support on every client version.

## Connect your PIO team

### OAuth

In a client that supports MCP OAuth, start its sign-in flow for the `pio` connection. Complete sign-in on PIO, select the intended team and authorize only the needed read scopes. The hosted service supplies OAuth discovery metadata; the plugin contains no client secret or OAuth configuration fields. A server URL alone does not enable browser sign-in in every client or client version. If your client lacks a compatible sign-in flow, use its protected PAT settings if supported. Never share credentials in chat to work around a failed connection.

### Existing personal access tokens

PAT connections remain supported. In PIO, select the intended team and open **User settings → AI assistant connections (MCP)**. Create a token with only the needed data scopes and expiry. Store it in the AI client's protected bearer-token or authorization-header settings, following that client's expected format. Use one authentication method for the connection at a time.

Available tools and prompts depend on the connection's scopes, your current PIO access and the team's permission settings. An administrator may restrict a business area. The `workspace` scope is not a public-information-only permission; use `pio-public` for account-free product information.

The chosen AI client receives the data returned by enabled tools. Connect only a team and data you are authorized to share with that client. Never put passwords or tokens in this package, an endpoint URL, GitHub, chat, screenshots or submission instructions.

## Included read-only workflow skills

Each skill provides a reusable request and a bounded workflow. Installing it does not grant access or itself call tools; the bot may select the skill when it matches your request. Native MCP prompt names are also shown for clients with a prompt picker; clients that support tools only can use the example requests in the skills.

| Skill | MCP prompt | Required scope | Question it helps answer |
| --- | --- | --- | --- |
| [Payment trace](skills/pio-payment-trace/SKILL.md) | `pio_payment_trace` | `payment` | What is the verified state of this bill or payment, and what can I do next? |
| [Payroll variance](skills/pio-payroll-variance/SKILL.md) | `pio_payroll_variance` | `payroll` | Why did this payroll period change, in each original currency? |
| [Onboarding next steps](skills/pio-onboarding-inbox/SKILL.md) | `pio_onboarding_inbox` | `employee` | What is blocking this person's onboarding, and what is the supported next step? |

Review actual tool results and evidence before accepting an answer. A successful connection is not proof that a particular business question was resolved. Missing or ambiguous records require clarification, not a broader query. Actions such as payment, recalculation, confirmation or an invitation remain in PIO.

For a connection test, use approved test data, minimum scopes and a disposable connection. Verify the selected journey against PIO's source records. Revoke the connection in PIO afterward, confirm subsequent calls are denied after the authorization cache expires, and remove its saved credential from the AI client. Removing a saved client credential alone is not server-side revocation.

## Optional public information and cost estimates

No PIO account or token is needed for `pio-public`. Ask the AI client to call `get_public_product_facts` with:

```json
{"topic":"eor","language":"en"}
```

Check for `status: "published_information"`, `available: true` and a public source URL. Product information is not customer-specific pricing, a country-availability guarantee or live account status.

For a fictional salary scenario, explicitly ask the AI client to call `estimate_employer_cost` once with:

```json
{"country_code":"RS","currency":"USD","salary":3500,"salary_period":"monthly","salary_basis":"gross","language":"en"}
```

Use only hypothetical numbers and location assumptions. Do not supply actual employee, personal or company information. Country, currency, gross/net basis and monthly/yearly period must be explicit; supported region requirements must also be satisfied.

A `processing` result contains no confirmed amount. Wait for `retryAfterSeconds`, then call `get_employer_cost_estimate` with the returned `estimate_id`. Keep that handle private and poll the same calculation; do not repeatedly submit it. Report an unavailable, incomplete, expired or failed calculation honestly. A completed response is still an estimate, not a quote or a complete employer cost: service fees, deposits and unlisted benefits are not established by the returned components. Preserve its currency, period, assumptions and limitations. Usage limits can prevent new calculations.

## Privacy and support

The connected AI client receives the data returned by tools you enable. Team access follows your PIO permissions and granted scopes. Public calculations should use hypothetical inputs only. See the [PIO privacy policy](https://pioinc.com/privacy-policy), and contact **hi@pioinc.com** for support.

## References

- [PIO products](https://pioinc.com)
- [PIO cost estimator](https://pioinc.com/cost-estimator)
