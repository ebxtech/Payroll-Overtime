// Copyright (c) 2024, EBX Technolgies and contributors
// For license information, please see license.txt

frappe.ui.form.on("Overtime Request", {
	calc_total_hours: function(frm){
        frappe.call({
            method: "get_difference",
            doc: frm.doc
        }).then(res=>{
            frm.set_value('overtime_hours',res.message);
        })
    },
    from_time: (frm)=>frm.trigger("calc_total_hours"),
    till_time: (frm)=>frm.trigger("calc_total_hours")
});
