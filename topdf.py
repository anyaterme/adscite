import ads
import time
import pdfkit
import sys
import datetime
import pickle
import argparse
from fpdf import FPDF

# Definir clase para manejar objetos

# Crear clase para generar PDF
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 10)
        self.cell(0, 10, 'Omaira Gonzalez Martin', 0, 1)

    def add_title(self, text, fontsize=16):
        self.set_font('Arial', 'B', fontsize)
        self.multi_cell(0, 8, text, 0, 1)

    def add_book(self, book):
        self.set_font('Arial', '', 12)
#         text = f'"{first_item(book.title)}". {";".join(book.author)}. {book.pub},{book.year})'
        text = f'"{first_item(book.title)}". {first_item(book.author)} et al.. {book.pub}, {book.year}'
        self.multi_cell(0, 8, text)

    def add_cite(self, cite, prefix=''):
        self.set_font('Arial', '', 10)
        text = f'{prefix}"{first_item(cite.title)}". {first_item(cite.author)} et al. '
        self.multi_cell(0, 6, text)

    def vspace(self, space=8):
        self.cell(0, space, '', 0, 1)


# Crear el PDF


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
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    parser.add_argument('-o', '--output', type=str, default='archivo_combinado.pdf', help='Nombre del archivo PDF de salida')
    args = parser.parse_args()


    with open(args.path, 'rb') as binfile:
        lista = pickle.load(binfile)
        [types_a, types_b, autocites, list_papers] = lista




    pdf = PDF()
    pdf.add_font('Arial', '', '/usr/share/fonts/dejavu/DejaVuSans.ttf', uni=True)


    print ("Info request finished".ljust(100))
    type_a_counter = 0
    type_b_counter = 0
    autocites_counter = 0
    for title in types_a:
        cites = types_a[title]
        type_a_counter += len(cites)
    for title in types_b:
        cites = types_b[title]
        type_b_counter += len(cites)
    for title in autocites:
        cites = autocites[title]
        autocites_counter += len(cites)

    pdf.add_page()
    pdf.add_title('Citas a trabajo de investigactión de Omaira González Martín')
    pdf.add_title(f'Total citas: {type_a_counter + type_b_counter + autocites_counter}')
    pdf.add_title(f'Tipo A: {type_a_counter}')
    pdf.add_title(f'Tipo B: {type_b_counter}')
    pdf.add_title(f'Autocitas: {autocites_counter}')
    pdf.add_title('Fuente: SAO/NASA ADS = https://ui.adsabs.harvard.edu')
    pdf.add_title('Definiciones SNI')
    pdf.add_title('Citas Tipo A: Aquellas citas realizadas por algún autor o grupo de investigación externo a usted o su grupo de trabajo.')
    pdf.add_title('Citas Tipo B: Aquellas citas realizadas en productos de investigación firmados por algún miembro del grupo de trabajo donde se realizó el producto.')
    pdf.add_title('Autocitas: Aquellas citas realizadas en productos de investigación firmados por el investigador mismo.\n')

    pdf.add_page()
    pdf.add_title('Citas Tipo A')
    aux_counter = 0
    for title in types_a:
        aux_counter += 1
        paper = list_papers[title]
        cites = types_a[title]
        type_a_counter += len(cites)
        if (len(cites) > 0):
            pdf.add_book(paper)
            counter = 0
            for cite in cites:
                counter += 1
                pdf.add_cite(cite, prefix=f"{counter}. ")
            pdf.vspace()
        print("Processing Type A: %.2lf %%    " % (aux_counter/len(types_a)*100), end="\r")
    print ("")

    pdf.add_page()
    pdf.add_title('Citas Tipo B')
    aux_counter = 0
    for title in types_b:
        aux_counter += 1
        paper = list_papers[title]
        cites = types_b[title]
        type_b_counter += len(cites)
        if (len(cites) > 0):
            pdf.add_book(paper)
            counter = 0
            for cite in cites:
                counter += 1
                pdf.add_cite(cite, prefix=f"{counter}. ")
        print("Processing Type B: %.2lf %%    " % (aux_counter/len(types_b)*100), end="\r")
    print ("")

    pdf.add_page()
    pdf.add_title('Autocitas')
    aux_counter = 0
    for title in autocites:
        aux_counter += 1
        paper = list_papers[title]
        cites = autocites[title]
        autocites_counter += len(cites)
        if (len(cites) > 0):
            pdf.add_book(paper)
            counter = 0
            for cite in cites:
                counter += 1
                pdf.add_cite(cite, prefix=f"{counter}. ")
        print("Processing Type B: %.2lf %%    " % (aux_counter/len(autocites)*100), end="\r")
    print ("")


    pdf_output = args.output
    pdf.output(pdf_output)

    print(f"PDF generado: {pdf_output}")
