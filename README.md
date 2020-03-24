# wikipedia-voikko-analyzer
Tools to extract text from Finnish Wikipedia and feed it to Voikko.

It uses [WikiExtractor](https://github.com/attardi/wikiextractor) to convert mediawiki format to plaintext. Only the actual text content is analyzed, and *all* templates are ignored.

This repository includes a script, `find-unknowns.py`, that finds all words that Voikko cannot recognize.

### Prerequisites

- Docker and `docker-compose`.

### How to use

- First, download https://dumps.wikimedia.org/fiwiki/latest/fiwiki-latest-pages-articles-multistream-index.txt.bz2 and https://dumps.wikimedia.org/fiwiki/latest/fiwiki-latest-pages-articles-multistream.xml.bz2 to `./work/wikipedia/`

- Run `docker-compose up`

- In another terminal, run `docker exec -ti wikipedia-voikko-analyzer_bulkvoikko_1 ./run.sh unknowns`

The process will write about 9000 files named `work/output/unknowns-*.txt`. Each file contains the unrecognized words of up to 100 Wikipedia articles. The file format:

    <pageid> <occurrence_count> <original_word_form>

NB: To resolve page from pageid, use the URL `https://fi.wikipedia.org/?curid=<pageid>`, e.g. https://fi.wikipedia.org/?curid=42.

A quick (and dirty) script that finds recurring words from the output file:

    perl -C -walne 'print $F[2] if length($F[2])>6' unknowns-*.txt | sort | perl -walne 'BEGIN{$p='X';} if(index($_, $p) == 0 and length() < length($p)+6) {push @o, $_} else { if(@o > 100) {print ""; print for sort @o}; $p=substr($_, 0, length($_)-3); @o=()}' | uniq -c

First, find all unknown words over 6 characters long. Then sort the output. For each word, strip the last three characters and see if the next lines contain the same prefix. If yes, and if more thatn 100 occurrences were found, print all the occurrences.

### How to do something else with this

- Copy `find-unknowns.py` to e.g. `find-compound-words.py`

- Modify to your needs

- Run `docker exec -ti wikipedia-voikko-analyzer_bulkvoikko_1 ./run.sh compound-words`

### How to analyze a single word

    docker exec -ti wikipedia-voikko-analyzer_bulkvoikko_1 python3 -c 'import json; from libvoikko import Voikko; print(json.dumps(Voikko("fi").analyze("alusta"), indent=2, sort_keys=True))'

### How to change the vocabulary

See `GENLEX_OPTS` in `Dockerfile`, and see possible values in https://github.com/voikko/corevoikko/blob/master/tools/bin/voikko-build-dicts.
