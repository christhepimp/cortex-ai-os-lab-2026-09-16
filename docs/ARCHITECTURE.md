# Architecture

```
+---------------------------------------------+
|  Cortex supervisor (AI policy / intent)     |
|  observe → decide → act (userspace only)    |
+---------------------------------------------+
|  Android userspace (init, zygote, system_server) |
+---------------------------------------------+
|  Linux kernel (Goldfish/ranchu or host)     |
|  drivers, scheduler, MM, syscalls           |
+---------------------------------------------+
|  QEMU / KVM / LXC / host hardware           |
+---------------------------------------------+
```

## Rule

The OS *feeling* can be AI. The kernel cannot be an LLM.

Replacing Linux means writing:
- boot + early init
- memory management
- process/thread scheduling
- syscall ABI
- filesystems
- device drivers for virtio, GPU, input, net

That is years of systems work. This lab treats Linux as the machine and Cortex as the government.

## Replacement order (slow)

1. Telemetry collector (`uname`, `/proc`, `ps`, `logcat`)
2. Policy file: allowlist of actions
3. Actuator over `adb shell` (root)
4. Own long-running services you start yourself
5. Optional: custom recovery / custom ramdisk later — still Linux
