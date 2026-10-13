# Narrowing-Down Techniques

Detail for the **How to check** field of a point in `SKILL.md` Stage 2. These are checks the **developer runs** on their own machine or board. Claude explains in plain words what to run and what each result means, and assumes no direct access to the target. Claude writes no code, repro program or script for any of them (Hard Rule 1). Pick the one check that fits the point, not all of them.

## Elimination Checklist

Turn the suspected causes into a short list of yes/no checks, ordered cheapest-to-check first. For each item, state what result confirms it and what result rules it out. Example shape:

1. Is the driver even probing? (look in `dmesg` for the probe log line)
2. Is the IRQ firing? (compare the `/proc/interrupts` count before and after triggering)
3. Is the DMA buffer correctly mapped? (check the mapping falls inside the device's addressable range)

Stop at the first confirmed item. That is the lead to chase; the rest of the list doesn't need checking.

## `git bisect`

Use when the bug is a regression (it used to work). Needs a known-good and known-bad commit/tag. The developer runs:

```sh
git bisect start
git bisect bad                  # current commit is broken
git bisect good v2023.04         # last known-good tag/commit
# git bisect checks out a midpoint; the developer builds/flashes/tests it, then:
git bisect good   # or: git bisect bad
# repeat until git bisect reports the first bad commit
git bisect reset
```

`git bisect run <script>` only makes sense if the developer already has a non-interactive way to test a commit (e.g. it boots under QEMU). Otherwise it stays a manual loop. Claude doesn't write that script.

## Standalone Program

Fits when the suspected point is in portable logic (parsing, a state machine, buffer math) rather than something inherently target-specific (a register access, a DMA path, an interrupt handler).

Tell the developer:
- which function or logic to pull out
- which inputs reproduce the failure
- which result shows the bug

The developer builds it on the host and runs it under:
- **AddressSanitizer / UndefinedBehaviorSanitizer** (`-fsanitize=address,undefined`): catches buffer overflows, use-after-free and UB.
- **Valgrind**: no rebuild needed, but slower.

Not applicable when the bug depends on real timing, hardware state, or peripheral behavior that can't be faithfully modeled off-target.

## `creduce`

Fits once the developer has a standalone C/C++ repro that's too large to reason about. `creduce` needs an *interestingness test*, a script that exits `0` exactly when the bug is still present. Tell the developer what that test must check: the exact compiler/sanitizer error or assertion text, not just "it fails". A test that's too loose (matches unrelated failures) reduces to the wrong thing. Shape of a test **the developer writes**:

```sh
#!/bin/sh
# interesting.sh
cc -fsanitize=address,undefined -o /tmp/repro repro.c 2>/tmp/err || exit 1
/tmp/repro >/tmp/out 2>>/tmp/err
grep -q "the specific assertion/sanitizer error" /tmp/err
```

```sh
creduce interesting.sh repro.c
```
