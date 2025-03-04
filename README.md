# python-mantis
A python API to manage everything about Mantis Bug Tracker

## Instalation
```bash
pip install python-mantis
```

## Usage
```python
from mantis import MantisBT

client = MantisBT('https://<your-mantisbt-server>:<your-mantisbt-port>/', '<your mantisbt token API>')

# Get all projects from your mantisbt server
projects = client.projects.get_all()

# Get first project
project = projects[0]
project.name # Project name

# Get all issues for project
issues = project.get_issues()

# Get first issues
issue = issues[0]
issue.summary       # Issue title
issue.description   # Issue Description

# Get all notes for issue
notes = issue.get_notes()

# Get first note
note = notes[0]
note._id    # Note ID
note.text   # Get note comment
```
