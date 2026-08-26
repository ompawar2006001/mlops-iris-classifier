# Version Control Workflow — MLOps Iris Classifier

## 1. Overview

This document describes the Git-based version control workflow used for the MLOps Iris Classifier project.

- **Repository:** https://github.com/ompawar2006001/mlops-iris-classifier
- **Primary language:** Python
- **Maintainer:** ompawar2006001

## 2. Branching Strategy

| Branch | Purpose |
|---|---|
| `main` | Stable, deployable code |
| `develop` | Integration branch for day-to-day development |
| `feature/<name>` | Individual features, branched from and merged back into `develop` |
| `conflict-demo-*` | Demonstration branches created for merge-conflict resolution practice |

### Branching Rule

No direct development commits should be made to `main`.

The normal flow is:

`feature/* → Pull Request → develop → main`

## 3. Commit Convention

Commits follow a short, imperative style with a type prefix.

- `feat:` — new functionality
- `fix:` — bug fixes
- `docs:` — documentation changes
- `chore:` — tooling, configuration, or maintenance
- `refactor:` — code restructuring without behavior change
- `test:` — adding or fixing tests

Example:

`feat: add classification report to training script`

## 4. Standard Feature Development Workflow

```bash
git switch develop
git pull origin develop
git switch -c feature/<short-description>

# Make changes

git add <files>
git commit -m "feat: <description>"
git push -u origin feature/<short-description>

# Open a Pull Request into develop on GitHub
# Review and merge the Pull Request

git branch -d feature/<short-description>
git push origin --delete feature/<short-description>

## 5. Merge Conflict Resolution Process

1. Attempt the merge. Git identifies conflicting files.
2. Open the conflicted file.
3. Locate the conflict markers:
   - `<<<<<<<`
   - `=======`
   - `>>>>>>>`
4. Decide which changes to keep or combine.
5. Remove all conflict markers.
6. Save the file.
7. Mark the file as resolved:

```bash
git add README.md