# agent_memory

## Per-task CLI console

The `/ui` task detail view includes a task-linked console. It can create custom sessions, persist discussion messages, display agent/tool events, and start the configured CLI agent.

Configure the runner on the server before using **Run CLI agent**:

```bash
export AGENT_CLI_COMMAND='codex --ask-for-approval never exec --sandbox workspace-write'
export AGENT_CLI_WORKSPACE='/path/to/workspace'
```

The command is server-configured and is never accepted from the browser. Each run receives the task description and prior session discussion through stdin. The child process also receives `AGENT_MEMORY_TASK_ID`, `AGENT_MEMORY_SESSION_ID`, and `AGENT_MEMORY_PROJECT_ID`; stdout and stderr are persisted as session events. Sending another console message and running again gives Codex the updated session transcript.

For a one-command setup and launch, the script creates `.venv` and installs the dependencies there:

```bash
./run_codex_console.sh
```

After the first installation, skip package installation with `SKIP_INSTALL=1 ./run_codex_console.sh`.
