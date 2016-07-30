from tap.formatter import format_as_diagnostics, format_exception
from tap.tests import TestCase


class TestFormatter(TestCase):

    def test_formats_as_diagnostics(self):
        data = ['foo\n', 'bar\n']
        expected_diagnostics = '# foo\n# bar\n'
        diagnostics = format_as_diagnostics(data)
        self.assertEqual(expected_diagnostics, diagnostics)

    def test_format_exception_as_diagnostics(self):
        exc = self.factory.make_exc()
        diagnostics = format_exception(exc)
        self.assertTrue(diagnostics.startswith('# '))
        self.assertTrue('boom' in diagnostics)
