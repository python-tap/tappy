import sys

from tap import formatter
from tap.tests import TestCase


class TestFormatter(TestCase):

    def test_formats_as_diagnostics(self):
        data = ['foo\n', 'bar\n']
        expected_diagnostics = '# foo\n# bar\n'
        diagnostics = formatter.format_as_diagnostics(data)
        self.assertEqual(expected_diagnostics, diagnostics)

    def test_format_exception_as_diagnostics(self):
        # Making a tracback intentionally is not straight forward.
        try:
            raise ValueError('boom')
        except ValueError:
            exc = sys.exc_info()
            diagnostics = formatter.format_exception(exc)
            self.assertTrue(diagnostics.startswith('# '))
            self.assertTrue('boom' in diagnostics)
