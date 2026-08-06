# ASM: OBS Studio

> OBS Studio is free, open-source software for real-time video and audio capture, composition, recording, and live streaming.

## 0. Identity

| Field | Details |
|---|---|
| Name | OBS Studio |
| Version | 32.2.1 documentation candidate; verify the installed version before use |
| Category | Recording, live streaming, and real-time audiovisual composition |
| Platforms | Windows, macOS, Linux |
| License | GPL-2.0-or-later |

> **Scope:** Profiles, Scene Collections, scenes, sources, Preview, the Audio Mixer, video and output settings, Studio Mode, local recording, diagnostics, and WebSocket security. Plugin development and exhaustive encoder tuning are not covered.
>
> **Confidence:** Based on official documentation and not yet tested on the target computer. Interface labels and available capture methods and encoders vary by platform, language, hardware, and version. OBS 32.2 replaced the Add Source drop-down menu with a new dialog, so older screenshots may look different.

## 1. Sources

- **User-provided · Official repository:** [obsproject/obs-studio](https://github.com/obsproject/obs-studio)
- **Agent search · Official:** [Quick Start Guide](https://obsproject.com/kb/quick-start-guide)
- **Agent search · Official:** [OBS Studio Overview](https://obsproject.com/kb/obs-studio-overview)
- **Agent search · Official:** [Sources Guide](https://obsproject.com/kb/sources-guide)
- **Agent search · Official:** [Audio Mixer Guide](https://obsproject.com/kb/audio-mixer-guide)
- **Agent search · Official:** [Scene Collections](https://obsproject.com/kb/scene-collections)
- **Agent search · Official:** [Audio/Video Formats Guide](https://obsproject.com/kb/audio-video-formats-guide)
- **Agent search · Official:** [Remote Control Guide](https://obsproject.com/kb/remote-control-guide)
- **Agent search · Official:** [OBS Studio 32.2.1 Release Notes](https://github.com/obsproject/obs-studio/releases/tag/32.2.1)

## 2. Capability Tree

```text
OBS Studio
├── Workspace isolation: Profile / Scene Collection
├── Visual composition: scenes / sources / Window Capture / transform and lock
├── Audio: mixer inspection / mute and filters
├── Output: resolution / recording format and path / start and stop recording
├── Production: Studio Mode transitions
└── Safety and diagnostics: output state / logs / WebSocket
```

## 3. Function Cards

### [Workspace Isolation > Profile] Isolate Output Settings

- **Purpose:** Keep test streaming, output, audio, and video settings separate from existing configurations.
- **Entry point:** `Profile` menu.
- **Procedure:** Create or duplicate a Profile → use a unique test prefix → switch to it and verify the current name → configure output only within that Profile.
- **Success check:** The new Profile is active, and the original Profile is unchanged.
- **Patch:** A Profile does not store scenes or sources; those belong to a Scene Collection. After switching, recheck the service, resolution, recording path, and audio tracks.

### [Workspace Isolation > Scene Collection] Isolate Scenes and Sources

- **Purpose:** Avoid affecting the user's existing visual layouts.
- **Entry point:** `Scene Collection` menu.
- **Procedure:** Create a collection with a unique test prefix → switch to it → add the test scenes and sources → inspect the Audio Mixer again.
- **Success check:** The new collection is active, and the original scenes are unchanged.
- **Patch:** A Scene Collection does not store output settings, so use a separate test Profile as well.

### [Visual Composition > Scenes and Sources] Create a Layout

- **Purpose:** Create complete layouts such as Demo and Standby screens.
- **Entry point:** The `+` buttons in the Scenes and Sources docks.
- **Procedure:** Create a scene → select it → add color, text, window, and other sources → adjust layer order and visibility → lock the sources when finished.
- **Success check:** Each scene displays the expected layout in Preview, with the sources in the correct order and locked.
- **Patch:** Sources higher in the list appear in front. “Add Existing” shares the same source object; hiding a source is not the same as deleting it.

### [Visual Composition > Window Capture] Capture Only the Specified Window

- **Purpose:** Avoid recording the entire desktop, notifications, or other windows.
- **Entry point:** Sources → `Window Capture`; the label may vary by platform.
- **Procedure:** Ask which window to use if none was specified → add Window Capture → select the exact window → verify it in Preview → crop only if necessary.
- **Success check:** Only the specified window is visible; the desktop and unrelated windows are not.
- **Patch:** Do not substitute Display Capture when the user requests Window Capture. If the source is black, check whether the window is minimized, whether privilege levels match, hardware acceleration, and the capture method. Do not click blindly.

### [Visual Composition > Transform and Lock] Fit the Source Without Stretching

- **Purpose:** Place a source while preserving its aspect ratio.
- **Entry point:** Transform handles in Preview, or right-click the source → Transform.
- **Procedure:** Select the source → scale proportionally or fit it → crop if necessary → inspect the edges → lock it.
- **Success check:** There is no obvious stretching, important content is visible, and the source cannot be dragged accidentally.

### [Audio > Mixer Inspection] Identify Active and Duplicate Capture

- **Purpose:** Confirm which audio paths have an actual signal and prevent duplicate capture or feedback.
- **Entry point:** Audio Mixer and Advanced Audio Properties.
- **Procedure:** Play a known sound and watch the meters → identify active channels → compare global devices with per-scene audio sources → mute only when there is a clear reason.
- **Success check:** Required audio has a signal, with no unnecessary duplicate channels or feedback.
- **Patch:** Do not judge activity from a source name alone. Do not change system audio devices without permission merely to make a meter move.

### [Output > Video and Recording Settings] Configure a 720p30 Local Recording

- **Purpose:** Produce a predictable, recoverable test file.
- **Entry point:** Settings → Video; Settings → Output → Recording.
- **Procedure:** Only in the test Profile, set output to 1280×720 at 30 FPS → choose a writable path → when available, select an interruption-resilient container such as MKV → use an encoder that is actually available on the computer → apply, reopen, and verify the settings.
- **Success check:** The resolution, frame rate, format, path, and encoder remain set to the selected values.
- **Patch:** Do not assume that NVENC, AMF, or QSV is available. If MP4 is ultimately required, remux after recording has stopped successfully.

### [Output > Start and Stop Recording] Create and Verify a File

- **Purpose:** Record the current Program output and confirm that the file is usable.
- **Entry point:** Controls → Start Recording / Stop Recording.
- **Procedure:** Confirm that no output is currently running → start recording → watch the indicator and timer → perform the task → stop recording → open the recording folder and inspect the newest file.
- **Success check:** Recording has stopped, and the new file exists with a nonzero size; review a short segment if the environment allows.
- **Patch:** Never use Start Streaming as a substitute. Do not delete the test file on your own.

### [Production > Studio Mode] Preview Before Transitioning

- **Purpose:** Prepare the next visual in Preview without changing Program.
- **Entry point:** Controls → Studio Mode.
- **Procedure:** Enable Studio Mode and identify Preview and Program → send the initial scene to Program → prepare the next scene in Preview → set the transition → run it and check Program.
- **Success check:** Program changes only after the transition, while Preview can be prepared independently.
- **Patch:** A scene visible in Preview has not necessarily been output. Check Program.

### [Safety and Diagnostics > Output State] Check Before Acting

- **Purpose:** Avoid accidentally changing a production environment that is currently streaming or recording.
- **Entry point:** Controls, status bar, timers, and status indicators.
- **Procedure:** Check streaming, recording, replay buffer, and virtual camera → report any active states → if an output is active, pause and ask the user what to do.
- **Success check:** All relevant states are known, and risky work begins only in an isolated, non-live environment.
- **Patch:** Never display stream keys or passwords in screenshots, logs, or reports.

### [Safety and Diagnostics > Logs and WebSocket] Diagnose with Evidence and Protect Remote Control

- **Purpose:** Troubleshoot from explicit errors and safely enable approved remote control.
- **Entry point:** Help → Log Files; Tools → WebSocket Server Settings. Exact labels vary by version.
- **Procedure:** Reproduce the issue once when safe → inspect the error at the corresponding time → redact before sharing; enable WebSocket only when genuinely needed → limit the listening scope → enable authentication → test with a trusted client.
- **Success check:** The report cites a specific error without sensitive information, and only approved clients can connect.
- **Patch:** Logs may contain computer and account information. Do not disable authentication or store the password in an ASM.
