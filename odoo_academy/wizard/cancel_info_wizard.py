# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CancelInfoWizard(models.TransientModel):
    _name = 'cancel.info.wizard'
    _description = 'Wizard: Gather Information on Sale Order Cancelation'
    
    def _default_sale(self):
        return self.env['academy.session'].browse(self._context.get('active_id'))
    
    sale_id = fields.Many2one(comodel_name='sale.order',
                                 string='Sale',
                                 required=True,
                                 default=_default_sale)

    
    cancel_reason = fields.Selection([('no_need', 'Do not need it anymore'),
                                      ('no_money', 'Not enough funds'),
                                      ('save_for_later', 'Saved for later')])
    
    cancel_explanation = fields.Text(help='A longer explanation of why the order was confirmed.')
                                    
    
    def record_cancel_reason(self):
        self.sale_id.write({'cancel_reason': self.cancel_reason,
                            'cancel_explanation': self.cancel_explanation})
        
        self.sale_id.action_cancel()