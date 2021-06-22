#!/bin/sh
rm -f *.html *.pdf 2> /dev/null
python cites.py
python topdf.py
pdfunite *.pdf fullreport.pdf
