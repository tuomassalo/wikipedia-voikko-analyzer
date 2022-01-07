import regex
# from extractor import extract_words
from analyzer import analyze_word
from plaintextreader import get_split_articles


prev_adjective = False

for (page_id, occurrences) in get_split_articles():

    # count the number of occurrence in this article
    word_occurrence = dict()

    for (word, properness, sentence) in occurrences:

        analysis = analyze_word(word)
        adj_analysis = next(filter(lambda a: a['CLASS'] == 'laatusana', analysis), False)
        if adj_analysis:
            prev_adjective = adj_analysis['BASEFORM']
            continue
        
        elif prev_adjective:
            subj_analysis = next(filter(lambda a: a['CLASS'] == 'nimisana', analysis), False)
            if subj_analysis:
                if subj_analysis['BASEFORM'][0:2] == prev_adjective[0:2]:
                    print(prev_adjective, subj_analysis['BASEFORM'], ' <== ', sentence)

        prev_adjective = False
        
