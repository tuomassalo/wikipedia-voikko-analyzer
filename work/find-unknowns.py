import regex
# from extractor import extract_words
from analyzer import analyze_word
from plaintextreader import get_split_articles


for (page_id, occurrences) in get_split_articles():

    # count the number of occurrence in this article
    word_occurrence = dict()

    for (word, properness, sentence) in occurrences:
        if(len(word) >= 5):
            analysis = analyze_word(word)
            if(len(analysis) == 0):
                word_occurrence[word] = word_occurrence.get(word, 0) + 1

    for (word, cnt) in word_occurrence.items():
        print(page_id, cnt, word)
