# Contributing to RevalytIQ

We welcome improvements from the community. By participating you agree to follow our [Code of Conduct](CODE_OF_CONDUCT.md).

## Getting Started

1. Fork the repository and create a feature branch.
2. Copy environment templates and install dependencies:
   ```bash
   cp backend/.env.example backend/.env
   cp frontend/.env.example frontend/.env.local
   make be-install fe-install
   ```
3. Run the applications locally (`make be-run` and `make fe-dev`) and verify your change.

## Commit Guidelines

We follow **Conventional Commits**:

- `feat: add new KPI widget`
- `fix: handle signup validation`
- `docs: update README`

Squash commits when appropriate before merging.

## Testing & Linting

Before submitting a pull request:

```bash
make be-test
make fe-test
make be-lint
```

Ensure tests pass and linting reports no new issues.

## Pull Request Checklist

- [ ] Tests cover the change (backend and/or frontend as applicable).
- [ ] Documentation updated (README, CHANGELOG, or inline comments).
- [ ] Environment variables documented if newly introduced.
- [ ] CI pipelines remain green.

Thank you for contributing!
