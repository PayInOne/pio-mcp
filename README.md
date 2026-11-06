# PIO MCP for Rakazo

Read PIO product guidance and team data permitted by your PIO personal access token. The connector is read-only: its tools cannot create or change records, make payments, or send messages. Available tools depend on the token's data scopes and your team's permissions.

Install this plugin from the public GitHub repository using the steps below, then connect your own PIO token through Rakazo's protected settings. This plugin has not been approved for the Rakazo marketplace.

## Install and authenticate

The plugin contains a hosted Streamable HTTP connection. Its endpoint is `https://app.pioinc.com/gateway/foundation/mcp`.

1. In Rakazo, open **Integrations → + → From GitHub**, enter **https://github.com/PayInOne/pio-mcp**, and choose **Preview**. Check that the PIO MCP server appears without skipped components, then choose **Connect**.
2. In PIO, select the team you intend to connect. Open **User settings → AI assistant connections (MCP)** and create a personal access token with only the required data scopes and expiry.
3. In Rakazo, open **Integrations → + → Manage MCP servers**, edit the installed PIO server, and expand **Advanced**. Put the token value in the protected **Access token (optional)** field. This is a bearer-token credential; enter the token itself, without an additional `Bearer ` prefix.
4. Select the intended bot and choose **Use in this bot** for the server. Confirm the available tools before using them.

Do not put a token in this package, its endpoint URL, GitHub, a chat message, a screenshot, or submission instructions. The JSON files contain no credentials, header values, variables, or local executable commands. PIO's current connection uses a personal access token; this package does not configure or promise OAuth sign-in.

## First acceptance test: public product guidance

Use an isolated account and data approved for the test. Create a disposable token with the **workspace** scope and the shortest available expiry. That scope also permits other workspace tools; it is not a public-knowledge-only permission. Restrict the first test to `get_product_facts`. If the client cannot restrict tools, review each call and do not allow other tools during this test.

Ask the bot to call `get_product_facts` with:

```json
{
  "question": "How do I invite a colleague as a company member in PIO?"
}
```

Verify that the answer contains PIO's published product guidance and matches the instructions in PIO. Confirm the tool returns a successful result with `available: true`, `matched: true`, and at least one fact. Do not use this first test to read employees, salaries, payments, cards, or other business records. The MCP handshake and tool result can include the connected company/team metadata, so use only an approved test scope.

Revoke the disposable token in PIO after the test. Wait at least 31 seconds and confirm the connection can no longer return data. Remove the test connection and its saved credential from Rakazo. Record the date, installed commit, client version, tool and result without credentials or personal data.

## References

- [Rakazo: Build a plugin](https://rakazo.com/docs/build-a-plugin/)
- [Rakazo's hosted MCP plugin example](https://github.com/elie222/rakazo/tree/main/examples/plugins/mcp-server)
- [PIO](https://pioinc.com)
