
from odoo import models, fields

class InheritedWarehouse(models.Model):
    _inherit = 'stock.warehouse'
    long = fields.Float()
    lat = fields.Float()
