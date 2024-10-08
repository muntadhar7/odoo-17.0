from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate_property_type"
    _description = "Types of properties"
    _order = "name"
    name = fields.Char(required = True)
    sequence= fields.Integer(default=1)
    property_id =fields.One2many("estate_property","type")

    _sql_constraints = [
        ('name_unique','Unique(name)','Type must be unique!')
    ]