# 4. Sharing your processor

A processor in a `SharedProcessors/` directory can be used by recipes in *any*
repo, not just your own. Three things make that work.

## 1. Filename must match the class name

When a recipe references a processor like:

```
com.github.jgstew.macadmins2026.SharedProcessors/FileHasher
```

AutoPkg imports a module named `FileHasher` and looks for a class named
`FileHasher` inside it. So the rules are:

- the **file** is `FileHasher.py`
- the **class** is `class FileHasher(Processor)`
- the name after the `/` is `FileHasher`

All three must match. This is why the workshop exercise files are named after
their class (`HelloWorld.py`, not `01_HelloWorld.py`) — the lesson numbering
lives in this guide instead of in the filenames.

## 2. The namespace before the `/` is a recipe identifier

The part before the slash —
`com.github.jgstew.macadmins2026.SharedProcessors` — is the **Identifier of a
recipe**. This repo ships a tiny "dummy" recipe whose only job is to claim that
identifier and point at this folder:
[`SharedProcessors/macadmins2026-SharedProcessors.recipe`](../SharedProcessors/macadmins2026-SharedProcessors.recipe).

```xml
<key>Identifier</key>
<string>com.github.jgstew.macadmins2026.SharedProcessors</string>
<key>Process</key>
<array/>   <!-- empty: it runs nothing -->
```

When AutoPkg sees `<that identifier>/FileHasher`, it finds this dummy recipe,
then loads `FileHasher.py` from the same directory. (The same trick is used by
[`jgstew-recipes`](https://github.com/jgstew/jgstew-recipes/blob/main/SharedProcessors/jgstew-SharedProcessors.recipe)
and many other repos.)

> During the workshop you don't even need the dummy recipe — passing
> `--search-dir SharedProcessors` to `autopkg run` lets it find the processors
> directly. The dummy recipe is what makes the namespace work once the repo is
> *shared* and discovered by identifier.

## 3. `MinimumVersion`

Every recipe declares the minimum AutoPkg version it needs:

```yaml
MinimumVersion: "2.3"
```

YAML recipes require AutoPkg **2.3+**. Bump this if you use a processor or
feature that needs something newer.

## Putting it on someone else's machine

Once the work is committed and pushed, anyone can use your processors:

```bash
autopkg repo-add https://github.com/jgstew/macadmins2026-recipes.git
autopkg run -vv com.github.jgstew.macadmins2026.test.FileHasher
```

Their recipes can now reference
`com.github.jgstew.macadmins2026.SharedProcessors/FileHasher` from anywhere.

## Going further

These four lessons stop at the standard library. Real-world processors in
[`jgstew-recipes`](https://github.com/jgstew/jgstew-recipes/tree/main/SharedProcessors)
show the next steps:

- **Subclassing an existing processor** — `URLDownloaderPython` extends
  AutoPkg's `URLDownloader` instead of `Processor`, reusing its helpers.
- **Sharing code between processors** — `SharedUtilityMethods` is a base class
  (and module of helper functions like `find_executable`) that other processors
  import and build on.
- **Third-party dependencies** — processors that need pip packages list them in
  `requirements.txt` (e.g. `certifi`, `Pillow`, `pefile`).
- **`summary_result`** — set a `*_summary_result` output to get a nice summary
  table at the end of an `autopkg run`.

You now know everything in `HelloWorld` — and the path from there to anything in
that repo is just more of the same three beats: **read → work → write**.
