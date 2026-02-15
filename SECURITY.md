# Security Policy

## Reporting a Vulnerability

The EUR-UN team takes security vulnerabilities seriously. We appreciate your efforts to responsibly disclose any issues you find.

### How to Report

**Please do NOT open a public GitHub issue for security vulnerabilities.**

Instead, report vulnerabilities via email:

📧 **[info@eurun.eu.org](mailto:info@eurun.eu.org)**

Include the following in your report:

- **Subject line**: `[SECURITY] <brief description>`
- **Affected repository**: Which EUR-UN repository is affected
- **Description**: Detailed description of the vulnerability
- **Steps to reproduce**: Minimal steps to reproduce the issue
- **Impact assessment**: What could an attacker achieve?
- **Suggested fix**: If you have one (optional)

### Response Timeline

| Stage | Timeframe |
|:------|:----------|
| Acknowledgment | Within **48 hours** |
| Initial assessment | Within **5 business days** |
| Fix development | Within **30 days** (critical), **90 days** (non-critical) |
| Public disclosure | After fix is deployed, coordinated with reporter |

### What to Expect

1. **Acknowledgment**: We will confirm receipt of your report within 48 hours.
2. **Assessment**: We will evaluate the severity and impact.
3. **Communication**: We will keep you informed of our progress.
4. **Fix & Release**: We will develop, test, and deploy a fix.
5. **Credit**: With your permission, we will credit you in the release notes.

## Supported Versions

We provide security updates for the **latest release** of each active repository. Older versions may not receive patches.

| Project | Supported Versions |
|:--------|:-------------------|
| All active repositories | Latest release on `master` / `main` |

## Security Best Practices

When contributing to EUR-UN projects, please:

- **Never commit secrets** (API keys, passwords, tokens) to the repository
- **Use environment variables** or external secret managers for sensitive configuration
- **Keep dependencies updated** — run `dependabot` or equivalent checks
- **Follow the principle of least privilege** in all code
- **Validate and sanitize** all user inputs

## Scope

This security policy applies to all repositories under the [EUR-UN](https://github.com/EUR-UN) GitHub organization.

---

**EUR-UN** · [eurun.eu.org](https://eurun.eu.org)
