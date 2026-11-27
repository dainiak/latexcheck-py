from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional

from .helpers import SupportedLanguages


@dataclass(frozen=True)
class MathRule:
    prefix: str
    suffix: str
    mode: str = "inline"
    line_prefix: Optional[str] = None
    infer_line_prefix: bool = False


@dataclass(frozen=True)
class MathSpan:
    start: int
    end: int
    body_start: int
    body_end: int
    mode: str
    line_prefix: Optional[str] = None


@dataclass
class EmbeddedFormat:
    name: str
    rules: List[MathRule]
    extensions: List[str] = field(default_factory=list)


BUILTIN_FORMATS: Dict[str, EmbeddedFormat] = {
    "markdown": EmbeddedFormat(
        name="markdown",
        rules=[MathRule("$$", "$$", "display"), MathRule("$", "$", "inline")],
    ),
    "doxygen": EmbeddedFormat(
        name="doxygen",
        rules=[
            MathRule(r"\f[", r"\f]", "display", infer_line_prefix=True),
            MathRule(r"\f$", r"\f$", "inline", infer_line_prefix=True),
        ],
    ),
}


def _normalize_mode(mode: str) -> str:
    if mode in ("inline", "math-inline"):
        return "inline"
    if mode in ("display", "math-display"):
        return "display"
    raise ValueError(f"unknown math mode: {mode!r}")


def _parse_rule(raw) -> MathRule:
    if not isinstance(raw, dict):
        raise ValueError("each rule must be an object")
    prefix = raw.get("prefix")
    suffix = raw.get("suffix")
    if not isinstance(prefix, str) or not prefix:
        raise ValueError("rule prefix must be a non-empty string")
    if not isinstance(suffix, str) or not suffix:
        raise ValueError("rule suffix must be a non-empty string")
    line_prefix = raw.get("line_prefix")
    if line_prefix is not None and not isinstance(line_prefix, str):
        raise ValueError("rule line_prefix must be a string")
    infer_line_prefix = raw.get("infer_line_prefix", False)
    if not isinstance(infer_line_prefix, bool):
        raise ValueError("rule infer_line_prefix must be a boolean")
    return MathRule(
        prefix=prefix,
        suffix=suffix,
        mode=_normalize_mode(raw.get("mode", "inline")),
        line_prefix=line_prefix or None,
        infer_line_prefix=infer_line_prefix,
    )


def load_formats(path: str) -> Dict[str, EmbeddedFormat]:
    with open(path, mode="r", encoding="utf-8") as infile:
        data = json.load(infile)
    if isinstance(data, dict):
        raw_formats = data.get("formats", [])
    elif isinstance(data, list):
        raw_formats = data
    else:
        raise ValueError("config must be a JSON object or array")

    formats: Dict[str, EmbeddedFormat] = {}
    for raw in raw_formats:
        if not isinstance(raw, dict):
            raise ValueError("each format must be an object")
        name = raw.get("name")
        if not isinstance(name, str) or not name:
            raise ValueError("each format needs a non-empty name")
        if name in BUILTIN_FORMATS or name == "tex":
            raise ValueError(f"format name {name!r} is reserved")
        raw_rules = raw.get("rules")
        if not isinstance(raw_rules, list) or not raw_rules:
            raise ValueError(f"format {name!r} needs a non-empty rules list")
        extensions = raw.get("extensions", [])
        if not isinstance(extensions, list) or not all(isinstance(ext, str) and ext for ext in extensions):
            raise ValueError(f"format {name!r} extensions must be strings")
        formats[name] = EmbeddedFormat(
            name=name,
            rules=[_parse_rule(rule) for rule in raw_rules],
            extensions=list(extensions),
        )
    return formats


def resolve_rules(filename: str, format_name: Optional[str], config_formats: Dict[str, EmbeddedFormat]):
    if format_name:
        if format_name == "tex":
            return None
        if format_name in BUILTIN_FORMATS:
            return BUILTIN_FORMATS[format_name].rules
        if format_name in config_formats:
            return config_formats[format_name].rules
        raise ValueError(f"unknown format: {format_name!r}")

    for fmt in config_formats.values():
        for extension in fmt.extensions:
            if filename.lower().endswith(extension.lower()):
                return fmt.rules
    return None


def extract_math(source: str, rules: Iterable[MathRule]) -> List[MathSpan]:
    candidates: List[MathSpan] = []
    for rule in rules:
        cursor = 0
        while True:
            start = source.find(rule.prefix, cursor)
            if start < 0:
                break
            body_start = start + len(rule.prefix)
            body_end = source.find(rule.suffix, body_start)
            if body_end < 0:
                break
            if source[body_start:body_end].strip():
                line_prefix = rule.line_prefix
                if line_prefix is None and rule.infer_line_prefix:
                    line_start = source.rfind("\n", 0, start) + 1
                    before = source[line_start:start]
                    match = re.match(r"[ \t]*(/\*\*|/\*!|\*|///|//!|//)[ \t]*", before)
                    if match:
                        marker = "*" if match.group(1) in ("/**", "/*!") else match.group(1)
                        line_prefix = r"^[ \t]*" + re.escape(marker) + r"[ \t]*"
                candidates.append(
                    MathSpan(
                        start,
                        body_end + len(rule.suffix),
                        body_start,
                        body_end,
                        rule.mode,
                        line_prefix,
                    )
                )
            cursor = start + 1

    candidates.sort(key=lambda span: (span.start, -(span.end - span.start)))
    spans: List[MathSpan] = []
    last_end = -1
    for span in candidates:
        if span.start >= last_end:
            spans.append(span)
            last_end = span.end
    return spans


def _strip_line_prefixes(body: str, base: int, pattern: Optional[str]):
    if not pattern:
        return body, None
    regex = re.compile(pattern)
    chars = []
    offsets = []
    for lineno, line in enumerate(body.splitlines(keepends=True)):
        start = 0
        if lineno:
            match = regex.match(line)
            if match:
                start = match.end()
        for index in range(start, len(line)):
            chars.append(line[index])
            offsets.append(base + index)
    return "".join(chars), offsets


def _map_position(position: int, span: MathSpan, wrapper_length: int, body_offsets=None) -> int:
    if position < wrapper_length:
        mapped = span.start + position
    else:
        body_index = position - wrapper_length
        if body_offsets is not None:
            if body_index < len(body_offsets):
                return body_offsets[body_index]
            return span.body_end
        mapped = span.body_start + body_index
    return max(span.start, min(mapped, span.end))


def perform_checks_embedded(
    source: str,
    rules: Iterable[MathRule],
    language: SupportedLanguages = SupportedLanguages.EN,
):
    from . import perform_checks

    errors: Dict[str, List[int]] = {}
    for span in extract_math(source, rules):
        body, body_offsets = _strip_line_prefixes(
            source[span.body_start : span.body_end], span.body_start, span.line_prefix
        )
        if span.mode == "display":
            fragment = "\\[" + body + "\\]"
            wrapper_length = 2
        else:
            fragment = "$" + body + "$"
            wrapper_length = 1

        try:
            fragment_errors = perform_checks(fragment, language=language)
        except Exception:
            fragment_errors = {"PARSE_ERROR": [0]}

        for code, positions in fragment_errors.items():
            bucket = errors.setdefault(code, [])
            if not positions:
                if code == "PARSE_ERROR":
                    bucket.append(span.start)
                continue
            for position in positions:
                bucket.append(_map_position(position, span, wrapper_length, body_offsets))

    for code, positions in errors.items():
        errors[code] = list(dict.fromkeys(sorted(positions)))
    return errors
