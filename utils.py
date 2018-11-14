import os
import time
import shutil
import traceback

from settings import options, WKHTMLTOPDF_PACKAGE_PATH, PDFS_DIRECTORY

import pdfkit


class PdfGenerator:

	def create_file(self, order_id, directory):
		config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PACKAGE_PATH)	
		output_file = '{directory}/order_{id}.pdf'.format(directory=directory, id=order_id[-1])
		pdf = pdfkit.from_string(order_id, output_file, configuration=config, options=options)
		return pdf

	def create_directory(self, username):
		timestamp = int(time.time())
		directory = "{pdfs_dir}/{username}_files_{timestamp}".format(pdfs_dir=PDFS_DIRECTORY, username=username, timestamp=timestamp)
		try:
		    os.makedirs(directory)
		except:
			traceback.print_exc()
			raise
			return None
		return directory			    	

	def remove_file(self, filename):
		try:
			os.remove(filename)
		except:
			traceback.print_exc()

	def remove_directory(self, directory):
		try:
			shutil.rmtree(directory)
		except:
			traceback.print_exc() 	 

	def compress_directory(self, directory):
		try:
			shutil.make_archive(directory, 'zip', directory)
			self.remove_directory(directory)		
		except:
			traceback.print_exc()

class Address:
    
    def __init__(self):
        self.address_line_1 = ''
        self.address_line_2 = ''
        self.city = ''
        self.zip = ''
        self.state = ''
        self.country_code = ''
        