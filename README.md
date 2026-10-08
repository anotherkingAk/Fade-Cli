# Fade CLI 1.1

Fade is a local-first autonomous coding agent for **Termux and desktop terminals**.
It is BYOK: users bring their own model API key. Projects remain on the local device.

Fade 1.1 is an independent implementation. It does **not** copy Claude Code source,
assets, prompts, or branding.

## UX goals

- One compact interface that adapts to terminal width.
- Calm ANSI colors and a small Fade agent mark.
- A visible thinking/progress line during model work.
- Explicit phases: inspect → plan → build → review → verify.
- No huge panels on narrow Termux screens.
- Wider terminals can show richer summaries and file lists.

## Install

```bash
python -m pip install -e .
fade init
fade key set
fade "Build a small FastAPI task API with tests"
```

Termux:

```bash
pkg update
pkg install python git
cd fade
python -m pip install -e .
fade doctor
```

## BYOK providers

Supported adapters in 1.1:

- OpenAI-compatible `/v1/chat/completions`
- Gemini `generateContent`

Environment variables:

```bash
export FADE_PROVIDER=openai
export FADE_MODEL=your-model
export FADE_API_KEY=your-key
```

Or use `fade key set`.

## Skills

A skill is a local `SKILL.md` instruction package. Install from GitHub or a local folder:

```bash
fade skill install owner/repository
fade skill install https://github.com/owner/repository
fade skill list
```

Fade does not execute skill files automatically. Skills are treated as instructions and are
reviewed/loaded into the agent context. Future versions can add signed executable tools.

## Generation pipeline

```text
User request
    ↓
Workspace inspection
    ↓
Commander / intent normalization
    ↓
Architecture plan
    ↓
UI/UX contract (when applicable)
    ↓
Implementation plan
    ↓
File generation / patching
    ↓
Static review
    ↓
Optional local verification
    ↓
Repair loop
    ↓
Final report + audit
```

The goal is not to make a single giant model call. The core contract keeps planning,
implementation, review and verification separate so the system can evolve into specialist
agents later.

## Narrow-terminal design

Fade detects terminal width. On small screens it uses one-line status updates and compact
file summaries. On desktop it can render multi-column phase summaries. No functionality
requires a large terminal.

## Safety

- API keys are never written to generated projects.
- Generated paths cannot escape the selected workspace.
- Shell execution is **not enabled by default** in 1.1.
- Verification commands require an explicit `--allow-run` flag.
- Third-party skills should be reviewed before use.

## License

Apache-2.0 for the Fade implementation in this repository. Third-party providers and
skills retain their own terms.
