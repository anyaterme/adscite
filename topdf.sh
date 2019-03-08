#!/bin/sh
for f in $(ls *.html);
do
	filename=$(echo $f|cut -d'.' -f1)
	wkhtmltopdf $f $filename.pdf

done
