from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


def default_date_availability(self) -> object:
    return fields.Date.add(fields.Date.today(), months=3)


class EstateProperty(models.Model):
    _name = 'estate_property'
    _description = 'Real estate model'
    _order = "id desc"
    name = fields.Char(required = True)
    description = fields.Text()
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(copy=False, default=default_date_availability, string="Available From")
    expected_price = fields.Float(required = True)
    selling_price = fields.Float(readonly = True, compute="_accept_offer", copy = False, store=True)
    bedrooms = fields.Integer(default = 2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([('north', 'North'),('south', 'South'),('east', 'East'),('west', 'West')])
    active = fields.Boolean(default = True)
    state = fields.Selection([('new','New'),('offer_received','Offer Received'),('offer_accepted','Offer Accepted'),('sold','Sold'),('cancelled','Cancelled')], default = 'new',readonly=False, required = True, copy = False)
    type = fields.Many2one("estate_property_type", string="Type")
    sales_person = fields.Many2one("res.users", string="Salesman")
    buyer = fields.Many2one("res.partner", string="Buyer")
    tags = fields.Many2many("estate_property_tags", string="Tags")
    offer = fields.One2many('estate_property_offer','property_id',string="Offer")
    total_area =fields.Integer(compute='_compute_area', readonly=True)
    best_offer = fields.Float(compute="_best_price", readonly=True)

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price>0)', 'Expected price must be positive'),
        ('check_selling_price', 'CHECK(selling_price>=0)', 'Selling price must be positive'),
    ]

    @api.constrains("selling_price")
    def _check_selling_price(self):
        for record in self:
            if record.selling_price/record.expected_price < 0.9 and record.selling_price != 0:
                raise ValidationError("Selling price must be greater than 90% of the expected price")

    @api.depends("living_area", "garden_area")
    def _compute_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer.price")
    def _best_price(self):
        for record in self:
            if record.offer:
                record.best_offer = max(o.price for o in record.offer)
            else:
                record.best_offer = 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = ""

    def action_sold(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError("Cancelled property_ids cant be sold")
            else:
                record.state = "sold"
        return True

    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError("Sold property_ids cant be cancelled")
            else:
                record.state = "cancelled"
        return True

    @api.depends("offer.status")
    def _accept_offer(self):
        for record in self:
            accepted_offer=None
            for f in record.offer:
                if f.status == "accepted":
                    accepted_offer = f
            if accepted_offer:
                record.selling_price = accepted_offer.price
                record.buyer = accepted_offer.partner_id
            else:
                record.selling_price = 0
                record.buyer = None

    @api.ondelete(at_uninstall=False)
    def delete(self):
        for record in self:
            if record.state not in ("new","cancelled"):
                raise UserError("Only new and cancelled property_ids can be deleted")

