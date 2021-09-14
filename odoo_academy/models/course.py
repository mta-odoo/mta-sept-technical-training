# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class Course(models.Model):
    
    _name = 'academy.course'
    _description = 'Course Info'
    
    name = fields.Char(string='Title', required=True)
    description = fields.Text(string='Description')

    level = fields.Selection(string='Level',
                             selection=[('beginner', 'Beginner'),
                                        ('intermediate', 'Intermediate'),
                                        ('advanced', 'Advanced')],
                             copy=False)
    
    active = fields.Boolean(string='Active', default=True)

    base_price = fields.Float(string='Base Price', default=0.00)

    additional_fee = fields.Float(string='Additional Fee', default=10.00)

    total_price = fields.Float(String='Total Price', readonly=True)
    