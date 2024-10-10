from __future__ import annotations

import argparse
import os
import re
import textwrap
from dataclasses import dataclass
from enum import Enum
from typing import List

import TexSoup

from .helpers import SupportedLanguages, error_descriptions


class LatCat(Enum):
    STR = 0
    ENV = 1
    CMD = 2
    BRACES = 3
    BRACKETS = 4


@dataclass
class Treenode:
    cat: LatCat = LatCat.STR
    token: str = None
    args: List[Treenode] = None
    children: List[Treenode] = None
    prev_sibling: Treenode = None
    next_sibling: Treenode = None
    prev_node: Treenode = None
    next_node: Treenode = None
    parent: Treenode = None
    is_in_math: bool = False
    is_in_display_math: bool = False
    is_in_arg: bool = False
    pos: int = None
    tex: str = None


AGG_STRINGS = True


def is_command_with_no_text_semantics(node: Treenode):
    if node is None:
        return False
    return node.cat == LatCat.CMD and node.token in ["label", "ref", "eqref", "tag"]


def is_display_math(x):
    if x is None:
        return False
    display_envs = [
        "$$",
        "align",
        "align*",
        "eqnarray",
        "eqnarray*",
        "equation",
        "equation*",
        "gather",
        "gather*",
        "multline",
        "multline*",
        "displaymath",
        "flalign",
        "flalign*",
        "alignat",
        "alignat*",
    ]
    if isinstance(x, Treenode):
        return (x.cat == LatCat.ENV) and (x.token in display_envs)
    return x in display_envs


def is_numbered_display_math(x):
    if x is None:
        return False
    numbered_display_envs = ["align", "eqnarray", "equation", "gather", "multline", "flalign", "alignat"]
    if isinstance(x, Treenode):
        return (x.cat == LatCat.ENV) and (x.token in numbered_display_envs)
    return x in numbered_display_envs


def is_math(x):
    if x is None:
        return False
    if isinstance(x, Treenode):
        return (x.token == "math") or is_display_math(x.token)
    return (x == "math") or is_display_math(x)


def initiates_text_mode(x):
    if x is None:
        return False
    text_envs = ["mbox", "hbox", "text", "textnormal", "textrm", "textit", "textsf", "texttt"]
    if isinstance(x, Treenode):
        return x.token in text_envs
    return x in text_envs


def has_descendant(node, predicate, recursive_call=False):
    if node is None:
        return False
    if predicate(node) and recursive_call:
        return True
    for nodelist in [node.args, node.children]:
        if nodelist is not None:
            for child in nodelist:
                if has_descendant(child, predicate, recursive_call=True):
                    return True
    return False


def has_child(node, predicate):
    if node is None:
        return False
    for nodelist in [node.args, node.children]:
        if nodelist is not None:
            for child in nodelist:
                if predicate(child):
                    return True
    return False


def has_sibling(node, predicate):
    if node is None or node.parent is None:
        return False
    return has_child(node.parent, (lambda x: x is not node and predicate(x)))


def is_pure_argument(node):
    while node.parent and node.parent.cat in [LatCat.BRACES, LatCat.BRACKETS]:
        node = node.parent
    return is_command_with_no_text_semantics(node)


