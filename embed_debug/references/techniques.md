# Narrowing-Down Techniques

Detail for the Stage 2 table in `SKILL.md`. These are things to *guide the developer through*, not things Claude runs itself — assume no direct access to the target board.

## Elimination Checklist

Turn the suspected causes into a short list of yes/no hypotheses, ordered cheapest-to-check first. For each item, state what result confirms it and what result rules it out. Example shape:

1. Is the driver even probing? (check `dmesg` for the probe log line)
2. Is the IRQ firing? (check `/proc/interrupts` count before/after triggering)
3. Is the DMA buffer correctly mapped? (check the mapping matches the device's addressable range)

Stop at the first confirmed item — that's the lead to chase, not the whole list.

## `git bisect`

Use when the bug is a regression (it used to work). Needs a known-good and known-bad commit/tag.

```sh
git bisect start
git bisect bad                  # current commit is broken
git bisect good v2023.04         # last known-good tag/commit
# git bisect checks out a midpoint; the developer builds/flashes/tests it, then:
git bisect good   # or: git bisect bad
# repeat until git bisect reports the first bad commit
git bisect reset
```

For kernel/bootloader bisects where a full build+flash cycle is slow, suggest `git bisect run <script>` only if the developer has a way to test a candidate commit non-interactively (e.g. boots under QEMU); otherwise it stays a manual loop.

## Simplify to a Standalone Program

When the suspected bug is in portable logic (parsing, a state machine, buffer math) rather than something inherently target-specific (a register access, a DMA path, an interrupt handler), help the developer extract just that logic into a small host-buildable program with the same inputs. This unlocks tools that don't run on the target:

- **AddressSanitizer / UndefinedBehaviorSanitizer** — `-fsanitize=address,undefined`, catches buffer overflows, use-after-free, UB, at the cost of extra memory not always available on the target.
- **Valgrind** — no rebuild needed, but slower.
- Faster iteration in general — no flash/reboot cycle.

Not applicable when the bug depends on real timing, hardware state, or peripheral behavior that can't be faithfully modeled off-target.

## `creduce`

Use once there's a standalone C/C++ repro that's too large to reason about by hand. `creduce` needs an interestingness test script that exits `0` exactly when the bug is still present:

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

Help the developer write the interestingness test precisely — a test that's too loose (matches unrelated failures) will reduce to the wrong thing.
