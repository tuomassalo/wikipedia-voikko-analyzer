import regex
# from extractor import extract_words
from analyzer import analyze_word
from plaintextreader import get_split_articles


prev_adjective = None

for (page_id, occurrences) in get_split_articles():

    # count the number of occurrence in this article
    word_occurrence = dict()

    for (word, properness, sentence) in occurrences:

        # if prev_adjective:
        #     analysis = analyze_word(word)
        #     if(len(analysis) == 1 and analysis[0]['CLASS'] == 'nimisana' and analysis[0]['SIJAMUOTO'] == prev_adjective['analysis'][0]['SIJAMUOTO']):
        #         print(prev_adjective['analysis'][0]['BASEFORM'], analysis[0]['BASEFORM'], '<==', prev_adjective['word'], word)
        #     prev_adjective = None

        # elif word.startswith("puna") or word.startswith("punoitt"):
        #     analysis = analyze_word(word)
        #     if(len(analysis) == 1):
        #         if(analysis[0]['CLASS'] == 'laatusana'):
        #             prev_adjective = dict(word=word, analysis=analysis)
        #         elif(analysis[0]['CLASS'] == 'nimisana' and '=' in analysis[0]['STRUCTURE'][1:]):
        #             print(analysis[0]['BASEFORM'], '<==', word)

        if "pun" in word[2:]:
            analysis = analyze_word(word)
            if len(analysis) == 1:
                if analysis[0]['BASEFORM'].endswith('punainen'):
                    print(analysis[0]['BASEFORM'], '<==', word)
