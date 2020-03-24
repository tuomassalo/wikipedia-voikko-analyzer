import regex
import fileinput
import json


def extract_words(plaintext):
    '''
        Splits plaintext to sentences and words. Yields tuples of type:
        (original_word_form, 'PROPER'|'NOT_PROPER'|'MAYBE_PROPER')
    '''

    # Un-fancify aposthropes
    plaintext = regex.sub(r'’', "'", plaintext)

    # strip punctuation (NB: longer dash, fancier quotes)
    plaintext = regex.sub(r'[–“”"()\[\]\{\}]+', ' ', plaintext)

    # strip aposthropes that are not in the middle of a word
    plaintext = regex.sub(r"'(?!\w)", '', plaintext, flags=regex.UNICODE)
    plaintext = regex.sub(r"(?<!\w)'", '', plaintext, flags=regex.UNICODE)

    # strip punctuation that is followed by a space but does not capitalize the next word.
    plaintext = regex.sub(r'[,;:]\s', ' ', plaintext)

    # strip punctuation (that is followed by a space)

    # based on:
    # perl -C -walne '/<form>(.*?)</ or next; $a{$_}=1 for split(//, lc $1); END {print sort keys %a}' joukahainen.xml
    # add aposthrope and hyphen
    for sentence in regex.split(r'[.?!]\s', plaintext + ' '):
        is_sentence_start = True
        for form in filter(
            lambda w: (regex.match(
                r"^[abcdefghijklmnopqrstuvwxyzµßàáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿńšžω'-]+$", w) and
                not regex.match(r"^['-]|['-]$", w)
            ),
            regex.split(r'\s+', sentence.strip())
        ):
            if is_sentence_start:
                # This word starts a sentence, so it's possibly a proper name.
                yield (form, 'MAYBE_PROPER')
            else:
                # The word is considered a proper name if it:
                # - has an uppercase letter followed by a lowercase letter ("Foo")
                # - or vice versa ("fOO")
                # - or if it's all uppercase ("FOO")
                # Thus, "LP-versio" is not considered a proper name.
                if(
                    regex.search(r'\p{Lu}\p{Ll}', form) or
                    regex.search(r'\p{Ll}\p{Lu}', form) or
                    not regex.search(r'\p{Ll}', form)
                ):
                    yield (form, 'PROPER')
                else:
                    yield(form, 'NOT_PROPER')
            is_sentence_start = False


def get_split_articles():
    '''
        Reads WikiExtractor.py output from stdin, yields tuples:

            (page_id, word_occurrences)

        where word_occurrences is an array of tuples:
            (original_word_form, 'PROPER'|'NOT_PROPER'|'MAYBE_PROPER')
    '''
    for page_json in fileinput.input():
        page = json.loads(page_json)

        # Remove "See also" sections.
        page['text'] = regex.sub(
            r'\nSection::::(Kirjallisuutta|Aiheesta muualla|Katso myös)\..*', '\n', page['text'], flags=regex.DOTALL)

        # remove some elements (NB: expecting that none of these tag names cannot be nested)
        page['text'] = regex.sub(r'<(ref|hiero|math|gallery|source\b)[^>]*>.*?</\1>', ' ', page['text'],
                                 flags=regex.DOTALL+regex.IGNORECASE)

        # remove soft hyphens
        page['text'] = regex.sub(r'\u00AD', '', page['text'])

        # remove section and bullet markers
        page['text'] = regex.sub(r'\nSection::::', '\n', page['text'])
        page['text'] = regex.sub(r'\nBULLET::::- ', '\n', page['text'])

        occurrences = list(extract_words(page['text']))

        yield (page['id'], occurrences)
