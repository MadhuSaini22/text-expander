# Release

## One-time PyPI Setup

1. Create accounts on PyPI and TestPyPI.
2. Create a GitHub repository named `text-expander` under `MadhuSaini22`.
3. On PyPI, add a pending trusted publisher:
   - Project name: `text-expander`
   - Owner: `MadhuSaini22`
   - Repository: `text-expander`
   - Workflow: `publish.yml`
   - Environment: `pypi`
4. On TestPyPI, add the same pending trusted publisher, but use environment `testpypi`.
5. In the GitHub repo settings, create environments named `pypi` and `testpypi`.
6. Require manual approval for the `pypi` environment.

## Publish

Test release:

```bash
gh workflow run publish.yml
```

Production release:

```bash
git tag v0.1.0
git push origin v0.1.0
```

Manual local upload with an API token:

```bash
python -m pip install --upgrade setuptools wheel twine
python setup.py sdist bdist_wheel
python -m twine check dist/*
python -m twine upload dist/*
```

