# Step 7: quick setup

Read at step 7 when the user chose quick setup (`A` after step 5), and in a headless run.

## What a quick run does

**Quick setup** (the user chose `A` after step 5). Probe and draft every group of both passes exactly as in `standards-interview.md` (lists, evidence, the not-offered line, Recommended), but do not ask per group: take each group's Recommended line, run no loop for the user's own conventions or checks, and do not ask `CONSTRAINTS.md` (default: no).

## The one read-back

Then send **one read-back** as its own reply, written as a **checklist with the Recommended items already ticked**:
- one line per item, `☑` for an item that will be written or kept and `☐` for one that will not (switched off, not offered, or drafted but not recommended), each with its ID, a few words on what it is and the reason in a few words.
- Not-offered items get their own `☐` lines too, with the command and count as the reason, so that every ID the user may tick is on the list.
- Group it by kit file, then the drafted repo rules (with trigger, severity and file), the review-only checks and the Do-not-flag lines, each with the file it goes to, so that no file is chosen after the approval; end with "`CONSTRAINTS.md`: not created (a detailed run asks for it)".

## The question

Ask once:
- `A` write as ticked (Recommended);
- `B` change the ticks with forms;
- `C` go through it group by group (switch to detailed);
- `D` stop without writing;
- Other: changes as `+ID` to tick and `-ID` to untick (for example `-S5 +S1`), or new items in your own words.

IDs are unique only within a file, so where an ID appears in more than one file of the checklist (repo checks are often all `V1`), print the file on those lines and take the change as `file#ID` (`-ops/environment#V1`), the form `standards.disable` uses; ask back when a bare ID matches more than one line.

## `B`: tick forms

For `B`, ask one multiple-choice question per kit file, then one for the repo rules and checks, listing every item of that group with what a tick does at the start of the label, as a colored icon and a word:
- `🔴 Remove · S4 secrets out of source and builds` for an item that is on, `🟢 Add · S1 server-side record access` for one that is off (the word in the user's language), not ☑/☐, because the form draws its own checkboxes; the icon shows the effect of a tick at a glance, the word keeps it readable where color is not shown or not seen;
- an item whose ID repeats in another file shows its file;
- after every item comes a `Keep this group as shown` option, marked Recommended (first instead where the choice tool asks for the recommended option first, as agy's does), because a form sent with nothing ticked is not a clear answer (omp's RPC clients show a Done row only after a tick) and omp picks the Recommended option when a question times out, so a timeout changes nothing.

The question says: "Tick what you want to change: 🔴 removes an item that is on, 🟢 adds one that is off; to change nothing, tick only Keep this group as shown." A tick means the action on its label, not the final state, because the CLIs' choice tools cannot pre-tick options; without a multiple-choice tool, ask for `+ID`/`-ID` as text instead. A new item in the user's words is confirmed like any user-added item.

## After a change

- After any change, write a reply that lists the lines whose mark changed, one checklist line each with its new mark, ID, a few words and the file (`☐ C5 map every value across layers (coding/review-basics)`), and nothing else: not a sentence such as "C5 goes from on to off", not a note in the question text, not unchanged items; then ask `A` write / Other once more.
- Write only after `A`.
- The approved checklist is the whole quick run: a gap noticed after it (while writing or rereading) is not asked as a new item but noted in `init-report.md` for a detailed run, because quick setup promises one read-back (in one run the agent asked for a new color check after writing).

## Report

In `init-report.md`, record that quick setup was used, the Recommended lines taken and every mark the user changed.
