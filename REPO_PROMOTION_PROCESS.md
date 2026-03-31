# Avida-ED-Test3 Promotion Process

This document is the step-by-step process for turning the local `Avida-ED-Test3`
checkout into its own GitHub repository and for recording follow-up actions as
the work continues.

Use this as the working checklist. Update it as each step is completed.

## Current situation

- This checkout began as a local copy of `Avida-ED-Test2`.
- The local git history still descends from `Avida-ED-Test2`.
- The local branch is `main`.
- The local remote named `origin` originally pointed to `Avida-ED-Test2`.
- The correct long-term destination is a separate GitHub repository named
  `Avida-ED-Test3`.

## Goal

Make this repository push to `Avida-ED-Test3` on GitHub without affecting
`Avida-ED-Test2`, then continue normal development in the new repo.

## One-time promotion steps

### 1. Create the new GitHub repository

A person must:

1. Create a new empty repository on GitHub named `Avida-ED-Test3` under the
   `Avida-ED` organization.
2. Do not initialize it with a README, `.gitignore`, or license if you want the
   first push from this local repo to define the contents cleanly.

Record here when done:

- Date: completed before 2026-03-29
- Who created it: user
- GitHub URL: `https://github.com/Avida-ED/Avida-ED-Test3`

### 2. Confirm the local checkout is the correct one

From the `Avida-ED-Test3` directory, verify:

```bash
git rev-parse --show-toplevel
git branch --show-current
git remote -v
```

Expected result before remote changes:

- top-level path is the `Avida-ED-Test3` directory
- current branch is `main`
- `origin` still points at `Avida-ED-Test2.git`

Record here when checked:

- Date: completed before initial promotion push
- Who checked it: user

### 3. Rename the old remote so it is not used by accident

Run:

```bash
git remote rename origin test2
```

This preserves the old remote reference but prevents `git push` from going to
`Avida-ED-Test2` by default.

Record here when done:

- Date: completed before initial promotion push
- Who renamed it: user

### 4. Add the new GitHub repo as `origin`

Run:

```bash
git remote add origin https://github.com/Avida-ED/Avida-ED-Test3.git
```

If SSH is preferred, use the SSH URL instead.

Record here when done:

- Date: completed before initial promotion push
- Who added it: user
- URL used: `https://github.com/Avida-ED/Avida-ED-Test3.git`

### 5. Verify remotes before pushing

Run:

```bash
git remote -v
```

Expected result:

- `origin` -> `Avida-ED-Test3.git`
- `test2` -> `Avida-ED-Test2.git`

Do not push until this is correct.

Record verification:

- Date: completed before initial promotion push
- Who verified it: user

### 6. Push the branch to the new repo

Run:

```bash
git push -u origin main
```

This establishes the new upstream branch and makes future `git push` commands
target `Avida-ED-Test3`.

Record here when done:

- Date: completed before 2026-03-29
- Who pushed it: user
- Result: initial push to `Avida-ED-Test3` completed

### 7. Enable GitHub Pages in the new repo

A person must do this in GitHub repository settings:

1. Open `Settings`
2. Open `Pages`
3. Set the source to `GitHub Actions`

This repo already includes a Pages workflow in `.github/workflows/deploy.yml`.

Record here when done:

- Date: completed before 2026-03-29
- Who configured Pages: user

### 8. Confirm the first Actions deployment succeeds

A person must:

1. Open the `Actions` tab in the new repo
2. Confirm the `Deploy to GitHub Pages` workflow runs on the pushed `main`
3. Confirm the Pages deployment finishes successfully
4. Confirm the site loads at the expected URL

Expected site URL:

- `https://avida-ed.github.io/Avida-ED-Test3/`

Record here when done:

- Date: completed before 2026-03-29
- Who checked it: user
- Result: site loads at `https://avida-ed.github.io/Avida-ED-Test3/`

## Follow-up cleanup after promotion

### 9. Decide whether to keep the old remote

If keeping the old remote is useful for comparison, leave `test2` in place.

If not needed, remove it:

```bash
git remote remove test2
```

Record decision:

- Keep `test2` remote: yes/no
- Date:
- Who decided:

### 10. Clean the working tree

Before future commits, decide what to do with the remaining local-only changes,
especially:

- generated `.docusaurus/` changes
- old deleted `docs/curriculum/...` paths if they are meant to be removed in git
- any root-level files that remain modified but were not part of the committed
  content migration

Recommended checks:

```bash
git status --short
git diff --stat
```

Record cleanup status:

- Date:
- Who checked:
- Notes:

## Repo settings and code settings already aligned

The following are already correct for `Avida-ED-Test3` and do not need to be
changed just for promotion:

- `docusaurus.config.js`
  `baseUrl` is `/Avida-ED-Test3/`
- `.github/workflows/deploy.yml`
  uses the standard GitHub Pages Actions flow

## Ongoing process notes

Add new notes here as work continues.

### Template for future entries

- Date:
- Person:
- What was done:
- What remains:
- Any blocker:

### Entries

- Date: 2026-03-29
  Person: Codex + user
  What was done: repo promotion completed and GitHub Pages is live; color-mode switch removed; landing page revised toward the intended Test3 presentation; navbar and route cleanup completed.
  What remains: continue normal site/content work in the promoted repo.
  Any blocker: none at the promotion level.

- Date: 2026-03-29
  Person: Codex
  What was done: instructor curriculum moved into `src/pages/curriculum/`, with a reduced docs-rendering comparison example left under `docs/instructors/`; a sticky in-page subnav prototype with breadcrumb and corrected anchor offsets was added to the curriculum landing page.
  What remains: decide whether to extend the page-level subnav pattern to other long pages.
  Any blocker: none.

- Date: 2026-03-29
  Person: Codex
  What was done: transcript tooling and process docs were added; transcript-first video support was built out; archive/news image paths were reconciled with local `static/img/about/` assets; section-based `static/img/` folders were created.
  What remains: continue transcript publication and decide how many remaining legacy video items should become transcript-first support pages.
  Any blocker: some source media is still not present locally.

- Date: 2026-03-29
  Person: Codex
  What was done: multiple learner/instructor-focused migration units were completed from the scraped legacy site:
  What remains: continue with lower-priority archive and background cleanup as needed.
  Any blocker: none.
  - student support and tutorial guidance
  - instructor FAQ and start guidance
  - curriculum framing refinements
  - legacy offline fallback guidance
  - about/archive context refinements
