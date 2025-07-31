# claude-code-tools

A collection of practical tools, hooks, and utilities for enhancing Claude Code.

## 🎮 tmux-cli: Bridging Claude Code and Interactive CLIs

Consider these scenarios:

You're using Claude Code (CC) to build an interactive script. The script prompts 
for user input, but CC can't respond to prompts.

You want Claude Code to debug using pdb, stepping through code line by line.

You need CC to launch another Claude Code instance for code review - not as a 
hidden sub-agent, but as a visible session you can monitor.

**tmux-cli enables these workflows** by giving Claude Code programmatic control 
over terminal applications.

For those new to [tmux](https://github.com/tmux/tmux/wiki), it's a terminal 
multiplexer that lets you create and manage multiple terminal sessions. The key 
benefit for our purposes is that tmux is scriptable and allows sending keystrokes 
to specific panes or sessions programmatically.

```bash
# Handle interactive prompts
tmux-cli --launch "python interactive_game.py"
tmux-cli --send "yes"
tmux-cli --capture

# Debug with pdb
tmux-cli --launch "python -m pdb buggy_script.py"
tmux-cli --send "n"  # next line
tmux-cli --send "p variable"  # print variable

# Launch another Claude Code instance
tmux-cli --launch "claude" --name reviewer
tmux-cli --send "Review this code for security issues..."
```

Now CC can test CLI applications, debug interactively, orchestrate multiple 
processes, and even run other instances of Claude Code in observable sessions.

**Think Playwright for terminals** - Terminal automation for AI agents.

**Works anywhere**: Automatically handles both local tmux panes and remote sessions.

## 🚀 Quick Start

```bash
# Install all the command-line tools
uv tool install git+https://github.com/pchalasani/claude-code-tools
```

This gives you:
- `tmux-cli` - The interactive CLI controller we just covered
- `find-claude-session` - Search and resume Claude Code sessions by keywords
- `vault` - Encrypted backup for your .env files

## 🎮 tmux-cli Deep Dive

### Common Use Cases

1. **Testing Interactive Scripts** - Test scripts that require user input, which
   Claude Code normally cannot handle:
   ```bash
   tmux-cli --launch "python interactive_script.py"
   tmux-cli --send "user input here"
   tmux-cli --capture
   ```

2. **UI Development & Testing** - Launch web apps and test them with browser
   automation:
   ```bash
   # Launch your app
   tmux-cli --launch "npm run dev" --name webapp
   
   # Use with Puppeteer MCP server to interact with the browser
   # Claude can now see the app running and test UI interactions
   ```

3. **Interactive Debugging** - Step through code with debuggers for deep
   understanding:
   ```bash
   # Python with pdb
   tmux-cli --launch "python -m pdb script.py"
   tmux-cli --send "n"  # next line
   tmux-cli --send "p variable_name"  # print variable
   
   # Node.js debugging
   tmux-cli --launch "node inspect app.js"
   
   # GDB for C/C++
   tmux-cli --launch "gdb ./program"
   ```

4. **Claude-to-Claude Communication** - Launch another Claude instance for
   specialized tasks:
   ```bash
   tmux-cli --launch "claude" --name reviewer
   tmux-cli --send "Review this code for security issues..."
   tmux-cli --capture
   ```

This tool transforms Claude Code from a static analyzer into an interactive
development companion that can test, debug, and validate code in real-time.

### Setting up tmux-cli for Claude Code

To enable CC to use tmux-cli, add this snippet to your global
`~/.claude/CLAUDE.md` file:

```markdown
# tmux-cli Command to interact with CLI applications

`tmux-cli` is a bash command that enables Claude Code to control CLI applications 
running in separate tmux panes - launch programs, send input, capture output, 
and manage interactive sessions. Run `tmux-cli --help` for detailed usage 
instructions.

Example uses:
- Interact with a script that waits for user input
- Launch another Claude Code instance to have it perform some analysis or review or 
  debugging etc
- Run a Python script with the Pdb debugger to step thru its execution, for 
  code-understanding and debugging
- Launch web apps and test them with browser automation MCP tools like Puppeteer
```

For detailed instructions, see [docs/tmux-cli-instructions.md](docs/tmux-cli-instructions.md).

## 🔍 find-claude-session

Search and resume Claude Code sessions by keywords with an interactive UI.

### Setup (Recommended)

Add this function to your shell config (.bashrc/.zshrc) for persistent directory
changes:

```bash
fcs() { eval "$(find-claude-session --shell "$@" | sed '/^$/d')"; }
```

Or source the provided function:
```bash
source /path/to/claude-code-tools/scripts/fcs-function.sh
```

### Usage

```bash
# Search in current project
fcs "keyword1,keyword2,keyword3"

# Search across all Claude projects  
fcs "keywords" --global
fcs "keywords" -g
```

### Features

- Interactive session selection with previews
- Cross-project search capabilities
- Automatic session resumption with `claude -r`
- Persistent directory changes when resuming cross-project sessions

Note: You can also use `find-claude-session` directly, but directory changes
won't persist after exiting Claude Code.

For detailed documentation, see [docs/find-claude-session.md](docs/find-claude-session.md).

## 🔐 vault

Centralized encrypted backup for .env files across all your projects using SOPS.

```bash
vault sync      # Smart sync (auto-detect direction)
vault encrypt   # Backup .env to ~/Git/dotenvs/
vault decrypt   # Restore .env from centralized vault
vault list      # Show all project backups
vault status    # Check sync status for current project
```

### Key Features

- Stores all encrypted .env files in `~/Git/dotenvs/`
- Automatic sync direction detection
- GPG encryption via SOPS
- Timestamped backups for safety

For detailed documentation, see [docs/vault-documentation.md](docs/vault-documentation.md).

## 🛡️ Claude Code Safety Hooks

This repository includes a comprehensive set of safety hooks that enhance Claude
Code's behavior and prevent dangerous operations.

### Key Safety Features

- **File Deletion Protection** - Blocks `rm` commands, enforces TRASH directory
  pattern
- **Git Safety** - Prevents dangerous `git add -A`, unsafe checkouts, and
  accidental data loss  
- **Context Management** - Blocks reading files >500 lines to prevent context
  bloat
- **Command Enhancement** - Enforces ripgrep (`rg`) over grep for better
  performance

### Quick Setup

1. Copy the sample hooks configuration:
   ```bash
   cp hooks/settings.sample.json hooks/settings.json
   export CLAUDE_CODE_TOOLS_PATH=/path/to/claude-code-tools
   ```

2. Reference in your Claude Code settings or use `--hooks` flag:
   ```bash
   claude --hooks /path/to/hooks/settings.json
   ```

### Available Hooks

- `bash_hook.py` - Comprehensive bash command safety checks
- `file_size_conditional_hook.py` - Prevents reading huge files
- `grep_block_hook.py` - Enforces ripgrep usage
- `notification_hook.sh` - Sends ntfy.sh notifications
- `pretask/posttask_subtask_flag.py` - Manages sub-agent state

For complete documentation, see [hooks/README.md](hooks/README.md).

## 🤖 Using Claude Code with Open-weight Anthropic API-compatible LLM Providers

You can use Claude Code with alternative LLMs served via Anthropic-compatible
APIs. Add these functions to your shell config (.bashrc/.zshrc):

```bash
kimi() {
    (
        export ANTHROPIC_BASE_URL=https://api.moonshot.ai/anthropic
        export ANTHROPIC_AUTH_TOKEN=$KIMI_API_KEY
        claude "$@"
    )
}

zai() {
    (
        export ANTHROPIC_BASE_URL=https://api.z.ai/api/anthropic
        export ANTHROPIC_AUTH_TOKEN=$Z_API_KEY
        claude "$@"
    )
}
```

After adding these functions:
- Set your API keys: `export KIMI_API_KEY=your-kimi-key` and 
  `export Z_API_KEY=your-z-key`
- Run `kimi` to use Claude Code with the Kimi K2 LLM
- Run `zai` to use Claude Code with the GLM-4.5 model

The functions use subshells to ensure the environment variables don't affect 
your main shell session, so you could be running multiple instances of Claude Code,
each using a different LLM.

## 📚 Documentation

- [tmux-cli detailed instructions](docs/tmux-cli-instructions.md) - 
  Comprehensive guide for using tmux-cli
- [Claude Code tmux tutorials](docs/claude-code-tmux-tutorials.md) - 
  Additional tutorials and examples
- [Vault documentation](docs/vault-documentation.md) - 
  Complete guide for the .env backup system
- [Hook configuration](hooks/README.md) - Setting up Claude Code hooks

## 📋 Requirements

- Python 3.11+
- uv (for installation)
- tmux (for tmux-cli functionality)
- SOPS (for vault functionality)

## 🛠️ Development

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/username/claude-code-tools
   cd claude-code-tools
   ```

2. Create and activate a virtual environment with uv:
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install in development mode:
   ```bash
   make install      # Install tools in editable mode
   make dev-install  # Install with dev dependencies (includes commitizen)
   ```

### Making Changes

- The tools are installed in editable mode, so changes take effect immediately
- Test your changes by running the commands directly
- Follow the existing code style and conventions

### Version Management

The project uses commitizen for version management:

```bash
make patch  # Bump patch version (0.0.X)
make minor  # Bump minor version (0.X.0)  
make major  # Bump major version (X.0.0)
```

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly
5. Commit your changes (commitizen will format the commit message)
6. Push to your fork
7. Open a Pull Request

### Available Make Commands

Run `make help` to see all available commands:
- `make install` - Install in editable mode for development
- `make dev-install` - Install with development dependencies
- `make release` - Bump patch version and install globally
- `make patch/minor/major` - Version bump commands

## 📄 License

MIT