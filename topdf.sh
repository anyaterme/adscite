#!/bin/sh
for f in $(ls *.html);
do
	filename=$(echo $f|cut -d'.' -f1)
	wkhtmltopdf -L 15mm -T 15mm -B 15mm -R 15mm $f $filename.pdf
done

pdfunite *.pdf fullreport.pdf
