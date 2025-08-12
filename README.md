# nobleo-pre-commit

This repository contains a pre-commit configuration that can be re-used in multiple projects.

## Usage

To use this pre-commit configuration, add the following to your `.pre-commit-config.yaml` file:

```yaml
repos:
  - repo: https://bitbucket.org/nobleo/nobleo-pre-commit
    rev: 25.8.0
    hooks:
    - id: nobleo-hooks
      verbose: true
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

For GitLab pipelines, you can use the following:

```yaml
pre-commit:
  image: nobleo/pre-commit:4
  cache:
    key: "pre-commit"
    paths:
      - ~/.cache/pre-commit
  script:
    - pre-commit run --all-files --verbose
```

## Development

To test the pre-commit configuration, run the following command:

```bash
pre-commit try-repo /path/to/nobleo-pre-commit --all-files --verbose
```
