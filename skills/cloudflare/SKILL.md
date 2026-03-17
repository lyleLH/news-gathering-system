---
name: cloudflare
description: Deploy websites and manage Cloudflare Pages/Workers using wrangler CLI.
metadata: {"nanobot":{"emoji":"☁️"}}
---

# Cloudflare Pages Deployment

You have full access to deploy websites via the `wrangler` CLI. The environment variables `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID` are already configured.

## Deploy a static site to Cloudflare Pages

```bash
npx wrangler pages project create <project-name> --production-branch main
npx wrangler pages deploy <directory> --project-name <project-name>
```

Example:
```bash
npx wrangler pages project create my-site --production-branch main
npx wrangler pages deploy ./frontend --project-name my-site
```

## List existing projects

```bash
npx wrangler pages project list
```

## Check deployment status

```bash
npx wrangler pages deployment list --project-name <project-name>
```

## Notes

- No login needed — uses `CLOUDFLARE_API_TOKEN` env var automatically.
- After deploy, the URL will be `https://<project-name>.pages.dev`
- You can also use `npx wrangler pages deploy` to update an existing project.
- For GitHub-connected projects, push to the repo triggers auto-deploy.
