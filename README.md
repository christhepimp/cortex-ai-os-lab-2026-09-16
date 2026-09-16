# Cortex AI OS Lab (2026-09-16)

Research scaffold: start from a **rooted Android emulator**, get a Linux shell, then grow an **AI control plane** that starts making OS-level decisions.

**This is not a finished operating system.** You cannot casually replace the Linux kernel inside Android and ship a new OS in one repo. Linux stays. The AI becomes the brain *on top* of Linux, then slowly owns more userspace.

Repo: https://github.com/christhepimp/cortex-ai-os-lab-2026-09-16

You already have many repos with this same goal (`synapse-aios`, `aetheros-ai-kernel`, `SentientOS`, `AetherAI-OS`, `AI-OS-Project`, and others). Use **one** lab and iterate. Duplicating the idea does not replace Linux.

## What is actually possible

| Layer | Reality |
| --- | --- |
| Android emulator | Yes. Official AVD, Genymotion, Waydroid |
| Root on emulator | Yes. AOSP/`google_apis` images often `adb root`. Play Store images need Magisk / AERoot / rootAVD |
| Linux inside Android | Yes. Android is a Linux kernel + Android userspace |
| Root shell / inspect `/proc`, kernel version | Yes |
| Custom userspace "AI OS" supervisor | Yes, as a process that observes and decides |
| Replace Linux kernel with an AI | No. A kernel is drivers, scheduler, MMU, syscalls. An LLM is not that |

The honest architecture: **Linux kernel remains**. An AI supervisor observes the system and gradually owns init, scheduling *policy*, package install, networking policy, and UI. That is how "the OS itself is AI" is built without lying about kernels.

## Recommended emulator path (rooted)

### 1. Fastest root: Android Studio AVD without Play Store

Use a **Google APIs** image, not Google Play.

```bash
adb devices
adb root
adb remount
adb shell
# you should see #
id
uname -a
cat /proc/version
```

Start writable if you need system changes:

```bash
emulator -avd YOUR_AVD -writable-system
```

### 2. Play Store images (need extra root tooling)

- AERoot (quarkslab) — on-the-fly root for Google Play AVDs via QEMU GDB stub
- android_emuroot (airbus-seclab) — older sibling of AERoot
- Magisk-on-emulator / rootAVD style patches of ramdisk.img
- Genymotion Desktop — many images support dynamic root

AERoot pattern:

```bash
emulator @Your_AVD -qemu -s
# then aeroot daemon  → adb shell is root
```

### 3. Linux-native Android (closest to "inside Linux")

- Waydroid — Android in an LXC container sharing the host kernel
- redroid — Android in Docker
- Android-x86 / Bliss OS — full Android as a VM/OS

These are better if the goal is "I want a Linux environment I control," not Play-certified apps.

## Staged replacement plan (do this order)

1. **Observe** — supervisor reads uname, /proc, ps, dumpsys, logcat.
2. **Advise** — AI proposes actions; human/script must confirm.
3. **Act in userspace** — start/stop services, set props, install packages, change network policy.
4. **Own init-adjacent jobs** — your supervisor becomes the thing that launches the rest of userspace.
5. **Never skip to rewriting the kernel** until you can write drivers and a scheduler. That is a multi-year OS project, not a weekend repo.

See `docs/ARCHITECTURE.md` and `supervisor/`.

## Layout

```
docs/ARCHITECTURE.md     why Linux stays, how AI becomes the OS brain
docs/EMULATORS.md        rooted emulator options
supervisor/cortex.py     tiny userspace observer/decision stub
```

## License

Research / educational. Do not use this to attack devices you do not own.
