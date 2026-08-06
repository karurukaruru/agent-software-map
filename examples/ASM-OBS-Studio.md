# ASM: OBS Studio

> OBS Studio is free, open-source software for real-time video/audio capture, composition, recording, and live streaming.

## 0. Identity

| Field | Value |
|---|---|
| Name | OBS Studio |
| Version | 32.2.1 documentation candidate; verify the installed version |
| Category | Recording, live streaming, real-time audiovisual composition |
| Platforms | Windows, macOS, Linux |
| License | GPL-2.0-or-later |

> **Scope:** Core desktop workflow: profiles, scene collections, scenes, sources, preview, audio mixer, video/output settings, Studio Mode, local recording, diagnostics, and WebSocket safety. Plugin development and exhaustive encoder tuning are excluded.
>
> **Confidence:** Documentation-based and not yet tested on the target machine. Interface labels and available capture/encoder choices vary by platform, language, hardware, and version. OBS 32.2 replaced the add-source dropdown with a new dialog, so earlier screenshots may differ.

## 1. Sources

- **User-provided · Official repository:** [obsproject/obs-studio](https://github.com/obsproject/obs-studio)
- **Agent-retrieved · Official:** [Quick Start Guide](https://obsproject.com/kb/quick-start-guide)
- **Agent-retrieved · Official:** [OBS Studio Overview](https://obsproject.com/kb/obs-studio-overview)
- **Agent-retrieved · Official:** [Sources Guide](https://obsproject.com/kb/sources-guide)
- **Agent-retrieved · Official:** [Audio Mixer Guide](https://obsproject.com/kb/audio-mixer-guide)
- **Agent-retrieved · Official:** [Scene Collections](https://obsproject.com/kb/scene-collections)
- **Agent-retrieved · Official:** [Audio/Video Formats Guide](https://obsproject.com/kb/audio-video-formats-guide)
- **Agent-retrieved · Official:** [Remote Control Guide](https://obsproject.com/kb/remote-control-guide)
- **Agent-retrieved · Official:** [OBS Studio 32.2.1 release](https://github.com/obsproject/obs-studio/releases/tag/32.2.1)

## 2. Capability tree

```text
OBS Studio
├── Workspace isolation
│   ├── Profile
│   └── Scene Collection
├── Composition
│   ├── Scene
│   ├── Source
│   ├── Window Capture
│   └── Transform and lock
├── Audio
│   ├── Mixer inspection
│   └── Mute and filters
├── Output
│   ├── Canvas and output resolution
│   ├── Recording format and path
│   └── Start and stop recording
├── Production
│   └── Studio Mode transition
└── Safety and diagnostics
    ├── Output-state preflight
    ├── Log inspection
    └── WebSocket access
```

## 3. Function cards

### [Workspace isolation > Profile] Isolate output settings

**Introduction**

- **Purpose:** Keep task-specific streaming, output, audio, and video settings separate.
- **Entry point:** `Profile` menu.
- **Procedure:** Create or duplicate a profile → use a unique task prefix → switch to it → verify the active name → configure output only inside it.
- **Success check:** The new profile is active and the original profile remains unchanged.

**Operational patches**

- A profile does not contain scenes and sources; those belong to a Scene Collection.
- Recheck service, output resolution, recording path, and audio tracks after switching.

### [Workspace isolation > Scene Collection] Isolate scenes and sources

**Introduction**

- **Purpose:** Keep a task's visual layout and source objects separate from existing work.
- **Entry point:** `Scene Collection` menu.
- **Procedure:** Create a collection with a unique task prefix → switch to it → add task scenes and sources → inspect the mixer after switching.
- **Success check:** The new collection is active and pre-existing scenes have not changed.

**Operational patches**

- Scene Collections do not hold output settings; use a Profile as well.
- Global audio devices can differ between collections. Recheck actual meter activity.

### [Composition > Scene] Create and switch scenes

**Introduction**

- **Purpose:** Organize complete layouts such as Demo and Standby.
- **Entry point:** Scenes dock `+` button or context menu.
- **Procedure:** Create uniquely named scenes → select one → add its sources → order scenes for easy switching.
- **Success check:** Selecting each scene shows the expected layout in Preview.

**Operational patches**

- Outside Studio Mode, switching scenes can immediately change the recorded or streamed output.

### [Composition > Source] Add and layer sources

**Introduction**

- **Purpose:** Compose color, text, images, windows, cameras, media, or other scenes.
- **Entry point:** Sources dock `+` button.
- **Procedure:** Select the target scene → add a source type → choose new or existing → configure it → order layers → set visibility → lock finished sources.
- **Success check:** The intended source is visible, correctly layered, and locked when layout is complete.

**Operational patches**

- Sources higher in the list render in front of lower sources.
- Reusing an existing source shares the same source object; edits may affect every scene that references it.
- Hiding is not deleting. Some hidden sources can still consume resources.

### [Composition > Window Capture] Capture one application window

**Introduction**

- **Purpose:** Capture a designated application without exposing the whole desktop.
- **Entry point:** Sources dock → `Window Capture` (label may vary by platform).
- **Procedure:** Ask the user which window if unspecified → add Window Capture → select the exact window → verify the preview → crop only if needed.
- **Success check:** Only the designated window appears; desktop, notifications, and unrelated windows are absent.

**Operational patches**

- Do not substitute Display Capture when the request is window-only.
- Minimized, protected, GPU-accelerated, or privilege-mismatched windows may appear blank. Recheck the target and capture method rather than clicking blindly.

### [Composition > Transform and lock] Fit without distortion

**Introduction**

- **Purpose:** Place a source on the canvas while preserving its proportions.
- **Entry point:** Preview transform handles or source context menu → Transform.
- **Procedure:** Select the source → fit or scale proportionally → crop if necessary → inspect edges → lock the source.
- **Success check:** The source has no obvious stretching, important content is visible, and accidental dragging is prevented.

**Operational patches**

- Drag a side handle only when intentional distortion is acceptable. Cropping and scaling solve different problems.

### [Audio > Mixer inspection] Check active and duplicate capture

**Introduction**

- **Purpose:** Confirm which audio paths have real signal and avoid duplicate capture.
- **Entry point:** Audio Mixer dock and Advanced Audio Properties.
- **Procedure:** Observe meters while known sound plays → identify active channels → compare global devices with per-scene audio sources → mute only with a stated reason.
- **Success check:** Required audio has signal, unwanted duplicates are absent or muted, and no feedback loop is created.

**Operational patches**

- Do not infer activity from a source name; use the meter.
- Do not change system audio devices merely to make a meter move without permission.

### [Output > Canvas and output resolution] Set 720p30 safely

**Introduction**

- **Purpose:** Configure a predictable video size and frame rate for a test recording.
- **Entry point:** Settings → Video.
- **Procedure:** In the isolated Profile, inspect base canvas → set output resolution to 1280×720 → set 30 FPS → apply → recheck Preview.
- **Success check:** Settings show 1280×720 at 30 FPS and sources still fit the canvas.

**Operational patches**

- Changing canvas size can alter layout. Avoid changing an existing user's Profile.

### [Output > Recording format and path] Choose a recoverable local recording

**Introduction**

- **Purpose:** Make a local test recording resilient to interruption and easy to find.
- **Entry point:** Settings → Output → Recording.
- **Procedure:** Inspect available modes and encoders → select an interruption-resilient container such as MKV when available → select a writable path → use an available encoder → apply.
- **Success check:** The chosen format, path, and encoder remain visible after reopening settings.

**Operational patches**

- Do not assume NVENC, AMF, QSV, or another hardware encoder exists.
- If MP4 is required, consider recording to MKV and remuxing after a successful stop.

### [Output > Start and stop recording] Produce and verify a local file

**Introduction**

- **Purpose:** Record the current Program output and prove that a usable file was created.
- **Entry point:** Controls dock → Start Recording / Stop Recording.
- **Procedure:** Confirm no output is already running → start recording → observe the recording indicator and timer → perform the scene action → stop → open the recording location → check the newest file.
- **Success check:** Recording is stopped and the new file exists with non-zero size; play back a short segment when permitted.

**Operational patches**

- Never press Start Streaming as a substitute. If the state is ambiguous, stop and inspect first.
- Do not delete the test file unless the user asks.

### [Production > Studio Mode transition] Prepare before changing Program

**Introduction**

- **Purpose:** Prepare a scene privately in Preview before sending it to the recorded or streamed Program output.
- **Entry point:** Controls dock → Studio Mode.
- **Procedure:** Enable Studio Mode → identify Preview and Program → put the initial scene in Program → prepare the next scene in Preview → select transition/duration → trigger transition → verify Program.
- **Success check:** Program changes only after the transition, while Preview can be edited independently.

**Operational patches**

- Do not treat a Preview-only change as published. Check the Program pane.

### [Safety and diagnostics > Output-state preflight] Check before editing

**Introduction**

- **Purpose:** Avoid changing a live or ongoing production accidentally.
- **Entry point:** Controls dock, status bar, and visible timers/indicators.
- **Procedure:** Inspect streaming, recording, replay buffer, and virtual camera states → report any active output → pause for user direction before modifying a live setup.
- **Success check:** All relevant states are known; risky work begins only in an isolated, non-live context.

**Operational patches**

- Never expose stream keys or passwords in screenshots, logs, or reports.

### [Safety and diagnostics > Log inspection] Diagnose with evidence

**Introduction**

- **Purpose:** Replace guessing with version, device, encoder, and error evidence.
- **Entry point:** Help → Log Files (exact label can vary by version).
- **Procedure:** Reproduce once when safe → open the current log → inspect timestamps and explicit errors → redact paths, account names, tokens, and service details before sharing.
- **Success check:** The report cites the relevant error and time without revealing sensitive data.

**Operational patches**

- Logs can contain machine and account information. Share the minimum necessary excerpt.

### [Safety and diagnostics > WebSocket access] Control OBS remotely

**Introduction**

- **Purpose:** Allow an approved controller to query or change OBS state.
- **Entry point:** Tools → WebSocket Server Settings in supported versions.
- **Procedure:** Confirm remote control is required → bind only as broadly as necessary → enable authentication → store the password outside the map → test with a trusted client.
- **Success check:** The approved client connects and unauthorized clients cannot.

**Operational patches**

- Do not disable authentication or publish the password. Treat remote output commands as high impact.