def traverse_tex(tex, parent_node_list=None, depth=0):
    global AGG_STRINGS
    no_parent = False
    if parent_node_list is None:
        parent_node_list = []
        no_parent = True
    if isinstance(tex, str):
        if tex.startswith("%"):
            return
        if AGG_STRINGS and len(parent_node_list) > 0 and parent_node_list[-1].cat == LatCat.STR:
            parent_node_list[-1].token += tex
        else:
            parent_node_list.append(Treenode(cat=LatCat.STR, token=tex))
        return

    new_node = Treenode(pos=tex.position, tex=str(tex))

    s = str(tex)

    if s.startswith(rf"\begin{{{tex.name}}}") or tex.name == "$$":
        new_node.cat = LatCat.ENV
        new_node.token = str(tex.name)
    elif tex.name == "$" or tex.name == "math":
        new_node.cat = LatCat.ENV
        new_node.token = "math"
    elif tex.name == "displaymath":
        new_node.cat = LatCat.ENV
        new_node.token = "displaymath"
    elif tex.name == "[tex]":
        new_node.cat = LatCat.ENV
        new_node.token = "document"
    elif s.startswith("{"):
        new_node.cat = LatCat.BRACES
    elif s.startswith("["):
        new_node.cat = LatCat.BRACKETS
    else:
        new_node.cat = LatCat.CMD
        new_node.token = str(tex.name)

    if tex.args:
        new_node.args = []
        for t in tex.args:
            traverse_tex(t, new_node.args, depth + 1)

    new_node.children = None
    if not is_command_with_no_text_semantics(new_node):
        new_node.children = []
        for t in tex.contents:
            traverse_tex(t, new_node.children, depth + 1)
        if new_node.args and not AGG_STRINGS:
            n_arg_tokens = sum(len(node.children) for node in new_node.args)
            new_node.children = new_node.children[n_arg_tokens:]

    for nodelist in [new_node.args, new_node.children]:
        if nodelist is None:
            continue
        prev_sibling = None
        for child in nodelist:
            if prev_sibling:
                prev_sibling.next_sibling = child
            child.prev_sibling = prev_sibling
            child.parent = new_node
            prev_sibling = child

    parent_node_list.append(new_node)
    if no_parent:
        return new_node


def fill_node_links(root_node):
    all_nodes = list()

    def recursive_fill_all_nodes_list(node, math_mode=0, in_args=False):
        nonlocal all_nodes
        if in_args:
            node.is_in_arg = True
        if math_mode:
            node.is_in_math = True
        if math_mode == 2:
            node.is_in_display_math = True
        if is_math(node) or node.is_in_math and not initiates_text_mode(node):
            math_mode = 1
        elif (node.is_in_display_math or is_display_math(node)) and not initiates_text_mode(node):
            math_mode = 2
        all_nodes.append(node)
        for nodelist in [node.args, node.children]:
            if nodelist is not None:
                for child in nodelist:
                    recursive_fill_all_nodes_list(
                        child, math_mode, in_args or (nodelist is node.args) and is_command_with_no_text_semantics(node)
                    )

    recursive_fill_all_nodes_list(root_node)
    for i in range(1, len(all_nodes)):
        all_nodes[i].prev_node = all_nodes[i - 1]
        all_nodes[i - 1].next_node = all_nodes[i]
    return all_nodes


def find_prev(node, condition):
    while node is not None:
        node = node.prev_node
        if (node is not None) and condition(node):
            return node


def find_next(node, condition):
    while node is not None:
        node = node.next_node
        if (node is not None) and condition(node):
            return node


def find_child(node, condition):
    if node is None:
        return None
    for nodelist in [node.args, node.children]:
        if nodelist is not None:
            for child in nodelist:
                if condition(child):
                    return child
    return None


def find_descendant(node, condition):
    if node is None:
        return None
    if condition(node):
        return node
    for nodelist in [node.args, node.children]:
        if nodelist is not None:
            for child in nodelist:
                d = find_descendant(child, condition)
                if d is not None:
                    return d
    return None


def tree_to_str(node, depth=0):
    s = ""
    s += f"{'  ' * depth} {node.cat} {repr(node.token or '')}\n"
    for nodelist in [node.args, node.children]:
        if nodelist is not None and nodelist != []:
            if nodelist is node.args:
                s += f"{'  ' * depth} ARGS:\n"
            else:
                s += f"{'  ' * depth} CHILDREN:\n"
            for child in nodelist:
                s += tree_to_str(child, depth + 1)
    return s


