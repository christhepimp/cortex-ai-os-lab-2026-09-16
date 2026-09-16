# Rooted Android emulator options

## Official Android Emulator (best lab)

- Create AVD with **Google APIs** (not Play Store) for `adb root`.
- Goldfish (old) / ranchu (current) kernels are Linux.
- `-writable-system` if you need remount.
- For Play images: AERoot + `emulator @AVD -qemu -s`.

Useful commands after root:

```bash
adb shell uname -a
adb shell cat /proc/version
adb shell getprop ro.build.version.release
adb shell ls /proc
```

## Other options

| Tool | Root | Notes |
| --- | --- | --- |
| Android Studio AVD google_apis | Usually `adb root` | First choice |
| AVD Play Store | Need AERoot / Magisk-on-emulator | Harder |
| Genymotion Desktop | Often toggle root | VirtualBox/QEMU |
| Waydroid | Host is already Linux; container root is separate | Best "I am in Linux" feel |
| redroid | Docker Android | CI / headless |
| Bliss OS / Android-x86 | Full VM OS | Not an app emulator |

## What "get in the Linux code" means here

You get a **root shell on a running Linux kernel**, not the AOSP kernel source tree automatically.

To work on kernel source:

- AOSP goldfish/common kernel repos from Android Open Source Project
- Build a custom kernel, point the AVD at it

That is a different project from an AI supervisor.
