#!/bin/bash

# This script feeds the multistream dump to WikiExtractor.py one stream at a time.
# https://en.wikipedia.org/wiki/Wikipedia:Database_download#Should_I_get_multistream?
# The XML file header is prepended to each chunk.

# WikiExtractor.py output is piped to find-$Script.py that tokenizes the plaintext to
# words, analyzes each one and prints something. This output is redirected to
# output/$Script-<offset>.txt files.

# If the execution of this script is interrupted, the next run will skip all the streams
# that are already processed.

Script="$1"

if [ ! -s "find-$Script.py" ]; then
  echo 'ERROR: Please give one argument, e.g. `unknowns`, and make sure that `find-unknowns.py` is found in the same directory as this script.' >&2
  exit 1
fi

set -e

MultistreamIndexFile='wikipedia/fiwiki-latest-pages-articles-multistream-index.txt.bz2'
MultistreamXmlFile='wikipedia/fiwiki-latest-pages-articles-multistream.xml.bz2'
MultistreamXmlFileSize=$(stat -c%s "$MultistreamXmlFile")

Header=$(bunzip2 < $MultistreamXmlFile|head -n 1000|perl -0777 -wpe 's!(</siteinfo>).*!$1\n!s')

PrevOffset=0
for Offset in $(
    bunzip2 < $MultistreamIndexFile | cut -d: -f1 | uniq ; echo $MultistreamXmlFileSize
); do
  if [ "$PrevOffset" != "0" ]; then

    Outfile="output/$Script-$PrevOffset.txt"

    perl -e 'printf("%6.2f", 100*'$Offset/$MultistreamXmlFileSize')'
    echo -n " % (Offset=$PrevOffset)" >&2
    if [ -f $Outfile ]; then
      echo " [Skipping, already exists]" >&2
    else
      echo >&2

      Length=$(($Offset-$PrevOffset))
      PrevOffsetPlusOne=$(($PrevOffset+1))

      (
        echo "$Header"
        dd status=none if=$MultistreamXmlFile bs=1 skip=$PrevOffset count=$Length | bunzip2
      ) |
      python3 /usr/src/WikiExtractor.py --quiet --json --sections --lists --min_text_length 50 --filter_disambig_pages --output - --no_templates - |
      python3 find-$Script.py > $Outfile.part

      mv -f $Outfile.part $Outfile
    fi
  fi
  PrevOffset=$Offset
done

echo "100.00 % - DONE!" >&2
