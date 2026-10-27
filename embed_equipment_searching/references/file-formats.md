# File formats for equipment searching

Fill these shapes. Keep the section letters and table names so every project reads the same. `<...>` is replaced; rows repeat.

## Export/<Topic>_selection_<date>.md

```markdown
# <Part> selection for <application> (<date>)

The part list is in `<Topic>_vendors_<date>.md`. Working files are in `Research/`.

## A. Requirements from the user
| # | Requirement | Source |
|---|---|---|
| A1 | <requirement, key number in bold> | <Requirements.md / Improvement_N.md / conversation <date> / Vendors/<file>.pdf> |

## B. Factors for choosing the <part>
| Factor | What it means |
|---|---|
| <factor> | <plain meaning, formula if any> |

## C. Known factors and what they leave
<what the known requirements fix (numbers from the script), the module vs. raw part rule, the shortlist with one line of reason each, and a link to the pairing table>

## D. Unknown factors (needed to finish the research)
| # | Unknown | Why it matters | Who supplies it |
|---|---|---|---|
| D1 | <unknown> | <effect on the choice> | <developer / datasheet / field test> |

## E. Recommendations for the system
<numbered, one recommendation per item, with its reason>

## F. Citations
- [<title>](<url>) or `Vendors/<file>.pdf`
```

## Export/<Topic>_vendors_<date>.md

```markdown
# <Part> vendors and models (<date>)

Target: <one line from A>. Factor meanings are in `<Topic>_selection_<date>.md`, section B.
All specs come from public pages and are unverified until the documents in `Research/Documents_to_collect_<date>.md` arrive.

## Factor key
| Code | Factor | ✓ means |
|---|---|---|
| F1 | <factor> | <condition> |

✓ = yes, ✗ = no, ? = not confirmed.

## Table 1a: modules (Type = Module)
| Type | Vendor | Model | <key specs> | Path to host | Mount/connector | Weight | Price | F1 | … | Fn |
|---|---|---|---|---|---|---|---|---|---|---|
| Module | <vendor> | [<model>](<model page>) | … | … | … | … | … | ✓ | … | ? |

## Table 1b: raw parts (Type = Raw part)
| Type | Vendor | Part | <key specs> | Native interface | Needed to reach host | F1 | … | Fn |

## Table 2…: derived tables
<numbers per candidate from the script, with the formula above the table; cite `Research/scripts/<name>.py`>

## Table N: pairing
| <Part A> | <Part B> | Fits? | <derived numbers> | Weight |
<the formula and the fit rule above the table>

## Sources
Grouped by kind (parts, accessories, papers). One line per link: - [<name>](<url>)
```

## Research/Documents_to_collect_<date>.md

```markdown
# Documents to collect (<date>)

The developer finds and supplies these. Put them in `Vendors/`.

## A. <kind, e.g. part datasheets>
- [ ] <exact document name, or search words> — needed for: <which unverified spec or factor>
```
