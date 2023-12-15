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

Help:
```bash
latexcheck --help
```
