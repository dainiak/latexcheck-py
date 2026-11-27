# LaTeXcheck — a linter for LaTeX documents

This is a console script version of a similarly designed [online LaTeX linter](https://www.dainiak.com/latexcheck/). The kind of errors that the program checks for are in the vein of [ChkTeX](https://ctan.org/pkg/chktex).

It is assumed that syntactic errors that lead to $\LaTeX$ compilation failures (like unbalanced parentheses) have been eliminated prior to running the tool.

Please note that the checker’s output may easily contain false positives. This is unlikely to be possible to completely eliminate due to $\LaTeX$ complexity and flexibility.

Installation:
```bash
pip install latexcheck
```

Usage:
```bash
latexcheck somefile.tex
```

TeX math is often embedded in Markdown or other markup instead of living in a standalone `.tex` file. Use `--format` to lint the formulas in place:

```bash
latexcheck --format doxygen doc.md
```

Built-in formats:
- `tex` (default): the whole file is LaTeX.
- `markdown`: `$...$` and `$$...$$`.
- `doxygen`: `\f$...\f$` and `\f[...\f]` (used by OpenCV's docs).

Doxygen rules set `infer_line_prefix`: the comment marker before the opening delimiter (`*`, `///`, or `//!`) is reused for continuation lines. A rule may also set `line_prefix` to an explicit regex.

For other delimiters, pass a JSON config. A format with `extensions` is selected automatically when `--format` is omitted:

```json
{
  "formats": [
    {
      "name": "opencv",
      "extensions": [".md"],
      "rules": [
        {"prefix": "\\f$", "suffix": "\\f$", "mode": "inline"},
        {"prefix": "\\f[", "suffix": "\\f]", "mode": "display"}
      ]
    }
  ]
}
```

```bash
latexcheck --config formats.json doc.md
```

To silence a check that does not apply, use `--exclude` (repeatable, comma-separated):

```bash
latexcheck --exclude MULTIPLICATION_SIGN doc.md
```

Help:
```bash
latexcheck --help
```
