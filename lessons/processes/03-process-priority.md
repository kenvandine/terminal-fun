---
title: Process Priority and Nice Values
description: Control CPU priority with nice and renice
order: 3
---

## Instructions

Not all processes are equally important. Linux lets you control how much CPU time each process gets using "nice" values.

### Understanding Nice Values

Nice values range from **-20** (highest priority) to **19** (lowest priority):

- **-20**: Highest priority (most CPU time)
- **0**: Default priority
- **19**: Lowest priority (least CPU time)

**Why "nice"?** Higher nice values are "nicer" to other processes by using less CPU.

### Starting Processes with Nice

Start a low-priority process:

```bash
nice -n 10 command
```

Start a high-priority process (requires sudo):

```bash
sudo nice -n -10 command
```

**Example:** Run a CPU-intensive task with low priority:

```bash
nice -n 15 ./intensive_script.sh
```

### Changing Priority of Running Process

Use `renice` to change the priority of a running process:

```bash
renice -n 10 -p PID
```

Change all processes owned by a user:

```bash
renice -n 5 -u username
```

**Note:** Only root can:
- Set negative nice values (higher priority)
- Decrease nice values (increase priority) of other users' processes

### Viewing Nice Values

The `ps` command shows nice values:

```bash
ps -eo pid,ni,cmd
```

- **NI** column shows the nice value

Or use `top` and look at the **NI** column.

### When to Use Nice/Renice

**Use nice for:**
- Backup scripts that can run slowly
- Batch processing jobs
- Long-running computations
- Downloads and uploads

**Example use cases:**

```bash
# Run backup with low priority
nice -n 19 tar -czf backup.tar.gz /data

# Compile code with medium-low priority
nice -n 10 make -j4

# Process video with low priority
nice -n 15 ffmpeg -i input.mp4 output.avi
```

### CPU Affinity

Advanced: You can also control which CPU cores a process uses with `taskset`:

```bash
taskset -c 0,1 command
```

This runs the command on CPU cores 0 and 1 only.

### Priority vs. Real-time

Nice values are for "normal" processes. For real-time requirements (audio, video), you'd use real-time scheduling (outside this lesson's scope).

## Exercise 1: Start a Low-Priority Process

Start a sleep command with low priority (nice value 10).

**Command:** `nice -n 10 sleep 5`

**Verify:**
```yaml
type: command_output
command: echo "Process completed"
contains: completed
```

## Exercise 2: View Nice Values

Start a background process and check its nice value with ps.

**Command:** `sleep 30 & ps -eo pid,ni,cmd | grep sleep`

**Verify:**
```yaml
type: command_output
command: ps -eo pid,ni,cmd | grep sleep
contains: sleep
```

## Exercise 3: Change Process Priority

Start a process, then change its priority with renice (may require sudo for some values).

**Command:** `sleep 40 & sleep 1 && renice -n 10 -p $(pgrep sleep)`

**Verify:**
```yaml
type: command_output
command: ps -eo pid,ni,cmd | grep sleep
```

## Exercise 4: Compare Nice Values

Start two processes with different nice values and observe them.

**Command:** `nice -n 0 sleep 10 & nice -n 19 sleep 10 & ps -eo pid,ni,cmd | grep sleep`

**Verify:**
```yaml
type: command_output
command: ps -eo pid,ni,cmd | grep sleep
```

Excellent! You've learned about:
- Nice values and CPU priority
- Starting processes with `nice`
- Changing priority with `renice`
- When to use different priorities
- Viewing nice values with `ps` and `top`

This knowledge helps you manage system resources effectively!
