from odoo import models, fields, api
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    is_booking_order = fields.Boolean(string='Is Booking Order', default=True)
    team_id_service_team = fields.Many2one('service.team', string='Team')
    team_leader_id = fields.Many2one('res.users', string='Team Leader')
    team_members_ids = fields.Many2many('res.users', string='Team Members')
    booking_start = fields.Datetime(string='Booking Start')
    booking_end = fields.Datetime(string='Booking End')

    
    # @api.onchange('team_id_service_team')
    # def _onchange_team_id(self):
    #     # if not self.team_id_service_team:
    #     #     raise UserError(_('Please fill team id !'))
    #     if self.state == 'sale':
    #         self.env['work.order'].create({
    #             'date_start': self.booking_start,
    #             'date_end': self.booking_end,
    #             'team_id':self.team_id_service_team,
    #             'team_leader_id':self.team_leader_id,
    #             'team_members_ids':self.team_members_ids,
    #             'sale_order_id': self.name
    #         })
    #     else:
    #         raise UserError(_('Please fill team id !'))
    # @api.depends('team_id_service_team')
    def action_check_availability(self):
        self.ensure_one()
        overlap = self.env['work.order'].search_count([
            ('team_id', '=', self.team_id_service_team.id),
            ('state', 'not in', ['cancelled']),
            ('planned_start', '<=', self.booking_end),
            ('planned_end', '>=', self.booking_start)
        ])
        if overlap:
            raise UserError(f"Team already has work order during that period on {self.name}")
        else:
            for record in self:
                record.team_leader_id = record.team_id_service_team.team_leader.id
                record.team_members_ids = record.team_id_service_team.team_members

    def action_confirm(self):
        for order in self:
            if order.is_booking_order:
                overlap = self.env['work.order'].search_count([
                    ('team_id', '=', order.team_id.id),
                    ('state', 'not in', ['cancelled']),
                    ('planned_start', '<=', order.booking_end),
                    ('planned_end', '>=', order.booking_start)
                ])
                if overlap:
                    raise UserError(f"Team is not available during this period, already booked on {order.name}. Please book on another date.")
                work_order_vals = {
                    'sale_order_id': order.id,
                    'team_id': order.team_id.id,
                    'team_leader_id': order.team_leader_id.id,
                    'team_members_ids': [(6, 0, order.team_members_ids.ids)],
                    'planned_start': order.booking_start,
                    'planned_end': order.booking_end,
                    'state': 'pending',
                }
                self.env['work.order'].create(work_order_vals)
        return super(SaleOrder, self).action_confirm()

