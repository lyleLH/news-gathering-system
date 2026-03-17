# Tool Usage Notes

Tool signatures are provided automatically via function calling.
This file documents non-obvious constraints and usage patterns.

## exec — Safety Limits

- Commands have a configurable timeout (default 60s)
- Dangerous commands are blocked (rm -rf, format, dd, shutdown, etc.)
- Output is truncated at 10,000 characters
- `restrictToWorkspace` config can limit file access to the workspace

## cron — Scheduled Reminders

- Please refer to cron skill for usage.

## GitHub (gh CLI)

- `gh` is authenticated and ready to use.
- You can create repos, push code, create PRs, etc.
- Git credential helper is configured: `git push` works directly.

## Cloudflare (wrangler CLI)

- `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID` are set in the environment.
- Use `npx wrangler pages deploy <dir> --project-name <name>` to deploy static sites.
- No manual login needed. See the cloudflare skill for details.
