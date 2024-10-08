from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name="estate_property_tags"
    _description = "Tags for properties"
    _order = "name"
    name = fields.Char(required=True)
    color = fields.Integer()

    _sql_constraints = [
        ('name_unique','Unique(name)','Type must be unique!')
    ]