def perform_checks(source: str, language: SupportedLanguages = SupportedLanguages.EN, debug_mode=False):
    errors = {}

    def add_error(err_code, bad_node=None):
        nonlocal errors
        if err_code not in error_descriptions[language]:
            return
        pos = None
        if isinstance(bad_node, int):
            pos = bad_node
        elif isinstance(bad_node, Treenode):
            pos = 0
            while bad_node is not None and bad_node.pos is None:
                bad_node = bad_node.prev_node
            if bad_node and bad_node.pos and bad_node.pos:
                pos = bad_node.pos

        if err_code not in errors:
            errors[err_code] = []
        if pos is not None:
            errors[err_code].append(pos)

    try:
        soup = TexSoup.TexSoup(source)
    except Exception as e:
        e = str(e)
        offset = re.search(r"\[Line:? \d+, Offset:? (\d+)]", e)
        if offset:
            offset = int(offset.group(1))
        add_error("PARSE_ERROR", offset)
        return errors

    try:
        latex_tree = traverse_tex(soup)
        all_nodes = fill_node_links(latex_tree)
    except Exception as _:
        add_error("PARSE_ERROR", None)
        return errors

    if debug_mode:
        print(tree_to_str(latex_tree))

    node = find_descendant(latex_tree, lambda n: n.token == "$$")
    if node is not None:
        add_error("DOUBLE_DOLLARS", node.pos)

    re_td = re.compile(r"т\. ?(д\.|н\.|ч\.|к\.)", re.IGNORECASE)
    re_dash_no_spaces = re.compile(r"--([^- ~\n]|$)|(^|[^- ~\n])--")
    re_dash_as_hyphen = re.compile(r"(^|\s)-\s+|\s+-(\s|$)")
    re_multiplication_star = re.compile(r"[^_^]\*|.\*")
    re_space_before_punctuation = re.compile(r"\s+[?!.,;:]")
    re_space_after_punctuation = re.compile(r"[?!.,;:][^ ~\t\n\\]")
    re_space_before_parenthesis = re.compile(r"[^()\[\]{}\n\t-/+]\(")
    re_space_after_parenthesis = re.compile(r"\(\s")
    re_cyrillic_tricky_letter = re.compile(r"[уехаос]")
    re_latin_c_in_rus_text = re.compile(r"[а-яё]\s*c|c\s*[а-яё]", re.IGNORECASE)
    re_math_command = re.compile(r"(\\(infty|cdot|sum))|([0-9 \n]+ *[=+*^])|([+*^] *[0-9 \n]+)")
    re_latin_letter_outside_math_ru = re.compile(r" (^|[, .~])[a-zA-Z]($|[,.:!? ~-]) ")
    re_latin_letter_outside_math_en = re.compile(r" (^|[, .~])[b-zA-HJ-Z]($|[,.:!? ~-]) ")
    re_capitalization_after_comma = re.compile(r"[,;:]\s*[А-ЯЁA-Z]")
    re_capitalization_after_period = re.compile(r"\.\s*[а-яёa-z]")
    re_starts_with_lowercase = re.compile(r"^\s*[а-яёa-z].*", re.DOTALL)
    re_starts_with_uppercase = re.compile(r"^\s*[А-ЯЁA-Z].*", re.DOTALL)
    re_ends_with_space = re.compile(r".*[ \n\t]$", re.DOTALL)
    re_starts_with_cyrillic = re.compile(r"^[а-яё]", re.IGNORECASE)
    re_ends_with_digit_or_letter = re.compile(r".*[0-9a-z]\s*$", re.IGNORECASE | re.DOTALL)
    re_possibly_word = re.compile(r"([^a-z\\]|^)([a-z]{4,}|bad|[a-z]{2,3}\.)", re.IGNORECASE)
    re_multiple_spaces = re.compile(r"(~|\\:|\\ |\\,|\\!|\\>|\\space|\{ }){2,}")
    re_trivial_label = re.compile(
        r"\{?\s*(eq|equation|eqn|th|thm|lemma|theorem|lem|fig|figure)?:?[^a-z}]\s*}?", re.IGNORECASE
    )
    re_nonsymbolic_reference = re.compile(
        r"(рис(унок|унка|унке|\.)|формул(а|е|ой|у|ы)|(равенств|тождеств)(о|а|е|у|ами|ах)|(соотношени|выражени)(е|ю|и|я|ями|ях|ям))\s+\(?\d+\)?",
        re.IGNORECASE,
    )
    re_mod_cmd = re.compile(r"\bmod\b")
    re_math_no_backslash = re.compile(
        r"([^\\a-z]|^)(cos|csc|exp|ker|limsup|max|min|sinh|arcsin|cosh|deg|gcd|lg|ln|Pr|sup|arctan|cot|det|hom|lim|log|sec|tan|arg|coth|dim|liminf|sin|tanh)[^a-z]"
    )
    re_ru_ordinal = re.compile(
        r"\s*-{1,2}\s*(ый|ого|о|тому|ому|ему|ом|ая|ой|ую|ые|ыми|и|ым|тым|той|им|его|того|тых|ых|том|ем|ём|ех|ёх|ух)([^а-яё]|$)",
        re.IGNORECASE | re.DOTALL | re.UNICODE,
    )
    re_small_numeral = re.compile(r"([,.!?:]|\W\s+)[0-5]([,.!?:]|\s+\W)")

    for node in all_nodes:
        if node.cat == LatCat.STR:
            if re_multiplication_star.search(node.token):
                add_error("MULTIPLICATION_SIGN", node)
            if re_multiple_spaces.search(node.token):
                add_error("INDENTATION_WITH_SPACES", node)
            if re_starts_with_cyrillic.search(node.token) and node.prev_node.cat == LatCat.CMD:
                add_error("NO_SPACE_AFTER_COMMAND_BEFORE_CYRILLIC", node)

        if is_numbered_display_math(node) and not has_descendant(node, (lambda x: x.token == "label")):
            add_error("NUMBERED_MATH_NEEDS_REFERENCING", node)
        if is_display_math(node):
            if node.next_sibling:
                if is_display_math(node.next_sibling):
                    add_error("CONSECUTIVE_DISPLAY_FORMULAE", node.next_sibling.pos or node.pos)
                if (node.next_sibling.cat == LatCat.STR) and node.next_sibling.token.startswith("\\\\"):
                    add_error("LINEBREAK_AFTER_DISPLAY_FORMULAE", node.next_sibling.pos or node.pos)
            if (
                node.prev_sibling
                and (node.prev_sibling.cat == LatCat.STR)
                and node.prev_sibling.token.startswith("\\\\")
            ):
                add_error("LINEBREAK_BEFORE_DISPLAY_FORMULAE", node.pos or node.prev_sibling.pos)

        if node.token in ["eqnarray", "eqnarray*"]:
            add_error("EQNARRAY_USED", node.pos)

        if is_math(node) and len(node.children) == 1 and node.children[0].cat != LatCat.STR:
            add_error("UNNECESSARY_MATH_MODE", node)

        if node.cat == LatCat.CMD and node.token == "mid" and not has_sibling(node, lambda x: r"\{" in x.token):
            add_error("MID_IN_SET_COMPREHENSION", node)

        if (
            node.cat == LatCat.CMD
            and node.token in ["sum", "prod", "frac", "binom"]
            and node.prev_node
            and node.prev_node.is_in_math
            and node.prev_node.cat != LatCat.CMD
            and not node.prev_node.is_in_arg
            and re_ends_with_digit_or_letter.match(node.prev_node.token)
        ):
            add_error("CDOT_FOR_READABILITY", node)
        if node.cat == LatCat.CMD and node.token == "centering":
            if not (node.parent and node.parent.token in ["figure", "table"]):
                add_error("CENTERING", node)
        if node.cat == LatCat.CMD and node.token == "not" and node.next_node:
            if (node.next_node.token.strip() + " ")[0] == "=" or node.next_node.token in ["in"]:
                add_error("INCORPORATE_NOT", node)
        if node.cat == LatCat.CMD and node.token == "over":
            add_error("OVER_VS_FRAC", node)
        if node.cat == LatCat.CMD and node.token == "choose":
            add_error("CHOOSE_VS_BINOM", node)
        if (
            node.cat == LatCat.CMD
            and node.token in ["in", "notin", "ni", "subset", "subseteq"]
            and node.next_node
            and node.next_node.token
            and (node.next_node.token.strip() + " ")[0] in "NRZQC"
        ):
            add_error("SETS_IN_BBFONT", node)

        if (
            node.cat == LatCat.CMD
            and node.token == "label"
            and node.args
            and len(node.args) == 1
            and re_trivial_label.match(node.args[0].tex)
        ):
            add_error("TRIVIAL_LABEL", node)

        if (
            node.cat == LatCat.CMD
            and node.token == "ref"
            and node.prev_node
            and node.prev_node.token
            and node.prev_node.token.endswith("(")
        ):
            add_error("EQREF_INSTEAD_OF_REF", node)
        if (
            node.cat == LatCat.CMD
            and node.token in ["ref", "eqref"]
            and node.prev_node
            and node.prev_node.token
            and re_ends_with_space.search(node.prev_node.token)
        ):
            add_error("NONBREAKABLE_SPACE_BEFORE_REF", node)

        if node.is_in_display_math and node.token == "limits":
            add_error("LIMITS_UNNECESSARY_IN_DISPLAY_MODE", node)

        if node.is_in_math and node.token in ["mbox", "hbox"]:
            add_error("REPLACE_MBOX_WITH_TEXT", node)

        if node.is_in_math and node.cat == LatCat.CMD and node.token in ["textbf", "textit"]:
            add_error("TEXT_COMMANDS_IN_MATH_MODE")

        if node.is_in_math and node.cat == LatCat.STR:
            if (
                "|" in node.token
                and (r"\{" in node.token or has_sibling(node, lambda x: r"\{" in (x.token or "")))
                and not has_sibling(node, lambda x: x.token == "mid")
            ):
                add_error("MID_IN_SET_COMPREHENSION", node)
            if "(" in node.token and node.next_node and node.next_node.token in ["sum", "prod", "frac", "binom"]:
                add_error("LEFT_RIGHT_RECOMMENDED", node)
            if re_mod_cmd.search(node.token):
                add_error("MOD_NOT_A_COMMAND", node)
            if "..." in node.token:
                add_error("ELLIPSIS_LDOTS", node)
            if re_possibly_word.search(node.token):
                add_error("TEXT_IN_MATH_MODE", node)
            if ">=" in node.token or "<=" in node.token:
                add_error("LE_AS_SINGLE_COMMAND", node)
            if re_math_no_backslash.search(node.token):
                add_error("BACKSLASH_NEEDED", node)
            if "√" in node.token:
                add_error("UNICODE_SQRT", node)
            if re_cyrillic_tricky_letter.search(node.token):
                add_error("CYRILLIC_LETTER_C_MISUSED", node)
            if '"' in node.token:
                add_error("QUOTES_IN_MATH", node)
            if node.token.strip().endswith("-") and node.next_node and not node.next_node.is_in_math:
                add_error("DASH_IN_MATH_MODE", node)
            if (
                node.token.strip() == ""
                and node.prev_sibling
                and node.prev_sibling.cat == LatCat.ENV
                and node.prev_sibling.token == "math"
                and node.next_sibling
                and node.next_sibling.cat == LatCat.ENV
                and node.next_sibling.token == "math"
            ):
                add_error("UNNECESSARY_FORMULA_BREAK", node)

        if not node.is_in_math and node.cat == LatCat.STR and not is_pure_argument(node):
            if re_nonsymbolic_reference.search(node.token):
                add_error("SYMBOLIC_LINKS")
            if (
                re_starts_with_uppercase.match(node.token)
                and node.prev_node.is_in_math
                and not (node.prev_node.cat == LatCat.STR and node.prev_node.token.strip().endswith("."))
            ):
                add_error("PERIOD_BEFORE_NEXT_SENTENCE")
            if "~ " in node.token or " ~" in node.token:
                add_error("TILDE_INEFFECTIVE_AS_NBSP", node)
            if re_capitalization_after_comma.search(node.token) or (
                re_starts_with_uppercase.match(node.token)
                and node.prev_node
                and node.prev_node.cat == LatCat.STR
                and node.prev_node.token.strip().endswith(",")
            ):
                add_error("CAPITALIZATION_AFTER_PUNCTUATION_MARK", node)
            if re_capitalization_after_period.search(node.token) or (
                re_starts_with_lowercase.match(node.token)
                and node.prev_node
                and node.prev_node.cat == LatCat.STR
                and node.prev_node.token.strip().endswith(".")
            ):
                add_error("CAPITALIZATION_AFTER_PERIOD", node)
            if "..." in node.token:
                # maybe make two different errors for math and text mode
                add_error("ELLIPSIS_LDOTS", node)
            if (node.token.strip() + " ")[0] in ",.:?!;" and is_display_math(node.prev_sibling):
                add_error("PUNCTUATION_AFTER_DISPLAY_MATH", node.prev_sibling)
            if re_space_before_parenthesis.search(node.token):
                add_error("SPACE_BEFORE_PARENTHESIS", node)
            if re_space_after_parenthesis.search(node.token):
                add_error("SPACE_AFTER_PARENTHESIS", node)
            if re_space_after_punctuation.search(node.token):
                add_error("SPACE_AFTER_PUNCTUATION_MARK", node)
            if re_space_before_punctuation.search(node.token):
                add_error("SPACE_BEFORE_PUNCTUATION_MARK", node)
            if re_latin_letter_outside_math_ru.search(node.token):
                add_error("LATIN_LETTER_OUTSIDE_MATH_RU", node)
            if re_latin_letter_outside_math_en.search(node.token):
                add_error("LATIN_LETTER_OUTSIDE_MATH_EN", node)
            if re_math_command.search(node.token):
                add_error("MATH_SEMANTICS_OUTSIDE_MATH", node)
            if re_latin_c_in_rus_text.search(node.token):
                add_error("LATIN_LETTER_C_MISUSED", node)
            if '"' in node.token and node.token != r"\"":
                add_error("WRONG_QUOTES", node)
            if "''" in node.token and "``" not in node.token or "``" in node.token and "''" not in node.token:
                add_error("WRONG_SAME_QUOTES", node)
            if re_dash_as_hyphen.search(node.token):
                add_error("DASH_HYPHEN", node)
            if re_td.search(node.token):
                add_error("ABBREVIATIONS_WITH_SPACE", node)
            if re_dash_no_spaces.search(node.token):
                add_error("DASH_SURROUND_WITH_SPACES", node)
            if re_ru_ordinal.search(node.token):
                add_error("RU_ORDINAL_ABBREVIATION", node)
            if "\\\\" in node.token:
                add_error("SUGGESTED_NEW_PARAGRAPH", node)
            if re_small_numeral.search(node.token):
                add_error("NUMERALS_AS_WORDS", node)
        if (
            (node.token and node.token.strip().endswith(r"\\") or node.token == r"par")
            and node.next_node
            and is_display_math(node.next_node)
        ):
            add_error("PARAGRAPH_BREAK_BEFORE_DISPLAY_FORMULA", node)

        if (
            node.cat == LatCat.ENV
            and node.token == "math"
            and node.next_sibling
            and node.next_sibling.cat == LatCat.ENV
            and node.next_sibling.token == "math"
        ):
            add_error("UNNECESSARY_FORMULA_BREAK", node)

        if node.cat == LatCat.CMD and node.token in ["it", "bf", "sf", "rm"]:
            add_error("LOW_LEVEL_FONT_COMMANDS", node)

        if node.cat == LatCat.CMD and node.token == "textit":
            add_error("ITALIC_INSTEAD_OF_EMPH", node)

        if (
            node.cat == LatCat.CMD
            and node.token == "cite"
            and (
                node.prev_node
                and (node.prev_node.is_in_math or is_math(node.prev_node))
                or node.next_sibling
                and is_math(node.next_sibling)
            )
        ):
            add_error("FORMULA_NEIGHBOURING_REFERENCE", node)
        if node.is_in_math and node.token == "includegraphics":
            add_error("GRAPHICS_IN_MATH_MODE", node)

    for node in all_nodes:
        if (
            (node.cat == LatCat.ENV)
            and is_display_math(node.token)
            and node.next_sibling
            and (node.next_sibling.cat == LatCat.ENV)
            and is_display_math(node.next_sibling.token)
        ):
            add_error("CONSECUTIVE_DISPLAY_FORMULAE", node.next_sibling.pos or node.pos)

    used_labels = set()
    for node in all_nodes:
        if node.cat == LatCat.CMD and node.token in ["ref", "eqref"] and node.args and len(node.args) == 1:
            used_labels.add(node.args[0].tex)
    for node in all_nodes:
        if (
            node.cat == LatCat.CMD
            and node.token in ["label"]
            and node.args
            and len(node.args) == 1
            and node.args[0].tex not in used_labels
        ):
            add_error("NUMBERED_MATH_NEEDS_REFERENCING", node)

    return errors


