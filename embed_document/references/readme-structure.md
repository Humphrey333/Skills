# README structure and style rules

Used by `embed_document` README mode as its structural template. Structure comes from the developer's `Requirements` file; the style is **CLI-focused + TOC**, chosen from https://github.com/matiassingers/awesome-readme.

## Style: CLI-focused + table of contents

- A reader should be able to install, build and run from the top of the README without scrolling past background.
- The table of contents comes right after the introduction, links every section and subsection, and each long section ends with `**[Back to top](#table-of-contents)**`.
- Commands are shown in fenced code blocks, one purpose per block, copy-pasteable from a clean checkout.
- Prose is short; link out (BUILD.md, `docs/`, Plans) instead of duplicating.
- Every sentence traces to a source (`embed_document` Step 2); one that no source confirms is asked about or becomes a `TODO:` before the draft goes to `embed_writing`. A heading with no sourced fact keeps a `TODO:` line.
- All prose then passes through `embed_writing` before it is shown: AI-writing signs reworded with the same meaning, sentence-case headings. Act on any sentence it flags; it deletes nothing itself.
- Not used: hero banners, GIF demos, badge walls. A CI build-status badge appears only when a CI configuration exists in the project.

## Sections, in order

| Section | Must contain | Source of truth |
|---|---|---|
| Title + intro | What the project does, why use it, link to project home | `Plans/` goal paragraph, `CMakeLists.txt` project name; home URL is `TODO:` unless known |
| Table of Contents | Every section and subsection | Generated from the headings |
| About the Project | What it is, intended use, how it works, who uses it, benefit; features; one-line contribution policy | Plans, code layout; contribution policy is `TODO:` unless stated |
| Project Status | Build status, current release, known issues, not-yet-implemented items, work in progress | Planned features only, each with the developer's status answer (working / partly / not working / not started); code and `git log` are hints, plans never confirm status |
| Getting Started → Dependencies | Required/optional dependencies, pointer to `BUILD.md` | Same facts as `BUILD.md` |
| Getting Started → Getting the Source | Clone command | `git remote -v`; URL is `TODO:` when no remote |
| Getting Started → Building | Configure, build, configuration options | CMake options and scripts in `tools/` |
| Getting Started → Running Tests | Test command, expected result | `test/`, CTest setup, plan verification criteria |
| Getting Started → Installation | How build artifacts are installed | CMake `install()` rules |
| Getting Started → Usage | How to run it, how to include it, API pointer | Entry points, headers in `include/` |
| Release Process | Cycle, how to find the latest release, branches | `git branch`/tags; otherwise `TODO:` |
| Release Process → Versioning | Scheme and where tags are listed | Tags; otherwise `TODO:` |
| How to Get Help | Contact or issue tracker | `TODO:` unless stated |
| Further Reading | Architecture refs, FAQ, INSTALL, CONTRIBUTING, CODEOWNERS, library docs | Files that actually exist in the project |
| Authors | Maintainers with links | `TODO:` unless stated; `git shortlog` is a suggestion, not an answer |
| License | Summary + link to `LICENSE`, plus licences of bundled external code | `LICENSE` file, `subprojects/` licences |

Omit a subsection (for example Installation for a host-only library) only after asking the developer; do not drop it silently.

## Update rules

- Keep hand-written wording that is still true; change only what the evidence contradicts or what is missing.
- Every `TODO:` carries what is missing, e.g. `TODO: license type` — so the final report can list them.
- Never copy template example text into a real project: "Embedded Artistry", "Phillip Johnston", `your-server`, `your/project`.

## Skeleton

Structure only — replace every line of guidance with content written from evidence, or a `TODO:` marker.

```markdown
# <project name>

<What it does, why use it, link to project home — TODO: if unknown>

## Table of Contents
<links to every section and subsection below>

## About the Project
<what / intended use / how it works / who uses it / benefit; features; contribution policy>

## Project Status
<build status; current release; known issues; not implemented; in progress>

## Getting Started
### Dependencies
<required/optional list; pointer to BUILD.md>
### Getting the Source
<clone command>
### Building
<configure + build commands, options>
### Running Tests
<test command, expected result>
### Installation
<how artifacts are installed>
### Usage
<how to run / include it; API pointer>

## Release Process
<cycle, how to find the latest release, branches>
### Versioning
<scheme, where tags are listed>

## How to Get Help
<contact or issue tracker>

## Further Reading
<links to docs that exist in the project>

## Authors
<maintainers with links>

## License
<summary + link to LICENSE; licences of bundled external code>
```
