import ads
import time
import pdfkit
import sys
import datetime

def show_exc(e):
    import sys

    exc_type, exc_obj, exc_tb = sys.exc_info()
    return ("ERROR ===:> [%s in %s:%d]: %s" % (exc_type, exc_tb.tb_frame.f_code.co_filename, exc_tb.tb_lineno, str(e)))


def first_item(items):
    if type(items) is list:
        return items[0]
    else:
        return items

#ads.config.token = 'Ekk7tm7P8bK6uCBLBYUllIpnv1NO4H4DKcNo7Xaz'
ads.config.token = '1yepOSln5yBKIroE6CAUbYym7cOH8h8K20fLXgIU'

papers = ads.SearchQuery(q='author:("Pasetto, A." OR "Pasetto, Alice")  year:2018-2021 property:refereed collection:astronomy', sort="date", rows=2000)

counter = 0
types_a = {}
types_b = {}
autocites = {}
list_papers = {}
a,b = 'áéíóúüñÁÉÍÓÚÜÑäëïöüÄËÏÖÜ','aeiouunAEIOUUNaeiouAEIOU'
trans=str.maketrans(a,b)
for paper in papers:
    counter += 1
    type_a = []
    type_b = []
    autocite = []
    print("Getting info about {0} [{1}].... ".format(paper.title, paper.year))
    try:
        query_str = 'citations(bibcode:"{0}" OR doi:"{0}")'.format(paper.doi[0])
        cites_papers = ads.SearchQuery(q=query_str)
        counter_cites = 0
        for cite in cites_papers:
            counter_cites += 1
            if ('Pasetto, A.' in cite.author or 'Pasetto, Alice' in cite.author) :
                autocite.append(cite)
            else:
                in_papers = set([author.translate(trans) for author in paper.author])
                in_cites = set([author.translate(trans) for author in cite.author])
                in_paper_aux = []
                for author in in_papers:
                    fields = author.split(',')
                    aux = fields[0]
                    cadena = ''
                    for f in fields[1:]:
                        cadena += f.strip()[0]+'.'
                    in_paper_aux.append('{}, {}'.format(aux, cadena))

                in_cites_aux = []
                for author in in_cites:
                    fields = author.split(',')
                    aux = fields[0]
                    cadena = ''
                    for f in fields[1:]:
                        cadena += f.strip()[0]+'.'
                    in_cites_aux.append('{}, {}'.format(aux, cadena))

                in_papers = in_paper_aux
                in_cites = in_cites_aux
                #cites_a = list(set(paper.author) & set(cite.author))
                cites_a = list(set(in_papers) & set(in_cites))
                type_b.append(cite)
                if len(cites_a) == 0:
                    type_a.append(cite)
#                 if len(cites_a) > 0:
#                     type_b.append(cite)
#                 else:
#                     type_a.append(cite)
    except Exception as e:
        print (show_exc(e))
        pass
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
f.write('<h1>Citas a trabajo de investigación de Pasetto, Alice</h1>\n')
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
