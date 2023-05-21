# Copyright (c) 2023, ARD and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class BarcodeGenerator(Document):
	
	@frappe.whitelist()
	def has_barcode(self, item_code):
		if frappe.db.sql(f'''select barcode from `tabItem Barcode` where parent="{item_code}";'''):
			return True
		return False
	
	@frappe.whitelist()
	def get_barcodes(self, item_code):
		barcodes = frappe.db.sql(f'''select barcode from `tabItem Barcode` where parent="{item_code}";''', as_dict=True)
		barcodes = [barcode['barcode'] for barcode in barcodes]

		return barcodes
	
	@frappe.whitelist()
	def get_price(self, item_code):
		return frappe.db.sql(f'''select price_list_rate from `tabItem Price` where item_code="{item_code}";''')
	
	@frappe.whitelist()
	def generate_barcode(self):
		# Getting the increment value to generate the barcode
		counter = int(frappe.get_doc('Item Barcode Generator Counter').barcode_counter)

		# doc = frappe.get_doc('Item', item_code)

		return f"{97}{'0' * (5 - len(str(counter)))}{counter}"