def html_to_console(html_text, rich_text=True, width=80):
    formats = {
        "red": "\033[91m",
        "green": "\033[92m",
        "blue": "\033[94m",
        "bold": "\033[1m",
        "italics": "\033[3m",
        "underline": "\033[4m",
        "end": "\033[0m",
    }
    if not rich_text:
        formats = {k: "" for k in formats}

    html_entities = {
        "&nbsp;": " ",
        "&thinsp;": "\u2009",
        "&amp;": "&",
        "&mdash;": "—",
        "&ndash;": "–",
        "&hellip;": "…",
        "&laquo;": "«",
        "&raquo;": "»",
        "&lt;": "<",
        "&gt;": ">",
    }

    text = html_text
    for entity, char in html_entities.items():
        text = text.replace(entity, char)

    wrapper = textwrap.TextWrapper(width=width)
    text = wrapper.fill(text)

    text = re.sub(r"<em>(.*?)</em>", f"{formats['italics']}\\1{formats['end']}", text)
    text = re.sub(r"<strong>(.*?)</strong>", f"{formats['bold']}\\1{formats['end']}", text)
    text = re.sub(r"<code>(.*?)</code>", f"{formats['green']}\\1{formats['end']}", text)
    text = re.sub(r'<a\s+href="([^"]*?)"[^>]*>(.*?)</a>', f"[{formats['underline']}\\2{formats['end']}](\\1)", text)

    return text


def main():
    parser = argparse.ArgumentParser(description="Perform checks on a LaTeX file.")
    parser.add_argument("filename", help="Path to the LaTeX file")
    parser.add_argument(
        "-l", "--language", choices=["EN", "RU"], default="EN", help="Language for error descriptions (EN or RU)"
    )
    parser.add_argument("-r", "--rich", choices=["Y", "N"], help="Enable rich text in console output", default="Y")
    args = parser.parse_args()

    filename = args.filename
    if not os.path.exists(filename):
        print(f"'File {filename} does not exist.")
        return

    with open(filename, mode="r", encoding="utf-8") as infile:
        source = infile.read()

    language = SupportedLanguages.EN if args.language.lower() == "en" else SupportedLanguages.RU
    rich = args.rich.lower() == "y"
    errors = perform_checks(source, language=language, debug_mode=False)

    for key, value in errors.items():
        print(f"{key}:")
        print("\n    ".join(repr(source[max(0, t - 10) : t + 20]) for t in value))
        if explanation := error_descriptions[language][key]:
            print(f'\nExplanation:  {html_to_console(explanation["msg"], rich_text=rich)}\n')


if __name__ == "__main__":
    main()
