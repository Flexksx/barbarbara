# barbarbara

## Project map

| Unit       | Path        | Stack              | Language   |
|------------|-------------|---------------------|-----------|
| api        | apps/api    | backend application | Python    |
| ui         | apps/ui     | frontend application| TypeScript|

## Tooling

- nix: dev shell and system tools
- moon: task graph and caching
- just: the only command entry point
- uv: Python dependency management
- pnpm: JavaScript workspace
- lefthook: pre-commit hooks

## Commands

```text
just format        # repo-wide format
just lint          # repo-wide lint
just build all     # build all units
just test api      # test one unit
just start ui      # start one unit
just sync          # rebuild unit indexes
just new python    # scaffold a Python unit
just new react     # scaffold a React unit
```

## Unit details

### apps/api (Python backend)

- Managed by uv, Python 3.14
- Linting: ruff + ty
- Testing: pytest
- Start: `uv run python -m api.main`

### apps/ui (React frontend)

- Vite + React 19 + TypeScript
- Linting: biome
- Formatting: biome
- Testing: vitest
- Start: `vite` dev server
