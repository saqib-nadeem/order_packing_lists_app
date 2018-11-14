# pdfkit settings and configs
'''
Make sure that you have wkhtmltopdf in your $PATH
or set via custom configuration. where wkhtmltopdf in Windows 
or which wkhtmltopdf on Linux should return actual path to binary.
'''
WKHTMLTOPDF_PACKAGE_PATH = '/usr/local/bin/wkhtmltopdf'
options = {
    'page-size': 'Letter',
    'margin-top': '0.75in',
    'margin-right': '0.75in',
    'margin-bottom': '0.75in',
    'margin-left': '0.75in',
    'encoding': "UTF-8",
    'custom-header' : [
        ('Accept-Encoding', 'gzip')
    ],
    'cookie': [
        ('cookie-name1', 'cookie-value1')
    ],
    'no-outline': None
}
PDFS_DIRECTORY = 'pdfs'

# from local_settings import *