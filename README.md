# agent_memory

## Per-task CLI console

The `/ui` task detail view includes a task-linked console. It can create custom sessions, persist discussion messages, display agent/tool events, and start the configured CLI agent.

Configure the runner on the server before using **Run CLI agent**:

```bash
export AGENT_CLI_COMMAND='codex --ask-for-approval never exec --sandbox workspace-write'
export AGENT_CLI_WORKSPACE='/path/to/workspace'
```

The command is server-configured and is never accepted from the browser. The bundled user service uses Codex with `--approve-for-me` (this flag selects the workspace-write approval flow); each task run resolves its workspace from the linked project's `metadata.repository` (an explicit `AGENT_CLI_WORKSPACE` override is supported). Each run receives the task description, saved session summary, and bounded recent discussion through stdin. The child process also receives `AGENT_MEMORY_TASK_ID`, `AGENT_MEMORY_SESSION_ID`, and `AGENT_MEMORY_PROJECT_ID`; stdout is persisted as assistant messages and stderr as tool events. The console polls active sessions, shows online/typing/offline state, and sending a message persists it and starts the next run automatically. Full event history remains server-side so reopening a session can resume without resending unbounded history.

For a one-command setup and launch, the script creates `.venv` and installs the dependencies there:

```bash
./run_codex_console.sh
```

After the first installation, skip package installation with `SKIP_INSTALL=1 ./run_codex_console.sh`.
