# phonecodes
This library provides tools for converting between the [International Phonetic Alphabet (IPA)](https://en.wikipedia.org/wiki/International_Phonetic_Alphabet) and other phonetic alphabets used to transcribe speech, including Callhome, [X-SAMPA](https://en.wikipedia.org/wiki/X-SAMPA), [ARPABET](https://en.wikipedia.org/wiki/ARPABET), [DISC/CELEX](https://catalog.ldc.upenn.edu/LDC96L14). Additionally, tools for searching mappings between phonetic symbols and reading/writing pronounciation lexicon files in several standard formats are also provided.

These functionalities are useful for processing data for automatic speech recognition, text to speech, and linguistic analyses of speech. 

# Setup and Installation
Install the library by running `pip install phonecodes` with python 3.10 or greater.

Developers may refer to the CONTRIBUTIONS.md for information on the development environment for testing, linting and contributing to the code. 

# Basic Usage
## Converting between Phonetic Alphabets
If you want to convert to or from IPA to some other phonetic code, use `phonecodes.phonecodes` as follows:
```
>>> from phonecodes import phonecodes
>>> print(phonecodes.CODES) # available phonetic alphabets
{'arpabet', 'ipa', 'xsampa', 'callhome', 'disc'}
>>> phonecodes.convert("ð ɪ s ɪ z ə t ˈɛ s t", "ipa", "arpabet") # convert from IPA to ARPABET with language optional
>>> phonecodes.convert("DH IH S IH Z AH0 T EH1 S T", "arpabet", "ipa", 'eng') # convert from IPA to ARPABET with language
'ð ɪ s ɪ z ə t ˈɛ s t'
'DH IH S IH Z AH0 T EH1 S T'
>>> phonecodes.ipa2arpabet('ð ɪ s ɪ z ə t ˈɛ s t', 'eng') # equivalent to previous, language required
'DH IH S IH Z AH0 T EH1 S T'
>>> phonecodes.convert("DH IH S IH Z AH0 T EH1 S T", "arpabet", "ipa") # convert from ARPABET to IPA, language optional
'ð ɪ s ɪ z ə t ˈɛ s t'
>>> phonecodes.arpabet2ipa("DH IH S IH Z AH0 T EH1 S T", 'eng') # equivalent to previous with language required
'ð ɪ s ɪ z ə t ˈɛ s t'
```

Note that for 'callhome' and 'disc' you should also specify a language code from the following lists:
- DISC/CELEX: Dutch `'nld'`, English `'eng'`, German `'deu'`. Uses German if unspecified. 
- Callhome: Spanish `'spa'`, Egyptian Arabic `'arz'`, Mandarin Chinese `'cmn'`. You MUST specify an appropriate language code or you'll get a KeyError.


## Reading Corpus Files
If you are working with specific corpora, you can also convert between certain corpus formats as follows:
```
>>> from phonecodes import pronlex
>>> my_lex = pronlex.read("test/fixtures/isle_eng_sample.txt", "isle", "eng") # Read in an English ISLE corpus file
>>> my_lex.w2p # see orthographic to phonetic word mapping
{'a': ['#', 'ə', '#'], 'is': ['#', 'ɪ', 'z', '#'], 'test': ['#', 't', 'ˈɛ', 's', 't', '#'], 'this': ['#', 'ð', 'ɪ', 's', '#']}
new_lex = my_lex.recode('arpabet') # Convert mapping to ARPABET
>>> new_lex.w2p
{'a': ['#', 'AH0', '#'], 'is': ['#', 'IH', 'Z', '#'], 'test': ['#', 'T', 'EH1', 'S', 'T', '#'], 'this': ['#', 'DH', 'IH', 'S', '#']}
```

The supported corpus formats and their corresponding phonetic alphabets are as follows:
| Corpus Format | Phonetic Alphabet | Language Options   | 
|---------------|-------------------|--------------------|
| 'babel' | 'xsampa' |'amh', 'asm', 'ben', 'yue', 'ceb', 'luo', 'kat', 'gug', 'hat', 'ibo', 'jav', 'kur', 'lao', 'lit', 'mon', 'pus', 'swa', 'tgl', 'tam', 'tpi', 'tur', 'vie', 'zul' | 
| 'callhome' | 'callhome' | 'arz', 'cmn', 'spa' | 
| 'celex' | 'disc' | 'eng', 'ndl', 'deu' | 
| 'isle' | 'ipa' |  Not required | 

