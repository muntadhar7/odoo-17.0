from odoo import fields, api, models

class InheritedContract(models.Model):
    _inherits = ['hr.contract', 'res.currency']

    wage_in_currency = fields.Monetary(string= 'Wage in Currency', currency_field='currency')
    currency = fields.Many2one(comodel_name='res.currency', string='Currency')
