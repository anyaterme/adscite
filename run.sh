#!/bin/sh
python ads.py && iconv -t utf-16 externals.html > externals16.html && iconv -t utf-16 noautocitas.html>noautocitas16.html && iconv -t utf-16 noautocitasfull.html > noautocitasfull16.html && mv externals16.html externals.html && mv noautocitas16.html noautocitas.html && mv noautocitasfull16.html noautocitasfull.html && ./topdf.sh
