---
title: Git Basics - Source Control Fundamentals
description: Learn Git from basics to advanced topics for effective version control
order: 1
---

## Instructions

Git is the most popular version control system in the world. It helps you track changes to your code, collaborate with others, and maintain a history of your project. Whether you're working alone or on a team, Git is an essential tool.

### What is Version Control?

Version control (also called source control) lets you:
- **Track changes** - See what changed, when, and by whom
- **Revert mistakes** - Go back to any previous version
- **Collaborate** - Work with others without conflicts
- **Experiment safely** - Try new ideas in branches
- **Maintain history** - Keep a complete record of your project

### Git Concepts

**Repository (Repo)** - A project tracked by Git (contains all files and history)

**Commit** - A snapshot of your project at a point in time

**Branch** - A parallel version of your code (for features or experiments)

**Remote** - A version of your repo hosted elsewhere (like GitHub)

## Basic Git Workflow

### 1. Creating a Repository

```bash
git init              # Create a new Git repository in current directory
git clone <url>       # Download an existing repository
```

### 2. Checking Status

```bash
git status            # See which files have changed
git diff              # See exactly what changed in files
git log               # View commit history
git log --oneline     # Compact commit history
```

### 3. The Three States

Git has three main states for your files:

1. **Working Directory** - Your actual files
2. **Staging Area** - Files ready to be committed
3. **Repository** - Committed snapshots

The workflow:
```
Working Directory -> (git add) -> Staging Area -> (git commit) -> Repository
```

### 4. Staging and Committing

```bash
git add <file>        # Stage a specific file
git add .             # Stage all changed files
git add *.py          # Stage all Python files

git commit -m "message"           # Commit staged files
git commit -am "message"          # Stage and commit all tracked files
```

**Good commit messages:**
- Start with a verb (Add, Fix, Update, Remove)
- Be specific but concise
- Example: "Add user authentication feature"
- Example: "Fix crash when loading empty file"

### 5. Viewing History

```bash
git log               # Full commit history
git log --oneline     # Compact one-line format
git log --graph       # Show branch structure
git log -n 5          # Show last 5 commits
git show <commit>     # Show details of a commit
```

## Intermediate Git - Branching

Branches let you work on features without affecting the main code.

### Branch Basics

```bash
git branch            # List all branches (* = current)
git branch <name>     # Create a new branch
git checkout <name>   # Switch to a branch
git checkout -b <name>  # Create and switch to new branch
git switch <name>     # Modern way to switch branches
```

### Merging Branches

```bash
git merge <branch>    # Merge specified branch into current branch
```

**Example workflow:**
```bash
git checkout -b feature-login    # Create feature branch
# ... make changes ...
git add .
git commit -m "Add login feature"
git checkout main                # Switch back to main
git merge feature-login          # Merge feature into main
git branch -d feature-login      # Delete merged branch
```

### Dealing with Conflicts

When merging, Git might find conflicts (same lines changed differently):

1. Git marks conflicts in files with `<<<<<<<`, `=======`, `>>>>>>>`
2. Edit the file to resolve the conflict
3. Remove the conflict markers
4. `git add <file>` to mark as resolved
5. `git commit` to complete the merge

## Advanced Git Topics

### Undoing Changes

```bash
# Undo working directory changes
git checkout -- <file>      # Discard changes in file
git restore <file>          # Modern way to discard changes

# Undo staging
git reset <file>            # Unstage file (keep changes)
git restore --staged <file> # Modern way to unstage

# Undo commits
git reset --soft HEAD~1     # Undo last commit, keep changes staged
git reset --hard HEAD~1     # Undo last commit, discard changes (DANGEROUS!)
git revert <commit>         # Create new commit that undoes changes
```

### Stashing Changes

Save your work temporarily without committing:

```bash
git stash               # Save changes and clean working directory
git stash list          # Show all stashes
git stash pop           # Apply most recent stash and remove it
git stash apply         # Apply stash but keep it in list
git stash drop          # Delete a stash
```

**Use case:** You're working on a feature but need to quickly fix a bug on main. Stash your feature work, switch branches, fix the bug, then pop your stash.

### Remote Repositories

Work with code hosted on GitHub, GitLab, etc:

