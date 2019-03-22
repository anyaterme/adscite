#!/bin/sh
rm -f *.html *.pdf 2> /dev/null
python ads.py && iconv -t utf-16 001_externals.html > 001_externals16.html && iconv -t utf-16 002_noautocitas.html>002_noautocitas16.html && iconv -t utf-16 noautocitasfull.html > noautocitasfull16.html && mv 001_externals16.html 001_externals.html && mv 002_noautocitas16.html 002_noautocitas.html && mv noautocitasfull16.html noautocitasfull.html && ./topdf.sh
