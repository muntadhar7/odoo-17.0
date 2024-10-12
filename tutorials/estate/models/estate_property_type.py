from odoo import models, fields, api


class EstatePropertyType(models.Model):
    _name = "estate_property_type"
    _description = "Types of property_ids"
    _order = "name"
    name = fields.Char(required = True)
    sequence= fields.Integer(default=1)
    property_id =fields.One2many("estate_property","type")
    offer_id = fields.One2many("estate_property_offer","property_type_id" )
    offer_count = fields.Integer(compute="_count_offers")

    _sql_constraints = [
        ('name_unique','Unique(name)','Type must be unique!')
    ]

    @api.depends("offer_id")
    def _count_offers(self):
        total = 0
        for record in self.offer_id:
            total+=1
        self.offer_count = total

    def action_view_offers(self):
        result = {
            "type": "ir.actions.act_window",
            "res_model": "estate_property_offer",
            "name": "Offers",
            'view_mode': 'tree,form',
        }
        return result