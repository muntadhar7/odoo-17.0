# models/your_model.py
from odoo import models, fields

class Custom(models.Model):
    _name = 'custom'
    _description = 'Custom'

    coordinates = fields.Text('Map Coordinates')  # Will store JSON {lat: x, lng: y}