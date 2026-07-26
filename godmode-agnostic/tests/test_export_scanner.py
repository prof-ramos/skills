"""Edge-case tests for the export.py lexer's _Scanner and the functions built on it.

Before this test existed, export.py's parsing correctness was checked only by
byte-for-byte comparison against the already-committed godmode_bundle.json
(test_export_bundle.py) -- which proves "matches today's output", not "handles
comments / escapes / cursor edge cases correctly". These tests target exactly
the gap: the scanner mechanics themselves, independent of any vendored file.
"""

from __future__ import annotations

from godmode_agnostic.export import (
    _Scanner,
    extract_single_quoted,
    extract_template_at,
    parse_hall_of_fame,
)


def test_scanner_peek_advance_eof():
    s = _Scanner("abc")
    assert s.peek() == "a"
    assert s.peek(1) == "b"
    assert not s.eof
    assert s.advance(2) == "ab"
    assert s.pos == 2
    assert s.advance() == "c"
    assert s.eof
    assert s.peek() == ""


def test_scanner_startswith():
    s = _Scanner("// comment\nrest", pos=0)
    assert s.startswith("//")
    assert not s.startswith("/*")


def test_skip_ws_and_comments_line_comment():
    s = _Scanner("   // this is a comment\n  value", pos=0)
    s.skip_ws_and_comments()
    assert s.source[s.pos :].startswith("value")


def test_skip_ws_and_comments_block_comment():
    s = _Scanner("/* multi\nline\ncomment */value", pos=0)
    s.skip_ws_and_comments()
    assert s.source[s.pos :] == "value"


def test_skip_ws_and_comments_unterminated_block_comment_consumes_to_eof():
    s = _Scanner("/* never closes", pos=0)
    s.skip_ws_and_comments()
    assert s.eof


def test_extract_single_quoted_decodes_unicode_escape():
    scanner = _Scanner(r"'hello é world'", pos=0)
    value = extract_single_quoted(scanner)
    assert value == "hello é world"
    # Cursor lands just past the closing quote, ready for the next field.
    assert scanner.pos == len(scanner.source)


def test_extract_single_quoted_unclosed_raises():
    scanner = _Scanner("'no closing quote", pos=0)
    try:
        extract_single_quoted(scanner)
    except ValueError as exc:
        assert "unclosed" in str(exc)
    else:
        raise AssertionError("expected ValueError")


def test_extract_template_at_handles_escaped_backtick():
    scanner = _Scanner(r"`a \` b`,rest", pos=0)
    value = extract_template_at(scanner)
    assert value == "a ` b"
    assert scanner.source[scanner.pos :] == ",rest"


def test_parse_hall_of_fame_skips_comments_between_fields():
    source = """
    export const HALL_OF_FAME = [
      {
        id: 'demo-combo', // trailing line comment
        /* block comment between fields */
        model: 'demo-model',
        codename: 'Demo',
        description: 'A demo entry',
        color: 'blue',
        system: `system prompt`,
        user: `user prompt`,
      },
    ];
    """
    combos = parse_hall_of_fame(source)
    assert len(combos) == 1
    assert combos[0]["id"] == "demo-combo"
    assert combos[0]["fast"] is False


def test_parse_hall_of_fame_honors_explicit_fast_true():
    source = """
    export const HALL_OF_FAME = [
      {
        id: 'fast-combo',
        model: 'demo-model',
        codename: 'Fast',
        description: 'A fast entry',
        color: 'red',
        system: `sys`,
        user: `usr`,
        fast: true,
      },
    ];
    """
    combos = parse_hall_of_fame(source)
    assert combos[0]["fast"] is True
