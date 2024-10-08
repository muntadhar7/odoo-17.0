from odoo import models, fields, api
from dateutil.relativedelta import relativedelta

from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate_property_offer"
    _description = "Properties offers"
    _order = "price desc"

    price = fields.Integer()
    status = fields.Selection([('accepted', 'Accepted'), ('refused', 'Refused')], copy=False, readonly=False)

    property_id = fields.Many2one('estate_property', required=True)
    partner_id = fields.Many2one('res.partner', required=True)

    validity = fields.Integer(default=7, store=True, compute='_inverse_deadline', inverse='_compute_deadline')
    date_deadline = fields.Date(store=True, compute='_compute_deadline', inverse='_inverse_deadline')

    _sql_constraints = [
        ('check_price','CHECK(price>0)','Offer price must be positive')
    ]

    @api.depends("create_date", "validity")
    def _compute_deadline(self):
        """ Compute the deadline based on the offer's create date and validity days. """
        for record in self:
            if record.create_date and record.validity:
                record.date_deadline = record.create_date + relativedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + relativedelta(days=record.validity)

    @api.depends("create_date", "date_deadline")
    def _inverse_deadline(self):
        """ When the user changes the deadline, adjust the validity period accordingly. """
        for record in self:
            if record.create_date and record.date_deadline:
                record.validity = (record.date_deadline - fields.Date.to_date(record.create_date)).days
            else:
                record.validity = 0

    def action_confirm(self):
        for record in self:
            # Check if any other offer for the same property has been accepted
            accepted_offers = self.search([
                ('property_id', '=', record.property_id.id),
                ('status', '=', 'accepted')
            ])

            # If there are already accepted offers, raise a validation error
            if accepted_offers:
                raise UserError("Another offer has already been accepted for this property.")

            # If no other offer has been accepted, mark this offer as accepted
            record.status = "accepted"

    def action_cancel(self):
        for record in self:
            record.status = "refused"


