import ads
import time
import pdfkit
import sys
import datetime

def first_item(items):
    if type(items) is list:
        return items[0]
    else:
        return items

#ads.config.token = 'Ekk7tm7P8bK6uCBLBYUllIpnv1NO4H4DKcNo7Xaz'
ads.config.token = '1yepOSln5yBKIroE6CAUbYym7cOH8h8K20fLXgIU'
papers = ads.SearchQuery(q='author:("Palau, Aina" OR "Palau, A.")  property:refereed collection:astronomy', sort="date", rows=2000)

counter = 0
types_a = {}
types_b = {}
autocites = {}
list_papers = {}
for paper in papers:
    counter += 1
    type_a = []
    type_b = []
    autocite = []
    print("Getting info about {0} [{1}].... ".format(paper.title, paper.year))
    query_str = 'citations(bibcode:"{0}" OR doi:"{0}")'.format(paper.doi[0])
    cites_papers = ads.SearchQuery(q=query_str)
    counter_cites = 0
    for cite in cites_papers:
        counter_cites += 1
        if ('Palau, Aina' in cite.author) or ('Palau, A.' in cite.author):
            autocite.append(cite)
        else:
            cites_a = list(set(paper.author) & set(cite.author))
            if len(cites_a) > 0:
                type_b.append(cite)
            else:
                type_a.append(cite)
    types_a[paper.title[0]] = type_a
    types_b[paper.title[0]] = type_b
    autocites[paper.title[0]] = autocite
    list_papers[paper.title[0]] = paper

print("")
type_a = 0
type_b = 0
autocite = 0
for paper in list_papers:
    type_a = type_a + len(types_a[paper])
    type_b = type_b + len(types_b[paper])
    autocite = autocite + len(autocites[paper])

print (type_a, type_b, autocite)

prefix = time.time()
print ("Info request finished".ljust(100))



print ("Info request finished".ljust(100))
#f = open("aux_summary.html" % time.time())
f = open("%d_cites_a.html" % prefix, "w")
f.write('<html><head>   <meta charset="UTF-8"></meta></head><body style="padding:0 5%">\n')
f.write('<h1>Citas Tipo A</h1>\n')
aux_counter = 0
for title in types_a:
    paper = list_papers[title]
    cites = types_a[title]
    if (len(cites) > 0):
        f.write('<h5>"{0}": {1}. {2}</h5>\n'.format(title,';'.join(paper.author), first_item(paper.year))) 
        f.write('<ol>\n')
        for cite in cites:
            aux_counter += 1
            f.write('<li>"{0}": {1}. {2}</li>\n'.format(cite.title[0],';'.join(cite.author), first_item(cite.year)))
        f.write('</ol>\n')
    print("Processing Type A...")
print ("")
type_a_counter = aux_counter
f.close()

f = open("%d_cites_b.html" % prefix, "w")
f.write('<html><head>   <meta charset="UTF-8"></meta></head><body style="padding:0 5%">\n')
f.write('<h1>Citas Tipo B</h1>\n')
aux_counter = 0
for title in types_b:
    paper = list_papers[title]
    cites = types_b[title]
    if (len(cites) > 0):
        f.write('<h5>"{0}": {1}. {2}</h5>\n'.format(title,';'.join(paper.author), first_item(paper.year))) 
        f.write('<ol>\n')
        for cite in cites:
            aux_counter += 1
            f.write('<li>"{0}": {1}. {2}</li>\n'.format(cite.title[0],';'.join(cite.author), first_item(cite.year)))
        f.write('</ol>\n')
    print("Processing Type B...")
type_b_counter = aux_counter
print ("")
f.close()

f = open("%d_autocites.html" % prefix, "w")
f.write('<html><head><meta charset="UTF-8"></meta></head><body style="padding:0 5%">\n')
f.write('<h1>Autocitas</h1>\n')
aux_counter = 0
for title in autocites:
    paper = list_papers[title]

    cites = autocites[title]
    if (len(cites) > 0):
        f.write('<h5>"{0}": {1}. {2}</h5>\n'.format(title,';'.join(paper.author), first_item(paper.year))) 
        f.write('<ol>\n')
        for cite in cites:
            aux_counter += 1
            f.write('<li>"{0}": {1}. {2}</li>\n'.format(cite.title[0],';'.join(cite.author), first_item(cite.year)))
        f.write('</ol>\n')
    print("Processing Autocites...")
f.write('</body></html>\n')
f.close()
autocites_counter = aux_counter
print("\nGenerating Summary")
f = open("%d_summary.html" % prefix, "w")
f.write('<html><head><meta charset="UTF-8"></meta></head><body style="padding:0 5%">\n')
f.write('<h1>Citas a trabajo de investigación de Palau Puigvert, Aina</h1>\n')
f.write('<h2>Resumen</h2>\n')
f.write('<strong>Fecha:</strong> %s<br><br>\n' % datetime.datetime.today().strftime('%Y/%m/%d'))
f.write('<strong>Total Citas:</strong> %d<br><br>\n' % (type_a_counter + type_b_counter + autocites_counter))
f.write('<strong>Tipo A:</strong> %d (%.2lf %%)<br><br>\n' % (type_a_counter, type_a_counter/(type_a_counter + type_b_counter + autocites_counter)*100))
f.write('<strong>Tipo B:</strong> %d (%.2lf %%)<br><br>\n' % (type_b_counter, type_b_counter/(type_a_counter + type_b_counter + autocites_counter)*100))
f.write('<strong>Autocitas:</strong> %d (%.2lf %%)<br><br>\n' % (autocites_counter, autocites_counter/(type_a_counter + type_b_counter + autocites_counter)*100))
f.write('Fuente: SAO/NASA ADS = https://ui.adsabs.harvard.edu<br>')
f.write('<h2>Definiciones SNI</h2>\n')
f.write('<strong>Citas Tipo A:</strong> Aquellas citas realizadas en productos de investigación firmados por uno o varios autores dentro de los cuales no hay ninguno que sea autor del trabajo referido a la cita.<br><br>\n')
f.write('<strong>Citas Tipo B:</strong> Aquellas citas realizadas en productos de investigación firmados por uno o varios autores dentro de los cuales puede haber uno o varios autores del trabajo referido en la cita, pero no el investigador mismo.<br><br>\n')
f.write('<strong>Autocitas:</strong> Aquellas citas realizadas en productos de investigación firmados por el investigador mismo.<br>\n')
f.close()
print("\nFinished")
