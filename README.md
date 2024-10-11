# nobleo-pre-commit

This repository contains a pre-commit configuration that can be re-used in multiple projects.

## Usage

To use this pre-commit configuration, add the following to your `.pre-commit-config.yaml` file:

```yaml
repos:
  - repo: https://bitbucket.org/nobleo/nobleo-pre-commit
    rev: 24.9.0
    hooks:
    - id: nobleo-hooks
      verbose: true
```

And something like this to your CI:

```yaml
definitions:
  caches:
    pre-commit: ~/.cache/pre-commit
  steps:
    - step: &nobleo-pre-commit
        name: Pre-commit
        image: nobleo/pre-commit:4
        caches: [pre-commit]
        script: [pre-commit run --all-files --verbose]

pipelines:
  default:
    - step: *nobleo-pre-commit
```

## Development

To test the pre-commit configuration, run the following command:

```bash
pre-commit try-repo /path/to/nobleo-pre-commit --all-files --verbose
```
