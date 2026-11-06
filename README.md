# PIO MCP

Explore PIO products and hypothetical employment costs, or connect your own PIO team to investigate payments, payroll changes and onboarding. Team tools are read-only: they cannot pay, approve payroll, edit employees, sign contracts or send messages. The public cost tool creates a calculation job, without creating a business record.

This package supports direct GitHub installation. Marketplace review and publication are separate from installing this package.

The two hosted servers are listed in the [official MCP Registry](https://registry.modelcontextprotocol.io/?q=io.github.PayInOne). Registry listing publishes server metadata; it does not imply approval by Claude, OpenAI or Rakazo. See [connecting from Claude](docs/claude.md) for the hosted connection workflow.

## Choose a connection

| Connection | Purpose | Authentication |
| --- | --- | --- |
| `pio-public` | Published product information and hypothetical employment cost estimates | None |
| `pio` | Read the connected team's permitted data | PIO OAuth in a compatible client, or a PIO personal access token |

Both connections use hosted Streamable HTTP. The team URL remains `https://app.pioinc.com/gateway/foundation/mcp`; the public URL is `https://app.pioinc.com/gateway/foundation/mcpPublic`.

In Rakazo, open **Integrations → + → From GitHub**, enter **https://github.com/PayInOne/pio-mcp**, and choose **Preview**. Review both servers and the three skills, resolve any skipped components, then choose **Connect** and add the skills. Select your intended bot and enable only its needed connection with **Use in this bot**. Existing installations are pinned to a commit; reinstall from the updated source to get changed files.

## Try the public tools

No PIO account or token is needed. Ask the bot to call `get_public_product_facts` with:

```json
{"topic":"eor","language":"en"}
```

Check for `status: "published_information"`, `available: true` and a public source URL. Product information is not customer-specific pricing, a country-availability guarantee or live account status.

For a fictional salary scenario, explicitly ask the bot to call `estimate_employer_cost` once with:

```json
{"country_code":"RS","currency":"USD","salary":3500,"salary_period":"monthly","salary_basis":"gross","language":"en"}
```

Use only hypothetical numbers and location assumptions. Do not supply actual employee, personal or company information. Country, currency, gross/net basis and monthly/yearly period must be explicit; supported region requirements must also be satisfied.

A `processing` result contains no confirmed amount. Wait for `retryAfterSeconds`, then call `get_employer_cost_estimate` with the returned `estimate_id`. Keep that handle private and poll the same calculation; do not repeatedly submit it. Report an unavailable, incomplete, expired or failed calculation honestly. A completed response is still an estimate, not a quote or a complete employer cost: service fees, deposits and unlisted benefits are not established by the returned components. Preserve its currency, period, assumptions and limitations. Usage limits can prevent new calculations.

## Connect your PIO team

### OAuth

In a client that supports MCP OAuth, choose **Sign in** on the installed `pio` server. Complete sign-in on PIO, select the intended team and authorize only the needed read scopes. Rakazo's documented OAuth flow discovers configuration from the server; the plugin contains no client secret or OAuth configuration fields. A server URL alone does not enable browser sign-in in every client or client version. If your client lacks a compatible sign-in flow, use its protected PAT settings as described below. Never share credentials in chat to work around a failed connection.

### Existing personal access tokens

PAT connections remain supported. In PIO, select the intended team and open **User settings → AI assistant connections (MCP)**. Create a token with only the needed data scopes and expiry. In Rakazo, open **Integrations → + → Manage MCP servers**, edit `pio`, expand **Advanced**, and enter the token itself in **Access token (optional)**, without an extra `Bearer ` prefix. Use one authentication method for the connection at a time.

Available tools and prompts depend on the connection's scopes, your current PIO access and the team's permission settings. An administrator may restrict a business area. The `workspace` scope is not a public-information-only permission; use `pio-public` for account-free product information.

The chosen AI client receives the data returned by enabled tools. Connect only a team and data you are authorized to share with that client. Never put passwords or tokens in this package, an endpoint URL, GitHub, chat, screenshots or submission instructions.

## Three read-only journeys

Each skill provides a reusable request and a bounded workflow. Installing it does not grant access or itself call tools; the bot may select the skill when it matches your request. Native MCP prompt names are also shown for clients with a prompt picker; clients that support tools only can use the example requests in the skills.

| Skill | MCP prompt | Required scope | Question it helps answer |
| --- | --- | --- | --- |
| [Payment trace](skills/pio-payment-trace/SKILL.md) | `pio_payment_trace` | `payment` | What is the verified state of this bill or payment, and what can I do next? |
| [Payroll variance](skills/pio-payroll-variance/SKILL.md) | `pio_payroll_variance` | `payroll` | Why did this payroll period change, in each original currency? |
| [Onboarding next steps](skills/pio-onboarding-inbox/SKILL.md) | `pio_onboarding_inbox` | `employee` | What is blocking this person's onboarding, and what is the supported next step? |

Review actual tool results and evidence before accepting an answer. A successful connection is not proof that a particular business question was resolved. Missing or ambiguous records require clarification, not a broader query. Actions such as payment, recalculation, confirmation or an invitation remain in PIO.

For a connection test, use approved test data, minimum scopes and a disposable connection. Verify the selected journey against PIO's source records. Revoke the connection in PIO afterward, confirm calls are denied after at least 31 seconds, and remove its saved credential from Rakazo. Removing a saved client credential alone is not server-side revocation.

## Privacy and support

The connected AI client receives the data returned by tools you enable. Team access follows your PIO permissions and granted scopes. Public calculations should use hypothetical inputs only. See the [PIO privacy policy](https://pioinc.com/privacy-policy), and contact **hi@pioinc.com** for support.

## References

- [Rakazo plugin format and connection setup](https://rakazo.com/docs/build-a-plugin/)
- [PIO products](https://pioinc.com)
- [PIO cost estimator](https://pioinc.com/cost-estimator)
