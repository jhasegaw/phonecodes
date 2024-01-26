"""Load some pronlexes from the 'fixtures' subdirectory,
test phone code conversion, and test both word and phone searches.
"""
import phonecodes.phonecodes as phonecodes

import pytest


# Test the phonecode conversions
phonecode_cases = [
    ("arpabet", "ipa", phonecodes.arpabet2ipa, "eng"),
    ("ipa", "arpabet", phonecodes.ipa2arpabet, "eng"),
    ("ipa", "callhome", phonecodes.ipa2callhome, "arz"),
    ("ipa", "callhome", phonecodes.ipa2callhome, "cmn"),
    ("ipa", "callhome", phonecodes.ipa2callhome, "spa"),
    ("callhome", "ipa", phonecodes.callhome2ipa, "arz"),
    ("callhome", "ipa", phonecodes.callhome2ipa, "cmn"),
    ("callhome", "ipa", phonecodes.callhome2ipa, "spa"),
    ("ipa", "disc", phonecodes.ipa2disc, "deu"),
    ("ipa", "disc", phonecodes.ipa2disc, "eng"),
    ("ipa", "disc", phonecodes.ipa2disc, "nld"),
    ("disc", "ipa", phonecodes.disc2ipa, "deu"),
    ("disc", "ipa", phonecodes.disc2ipa, "eng"),
    ("disc", "ipa", phonecodes.disc2ipa, "nld"),
    ("ipa", "xsampa", phonecodes.ipa2xsampa, "amh"),
    ("ipa", "xsampa", phonecodes.ipa2xsampa, "ben"),
    ("xsampa", "ipa", phonecodes.xsampa2ipa, "amh"),
    ("xsampa", "ipa", phonecodes.xsampa2ipa, "ben"),
]


@pytest.mark.parametrize("in_code, out_code, fn_call, language", phonecode_cases)
def test_conversions(in_code, out_code, fn_call, language, sentences):
    result = fn_call(sentences[language][in_code], language)
    expected = sentences[language][out_code]
    assert result == expected
