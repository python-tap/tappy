import inspect
import sys
import tempfile
import unittest
from contextlib import contextmanager
from io import StringIO
from unittest import mock

from tap.parser import Parser

try:
    import yaml
    from more_itertools import peekable  # noqa

    have_yaml = True
except ImportError:
    have_yaml = False


@contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err


class TestParser(unittest.TestCase):
    """Tests for tap.parser.Parser"""

    def test_finds_ok(self):
        """The parser extracts an ok line."""
        parser = Parser()

        line = parser.parse_line("ok - This is a passing test line.")

        self.assertEqual("test", line.category)
        self.assertTrue(line.ok)
        self.assertTrue(line.number is None)

    def test_finds_number(self):
        """The parser extracts a test number."""
        parser = Parser()

        line = parser.parse_line("ok 42 is the magic number.")

        self.assertEqual("test", line.category)
        self.assertEqual(42, line.number)

    def test_finds_description(self):
        parser = Parser()

        line = parser.parse_line("ok 42 A passing test.")

        self.assertEqual("test", line.category)
        self.assertEqual("A passing test.", line.description)

    def test_after_hash_is_not_description(self):
        parser = Parser()

        line = parser.parse_line("ok A description # Not part of description.")

        self.assertEqual("test", line.category)
        self.assertEqual("A description", line.description)

    def test_finds_todo(self):
        parser = Parser()

        line = parser.parse_line("ok A description # TODO Not done")

        self.assertEqual("test", line.category)
        self.assertTrue(line.todo)

    def test_finds_skip(self):
        parser = Parser()

        line = parser.parse_line("ok A description # SKIP for now")

        self.assertEqual("test", line.category)
        self.assertTrue(line.skip)

    def test_finds_not_ok(self):
        """The parser extracts a not ok line."""
        parser = Parser()

        line = parser.parse_line("not ok - This is a failing test line.")

        self.assertEqual("test", line.category)
        self.assertFalse(line.ok)
        self.assertTrue(line.number is None)
        self.assertEqual("", line.directive.text)

    def test_finds_directive(self):
        """The parser extracts a directive"""
        parser = Parser()
        test_line = "not ok - This line fails # TODO not implemented"

        line = parser.parse_line(test_line)
        directive = line.directive

        self.assertEqual("test", line.category)
        self.assertEqual("TODO not implemented", directive.text)
        self.assertFalse(directive.skip)
        self.assertTrue(directive.todo)
        self.assertEqual("not implemented", directive.reason)

    def test_unrecognizable_line(self):
        """The parser returns an unrecognizable line."""
        parser = Parser()

        line = parser.parse_line("This is not a valid TAP line. # srsly")

        self.assertEqual("unknown", line.category)

    def test_diagnostic_line(self):
        """The parser extracts a diagnostic line."""
        text = "# An example diagnostic line"
        parser = Parser()

        line = parser.parse_line(text)

        self.assertEqual("diagnostic", line.category)
        self.assertEqual(text, line.text)

    def test_bail_out_line(self):
        """The parser extracts a bail out line."""
        parser = Parser()

        line = parser.parse_line("Bail out! This is the reason to bail.")

        self.assertEqual("bail", line.category)
        self.assertEqual("This is the reason to bail.", line.reason)

    def test_finds_version(self):
        """The parser extracts a version line."""
        parser = Parser()

        line = parser.parse_line("TAP version 13")

        self.assertEqual("version", line.category)
        self.assertEqual(13, line.version)

    def test_errors_on_old_version(self):
        """The TAP spec dictates that anything less than 13 is an error."""
        parser = Parser()

        with self.assertRaises(ValueError):
            parser.parse_line("TAP version 12")

    def test_finds_plan(self):
        """The parser extracts a plan line."""
        parser = Parser()

        line = parser.parse_line("1..42")

        self.assertEqual("plan", line.category)
        self.assertEqual(42, line.expected_tests)

    def test_finds_plan_with_skip(self):
        """The parser extracts a plan line containing a SKIP."""
        parser = Parser()

        line = parser.parse_line("1..42 # Skipping this test file.")

        self.assertEqual("plan", line.category)
        self.assertTrue(line.skip)

    def test_ignores_plan_with_any_non_skip_directive(self):
        """The parser only recognizes SKIP directives in plans."""
        parser = Parser()

        line = parser.parse_line("1..42 # TODO will not work.")

        self.assertEqual("unknown", line.category)

    def test_parses_text(self):
        sample = inspect.cleandoc(
            """1..2
            ok 1 A passing test
            not ok 2 A failing test"""
        )
        parser = Parser()
        lines = []

        for line in parser.parse_text(sample):
            lines.append(line)

        self.assertEqual(3, len(lines))
        self.assertEqual("plan", lines[0].category)
        self.assertEqual("test", lines[1].category)
        self.assertTrue(lines[1].ok)
        self.assertEqual("test", lines[2].category)
        self.assertFalse(lines[2].ok)

    def test_parses_file(self):
        sample = inspect.cleandoc(
            """1..2
            ok 1 A passing test
            not ok 2 A failing test"""
        )
        temp = tempfile.NamedTemporaryFile(delete=False)  # noqa: SIM115
        temp.write(sample.encode("utf-8"))
        temp.close()
        parser = Parser()
        lines = []

        for line in parser.parse_file(temp.name):
            lines.append(line)

        self.assertEqual(3, len(lines))
        self.assertEqual("plan", lines[0].category)
        self.assertEqual("test", lines[1].category)
        self.assertTrue(lines[1].ok)
        self.assertIsNone(lines[1].yaml_block)
        self.assertEqual("test", lines[2].category)
        self.assertFalse(lines[2].ok)

    def test_parses_yaml(self):
        sample = inspect.cleandoc(
            """TAP version 13
            1..2
            ok 1 A passing test
               ---
               test: sample yaml
               ...
            not ok 2 A failing test"""
        )
        parser = Parser()
        lines = []

        for line in parser.parse_text(sample):
            lines.append(line)

        if have_yaml:
            converted_yaml = yaml.safe_load("""test: sample yaml""")
            self.assertEqual(4, len(lines))
            self.assertEqual(13, lines[0].version)
            self.assertEqual(converted_yaml, lines[2].yaml_block)
            self.assertEqual("test", lines[3].category)
            self.assertIsNone(lines[3].yaml_block)
        else:
            self.assertEqual(7, len(lines))
            self.assertEqual(13, lines[0].version)
            for line_index in list(range(3, 6)):
                self.assertEqual("unknown", lines[line_index].category)
            self.assertEqual("test", lines[6].category)

    def test_parses_mixed(self):
        # Test that we can parse both a version 13 and earlier version files
        # using the same parser. Make sure that parsing works regardless of
        # the order of the incoming documents.
        sample_version_13 = inspect.cleandoc(
            """TAP version 13
            1..2
            ok 1 A passing version 13 test
               ---
               test: sample yaml
               ...
            not ok 2 A failing version 13 test"""
        )
        sample_pre_13 = inspect.cleandoc(
            """1..2
            ok 1 A passing pre-13 test
            not ok 2 A failing pre-13 test"""
        )

        parser = Parser()
        lines = []
        lines.extend(parser.parse_text(sample_version_13))
        lines.extend(parser.parse_text(sample_pre_13))
        if have_yaml:
            self.assertEqual(13, lines[0].version)
            self.assertEqual("A passing version 13 test", lines[2].description)
            self.assertEqual("A failing version 13 test", lines[3].description)
            self.assertEqual("A passing pre-13 test", lines[5].description)
            self.assertEqual("A failing pre-13 test", lines[6].description)
        else:
            self.assertEqual(13, lines[0].version)
            self.assertEqual("A passing version 13 test", lines[2].description)
            self.assertEqual("A failing version 13 test", lines[6].description)
            self.assertEqual("A passing pre-13 test", lines[8].description)
            self.assertEqual("A failing pre-13 test", lines[9].description)

        # Test parsing documents in reverse order
        parser = Parser()
        lines = []
        lines.extend(parser.parse_text(sample_pre_13))
        lines.extend(parser.parse_text(sample_version_13))
        if have_yaml:
            self.assertEqual("A passing pre-13 test", lines[1].description)
            self.assertEqual("A failing pre-13 test", lines[2].description)
            self.assertEqual(13, lines[3].version)
            self.assertEqual("A passing version 13 test", lines[5].description)
            self.assertEqual("A failing version 13 test", lines[6].description)
        else:
            self.assertEqual("A passing pre-13 test", lines[1].description)
            self.assertEqual("A failing pre-13 test", lines[2].description)
            self.assertEqual(13, lines[3].version)
            self.assertEqual("A passing version 13 test", lines[5].description)
            self.assertEqual("A failing version 13 test", lines[9].description)

    def test_parses_yaml_no_end(self):
        sample = inspect.cleandoc(
            """TAP version 13
            1..2
            ok 1 A passing test
               ---
               test: sample yaml
            not ok 2 A failing test"""
        )
        parser = Parser()
        lines = []

        for line in parser.parse_text(sample):
            lines.append(line)

        if have_yaml:
            converted_yaml = yaml.safe_load("""test: sample yaml""")
            self.assertEqual(4, len(lines))
            self.assertEqual(13, lines[0].version)
            self.assertEqual(converted_yaml, lines[2].yaml_block)
            self.assertEqual("test", lines[3].category)
            self.assertIsNone(lines[3].yaml_block)
        else:
            self.assertEqual(6, len(lines))
            self.assertEqual(13, lines[0].version)
            for line_index in list(range(3, 5)):
                self.assertEqual("unknown", lines[line_index].category)
            self.assertEqual("test", lines[5].category)

    def test_parses_yaml_more_complex(self):
        sample = inspect.cleandoc(
            """TAP version 13
            1..2
            ok 1 A passing test
               ---
               message: test
               severity: fail
               data:
                 got:
                   - foo
                 expect:
                   - bar
               output: |-
                 a multiline string
                 must be handled properly
                 even with | pipes
                 | here > and: there
               last_nl: |+
                 there's a newline here ->
               """
        )
        parser = Parser()
        lines = []

        for line in parser.parse_text(sample):
            lines.append(line)

        if have_yaml:
            converted_yaml = yaml.safe_load(
                r'''
               message: test
               severity: fail
               data:
                 got:
                   - foo
                 expect:
                   - bar
               output: "a multiline string\nmust be handled properly\neven with | pipes\n| here > and: there"
               last_nl: "there's a newline here ->\n"'''  # noqa
            )
            self.assertEqual(3, len(lines))
            self.assertEqual(13, lines[0].version)
            self.assertEqual(converted_yaml, lines[2].yaml_block)
        else:
            self.assertEqual(19, len(lines))
            self.assertEqual(13, lines[0].version)
            for line_index in list(range(3, 11)):
                self.assertEqual("unknown", lines[line_index].category)

    def test_parses_yaml_no_association(self):
        sample = inspect.cleandoc(
            """TAP version 13
            1..2
            ok 1 A passing test
            # Diagnostic line
               ---
               test: sample yaml
               ...
            not ok 2 A failing test"""
        )
        parser = Parser()
        lines = []

        for line in parser.parse_text(sample):
            lines.append(line)

        self.assertEqual(8, len(lines))
        self.assertEqual(13, lines[0].version)
        self.assertIsNone(lines[2].yaml_block)
        self.assertEqual("diagnostic", lines[3].category)
        for line_index in list(range(4, 7)):
            self.assertEqual("unknown", lines[line_index].category)
        self.assertEqual("test", lines[7].category)

    def test_parses_yaml_no_start(self):
        sample = inspect.cleandoc(
            """TAP version 13
            1..2
            ok 1 A passing test
               test: sample yaml
               ...
            not ok 2 A failing test"""
        )
        parser = Parser()
        lines = []

        for line in parser.parse_text(sample):
            lines.append(line)

        self.assertEqual(6, len(lines))
        self.assertEqual(13, lines[0].version)
        self.assertIsNone(lines[2].yaml_block)
        for line_index in list(range(3, 5)):
            self.assertEqual("unknown", lines[line_index].category)
        self.assertEqual("test", lines[5].category)

    def test_malformed_yaml(self):
        self.maxDiff = None
        sample = inspect.cleandoc(
            """TAP version 13
            1..2
            ok 1 A passing test
               ---
               test: sample yaml
               \tfail: tabs are not allowed!
               ...
            not ok 2 A failing test"""
        )
        yaml_err = inspect.cleandoc(
            """
WARNING: Optional imports not found, TAP 13 output will be
    ignored. To parse yaml, see requirements in docs:
    https://tappy.readthedocs.io/en/latest/consumers.html#tap-version-13"""
        )
        parser = Parser()
        lines = []

        with captured_output() as (parse_out, _):
            for line in parser.parse_text(sample):
                lines.append(line)

        if have_yaml:
            self.assertEqual(4, len(lines))
            self.assertEqual(13, lines[0].version)
            with captured_output() as (out, _):
                self.assertIsNone(lines[2].yaml_block)
            self.assertEqual(
                "Error parsing yaml block. Check formatting.", out.getvalue().strip()
            )
            self.assertEqual("test", lines[3].category)
            self.assertIsNone(lines[3].yaml_block)
        else:
            self.assertEqual(8, len(lines))
            self.assertEqual(13, lines[0].version)
            for line_index in list(range(3, 7)):
                self.assertEqual("unknown", lines[line_index].category)
            self.assertEqual("test", lines[7].category)
            self.assertEqual(yaml_err, parse_out.getvalue().strip())

    def test_parse_empty_file(self):
        temp = tempfile.NamedTemporaryFile(delete=False)  # noqa: SIM115
        temp.close()
        parser = Parser()
        lines = []

        for line in parser.parse_file(temp.name):
            lines.append(line)

        self.assertEqual(0, len(lines))

    @mock.patch(
        "tap.parser.sys.stdin",
        StringIO(
            """1..2
ok 1 A passing test
not ok 2 A failing test"""
        ),
    )
    def test_parses_stdin(self):
        parser = Parser()
        lines = []

        for line in parser.parse_stdin():
            lines.append(line)

        self.assertEqual(3, len(lines))
        self.assertEqual("plan", lines[0].category)
        self.assertEqual("test", lines[1].category)
        self.assertTrue(lines[1].ok)
        self.assertEqual("test", lines[2].category)
        self.assertFalse(lines[2].ok)
