# Copyright (c) 2023, ARD and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt


class BarcodeGenerator(Document):
    @frappe.whitelist()
    def has_barcode(self, item_code):
        if frappe.db.sql(
            f"""select barcode from `tabItem Barcode` where parent="{item_code}";"""
        ):
            return True
        return False

    @frappe.whitelist()
    def get_barcodes(self, item_code):
        barcodes = frappe.db.sql(
            f"""select barcode from `tabItem Barcode` where parent="{item_code}";""",
            as_dict=True,
        )
        barcodes = [barcode["barcode"] for barcode in barcodes]

        return barcodes

    @frappe.whitelist()
    def get_price(self, item_code, price_list):
        try:
            price = frappe.db.sql(
                f"""select price_list_rate from `tabItem Price` where item_code="{item_code}" and price_list="{price_list}";"""
            )
            if price:
                return flt(price[0][0])
        except IndexError:
            return False

    @frappe.whitelist()
    def generate_barcode(self):
        # Getting the increment value to generate the barcode
        counter = int(frappe.get_doc("Item Barcode Generator Counter").barcode_counter)

        # doc = frappe.get_doc('Item', item_code)

        return f"{97}{'0' * (5 - len(str(counter)))}{counter}"

    def validate(self):
        price = self.get_price(self.item_code, self.price_list)
        if price and not self.item_price:
            # frappe.msgprint(f"Item {self.item_code} have a price list rate of {price}")
            self.item_price = price
