# adscite
Get cites from ADSabs

==== REQUIREMENTS ====
Python 2.7.15
You must to have installed wkhtmltopdf and pdfunite
You must to have the apikey for ads (edit get-cites.py and add the apikey in line 27)

Install requirements.txt
    - pip install -r requirements.txt

==== USE ====

./run.sh 'Diaz-Gonzalez, D.; Diaz-Gonzalez, Daniel Jacobo' 9999

'Diaz-Gonzalez,D.; Diaz-Gonzalez, Daniel Jacobo' => Author in multiples formats separated by ';'.
9999 => The N=9999 papers with highest citation number. 

--- Output: fullreport.pdf
