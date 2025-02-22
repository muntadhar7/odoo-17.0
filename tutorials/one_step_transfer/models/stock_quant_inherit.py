from odoo import models, fields, api
from odoo.exceptions import ValidationError

class InheritedQuants(models.Model):
    _inherit = 'stock.quant'

    destination_location_id = fields.Many2one(
        'stock.location', string='Destination Location',
        help="The location where the stock is expected to be moved."
    )
    qty_transfer = fields.Float(
        string='Transfer Quantity',
        help="The quantity to transfer to the destination location."
    )

    def create_transfer(self):
        """
        Create a single stock transfer (picking) with multiple lines for selected stock quants.
        """
        if not self:
            raise ValidationError("No records selected.")

        # Validate input data for all selected records
        for quant in self:
            if not quant.destination_location_id:
                raise ValidationError(f"Destination Location is required for product {quant.product_id.display_name}.")
            if quant.qty_transfer <= 0:
                raise ValidationError(f"Transfer Quantity must be greater than zero for product {quant.product_id.display_name}.")
            if quant.qty_transfer > quant.quantity:
                raise ValidationError(f"Transfer Quantity cannot exceed the available quantity for product {quant.product_id.display_name}.")

        # Get the internal transfer picking type
        picking_type = self.env['stock.picking.type'].search([
            ('code', '=', 'internal')
        ], limit=1)
        if not picking_type:
            raise ValidationError("No internal transfer picking type configured.")

        # Create a new picking
        picking = self.env['stock.picking'].create({
            'picking_type_id': picking_type.id,
            'location_id': self[0].location_id.id,  # Use the location of the first record
            'location_dest_id': self[0].destination_location_id.id,  # Use the destination of the first record
        })

        # Create stock moves for each selected quant
        for quant in self:
            self.env['stock.move'].create({
                'name': quant.product_id.name,
                'product_id': quant.product_id.id,
                'product_uom_qty': quant.qty_transfer,
                'product_uom': quant.product_id.uom_id.id,
                'picking_id': picking.id,
                'location_id': quant.location_id.id,
                'location_dest_id': quant.destination_location_id.id,
            })
            quant.destination_location_id = False
            quant.qty_transfer = False

        # Confirm and assign the picking
        picking.action_confirm()
        picking.action_assign()

        # Return the created picking
        return picking