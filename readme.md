# Esteemer

Evaluate acceptable candidates for promotion to figure generation.

## Use

```bash
cat spek.json | bin/esteemer.sh
```

## Default Esteemer Criteria
Provides a passthrough for all acceptable candidates.
Any candidate that is `acceptable_by` is annoted as `promoted_by http://example.com/slowmo#esteemer_default_criteria`
