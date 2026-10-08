# Flag grammar

```
/tpmorpedo [mode] [key:value ...] #1 <dataset one> #2 <dataset two>
/tpmorpedo [mode] set:<name> view:<filters> [free subject]
```

## Modes

| Mode | What runs |
|---|---|
| `prompt` | Filled dual-mining prompt only. Default when no run verb is present. |
| `mine` | Prompt plus both inventories, crosswalk, and gap log. |
| `pages` | Prompt plus public web-app page upgrade from the inventories (mine first if inventories are missing). |
| `all` | Prompt, mine, and pages. |

Run verbs that force `mine` or `all`: `run`, `mine`, `gather`, `procure`, `build`, `upgrade pages`.

## Keys

| Key | Meaning |
|---|---|
| `set` | Single subject. Becomes Dataset #1. Dataset #2 is the same subject under `view`. |
| `view` | `all-types` or a comma filter: `stats`, `images`, `motion`, `holo`. |
| `filter` | Alias of `view`. |
| `slug` | Folder stem under `/workspace/artifacts/tpmorpedo/`. |
| `pages` | Comma list of public routes to upgrade. |
| `geo` | Geography lock for statistics. |
| `since` | ISO date floor for records. |
| `until` | ISO date ceiling. |

Unknown keys stay in the free-subject bag.

## Split rules

1. Text after `#1` and before `#2` is Dataset #1.
2. Text after `#2` is Dataset #2.
3. If only one of `#1` or `#2` is present, the other lane is the same subject with `view` applied (default `all-types`).
4. If neither marker is present, the free subject is Dataset #1 and Dataset #2 is `all-types of <subject>`.
5. Never drop a noun the user typed.

## Examples

```
/tpmorpedo #1 geothermal contractor directory #2 US geothermal market statistics
/tpmorpedo mine view:stats,images set:Aqua Claro pitcher
/tpmorpedo all pages:home,pricing #1 BestSexToys.online catalog #2 adult wellness device market
/tpmorpedo
```
