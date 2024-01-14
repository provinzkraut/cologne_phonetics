import unittest
from unittest import mock

import cologne_phonetics
from cologne_phonetics import cli, compare, encode


def enc_first(val, **kwargs):
    return encode(val, **kwargs)[0][1]


class TestEncode(unittest.TestCase):
    def multiple_before(self, char=None, before=None, exp=None):
        for b in before:
            self.assertEqual(encode(char + b), exp)

    def multiple_after(self, char=None, after=None, exp=None):
        for b in after:
            self.assertEqual(enc_first(b + char), exp)

    def fuzz(self, char, exp, alt_exp="None", fuzzer="h"):
        for stmt in (char, fuzzer + char, char + fuzzer):
            try:
                self.assertEqual(enc_first(stmt), exp)
            except AssertionError as e:
                if alt_exp == "None":
                    raise e
                self.assertEqual(enc_first(stmt), alt_exp)

    def test_aeijouy(self):
        chars = ["a", "ä", "á", "à", "e", "é", "è", "i", "j", "o", "ö", "u", "ü", "y"]
        for c in chars:
            self.fuzz(c, "0")

    def test_h(self):
        self.assertEqual(enc_first("h"), "")
        self.fuzz("h", "0", alt_exp="", fuzzer="a")

    def test_h_in_context(self):
        self.assertEqual(enc_first("aha"), "0")
        self.assertEqual(enc_first("ha"), "0")
        self.assertEqual(enc_first("ah"), "0")

    def test_b(self):
        self.fuzz("b", "1")

    def test_p_not_before_h(self):
        self.assertEqual(enc_first("apa"), "01")
        self.assertEqual(enc_first("pa"), "1")
        self.assertNotEqual(enc_first("ph"), "1")

    def test_p_before_h(self):
        self.assertEqual(enc_first("ph"), "3")
        self.assertEqual(enc_first("aph"), "03")

    def test_dt_not_before_csz(self):
        self.assertEqual(enc_first("da"), "2")
        self.assertNotEqual(enc_first("dc"), "2")
        self.assertEqual(enc_first("ta"), "2")
        self.assertNotEqual(enc_first("tc"), "2")

    def test_dt_before_csz(self):
        self.assertNotEqual(enc_first("da"), "8")
        self.assertEqual(enc_first("dc"), "8")
        self.assertNotEqual(enc_first("ta"), "8")
        self.assertEqual(enc_first("tc"), "8")

    def test_fvw(self):
        self.assertEqual(enc_first("fvw"), "3")
        self.assertEqual(enc_first("af"), "03")

    def test_gkq(self):
        self.assertEqual(enc_first("gkq"), "4")
        self.assertEqual(enc_first("ag"), "04")

    def test_c_init_before_ahkloqrux(self):
        self.assertEqual(enc_first("ca"), "4")
        self.assertNotEqual(enc_first("ac"), "04")
        self.assertNotEqual(enc_first("cm"), "4")

    def test_c_before_ahkoqux_not_after_sz(self):
        self.assertEqual(enc_first("ch"), "4")
        self.assertFalse(enc_first("sc").endswith("4"))
        self.assertFalse(enc_first("zc").endswith("4"))

    def test_x(self):
        self.fuzz("x", "48")
        self.multiple_after(char="x", after="ckq", exp="48")

    def test_l(self):
        self.fuzz("l", "5")

    def test_mn(self):
        self.fuzz("m", "6")
        self.fuzz("n", "6")

    def test_r(self):
        self.fuzz("r", "7")

    def test_sz(self):
        self.fuzz("s", "8")
        self.fuzz("z", "8")

    def test_special_chars(self):
        special_chars = {
            "ä": "ae",
            "á": "a",
            "à": "a",
            "ü": "ue",
            "ö": "oe",
            "é": "e",
            "è": "e",
            "ß": "s",
            "ç": "c",
            "š": "s",
        }
        for char, repl in special_chars.items():
            self.assertEqual(enc_first(char), enc_first(repl))

    def test_ignore_invalid(self):
        self.assertEqual(enc_first("ah"), enc_first("ahø"))

    def test_concatenation(self):
        self.assertTrue(encode("a-a") == encode("a a"))
        self.assertEqual(encode("a-a", concat=True), [("a-a", "0")])
        self.assertEqual(encode("a a", concat=True), [("a", "0"), ("a", "0")])

    def test_case_insensitive(self):
        self.assertEqual(encode("foo"), encode("FoO"))

    def test_returns_altered(self):
        self.assertEqual(encode("bäTes")[0][0], "baetes")


class TestCompare(unittest.TestCase):
    def test_input(self):
        self.assertEqual(compare(["a", "b", "c"]), compare("a", "b", "c"))

    def test_iterinput(self):
        for i in (["a", "b"], ("a", "b"), {"a", "b"}):
            self.assertFalse(compare(i))

    def test_case_insensitive(self):
        self.assertTrue(compare("foo", "FoO"))

    def test_compare(self):
        self.assertTrue(compare("a", "a"))
        self.assertFalse(compare("a", "x"))
        self.assertTrue(compare("foo", "fuh"))
        self.assertTrue(compare("foo-foo", "foo-fuh"))
        self.assertTrue(compare("foo foo", "foo-fuh"))
        self.assertFalse(compare("foo-foo", "foo-fuh", "foo bar"))

    def test_raises_on_one_value(self):
        with self.assertRaises(ValueError):
            compare("foo")
        with self.assertRaises(ValueError):
            compare(["foo"])
        with self.assertRaises(ValueError):
            compare("f")
        with self.assertRaises(ValueError):
            compare(["f"])


class TestCLI(unittest.TestCase):
    def setUp(self):
        cologne_phonetics.print = mock.MagicMock()
        self.mock_print = cologne_phonetics.print

    def tearDown(self):
        cologne_phonetics.sys.argv = ["test_cologne_phonetics.py"]

    def compare_enc_call(self, mocked, data):
        encoded = enc_first(data)
        mocked.assert_called_with(encoded)

    def test_encode(self):
        cli(["foo"])
        self.mock_print.assert_called_with(enc_first("foo"))

    @mock.patch("cologne_phonetics.encode")
    def test_concat(self, mock_encode):
        cli(["foo", "-c"])
        mock_encode.assert_called_with("foo", concat=True)

    def test_verbose(self):
        cli(["foo", "-v"])
        self.mock_print.assert_called_with("foo: 3")

    def test_pretty(self):
        cli(["foo-bar", "-vp"])
        self.mock_print.assert_called_with("foo: 3\nbar: 17")


if __name__ == "__main__":
    unittest.main()
