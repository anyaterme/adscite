import ads
import time
import pdfkit
import sys
import datetime
import pickle

def show_exc(e):
    import sys

    exc_type, exc_obj, exc_tb = sys.exc_info()
    return ("ERROR ===:> [%s in %s:%d]: %s" % (exc_type, exc_tb.tb_frame.f_code.co_filename, exc_tb.tb_lineno, str(e)))

def first_item(items):
    if type(items) is list:
        return items[0]
    else:
        return items

author = ['Gonzalez-Martin, O.', 'Gonzalez-Martin, Omaira']
papers = ads.SearchQuery(q=f"author:'{author[0]}'  collection:astronomy", sort="date", rows=2000,  fl=['bibcode','doi','author','year','title','citation_count','citation','pub'])

counter = 0
types_a = {}
types_b = {}
autocites = {}
list_papers = {}
citations = {}
for paper in papers:
    counter += 1
    type_a = []
    type_b = []
    autocite = []
    try:
        print("Getting info about {0} [{1}].... ".format(paper.title, paper.year))
#         query_str = 'citations(bibcode:"{0}" OR doi:"{0}")'.format(paper.bibcode)
#         cites_papers = ads.SearchQuery(q=query_str, rows=5000)
        cites_papers = paper.citation
        if cites_papers is None:
            continue
        counter_cites = 0
        for bibcode in cites_papers:
            try:
                if (bibcode not in citations.keys()):
                    query_str = 'bibcode:"{0}"'.format(bibcode)
                    cite = list(ads.SearchQuery(q=query_str, fl=['title','pub','author', 'bibcode', 'year']))[0]
                    citations[bibcode] = cite
                else:
                    cite = citations[bibcode]
            except:
                citations[bibcode] = None
                cite = None
            if cite is not None:
                is_autocite = False
                counter_cites += 1
                for selfauthor in author:
                    if selfauthor in cite.author:
                        is_autocite = True
                        break
                if is_autocite:
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
    except Exception as e:
        print(show_exc(e))
        sys.exit()

prefix = int(time.time())
print("")

lista = [types_a, types_b, autocites, list_papers]

with open(f'{prefix}_cites.bin', 'wb') as binfile:
    pickle.dump(lista, binfile)

print ("Info request finished".ljust(100))
