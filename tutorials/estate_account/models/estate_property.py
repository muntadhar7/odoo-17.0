from odoo import models, Command
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _inherit = "estate_property"
    def action_sold(self):

        move_type = "out_invoice"
        partner_id = self.buyer
        self.env['account.move'].create({
            'move_type': 'out_invoice',
            "line_ids": [
                Command.create({
                    "name": "Property value",
                    "quantity": "1",
                    "price_unit": self.selling_price,
                }),
                Command.create({
                    "name": "Fees",
                    "quantity": "1",
                    "price_unit": self.selling_price*0.06,
                }),
                Command.create({
                    "name": "Administrative fees",
                    "quantity": "1",
                    "price_unit": 100,
                })
            ],
        })

        return super().action_sold()

