# Use PIO with Claude

PIO offers two hosted MCP connections. Choose the one that fits your task.

| Connection | URL | Sign-in |
| --- | --- | --- |
| PIO team data | `https://app.pioinc.com/gateway/foundation/mcp` | PIO OAuth |
| Public PIO information and hypothetical costs | `https://app.pioinc.com/gateway/foundation/mcpPublic` | None |

## Connect your PIO team

Add the PIO team URL as a custom connector in Claude, or select PIO from the directory once a listing is available. Follow Claude's sign-in flow. Sign in on PIO, select your intended team and authorize only the read areas needed for your task. Use your normal PIO sign-in screen; never place a password or access token in a conversation or connector URL.

The connection uses your current PIO permissions and the read scopes you granted. An administrator may restrict a business area. If a required tool is unavailable, review the connection's scopes and your PIO team access. The `workspace` scope is not an account-free public-information permission.

The data returned by enabled tools is shared with Claude. Connect only data you are authorized to share with that client. PIO's [privacy policy](https://pioinc.com/privacy-policy) describes its data practices. For PIO support, contact `hi@pioinc.com`.

### Trace a payment

> Trace document <exact bill, order or payment-request reference>. Show its verified status, source amount and currency, evidence, unknowns and the next action I can take in PIO. Do not initiate or confirm payment.

The `trace_payment_order` tool requires the `payment` read area. Supply an exact document reference, a specific employee reference, or both. An ambiguous match needs clarification. A bill amount is not fixed salary or proof of receipt, and processing is not paid.

### Understand payroll changes

> Explain <current YYYY-MM> payroll versus <earlier YYYY-MM> using employerCost. Preserve each currency and PIO's explanation sentences. Show the actual periods, joiner/leaver/continuing changes, missing evidence and items to review. Do not recalculate or confirm payroll.

The `explain_payroll_run_variance` tool requires the `payroll` read area. Use a run ID or month selectors, not both. Months mean pay-period end month, not payment month. Several matching runs require selection. Uploaded results, uncalculated or stale data, absent prior periods and missing person-level evidence cannot establish zero change. PIO supplies the amounts and explanations; the assistant must not invent replacement differences, percentages or currency conversions.

### Check onboarding

> What is blocking onboarding for <employee reference>? Check this person's employment lifecycle, onboarding stage and account activation separately. Show evidence, unknowns and the next action I can take in PIO. Do not invite, remind, edit records or sign a contract.

The `employee` read area exposes `get_employee_onboarding_progress` and `get_employee_blockers`. Resolve exactly one person before continuing. A progress stage describes workflow position, not guaranteed field completeness. An empty blocker list does not prove that every requirement is complete.

## Use public information and hypothetical costs

Add the public URL without a PIO login. Ask for a product topic such as EOR and request its source URL.

For a fictional estimate:

> Estimate hypothetical employer cost in Serbia for USD 3,500 monthly gross salary. Use country_code RS, currency USD, salary 3500, salary_period monthly and salary_basis gross. Submit the scenario once, then check that calculation after its suggested wait. Report the original currency, period, returned components and limitations. This is fictional and contains no employee or company data.

`estimate_employer_cost` starts a calculation job; it is not a read-only operation. It cannot create an employee, bill or payment. A `processing` response has no confirmed amount. Wait for `retryAfterSeconds`, then call `get_employer_cost_estimate` with the returned `estimate_id`. Keep the handle private and poll the same job. Report incomplete, unavailable, expired and failed results honestly.

A completed estimate is not a quote or actual payroll. Totals cover the returned components only; service fees, deposits and unlisted benefits are not established. Use only hypothetical inputs, with explicit country, currency, salary basis and period.

## Disconnect

Revoke the connection in PIO's **User settings → AI assistant connections (MCP)** and remove the saved connection in Claude. Removing only the client connection does not itself revoke PIO authorization. Confirm that subsequent calls are denied after the authorization cache has had time to expire.

## Availability

This guide describes the PIO server's supported workflow. Availability in Claude's directory and successful sign-in on each Claude surface are separate checks. This guide does not imply directory approval or compatibility with every Claude client.
