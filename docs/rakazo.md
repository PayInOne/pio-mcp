# Use PIO with Rakazo

This guide covers Rakazo's installation controls for the shared [PIO MCP connections](../README.md#choose-a-connection).

## Install

Open **Integrations → + → From GitHub**, enter **https://github.com/PayInOne/pio-mcp**, then choose **Preview**. Review the two servers and three skills, including skipped components. Choose **Connect** and add the skills. Select a bot and enable only its needed connection with **Use in this bot**.

## Authenticate

For `pio`, choose **Sign in** and complete PIO OAuth. Select the intended team and required read scopes. Rakazo discovers OAuth from the hosted server; no secrets belong in the package.

Alternatively, create a scoped token in PIO's **User settings → AI assistant connections (MCP)**. In Rakazo, open **Integrations → + → Manage MCP servers**, edit `pio`, and expand **Advanced**. Put the token in **Access token (optional)** without an extra `Bearer ` prefix. Use one authentication method per connection.

`pio-public` needs no credentials. It provides public information and hypothetical estimates, not team records.

## Verify and disconnect

Use the [workflow skills](../README.md#included-read-only-workflow-skills) to check authorized records. Revoke test access in PIO, verify subsequent requests fail after cache expiry, then remove saved credentials from Rakazo.

## Updates

Installed content and approved listings are pinned to commits. Updating GitHub does not update them automatically. Test an installation from the updated source before requesting a marketplace update.

See [Rakazo's plugin documentation](https://rakazo.com/docs/build-a-plugin/) for its current controls and submission requirements.
