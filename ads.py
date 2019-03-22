#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import time
import urllib2
import urllib
#from BeautifulSoup import BeautifulSoup# parsing
from xml.dom import minidom
#import datetime
import argparse
import getpass
import codecs
import unicodedata
import re
import datetime

def remove_accents(cadena):
    s = ''.join((c for c in unicodedata.normalize('NFD',unicode(cadena)) if unicodedata.category(c) != 'Mn'))
    try:
        return s.decode()
    except:
        return cadena

def same_author(author1, author2):
    author1 = remove_accents(author1.replace(' ','-').replace(".",""))
    author2 = remove_accents(author2.replace(' ','-').replace(".",""))
    author1 = author1.split(',')
    author2 = author2.split(',')
    surname1 = author1[0]
    surname2 = author2[0]
    if surname1.upper() == surname2.upper():
        try:
            name1 = re.sub("[a-z]","",author1[1])
            name2 = re.sub("[a-z]","",author2[1])
            return ((name1.startswith(name2)) or (name2.startswith(name1)))
        except Exception as e:
            mystr = "======================WARNING %s : %s <-> %s " % (e, author1, author2)
            print (mystr.encode('latin-1', 'replace'))
            return (True)
    return False

def ads(author=""):
    if (author != ""):
        headLatex ="<html><body>\n"

        tailLatex = "</body></html>"

        #author = "Gonzalez Martin, Omaira"
        #author = "Carrasco Gonzalez, Carlos"
        #author = "Palau, Aina"
        authorOrig = author
        author = author.replace(" ","+").replace(",","%2C")


        urlSearch = "http://adsabs.harvard.edu/cgi-bin/nph-abs_connect?db_key=AST&db_key=PRE&qform=AST&arxiv_sel=astro-ph&arxiv_sel=cond-mat&arxiv_sel=cs&arxiv_sel=gr-qc&arxiv_sel=hep-ex&arxiv_sel=hep-lat&arxiv_sel=hep-ph&arxiv_sel=hep-th&arxiv_sel=math&arxiv_sel=math-ph&arxiv_sel=nlin&arxiv_sel=nucl-ex&arxiv_sel=nucl-th&arxiv_sel=physics&arxiv_sel=quant-ph&arxiv_sel=q-bio&sim_query=YES&ned_query=YES&adsobj_query=YES&aut_logic=OR&obj_logic=OR&author="+author+"&object=&start_mon=&start_year=&end_mon=&end_year=&ttl_logic=OR&title=&txt_logic=OR&text=&nr_to_return=200&start_nr=1&jou_pick=ALL&ref_stems=&data_and=ALL&group_and=ALL&start_entry_day=&start_entry_mon=&start_entry_year=&end_entry_day=&end_entry_mon=&end_entry_year=&min_score=&sort=CITATIONS&data_type=SHORT_XML&aut_syn=YES&ttl_syn=YES&txt_syn=YES&aut_wt=1.0&obj_wt=1.0&ttl_wt=0.3&txt_wt=3.0&aut_wgt=YES&obj_wgt=YES&ttl_wgt=YES&txt_wgt=YES&ttl_sco=YES&txt_sco=YES&version=1"
        if (start_year != None) and (start_year != ""):
            urlSearch = "%s&start_year=%s" % (urlSearch, start_year)
        if (end_year != None) and (end_year != ""):
            urlSearch = "%s&end_year=%s" % (urlSearch, end_year)
        response=urllib2.urlopen(urlSearch)
        data = response.read()
        xml = minidom.parseString(data)
        articles = xml.getElementsByTagName("record")
        f = codecs.open("001_externals.html", "w", "utf-8")
        f2 = codecs.open("002_noautocitas.html", "w", "utf-8")
        f3 = codecs.open("noautocitasfull.html", "w", "utf-8")
        f4 = codecs.open("003_autocitas.html", "w", "utf-8")
        f5 = codecs.open("000_header.html", "w", "utf-8")
        f.write(headLatex)
        f2.write(headLatex)
        f3.write(headLatex)
        f4.write(headLatex)
        f5.write(headLatex)
        f.write("<h2>Citas Tipo A</h2>")
        f2.write("<h2>Citas Tipo B</h2>")
        f3.write("<h2>Citas Tipo B</h2>")
        f4.write("<h2>Citas Tipo C</h2>")
        f5.write("<h1>Citas a trabajo de investigaci&oacute;n de %s</h1>" % authorOrig)
        a_counter = 0
        b_counter = 0
        c_counter = 0
        cites_to_art = []

        cont = 0
        for article in articles:
            cont+=1
            externalArts = []
            noautoArts = []
            autoArts = []
            title = article.getElementsByTagName("title").item(0).firstChild.nodeValue
            links = article.getElementsByTagName("link")
            authors = article.getElementsByTagName("author")
            mystr = "Review %s" % (title)
            print (mystr.encode('latin-1', 'replace'))
            line = "<h3>\"%s\": " % (title)
            line4 = "<h3>\"%s\": " % (title)
            line2 = "<h3>\"%s\": " % (title)
            for author in authors:
                line = "%s %s;" % (line, remove_accents(author.firstChild.nodeValue))
                line2 = "%s %s;" % (line2, remove_accents(author.firstChild.nodeValue))
            line = ("%s. %s</h3> \n" % (line, article.getElementsByTagName("bibcode").item(0).firstChild.nodeValue))
            line2 = ("%s. %s</h3> \n" % (line2, article.getElementsByTagName("bibcode").item(0).firstChild.nodeValue))
            line4 = ("%s. %s</h3> \n" % (line, article.getElementsByTagName("bibcode").item(0).firstChild.nodeValue))
            for link in links:
                if (link.getAttribute("type") == "CITATIONS"):
                    url = "%s&data_type=SHORT_XML" % link.getElementsByTagName("url").item(0).firstChild.nodeValue
                    response = urllib2.urlopen(url)
                    refXml = minidom.parseString(response.read())
                    refArticles = refXml.getElementsByTagName("record")
                    cites_to_art.append(len(refArticles))
                    for refArticle in refArticles:
                        refTitle = refArticle.getElementsByTagName("title").item(0).firstChild.nodeValue
                        print "...Checking %s" % (refTitle.encode('utf-8'))
                        refAuthors = refArticle.getElementsByTagName("author")
                        external = True
                        autocita = False
                        for refAuthor in refAuthors:
                            if (same_author(authorOrig, refAuthor.firstChild.nodeValue)):
                                autocita = True
                            for author in authors:
                                if (same_author(author.firstChild.nodeValue, refAuthor.firstChild.nodeValue)):
                                    mystr = ("\t%s == %s" % (author.firstChild.nodeValue, refAuthor.firstChild.nodeValue))
                                    print (mystr.encode('latin-1','replace'))
                                    external = False
                        if external:
                            if (refArticle not in externalArts):
                                externalArts.append(refArticle)
                                a_counter += 1
                        if not autocita:
                            if (refArticle not in noautoArts):
                                noautoArts.append(refArticle)
                                if (refArticle not in externalArts):
                                    b_counter += 1
                        else:
                            if (refArticle not in autoArts):
                                autoArts.append(refArticle)
                                c_counter += 1
            if (len(externalArts) > 0):
                line = ("%s\n<ol>" % line)
                for ext in externalArts:
                    try:
                        line = "%s<li>\"%s\":" % (line, (ext.getElementsByTagName("title").item(0).firstChild.nodeValue.decode('utf-8')))
                    except:
                        line = "%s<li>\"%s\":" % (line, unicode(ext.getElementsByTagName("title").item(0).firstChild.nodeValue))
                    for extAuthor in ext.getElementsByTagName("author"):
                        try:
                            line = "%s %s;" % (line, (extAuthor.firstChild.nodeValue.decode('utf-8')))
                        except:
                            line = "%s %s;" % (line, unicode(extAuthor.firstChild.nodeValue))
                    try:
                        line = "%s %s</li>" % (line, (ext.getElementsByTagName("bibcode").item(0).firstChild.nodeValue.decode('utf-8')))
                    except:
                        line = "%s %s</li>" % (line, (ext.getElementsByTagName("bibcode").item(0).firstChild.nodeValue))
                line = ("%s</ol><br>" % line)
                f.write(line)
            line3 = line2
            if ( (len(noautoArts)>0) and (len(noautoArts) != len(externalArts))):
                line2 = ("%s\n<ol>" % line2);
                for ext in noautoArts:
                    if (ext not in externalArts):
                        try:
                            line2 = "%s<li>\"%s\":" % (line2, (ext.getElementsByTagName("title").item(0).firstChild.nodeValue.decode('utf-8')))
                        except:
                            line2 = "%s<li>\"%s\":" % (line2, unicode(ext.getElementsByTagName("title").item(0).firstChild.nodeValue))
                        for extAuthor in ext.getElementsByTagName("author"):
                            try:
                                line2 = "%s %s;" % (line2, (extAuthor.firstChild.nodeValue.decode('utf-8')))
                            except:
                                line2 = "%s %s;" % (line2, unicode(extAuthor.firstChild.nodeValue))
                        try:
                            line2 = "%s %s</li>" % (line2, (ext.getElementsByTagName("bibcode").item(0).firstChild.nodeValue.decode('utf-8')))
                        except:
                            line2 = "%s %s</li>" % (line2, (ext.getElementsByTagName("bibcode").item(0).firstChild.nodeValue))
                f2.write("%s</ol><br>" % line2)

            if ((len(noautoArts)>0)):
                line3 = ("%s\n<ol>" % line3);
                for ext in noautoArts:
                    try:
                        line3 = "%s<li>\"%s\":" % (line3, (ext.getElementsByTagName("title").item(0).firstChild.nodeValue.decode('utf-8')))
                    except:
                        line3 = "%s<li>\"%s\":" % (line3, unicode(ext.getElementsByTagName("title").item(0).firstChild.nodeValue))
                    for extAuthor in ext.getElementsByTagName("author"):
                        try:
                            line3 = "%s %s;" % (line3, (extAuthor.firstChild.nodeValue.decode('utf-8')))
                        except:
                            line3 = "%s %s;" % (line3, unicode(extAuthor.firstChild.nodeValue))
                    try:
                        line3 = "%s %s</li>" % (line3, (ext.getElementsByTagName("bibcode").item(0).firstChild.nodeValue.decode('utf-8')))
                    except:
                        line3 = "%s %s</li>" % (line3, (ext.getElementsByTagName("bibcode").item(0).firstChild.nodeValue))
                f3.write("%s</ol><br>" % line3)
            if ((len(autoArts)>0)):
                line4 = ("%s\n<ol>" % line4);
                for ext in autoArts:
                    try:
                        #line4 = "%s<li>\"%s\":" % (line4, (ext.getElementsByTagName("title").item(0).firstChild.nodeValue.decode('utf-8')))
                        line4 = "%s<li>\"%s\":" % (line4, remove_accents(ext.getElementsByTagName("title").item(0).firstChild.nodeValue))
                    except:
                        line4 = "%s<li>\"%s\":" % (line4, unicode(ext.getElementsByTagName("title").item(0).firstChild.nodeValue))
                    for extAuthor in ext.getElementsByTagName("author"):
                        try:
                            line4 = "%s %s;" % (line4, remove_accents(extAuthor.firstChild.nodeValue))
                            #line4 = "%s %s;" % (line4, (extAuthor.firstChild.nodeValue.decode('utf-8')))
                        except:
                            line4 = "%s %s;" % (line4, unicode(extAuthor.firstChild.nodeValue))
                    try:
                        #line4 = "%s %s</li>" % (line4, (ext.getElementsByTagName("bibcode").item(0).firstChild.nodeValue.decode('utf-8')))
                        line4 = "%s %s</li>" % (line4, remove_accents(ext.getElementsByTagName("bibcode").item(0).firstChild.nodeValue))
                    except:
                        line4 = "%s %s</li>" % (line4, (ext.getElementsByTagName("bibcode").item(0).firstChild.nodeValue))
                f4.write("%s</ol><br>" % line4)

        total_cites = a_counter + b_counter + c_counter

        cites_to_art = sorted(cites_to_art, reverse=True)
        numH = 0
        for idx,cites in enumerate(cites_to_art):
            if  cites < idx+1:
                break
            numH = idx+1

        f5.write("<h2>Resumen</h2>")
        f5.write('<br><strong>Fecha:</strong> %s<br>' % datetime.datetime.today().strftime("%Y/%M/%d"))
        f5.write('<br><strong>Total citas:</strong> %d<br>' % (total_cites))
        f5.write('<br><strong>Tipo A:</strong> %d (%.1lf %%)<br>' % (a_counter, a_counter*100./total_cites))
        f5.write('<br><strong>Tipo B:</strong> %d (%.1lf %%)<br>' % (b_counter, b_counter*100./total_cites ))
        f5.write('<br><strong>Tipo C:</strong> %d (%.1lf %%)<br>' % (c_counter, c_counter*100./total_cites ))
        f5.write('<br><strong>N&uacute;mero H:</strong> %d<br>' % (numH))
        f5.write('<br>Fuente: SAO/NASA ADS = http://adsabs.harvard.edu/abstract service.html<br>')
        f5.write('<br><br><h2>Definiciones SNI</h2><br>')
        f5.write('<br><strong>Citas Tipo A: </strong>Aquellas citas realizadas en productos de investigaci&oacute;n firmados por uno o varios autores dentro de los cuales no hay ninguno que sea autor del trabajo referido a la cita.<br>')
        f5.write('<br><strong>Citas Tipo B: </strong>Aquellas citas realizadas en productos de investigaci&oacute;n firmados por uno o varios autores dentro de los cuales puede haber uno o varios autores del trabajo referido en la cita, pero no el investigador mismo.<br>')
        f5.write('<br><strong>Citas Tipo C: </strong>Auto citas.<br>')
        f.write(tailLatex)
        f2.write(tailLatex)
        f3.write(tailLatex)
        f4.write(tailLatex)
        f5.write(tailLatex)
        f.close()
        f2.close()
        f3.close()
        f4.close()
        f5.close()
        return True
    else:
        print "You have to indicate the author"
        return False

ap = argparse.ArgumentParser(description="Dowonload data of archive archive.nrao.edu")
ap.add_argument("-a", "--author", help = "Author's name", required=False)
ap.add_argument("-from", "--year", help = "Author's name", required=False)
ap.add_argument("-to", "--yearend", help = "Author's name", required=False)
args = vars(ap.parse_args())

author = args["author"]
start_year = args["year"]
end_year = args["yearend"]
if (author == None):
    author = raw_input("Author's name: ")
if (start_year == None):
    start_year= raw_input("From Year (YYYY): ")
if (end_year == None):
    end_year= raw_input("To Year (YYYY): ")
if ads(author):
    exit(0)
else:
    exit(1)
