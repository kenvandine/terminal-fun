---
title: Managing Processes
description: Learn to control processes with kill, killall, and signals
order: 2
---

## Instructions

Now that you can view processes, let's learn how to control them - start, stop, pause, and terminate.

### Background and Foreground Jobs

**Run a command in the background:**

```bash
command &
```

The `&` symbol runs the command in the background, giving you back the prompt.

**Example:**

```bash
sleep 60 &
```

**View background jobs:**

```bash
jobs
```

**Bring a job to foreground:**

```bash
fg %1
```

**Send current process to background:**

Press `Ctrl+Z` to suspend it, then:

```bash
bg
```

### Killing Processes

The `kill` command sends signals to processes. The most common:

**Terminate a process gracefully:**

```bash
kill PID
```

**Force kill (when graceful doesn't work):**

```bash
kill -9 PID
```

**Kill by name:**

```bash
killall process_name
```

Or use `pkill`:

```bash
pkill process_name
```

### Common Signals

Signals are messages sent to processes:

- **SIGTERM (15)**: Polite termination request (default for `kill`)
- **SIGKILL (9)**: Force kill immediately (can't be ignored)
- **SIGHUP (1)**: Hang up (reload config)
- **SIGSTOP (19)**: Pause process
- **SIGCONT (18)**: Resume paused process

**Send specific signal:**

```bash
kill -SIGTERM PID
# or
kill -15 PID
```

### Best Practices

1. **Always try regular kill first**: `kill PID`
2. **Wait a few seconds** for the process to clean up
3. **Use kill -9 only as last resort**: It doesn't allow cleanup
4. **Be careful with killall**: It kills ALL matching processes
5. **Check you have the right PID** before killing

### Finding PID for a Process

```bash
pgrep process_name
```

Or:

```bash
pidof process_name
```

### Useful Patterns

Kill all firefox processes:

```bash
killall firefox
```

Kill process and wait for it to end:

```bash
kill PID && wait PID
```

Kill multiple processes:

```bash
kill 1234 1235 1236
```

## Exercise 1: Run a Background Process

Start a long-running process in the background using `sleep 30 &`.

**Command:** `sleep 30 &`

**Verify:**
```yaml
type: command_output
command: jobs
contains: sleep
```

## Exercise 2: View Background Jobs

Use the `jobs` command to see your background jobs.

**Command:** `jobs`

**Verify:**
```yaml
type: command_output
command: jobs
```

## Exercise 3: Kill a Process by PID

Start a sleep process, find its PID with `pgrep`, then kill it.

**Command:** `sleep 100 & sleep 1 && kill $(pgrep sleep)`

**Verify:**
```yaml
type: command_output
command: pgrep sleep
```

## Exercise 4: Use killall

Start multiple sleep processes and kill them all with killall.

**Command:** `sleep 50 & sleep 50 & sleep 50 & sleep 1 && killall sleep`

**Verify:**
```yaml
type: command_output
command: pgrep sleep
```

Great job! You now know how to:
- Run processes in the background with `&`
- Manage jobs with `jobs`, `fg`, and `bg`
- Kill processes with `kill`, `killall`, and `pkill`
- Understand different signals
- Find PIDs with `pgrep` and `pidof`

You're becoming a process management expert!
