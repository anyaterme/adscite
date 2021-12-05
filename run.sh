#!/bin/sh
rm -f *.html *.pdf 2> /dev/null
python cites.py "${1}"
python topdf.py 2> /dev/null > /dev/null
pdfunite *.pdf fullreport.pdf 2> /dev/null > /dev/null
rm -f *.html 0*.pdf 2> /dev/null
