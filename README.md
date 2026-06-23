# toolit-architecture-decision-records
Toolit Plugin used for creating architecture decision records (ADR's) from a template using CLI commands

This is an example of a Toolit Plugin. It defines a set of commands that can be used to interact with Azure DevOps, specifically tailored for a trunk-based branching strategy.

## Installation
You can install this package using uv:

```bash
uv add "toolit-architecture-decision-records @ git+https://github.com/martinmoldrup/toolit-architecture-decision-records" --dev
```

The git commit version will be locked in the lock file. To update to the latest version, you can use:

```bash
uv add toolit-architecture-decision-records --upgrade-package toolit-architecture-decision-records --dev
```