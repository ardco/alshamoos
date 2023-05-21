// Copyright (c) 2023, ARD and contributors
// For license information, please see license.txt

frappe.ui.form.on('Barcode Generator', {
	// refresh: function(frm) {

	// },
	item_code: function (frm) {
		frm.doc.item_price = ''

		if (frm.doc.item_code)
			frappe.call({
				doc: frm.doc,
				method: 'has_barcode',
				args: { item_code: frm.doc.item_code },
				callback: function (response1) { 
					if (response1.message) {
						// msgprint('Has barcode')
						frm.doc.new_barcode = 0

						frappe.call({
							doc: frm.doc,
							method: 'get_price',
							args: { item_code: frm.doc.item_code },
							callback: function (response4) {
								if (response4.message) {
									frm.doc.item_price = response4.message
									frm.refresh_fields()
								}
							}
						})


						frappe.call({
							doc: frm.doc,
							method: 'get_barcodes',
							args: { item_code: frm.doc.item_code },
							callback: function (response2) {
								// Adding a drop-down years selector list
								frm.set_df_property('barcodes', 'options', [''].concat(response2.message));
							}
						})


					}
					else {
						// msgprint('Does not has barcode!')
						frm.doc.new_barcode = 1
						frappe.call({
							doc: frm.doc,
							method: 'generate_barcode',
							args: { },
							callback: function (response5) {
								console.log(response5.message)
								frm.call({
									method: "alshamoos.api.get_barcode",
									args: { data: response5.message },
									callback: function (response6) {
										frm.doc.barcode_code = response6.message;
										frm.refresh_fields();
									}
								})
							}
						})
					}
				}
			})
		else {
			frm.doc.item_price = ''
			frm.refresh_fields()
		}
	},
	barcodes: function (frm) { 
		frm.call({
			method: "alshamoos.api.get_barcode",
			args: { data: frm.doc.barcodes },
			callback: function (response3) {
				frm.doc.barcode_code = response3.message;
				frm.refresh_fields();
			}
		})
	},
	after_save: function (frm) {
		if (frm.doc.new_barcode) {
			frm.call({
				method: 'alshamoos.api.scan_barcode',
				args: { doc: frm.doc.name },
				callback: function (ft) {
					console.log(ft.message)
				frm.call({
					method: 'alshamoos.api.add_barcode',
					args: { barcode: ft.message, docname: frm.doc.item_code },
					callback: function (f) {
						console.log(f.message)
					},
					error: function (err) {
						frm.dirty();
					},
				});
				}
			});	
		}
	
	}
});
