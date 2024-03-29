# -*- coding: utf-8 -*-
import ads
import time
import pdfkit
import sys
import datetime
import argparse

def show_exc(e):
    import sys

    exc_type, exc_obj, exc_tb = sys.exc_info()
    return ("ERROR ===:> [%s in %s:%d]: %s" % (exc_type, exc_tb.tb_frame.f_code.co_filename, exc_tb.tb_lineno, str(e)))


def first_item(items):
    if type(items) is list:
        return items[0]
    else:
        return items

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get Cites from ADS')
    parser.add_argument('author', type=str, help="Author (multiples references separated by ;)")
    parser.add_argument('--limit', type=int, default=999999, help="N first papers")
    parser.add_argument('--summary', action='store_true', default=False, help="Only summary in summary.txt")

    args = parser.parse_args()
    ads.config.token = ''

    ref_authors = args.author.split(';')
    ref_authors_list = ['"{}"'.format(i.strip()) for i in ref_authors]
    ref_authors = ' OR '.join(ref_authors_list)

    papers = ads.SearchQuery(q='author:({}) year:1960-2021'.format(ref_authors), sort="citation_count desc", rows=2000)

    counter = 0
    types_a = {}
    types_b = {}
    autocites = {}
    list_papers = {}
    a,b = 'áéíóúüñÁÉÍÓÚÜÑäëïöüÄËÏÖÜ','aeiouunAEIOUUNaeiouAEIOU'
    trans=str.maketrans(a,b)
    summary_txt = open ('./summary.txt','w')
    count_A = []
    count_B = []
    count_C = []
    for paper in papers:
        cit_count = paper.citation_count
        summary_txt.write('[{}] - {}\n'.format(paper.title, cit_count))
        if args.summary:
            continue
        if counter == args.limit:
            break
        type_a = []
        type_b = []
        autocite = []
        print("Getting info about {0} [{1}].... ".format(paper.title, paper.year))
        if paper.bibcode is not None and paper.bibcode != "":
            query_str = 'citations(bibcode:{0})'.format(paper.bibcode)
        elif paper.doi is not None:
            query_str = 'citations(doi:"{0}")'.format(paper.doi[0])
        else:
            query_str = None

        if query_str is not None:
            rows = 2000
            page = 0
            in_papers = set([author.translate(trans) for author in paper.author])
            while rows == 2000:
                rows = 0
                cites_papers = ads.SearchQuery(q=query_str, rows=2000, start=2000*page)
                if cites_papers is not None:
                    page += 1
                    for cite in cites_papers:
                        rows += 1
                        try:
                            is_autocite = False
                            for i in ref_authors_list:
                                if i.replace('"','') in cite.author:
                                    autocite.append(cite)
                                    is_autocite = True
                                    break
                            if not is_autocite:
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
                                # type_b.append(cite) #Susana Change
                                if len(cites_a) == 0:
                                    type_a.append(cite)
                                else:
                                    type_b.append(cite)
                        except Exception as e:
                            type_b.append(cite)
                            print (show_exc(e))
                            pass

        types_a[paper.title[0]] = type_a
        types_b[paper.title[0]] = type_b
        autocites[paper.title[0]] = autocite
        total_paper_cites = len(type_a) + len(type_b) + len(autocite)
        if cit_count != total_paper_cites:
            print ("====== Warning: in paper[{}] ({}) {} != {}".format(counter, paper.title[0], cit_count, total_paper_cites))
        list_papers[paper.title[0]] = paper
        counter += 1
        count_A.append(len(type_a))
        count_B.append(len(type_b))
        count_C.append(len(autocite))



    summary_txt.close()


    if not args.summary:
        print("")
        type_a = 0
        type_b = 0
        autocite = 0
        for paper in list_papers:
            type_a = type_a + len(types_a[paper])
            type_b = type_b + len(types_b[paper])
            autocite = autocite + len(autocites[paper])

        prefix = time.time()
        print ("Info request finished".ljust(100))
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
        #type_a_counter = aux_counter
        type_a_counter = sum(count_A)
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
                    cite_author = cite.author
                    if cite.author is None:
                        cite_author = ''
                    f.write('<li>"{0}": {1}. {2}</li>\n'.format(cite.title[0],';'.join(cite_author), first_item(cite.year)))
                f.write('</ol>\n')
        #type_b_counter = aux_counter
        type_b_counter = sum(count_B)
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
        f.write('</body></html>\n')
        f.close()
        autocites_counter = aux_counter
        autocites_counter = sum(count_C)
        total = type_a_counter + type_b_counter + autocites_counter
        print("\nGenerating Summary")
        f = open("%d_summary.html" % prefix, "w")
        f.write('<html><head><meta charset="UTF-8"></meta></head><body style="padding:0 5%">\n')
        f.write('<h1>Citas a trabajo de investigación de {}</h1>\n'.format(ref_authors_list[0]))
        f.write('<h2>Resumen</h2>\n')
        f.write('<strong>Fecha:</strong> %s<br><br>\n' % datetime.datetime.today().strftime('%Y/%m/%d'))
        f.write('<strong>Total Citas:</strong> %d<br><br>\n' % (total))
        f.write('<strong>Tipo A:</strong> %d (%.2lf %%)<br><br>\n' % (type_a_counter, type_a_counter/(total)*100))
        f.write('<strong>Tipo B:</strong> %d (%.2lf %%)<br><br>\n' % (type_b_counter, type_b_counter/(total)*100))
        f.write('<strong>Autocitas:</strong> %d (%.2lf %%)<br><br>\n' % (autocites_counter, autocites_counter/(total)*100))
        f.write('Fuente: SAO/NASA ADS = https://ui.adsabs.harvard.edu<br>')
        f.write('<h2>Definiciones SNI</h2>\n')
        f.write('<strong>Citas Tipo A:</strong> Aquellas citas realizadas en productos de investigación firmados por uno o varios autores dentro de los cuales no hay ninguno que sea autor del trabajo referido a la cita.<br><br>\n')
        f.write('<strong>Citas Tipo B:</strong> Aquellas citas realizadas en productos de investigación firmados por uno o varios autores dentro de los cuales puede haber uno o varios autores del trabajo referido en la cita, pero no el investigador mismo.<br><br>\n')
        f.write('<strong>Autocitas:</strong> Aquellas citas realizadas en productos de investigación firmados por el investigador mismo.<br>\n')
        f.close()
    print("\nFinished")
