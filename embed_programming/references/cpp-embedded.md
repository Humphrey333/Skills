# C and C++ rules for embedded Linux

Rules for C and C++ code written or changed with `embed_programming`. Target: NVIDIA Jetson-class boards, where memory and CPU are not tight, so ordinary heap use is fine outside interrupt and real-time paths. Each rule names its source. When the project's own style or `.clang-tidy` says otherwise, the project wins: mention the conflict, do not override it.

Sources: C++ Core Guidelines (CppCoreGuidelines, `R`, `ES`, `CP`, `E`, `Enum`, `Con` sections); Linux kernel documentation (`Documentation/process/coding-style.rst`, `Documentation/core-api/genericirq.rst`, `Documentation/driver-api/driver-model/devres.rst`); AUTOSAR C++14 and MISRA C++ (ideas only, not full compliance).

## Ownership and memory (C++)

- Own resources with RAII: a constructor acquires, the destructor releases. Files, sockets, mutex locks, mapped memory, GStreamer/V4L2 handles all get an owning object (Core Guidelines R.1).
- `std::unique_ptr` by default; `std::shared_ptr` only when ownership is really shared (R.20, R.21). Create with `std::make_unique` / `std::make_shared` (R.22, R.23).
- No raw `new` or `delete` in application code (R.11). A C library handle gets a `unique_ptr` with a custom deleter.
- A raw pointer or reference means "borrowed, not owned" (R.3).
- No allocation, and no container growth, in interrupt handlers, signal handlers or real-time callbacks. Allocate up front (AUTOSAR A18-5 idea).

## Types and constants

- `constexpr` or `const` variables instead of `#define` constants; `enum class` instead of plain enums or `#define` lists (ES.31, Enum.3).
- Fixed-width integers (`uint32_t`, `int16_t`) for registers, protocol fields and file formats (MISRA idea).
- `const` by default for variables, parameters and member functions (Con.1–Con.4).
- No undefined behaviour: no signed overflow, no out-of-bounds access, no type punning through casts; use `std::memcpy` or `std::bit_cast` (ES.103, ES.48).

## Errors

- Check every return value of a system call, driver call or library call that can fail. Log it with context and pass it up (E.2, kernel coding-style ch. 16).
- Every blocking wait has a timeout: `poll`, `select`, condition variables, I2C/SPI transfers, `wait_event_timeout` in the kernel.
- Kernel C: unwind error paths with `goto` labels in reverse order of setup (coding-style ch. 7). Prefer `devm_` managed resources in probe so remove and error paths free them (devres.rst).

## Concurrency and hardware access

- `volatile` only for memory-mapped I/O in userspace; never as a thread sync tool (CP.8). In the kernel use `readl`/`writel`, never `volatile` (coding-style ch. 20).
- Data shared between threads is protected by a `std::mutex` (with `std::lock_guard` / `std::scoped_lock`) or is `std::atomic` (CP.2, CP.20).
- Interrupt handlers, signal handlers and real-time callbacks stay short: no blocking, no sleeping locks, no allocation, no logging that can block. Record the event and defer the work to a thread, a threaded IRQ (`request_threaded_irq`) or a workqueue (genericirq.rst).
- Signal handlers call only async-signal-safe functions; set a `volatile sig_atomic_t` or write to a self-pipe and let the main loop act (POSIX `signal-safety(7)`).

## Style and checks

- Every new or changed function has the header comment from `embed_programming` (purpose, in / out, how it works): Doxygen in userspace C/C++, kernel-doc in kernel code (`Documentation/doc-guide/kernel-doc.rst`).
- Kernel code follows kernel coding style and passes `scripts/checkpatch.pl`.
- Userspace C++ follows the project's `.clang-format` and `.clang-tidy` (the `embed_create_coding_template` configs if the project came from it).
- Host builds of new or changed code run once under AddressSanitizer and UndefinedBehaviorSanitizer (`-fsanitize=address,undefined`), or `valgrind --leak-check=full`, when the code can run on the host. A leak or UB report is a failed verify.
