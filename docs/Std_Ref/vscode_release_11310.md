Visual Studio Code 1.131

Show release notes after an update

Follow us on LinkedIn, X, Bluesky | View online

Release date: July 29, 2026

Welcome to the 1.131 release of Visual Studio Code. This release brings more visibility into running subagents, built-in dictation across the workbench, and a new hybrid Markdown editor.

Subagents: See a running subagent's model, elapsed time, and active tool call without opening its conversation.

Built-in dictation (Experimental): Dictate in chat, editors, and the terminal without installing the Speech extension.

Hybrid Markdown editor (Experimental): View, edit, and add agent-actionable comments to Markdown files in the Agents window.

Happy Coding!

VS Code is rolling out gradually to all users. Use Check for Updates in VS Code to get the latest version immediately.

To try new features as soon as possible, download the nightly Insiders build, which includes the latest updates as soon as they are available.

In this update
Agents
Chat
Editor Experience
Accessibility
Terminal
Languages
Deprecated features and settings
Thank you
Agents
Agent host
As mentioned in our last few releases, we're rearchitecting how agent sessions work in VS Code around the agent host - a dedicated process that runs agent harnesses such as Copilot, Claude, and Codex, based on the Agent Host Protocol (AHP). Because a session lives in its own process, the same session can be connected to and rendered from multiple VS Code windows at once. The agent host's Copilot agent is powered by the Copilot SDK, which means that its behavior and functionality is aligned with the Copilot CLI, the standalone GitHub Copilot app, and other Copilot products.

We're actively developing the agent host and progressively rolling it out to users. To opt in, enable   chat.agentHost.enabled and then select an agent host harness from the harness dropdown. The screenshot below shows how to select the Copilot harness on the agent host in the editor window:

Screenshot showing the harness dropdown in the editor window.

You can learn more in our VS Code Agent Host architecture documentation. If you have any feedback or requests, please let us know by filing an issue.

More information about running subagents (Agents window)
When working on complex tasks, the agent can delegate tasks to subagents to run them in parallel in its own context window. You can now quickly see what a running subagent is doing without opening its conversation. In the Agents window, the main conversation shows the following information for each running subagent:

The model used by the subagent
How long the subagent has been running
The tool that the subagent is actively calling
Select a running subagent to open its conversation in another chat, where you can review its full progress while the parent conversation remains available.


Chat
VS Code pet (Experimental)
A new highly experimental pet has been discovered in VS Code! Enter /vscode-pet in chat to meet your new companion.


Editor Experience
Built-in dictation across VS Code (Experimental)
Setting:   dictation.enabled , dictation.showTranscript,   dictation.experimental.llmCleanup

To use dictation in VS Code, you no longer need to install the VS Code Speech extension. The built-in transcription service works in chat inputs, text editors, and the integrated terminal, with live text and controls suited to each surface. A single speech session and microphone selection are shared across all three surfaces, which prevents overlapping recordings and keeps dictated text in the intended location.


Built-in dictation uses the private, offline Nemotron model. The model downloads on first use and keeps audio on your device.

Use dictation.showTranscript to control whether the live transcript appears while you dictate. With   dictation.experimental.llmCleanup enabled, Copilot refines your transcript as you speak by adding formatting and removing filler words. Transcript text is sent to a language model for cleanup. If cleanup is unavailable, VS Code keeps the raw transcript.

Platform support
The following platforms are supported for built-in dictation:

Windows x64 and Arm64
macOS on Apple silicon
Linux x64 and Arm64 with glibc 2.34 or later
Remote workspaces (because transcription runs on the local VS Code client)
The following platforms are not currently supported for built-in dictation:

VS Code for the Web
Intel-based Macs, 32-bit systems, and Arm32 systems
Support for more platforms and languages is a work in progress.

Hybrid Markdown editor (Experimental)
Setting:   workbench.editor.markdownDefaultEditorInAgentsWindow

In this release, we introduce a new hybrid Markdown editor in the agents window. It lets you view Markdown files, edit them in-place, and add comments that an agent can act on.

By using Reopen Editor With you can switch between the text editor and this new Markdown editor, both in the Agents window and editor windows.


Accessibility
More control over terminal screen reader updates
Setting:   terminal.integrated.accessibleViewPreserveCursorPosition

Screen reader users can read terminal output at their own pace while commands continue to produce output. Set   terminal.integrated.accessibleViewPreserveCursorPosition to always to preserve the cursor position in the terminal Accessible View, including when new content arrives. Existing true and false values continue to work.

Terminal live updates also use a non-interrupting ARIA status announcement instead of an assertive alert. Output remains available to screen readers without repeatedly interrupting other speech.

Terminal
Control the terminal resize dimensions overlay
Setting:   terminal.integrated.resizeDimensionsOverlay.enabled

If you find the columns-by-rows overlay distracting when resizing the terminal, you can disable it with the   terminal.integrated.resizeDimensionsOverlay.enabled setting. The overlay remains enabled by default, and setting changes apply immediately to open terminals without a restart.

Screenshot of the overlay that appears in the middle of the terminal with the current columns and rows when a terminal resize happens.

Languages
Python
Python Environments is the default environment-management experience in VS Code Stable and Insiders after its rollout reached 100% of users. Review the Python Environments rollout details and tracking.

Python projects start faster and spend less time refreshing environments. Conda discovery is deferred until needed, concurrent environment scans are consolidated, and Pylance can use the last-known interpreter while a full refresh continues. #1600: Lazy-register Conda manager, #1598: Coalesce concurrent native finder refreshes with the same key, #1607: Return last-known environment when getEnvironment times out

Deprecated features and settings
None

Thank you
Contributions to vscode:

@accnops (Arthur Cnops): voice: make passive ptt_start the canonical hands-free narration fix PR #326405
@bwateratmsft (Brandon Waterloo [MSFT]): Add a when clause context key for detecting if an extension is installed+enabled PR #326814
@Kaidesuyoo (Kaidesuyo): fix performance regression caused by modern UI styles PR #325985
@mirimadahmed (Mir): Fix voice barge in regression PR #326611
@piyushmadan (Piyush Madan): Resolve execution subagent model by exact CAPI id before family fallback PR #324859
@SimonSiefke (Simon Siefke)
fix: memory leak in abstractTaskService PR #326934
fix: memory leak in abstractRuntimeExtensionsEditor PR #326890
fix: memory leak in terminalProcessManager PR #326930
fix: memory leak in debugModel PR #327047
fix: memory leak in terminalService PR #327156
fix: memory leak in mainThreadTerminalService PR #327155
@SixFive7 (Jori Huisman): Honor Explorer's minItems for the Windows taskbar jump list PR #318117
@soreavis: Git - resolve the active notebook for Open Changes / Open File PR #326468
Issue tracking
Contributions to our issue tracking:

@gjsjohnmurray (John Murray)
@RedCMD (RedCMD)
@IllusionMH (Andrii Dieiev)
@albertosantini (Alberto Santini)
We really appreciate people trying our new features as soon as they are ready, so check back here often and learn what's new.

If you'd like to read release notes for previous VS Code versions, go to Updates on code.visualstudio.com.