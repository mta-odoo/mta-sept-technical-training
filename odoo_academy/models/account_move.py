# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.tools import pycompat
import io, base64, random, string

from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning
from odoo.tools import email_re, email_split, email_escape_char, float_is_zero, float_compare, \
    pycompat, date_utils

def _csv_write_rows(rows):
    f = io.BytesIO()
    writer = pycompat.csv_writer(f, delimiter=',', quotechar='"', quoting=2, dialect='excel')
    rows_length = len(rows)
    for i, row in enumerate(rows):
        writer.writerow(row)

    fvalue = f.getvalue()
    f.close()
    return fvalue


class AccountMove(models.Model):
    _inherit = 'account.move'

    def generate_export_data(self):
        header = ['Quickbook Name:',
                  'Export #',
                  'Bill No',
                  'Vendor',
                  'Date',
                  'Due Date',
                  'AP Account',
                  'Memo',
                  'Expense Class',
                  'Expense Account',
                  'Expense Customer',
                  'Expense Amount',
                  'Expense Memo',
                  ]

        content = []
        for invoice in self:
           invoice_group = {}
            for line in invoice.invoice_line_ids:
                key = (line.export_sequence or '',
                       line.invoice_id.reference or line.invoice_id.number or '',
                       line.invoice_id.partner_id.name or '',
                       line.invoice_id.date_invoice.strftime("%m/%d/%Y") or '',
                       line.invoice_id.date_due.strftime("%m/%d/%Y") or '',
                       line.ap_gl_account.name or '',
                       line.purchase_id.name or '',
                       line.purchase_id.expense_class.name or '',
                       line.account_group.name or '',
                       line.invoice_id.charge_code_id.name or ''
                       )
                line_data = line.price_total  # assuming they are using the same currency here, might need to revise if they want multicurrency
                invoice_group[key] = line_data
            content.extend([[""] + list(k) + list(invoice_group.get(k)) for k in invoice_group.keys()])

        data = [header] + content
        return _csv_write_rows(data)


    def action_export(self):
        self = self.env['account.move'].search([
            ('id', 'in', self.ids),
            ('state', 'not in', ('draft', 'cancel')),
            ('type', '=', 'in_invoice'),
        ])

        if not self:
            return {}

        Attachment = self.env['ir.attachment'].sudo()
        attachment_name = 'Invoice_Export.csv'
        data = self.generate_export_data(export_sequence)

        attachment_vals = {
            'name': attachment_name,
            'datas': base64.encodestring(data),
            'datas_fname': attachment_name,
            'res_model': 'account.move',
        }

        Attachment.search([('name', '=', attachment_name)]).unlink()

        attachment = Attachment.create(attachment_vals)

        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/{}?download=true'.format(attachment.id),
            'target': 'self'
        }
