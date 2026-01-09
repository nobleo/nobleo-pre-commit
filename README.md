<!--
Copyright (C) 2025 Nobleo Autonomous Solutions B.V.
-->

# nobleo-pre-commit

This repository contains a pre-commit configuration that can be re-used in multiple projects.

## Usage

To use this pre-commit configuration, add the following to your `.pre-commit-config.yaml` file:

```yaml
repos:
  - repo: https://bitbucket.org/nobleo/nobleo-pre-commit
    rev: 25.12.0
    hooks:
    - id: nobleo-hooks
      verbose: true
```

To use only specific hooks, you can specify them like this:

```yaml
repos:
  - repo: https://bitbucket.org/nobleo/nobleo-pre-commit
    rev: 25.12.0
    hooks:
    - id: launch-depends
```

### Automatically run on commit

If you like your code to be formatted according to the pre-commit configuration on every commit, you can install the pre-commit package and configure it to run on every commit.

```bash
apt install pre-commit
```

In a repository where there is a `.pre-commit-config.yaml` file, run the following command:

```bash
pre-commit install
```

Note that this command has to be repeated for every repository.

### CI

#### Bitbucket

For bitbucket pipelines, add something like this to your `bitbucket-pipelines.yml` file:

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

#### Github

For GitHub actions, add a file named `.github/workflows/pre-commit.yml`:

```yaml
name: pre-commit

on:
  pull_request:
  push:

jobs:
  pre-commit:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v5
    - uses: actions/setup-python@v6
    - uses: pre-commit/action@v3.0.1
      with:
        extra_args: --all-files --verbose
```

#### GitLab

For GitLab pipelines, you can use the following:

```yaml
pre-commit:
  image: nobleo/pre-commit:4
  variables:
    PRE_COMMIT_HOME: "${CI_PROJECT_DIR}/.cache/pre-commit"
  cache:
    key: "pre-commit"
    paths:
      - "${PRE_COMMIT_HOME}"
  script:
    - pre-commit run --all-files --verbose
```

#### Azure DevOps

For Azure DevOps pipelines, you can use the following:

```yaml
trigger:
  - '*'

pool:
  vmImage: ubuntu-latest

variables:
  PRE_COMMIT_HOME: $(Pipeline.Workspace)/pre-commit

jobs:
  - job: PreCommit
    container: nobleo/pre-commit:4
    steps:
      - task: Cache@2
        inputs:
          key: pre-commit
          path: $(PRE_COMMIT_HOME)
      - script: |
          pre-commit run --all-files --verbose
        displayName: 'Run pre-commit'
```

## Development

To test the pre-commit configuration, run the following command:

```bash
pre-commit try-repo /path/to/nobleo-pre-commit --all-files --verbose
```
