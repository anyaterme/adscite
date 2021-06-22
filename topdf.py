import pdfkit
import glob
options = {
        'page-size': 'Letter',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'custom-header': [
            ('Accept-Encoding', 'gzip')
        ],
        'cookie': [
            ('cookie-name1', 'cookie-value1'),
            ('cookie-name2', 'cookie-value2'),
        ],
        'outline-depth': 10,
}

cites = sorted(glob.glob("1*cites_a.html"))[-1]
pdfkit.from_url(cites, '00_cites_a.pdf', options=options)
cites = sorted(glob.glob("1*cites_b.html"))[-1]
pdfkit.from_url(cites, '01_cites_b.pdf', options=options)
cites = sorted(glob.glob("1*autocites.html"))[-1]
pdfkit.from_url(cites, '02_autocites.pdf', options=options)
summary = sorted(glob.glob("1*summary.html"))[-1]
pdfkit.from_url(summary, '03_summary.pdf', options=options)

