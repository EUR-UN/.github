# Contributing to EUR-UN

Thank you for your interest in contributing to **EUR-UN** projects! This document provides guidelines and standards for contributing to any repository within our organization.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Workflow](#workflow)
- [Coding Standards](#coding-standards)
- [Commit Conventions](#commit-conventions)
- [Pull Request Guidelines](#pull-request-guidelines)
- [Issue Reporting](#issue-reporting)
- [Language & Documentation](#language--documentation)
- [License](#license)

---

## Code of Conduct

All contributors are expected to adhere to our [Code of Conduct](CODE_OF_CONDUCT.md). Please read it before participating.

---

## Getting Started

1. **Fork** the target repository to your own GitHub account.
2. **Clone** your fork locally:
   ```bash
   git clone https://github.com/<your-username>/<repo-name>.git
   cd <repo-name>
   ```
3. **Add upstream** remote to stay in sync:
   ```bash
   git remote add upstream https://github.com/EUR-UN/<repo-name>.git
   ```
4. **Install dependencies** as documented in the project's README.

---

## Workflow

We use the **Fork & Pull Request** model.

```
fork → clone → branch → commit → push → pull request → review → merge
```

### Branch Naming

| Prefix | Purpose | Example |
|:-------|:--------|:--------|
| `feature/` | New feature | `feature/add-mqtt-auth` |
| `fix/` | Bug fix | `fix/cert-renewal-crash` |
| `docs/` | Documentation only | `docs/update-api-reference` |
| `refactor/` | Code refactoring | `refactor/extract-parser` |
| `test/` | Adding or updating tests | `test/add-unit-tests` |
| `chore/` | Maintenance tasks | `chore/update-dependencies` |

### Keeping Your Fork Updated

```bash
git fetch upstream
git checkout master
git merge upstream/master
git push origin master
```

---

## Coding Standards

### General

- Write clean, readable code with meaningful variable and function names.
- Follow the existing code style of the project you are contributing to.
- Add comments for complex logic — but prefer self-documenting code.

### Language-Specific

| Language | Formatter / Linter | Style Guide |
|:---------|:-------------------|:------------|
| Python | `black`, `ruff` / `flake8` | PEP 8 |
| Go | `gofmt`, `golangci-lint` | Effective Go |
| TypeScript | `prettier`, `eslint` | Airbnb / project config |
| Shell | `shellcheck` | Google Shell Style Guide |
| VHDL | — | IEEE Std 1076-2008 conventions |

### Notebooks (Jupyter)

- **Clear output cells** before committing (unless output is necessary for demonstration).
- Keep cells focused — one logical step per cell.
- Include markdown cells to explain methodology.

---

## Commit Conventions

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

### Types

| Type | Description |
|:-----|:------------|
| `feat` | A new feature |
| `fix` | A bug fix |
| `docs` | Documentation changes |
| `style` | Formatting, missing semicolons, etc. (no code change) |
| `refactor` | Code change that neither fixes a bug nor adds a feature |
| `test` | Adding or updating tests |
| `chore` | Build process or auxiliary tool changes |
| `perf` | Performance improvements |
| `ci` | CI configuration changes |

### Examples

```
feat(monitor): add Telegram push notification support
fix(cert): resolve renewal timeout on slow networks
docs(readme): add Chinese translation for installation section
```

---

## Pull Request Guidelines

1. **One PR = One logical change.** Keep PRs focused and reviewable.
2. **Fill out the PR template** — describe what changed and why.
3. **Reference related issues** using `Closes #123` or `Fixes #456`.
4. **Ensure all checks pass** — CI, lint, and tests must be green.
5. **Be responsive** to review feedback.
6. **Squash commits** if requested during review.

### PR Title Format

```
<type>(<scope>): <concise description>
```

Example: `feat(api): add webhook retry mechanism`

---

## Issue Reporting

### Bug Reports

Please include:
- **Environment**: OS, language/runtime version, relevant tool versions
- **Steps to reproduce**: Minimal, reproducible steps
- **Expected behavior**: What you expected to happen
- **Actual behavior**: What actually happened
- **Logs/screenshots**: If applicable

### Feature Requests

Please include:
- **Problem statement**: What problem does this solve?
- **Proposed solution**: How should it work?
- **Alternatives considered**: What other approaches did you consider?

---

## Language & Documentation

We maintain **multilingual documentation** (English / 中文 / Français) across most projects. When contributing documentation:

- Write the primary version in **English**.
- Add **Chinese** translations where the project already has bilingual docs.
- Add **French** translations where applicable.
- For Czech-specific tools, include **Czech** terminology where appropriate.

---

## License

By contributing to any EUR-UN repository, you agree that your contributions will be licensed under the same license as the project (typically MIT or GPL-3.0). See each project's `LICENSE` file.

---

Thank you for helping make EUR-UN better! If you have questions, reach out at [info@eurun.eu.org](mailto:info@eurun.eu.org).
