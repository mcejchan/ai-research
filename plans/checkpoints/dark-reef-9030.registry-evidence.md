# Registry Evidence: dark-reef-9030

## Delivered External Change

The `ai-research` registry change is stored outside this repository in
`/Users/michal/.openclaw/workspace`, commit
`169c092c98bd008af96d0835874cac6208149f69`.

Command used to inspect the scoped committed change:

```sh
git show --format= --no-ext-diff 169c092c98 -- skills/opencode-dev/projects.yaml
```

Exact scoped diff:

```diff
diff --git a/workspace/skills/opencode-dev/projects.yaml b/workspace/skills/opencode-dev/projects.yaml
index 7156ea77c0..6829d9ec4b 100644
--- a/workspace/skills/opencode-dev/projects.yaml
+++ b/workspace/skills/opencode-dev/projects.yaml
@@ -173,7 +173,7 @@ projects:
       outputDir: .architecture-reviews
     branchPolicy: main
     post_impl: ''
-    testCommand: cd ~/Projects/ai-research/youtube-transcript-pipeline && pytest
+    testCommand: cd ~/Projects/ai-research && make test
     description: AI research — knowledge base, YouTube transcript pipeline, helper
       scripts
     deploy:
```

Current delivered entry:

```yaml
  ai-research:
    dir: ~/Projects/ai-research
    testCommand: cd ~/Projects/ai-research && make test
```

## TDD Provenance

No new RED was created for this already-delivered configuration change.
`plans/checkpoints/bold-dune-3929.red-green-proof.md` contains the historical
genuine RED/GREEN for the root test gate. The generated lineage artifact
`plans/checkpoints/dark-vale-6236.evidence.md` reports the parent RED and GREEN,
and records `command_lines_truncated` as an evidence gap.

## Fresh GREEN Verification

- `make test` from `/Users/michal/Projects/ai-research` -> exit 0; quiz 2
  passed, viewer 1 passed, pipeline 41 passed.
- Parsed `skills/opencode-dev/projects.yaml` with `yaml.safe_load` and asserted
  `projects.ai-research.testCommand == "cd ~/Projects/ai-research && make test"`
  -> exit 0; printed the expected command.
- `git diff --check -- skills/opencode-dev/projects.yaml` and
  `git show --check --oneline 169c092c98 -- skills/opencode-dev/projects.yaml`
  from `/Users/michal/.openclaw/workspace` -> exit 0.
- `git diff --check` for the task checkpoint and evidence artifacts -> exit 0.
