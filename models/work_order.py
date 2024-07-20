from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import timedelta, datetime, date
import pytz
import logging
import re
_logger = logging.getLogger(__name__)
from odoo.tools.mail import html2plaintext

class WorkOrder(models.Model):
    _name = 'work.order'
    _description = 'Work Order'

    name = fields.Char(string='WO Number' ,default=lambda self: _('New'), copy=False, readonly=True, tracking=True)
    sale_order_id = fields.Many2one('sale.order', string='Booking Order Reference', readonly=True)
    team_id = fields.Many2one('service.team', string='Team', required=True)
    team_leader_id = fields.Many2one('res.users', string='Team Leader', required=True)
    team_members_ids = fields.Many2many('res.users', string='Team Members')
    planned_start = fields.Datetime(string='Planned Start', required=True)
    planned_end = fields.Datetime(string='Planned End', required=True)
    date_start = fields.Datetime(string='Date Start', readonly=True)
    date_end = fields.Datetime(string='Date End', readonly=True)
    state = fields.Selection([
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled')
    ], string='State', default='pending')
    notes = fields.Text(string='Notes')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('work.order') or 'New'
        return super(WorkOrder, self).create(vals_list)
        # if vals.get('name', _('New')) == _('New'):
        #     vals['name'] = self.env['ir.sequence'].next_by_code('work.order') or _('New')
        
    
    def action_start_work(self):
        self.ensure_one()
        if self.state != 'pending':
            raise UserError("Only pending work orders can be started.")
        self.write({
            'state': 'in_progress',
            'date_start': fields.Datetime.now()
        })
    
    def action_end_work(self):
        self.ensure_one()
        if self.state != 'in_progress':
            raise UserError("Only in-progress work orders can be ended.")
        self.write({
            'state': 'done',
            'date_end': fields.Datetime.now()
        })
    
    def action_reset(self):
        self.ensure_one()
        if self.state != 'in_progress':
            raise UserError("Only in-progress work orders can be reset.")
        self.write({
            'state': 'pending',
            'date_start': False
        })
        
    def action_cancel(self, reason=None):
        self.ensure_one()
        if not reason:
            raise UserError("Reason for cancellation is required.")
        self.write({
            'state': 'cancelled',
            'notes': (self.notes or '') + "\nReason for cancellation: " + reason
        })
    
    def button_action_cancel(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'work.order.cancel.reason',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_work_order_id': self.id},
        }
    def print_work_order(self):
        return self.env.ref("booking_order_AgusRianS_17072024.work_order_print").report_action(self,config=False)
class WorkOrderCancelReason(models.TransientModel):
    _name = 'work.order.cancel.reason'
    _description = 'Reason for Cancelling Work Order'

    reason = fields.Text(string='Reason for Cancellation', required=True)

    def action_cancel_confirm(self):
        work_order = self.env['work.order'].browse(self.env.context.get('active_id'))
        work_order.action_cancel(self.reason)
