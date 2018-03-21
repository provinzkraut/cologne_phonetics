import unittest

from cologne_phonetics import encode


class TestColognePhonetics(unittest.TestCase):

    def multiple_before(self, char=None, before=None, exp=None):
        for b in before:
            self.assertEqual(encode(char+b), exp)

    def multiple_after(self, char=None, after=None, exp=None):
        for b in after:
            self.assertEqual(encode(b+char), exp)

    def fuzz(self, char, exp, alt_exp=None, fuzzer="h"):
        for stmt in (char, fuzzer+char, char+fuzzer):
            try:
                self.assertEqual(encode(stmt), exp)
            except AssertionError:
                self.assertEqual(encode(stmt), alt_exp)

    def test_aeijouy(self):
        chars = ["a","ä","á","à","e","é","è","i","j","o","ö","u","ü","y"]
        for c in chars:
            self.fuzz(c, "0")

    def test_h(self):
        self.assertEqual(encode("h"), "")
        self.fuzz("h", "0", alt_exp="", fuzzer="a")

    def test_h_in_context(self):
        self.assertEqual(encode("aha"), "0")
        self.assertEqual(encode("ha"), "0")
        self.assertEqual(encode("ah"), "0")

    def test_b(self):
        self.fuzz("b", "1")

    def test_p_not_before_h(self):
        self.assertEqual(encode("apa"), "01")
        self.assertEqual(encode("pa"), "1")
        self.assertNotEqual(encode("ph"), "1")

    def test_p_before_h(self):
        self.assertEqual(encode("ph"), "3")
        self.assertEqual(encode("aph"), "03")

    def test_dt_not_before_csz(self):
        self.assertEqual(encode("da"), "2")
        self.assertNotEqual(encode("dc"), "2")
        self.assertEqual(encode("ta"), "2")
        self.assertNotEqual(encode("tc"), "2")

    def test_dt_before_csz(self):
        self.assertNotEqual(encode("da"), "8")
        self.assertEqual(encode("dc"), "8")
        self.assertNotEqual(encode("ta"), "8")
        self.assertEqual(encode("tc"), "8")

    def test_fvw(self):
        self.assertEqual(encode("fvw"), "3")
        self.assertEqual(encode("af"), "03")

    def test_gkq(self):
        self.assertEqual(encode("gkq"), "4")
        self.assertEqual(encode("ag"), "04")

    def test_c_init_before_ahkloqrux(self):
        self.assertEqual(encode("ca"), "4")
        self.assertNotEqual(encode("ac"), "04")
        self.assertNotEqual(encode("cm"), "4")

    def test_c_before_ahkoqux_not_after_sz(self):
        self.assertEqual(encode("ch"), "4")
        self.assertFalse(encode("sc").endswith("4"))
        self.assertFalse(encode("zc").endswith("4"))

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
            "ç": "c"
        }
        for char, repl in special_chars.items():
            self.assertEqual(encode(char), encode(repl))

    def test_ignore_invalid(self):
        self.assertEqual(encode("ah"), encode("ahø"))

    def test_concatenation(self):
        self.assertTrue(encode("a-a")==encode("a a")==["0","0"])
        self.assertEqual(encode("a-a", concat=True), "0")
        self.assertEqual(encode("a a", concat=True), ["0", "0"])


if __name__ == "__main__":
    unittest.main()
