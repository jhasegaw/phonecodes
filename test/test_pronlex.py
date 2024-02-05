""" Load some pronlexes from the 'fixtures' subdirectory, 
test phone code conversion, and test both word and phone searches.
"""
import re

import pytest

import phonecodes.pronlex as pronlex

pronlex_conversions = [
    ["isle_eng_sample", ["arpabet", "disc", "xsampa"]],
    ["babel_amh_sample", ["xsampa"]],
    ["babel_ben_sample", ["xsampa"]],
    ["celex_deu_sample", ["disc", "xsampa"]],
    ["celex_eng_sample", ["arpabet", "disc", "xsampa"]],
    ["celex_nld_sample", ["disc", "xsampa"]],
    ["callhome_arz_sample", ["callhome", "xsampa"]],
    ["callhome_cmn_sample", ["callhome", "xsampa"]],
    ["callhome_spa_sample", ["callhome", "xsampa"]],
]


# Read test dictionaries in
@pytest.fixture(scope="module")
def lex_objects(fixture_path):
    results = {}
    for identifier, codes in pronlex_conversions:
        results[identifier] = {}
        (dtype, lang, rem) = identifier.split("_")
        dict_params = {}
        if dtype == "isle":
            dict_params["discard_phones"] = "#."

        # Read in sample file and code as IPA
        results[identifier]["ipa"] = pronlex.read(fixture_path / f"{identifier}.txt", lang, dtype, dict_params).recode(
            "ipa"
        )

        # Recode into supported alphabets
        for c in codes:
            results[identifier][c] = results[identifier]["ipa"].recode(c)
    return results


# Check converting between IPA and other phone codes works
@pytest.mark.parametrize("srcfile, codes", pronlex_conversions)
def test_dictionaries_convert_phonecodes(srcfile, codes, tmp_path, fixture_path, lex_objects):
    for c1 in codes:
        for c in [["ipa", c1], [c1, "ipa"]]:
            destfile = re.sub(r"sample", c[1], srcfile)

            # Save lex output to temp dir
            lex_objects[srcfile][c[1]].save(tmp_path / f"{destfile}.txt")
            expected = (fixture_path / f"{destfile}.txt").read_text()
            output = (tmp_path / f"{destfile}.txt").read_text()
            assert output == expected


@pytest.mark.parametrize("srcfile, codes", pronlex_conversions)
def test_words2phones(srcfile, codes, tokenized_sentences, lex_objects):
    (dtype, lang, rem) = srcfile.split("_")
    for code in ["ipa"] + codes:
        res = lex_objects[srcfile][code].words2phones(tokenized_sentences[lang]["word"])
        assert res == tokenized_sentences[lang][code]

        # Possible failure modes - leftover from old test code, might be helpful for debugging
        # m = min(len(res), len(tokenized_sentences[lang][code]))
        # for n in range(0, m):
        #    if tokenized_sentences[lang][code][n] == res[n]:
        #        print("%s == %s" % (res[n], tokenized_sentences[lang][code][n]))
        #    else:
        #        print("%s != %s" % (res[n], tokenized_sentences[lang][code][n]))
        # if len(tokenized_sentences[lang][code]) > m:
        #    print("Ref chars not in hyp:" + ":".join(tokenized_sentences[lang][code][m:]))
        # elif len(res) > m:
        #    print("Hyp chars not in ref:" + ":".join(res[m:]))


@pytest.mark.parametrize("srcfile, codes", pronlex_conversions)
def test_phones2words(srcfile, codes, tokenized_sentences, lex_objects):
    (dtype, lang, rem) = srcfile.split("_")
    for code in ["ipa"] + codes:
        res = lex_objects[srcfile][code].phones2words(tokenized_sentences[lang][code])
        pat = re.compile(" ".join(tokenized_sentences[lang]["word"]), re.IGNORECASE)
        assert any(re.match(pat, " ".join(x)) for x in res[0])


def test_phone_edit_distance(lex_objects, tokenized_sentences):
    srcfile = "isle_eng_sample"
    lang = "eng"
    c1 = "ipa"
    res = lex_objects[srcfile][c1].phones2words(tokenized_sentences[lang][c1], 2)
    # Test phones2words with 0, 1 or 2 phone distance allowed
    assert res[0] == [["this", "is", "a", "test"]]

    # I don't know why there are repeats, but this is what the original code output
    assert len(res[1]) == 6
    expected_dist_1 = [
        "a this is a test",
        "this a is a test",
        "this is a a test",
        "this is a a test",
        "this is a test a",
        "this is test",
    ]
    assert res[1] == [s.split() for s in expected_dist_1]

    expected_dist_2 = [
        "a a this is a test",
        "a this a is a test",
        "a this is a a test",
        "a this is a a test",
        "a this is a test a",
        "a this is test",
        "is is a test",
        "is this is a test",
        "this a a is a test",
        "this a is a a test",
        "this a is a a test",
        "this a is a test",
        "this a is a test a",
        "this a is test",
        "this is a a a test",
        "this is a a a test",
        "this is a a a test",
        "this is a a test",
        "this is a a test a",
        "this is a a test a",
        "this is a is test",
        "this is a test",
        "this is a test",
        "this is a test",
        "this is a test",
        "this is a test",
        "this is a test",
        "this is a test",
        "this is a test",
        "this is a test",
        "this is a test a a",
        "this is a test is",
        "this is is a test",
        "this is is a test",
        "this is is a test",
        "this is is test",
        "this is test a",
        "this this a test",
    ]

    assert len(res[2]) == 38
    assert res[2] == [s.split() for s in expected_dist_2]
