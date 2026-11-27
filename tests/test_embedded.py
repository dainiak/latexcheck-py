import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from latexcheck import filter_errors, parse_excludes, perform_checks
from latexcheck.embedded import (
    BUILTIN_FORMATS,
    extract_math,
    load_formats,
    perform_checks_embedded,
    resolve_rules,
)


class EmbeddedMathTests(unittest.TestCase):
    def test_extracts_doxygen_delimiters(self):
        source = r"a \f$x\f$ b \f[V \leftarrow max(R,G,B)\f] c"
        spans = extract_math(source, BUILTIN_FORMATS["doxygen"].rules)
        self.assertEqual([span.mode for span in spans], ["inline", "display"])
        self.assertEqual(source[spans[0].body_start : spans[0].body_end], "x")
        self.assertIn("max(R,G,B)", source[spans[1].body_start : spans[1].body_end])

    def test_doxygen_comment_prefix_is_not_multiplication(self):
        rules = BUILTIN_FORMATS["doxygen"].rules
        source = "* " + r"\f[" + "\n * x = y\n * " + r"\f]" + "\n"
        errors = perform_checks_embedded(source, rules)
        self.assertNotIn("MULTIPLICATION_SIGN", errors)

        source = "* " + r"\f[" + "\n * x = y * z\n * " + r"\f]" + "\n"
        errors = perform_checks_embedded(source, rules)
        self.assertEqual(len(errors.get("MULTIPLICATION_SIGN", [])), 1)

    def test_display_wins_over_inline(self):
        spans = extract_math("$$x$$", BUILTIN_FORMATS["markdown"].rules)
        self.assertEqual(len(spans), 1)
        self.assertEqual(spans[0].mode, "display")
        self.assertEqual(spans[0].body_start, 2)
        self.assertEqual(spans[0].body_end, 3)

    def test_positions_stay_in_source(self):
        source = r"prefix \f$delta\f$ suffix"
        errors = perform_checks_embedded(source, BUILTIN_FORMATS["doxygen"].rules)
        self.assertIn("TEXT_IN_MATH_MODE", errors)
        for positions in errors.values():
            for position in positions:
                self.assertGreaterEqual(position, 0)
                self.assertLessEqual(position, len(source))

    def test_fork_with_frac_does_not_crash(self):
        formula = r"S \leftarrow \fork{\frac{V-min(R,G,B)}{V}}{if \(V \neq 0\)}{0}{otherwise}"
        source = r"\f[" + formula + r"\f]"
        errors = perform_checks_embedded(source, BUILTIN_FORMATS["doxygen"].rules)
        self.assertIsInstance(errors, dict)
        perform_checks(r"\[ " + formula + r" \]")

    def test_exclude_codes(self):
        self.assertEqual(
            parse_excludes(["MULTIPLICATION_SIGN,TEXT_IN_MATH_MODE", " foo "]),
            {"MULTIPLICATION_SIGN", "TEXT_IN_MATH_MODE", "FOO"},
        )
        errors = {"MULTIPLICATION_SIGN": [1], "BACKSLASH_NEEDED": [2]}
        self.assertEqual(filter_errors(errors, {"MULTIPLICATION_SIGN"}), {"BACKSLASH_NEEDED": [2]})
        self.assertEqual(filter_errors(errors, set()), errors)

    def test_config_auto_selects_by_extension(self):
        config = {
            "formats": [
                {
                    "name": "custom",
                    "extensions": [".md"],
                    "rules": [{"prefix": "%%", "suffix": "%%", "mode": "math-display"}],
                }
            ]
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "formats.json")
            with open(path, "w", encoding="utf-8") as f:
                json.dump(config, f)
            formats = load_formats(path)
        self.assertEqual(resolve_rules("doc.md", None, formats)[0].mode, "display")
        self.assertIsNone(resolve_rules("doc.txt", None, formats))
        self.assertIsNone(resolve_rules("doc.md", "tex", formats))
        with self.assertRaises(ValueError):
            resolve_rules("doc.md", "missing", formats)


if __name__ == "__main__":
    unittest.main()
