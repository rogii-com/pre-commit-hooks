# pre-commit-hooks
Git hooks to integrate with [pre-commit](http://pre-commit.com).

## Using pre-commit-hooks with pre-commit

Add this to your `.pre-commit-config.yaml`

```yaml
-   repo: https://github.com/rogii-com/pre-commit-hooks
    rev: v1.1.0  # Use the ref you want to point at
    hooks:
    -   id: check-line-endings
    -   id: check-trailing-whitespaces
    -   id: check-end-of-file
    -   id: check-q-emit
```
