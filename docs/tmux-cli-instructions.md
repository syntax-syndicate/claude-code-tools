# tmux-cli Instructions

A command-line tool for controlling CLI applications running in tmux panes/windows.
Automatically detects whether you're inside or outside tmux and uses the appropriate mode.

## Auto-Detection
- **Inside tmux (Local Mode)**: Manages panes in your current tmux window
- **Outside tmux (Remote Mode)**: Creates and manages a separate tmux session with windows

## Prerequisites
- tmux must be installed
- The `tmux-cli` command must be available (installed via `uv tool install`)

## ⚠️ IMPORTANT: Always Launch a Shell First!

**Always launch zsh first** to prevent losing output when commands fail:
```bash
tmux-cli launch "zsh"  # Do this FIRST
tmux-cli send "your-command" --pane=%48  # Then run commands
```

If you launch a command directly and it errors, the pane closes immediately and you lose all output!

## Core Commands

### Launch a CLI application
```bash
tmux-cli launch "command"
# Example: tmux-cli launch "python3"
# Returns: pane ID (e.g., %48)
```

### Send input to a pane
```bash
tmux-cli send "text" --pane=PANE_ID
# Example: tmux-cli send "print('hello')" --pane=%48

# By default, there's a 1-second delay between text and Enter.
# This ensures compatibility with various CLI applications.

# To send without Enter:
tmux-cli send "text" --pane=PANE_ID --enter=False

# To send immediately without delay:
tmux-cli send "text" --pane=PANE_ID --delay-enter=False

# To use a custom delay (in seconds):
tmux-cli send "text" --pane=PANE_ID --delay-enter=0.5
```

### Capture output from a pane
```bash
tmux-cli capture --pane=PANE_ID
# Example: tmux-cli capture --pane=%48
```

### List all panes
```bash
tmux-cli list_panes
# Returns: JSON with pane IDs, indices, and status
```

### Kill a pane
```bash
tmux-cli kill --pane=PANE_ID
# Example: tmux-cli kill --pane=%48

# SAFETY: You cannot kill your own pane - this will give an error
# to prevent accidentally terminating your session
```

### Send interrupt (Ctrl+C)
```bash
tmux-cli interrupt --pane=PANE_ID
```

### Send escape key
```bash
tmux-cli escape --pane=PANE_ID
# Useful for exiting Claude or vim-like applications
```

### Wait for pane to become idle
```bash
tmux-cli wait_idle --pane=PANE_ID
# Waits until no output changes for 2 seconds (default)

# Custom idle time and timeout:
tmux-cli wait_idle --pane=PANE_ID --idle-time=3.0 --timeout=60
```

### Get help
```bash
tmux-cli help
# Displays this documentation
```

## Typical Workflow

1. **ALWAYS launch a shell first** (prefer zsh) - this prevents losing output on errors:
   ```bash
   tmux-cli launch "zsh"  # Returns pane ID - DO THIS FIRST!
   ```

2. Run your command in the shell:
   ```bash
   tmux-cli send "python script.py" --pane=%48
   ```

3. Interact with the program:
   ```bash
   tmux-cli send "user input" --pane=%48
   tmux-cli capture --pane=%48  # Check output
   ```

4. Clean up when done:
   ```bash
   tmux-cli kill --pane=%48
   ```

## Remote Mode Specific Commands

These commands are only available when running outside tmux:

### Attach to session
```bash
tmux-cli attach
# Opens the managed tmux session to view live
```

### Clean up session
```bash
tmux-cli cleanup
# Kills the entire managed session and all its windows
```

### List windows
```bash
tmux-cli list_windows
# Shows all windows in the managed session
```

## Tips
- Always save the pane/window ID returned by `launch`
- Use `capture` to check the current state before sending input
- In local mode: Pane IDs can be like `%48` or pane indices like `1`, `2`
- In remote mode: Window IDs can be indices like `0`, `1` or full form like `session:0.0`
- If you launch a command directly (not via shell), the pane/window closes when
  the command exits
- **IMPORTANT**: The tool prevents you from killing your own pane/window to avoid
  accidentally terminating your session

## Avoiding Polling
Instead of repeatedly checking with `capture`, use `wait_idle`:
```bash
# Send command to a CLI application
tmux-cli send "analyze this code" --pane=%48

# Wait for it to finish (no output for 3 seconds)
tmux-cli wait_idle --pane=%48 --idle-time=3.0

# Now capture the result
tmux-cli capture --pane=%48
```