```bash
git remote -v                    # Show remote repositories
git remote add origin <url>      # Add a remote named 'origin'

git push origin main             # Push commits to remote
git pull origin main             # Fetch and merge from remote
git fetch origin                 # Download changes without merging

git clone <url>                  # Download a repository
```

### Rebasing

Rebase rewrites history by applying commits on top of another branch:

```bash
git rebase main         # Reapply current branch commits on top of main
```

**Merge vs Rebase:**
- **Merge** - Preserves history, creates merge commit
- **Rebase** - Clean linear history, but rewrites commits

**⚠️ Warning:** Never rebase commits you've already pushed to a shared repository!

### Tags

Mark specific points in history (usually releases):

```bash
git tag                     # List tags
git tag v1.0.0              # Create lightweight tag
git tag -a v1.0.0 -m "Release 1.0"  # Annotated tag with message
git push origin v1.0.0      # Push tag to remote
```

### Viewing Diffs

```bash
git diff                    # Changes in working directory
git diff --staged           # Changes in staging area
git diff main..feature      # Differences between branches
git diff HEAD~2             # Compare with 2 commits ago
```

## Git Best Practices

1. **Commit Often** - Small, focused commits are easier to understand and revert
2. **Write Clear Messages** - Your future self will thank you
3. **Use Branches** - Keep main stable, experiment in branches
4. **Pull Before Push** - Sync with remote before pushing your changes
5. **Don't Commit Secrets** - Never commit passwords, API keys, etc.
6. **Use .gitignore** - Exclude files Git should never track (node_modules/, .env, etc.)

## Common Git Workflows

### Feature Branch Workflow

1. `git checkout -b feature-name`
2. Make changes and commit
3. `git checkout main`
4. `git pull origin main` (get latest)
5. `git checkout feature-name`
6. `git rebase main` (optional, for clean history)
7. `git checkout main`
8. `git merge feature-name`
9. `git push origin main`

### Fixing a Mistake

**Made a typo in last commit?**
```bash
git commit --amend -m "Corrected message"
```

**Committed to wrong branch?**
```bash
git reset HEAD~1              # Undo commit, keep changes
git checkout correct-branch
git add .
git commit -m "message"
```

**Need to undo a pushed commit?**
```bash
git revert <commit-hash>      # Safe way - creates new commit
```

## Exercise 1: Create Your First Repository

Initialize a new Git repository in a test directory.

**Command:** `mkdir my-project && cd my-project && git init`

**Verify:**
```yaml
type: command_output
command: git status
contains: On branch
```

## Exercise 2: Make Your First Commit

Create a file and make your first commit.

**Command:** `echo "# My Project" > README.md && git add README.md && git commit -m "Initial commit: Add README"`

**Verify:**
```yaml
type: command_output
command: git log --oneline
contains: Initial commit
```

## Exercise 3: Check Your History

View the commit history to see your first commit.

**Command:** `git log`

**Verify:**
```yaml
type: command_output
command: git log --oneline
contains: README
```

## Exercise 4: Create and Merge a Branch

Create a feature branch, make changes, and merge it back.

**Command:** `git checkout -b feature-test && echo "New feature" >> README.md && git add . && git commit -m "Add feature" && git checkout main && git merge feature-test`

**Verify:**
```yaml
type: command_output
command: git log --oneline
contains: Add feature
```

## Exercise 5: Practice Git Status

Make a change without committing and check the status.

**Command:** `echo "Uncommitted change" >> README.md && git status`

**Verify:**
```yaml
type: command_output
command: git status
contains: modified
```

Congratulations! You've learned Git from basics to advanced topics:
- How to create repositories and make commits
- The Git workflow (working directory → staging → repository)
- Branching and merging
- Undoing changes (reset, revert, stash)
- Working with remotes (push, pull, fetch)
- Advanced topics (rebase, tags, diffs)
- Best practices for clean history

**Next Steps:**
- Practice these commands regularly
- Create a GitHub/GitLab account for remote repositories
- Learn about pull requests for team collaboration
- Explore Git GUIs like GitKraken or Sourcetree
- Read `.gitignore` documentation for your language

**Pro Tips:**
- Use `git status` constantly - it's your friend!
- Commit early, commit often
- Write commits that tell a story
- When in doubt, create a branch
- Learn `git reflog` for recovering "lost" commits
