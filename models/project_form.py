# -*- coding: utf-8 -*-
from odoo import models, fields, Command
import datetime
from datetime import datetime, timedelta


class ProjectForm(models.Model):
    _inherit = "project.project"
    _description = "project Form"

    detail_field = fields.One2many('project.activity', 'project_id', string="Details", readonly=True)
    schedule_active = fields.Boolean(string="Schedule Active", default=True)

    def generate_schedule_dates(self):
        """Function for generating schedule date"""
        self.schedule_active = False
        activity_values = []
        current_year = datetime.now().year
        for month in range(1, 13):
            last_day_of_month = (datetime(current_year, month % 12 + 1, 1) - timedelta(days=1)).day
            activity_values.append((Command.create({
                'month': str(month),
                'year': current_year,
                'from_date': datetime(current_year, month, 1).strftime('%Y-%m-%d'),
                'to_date': datetime(current_year, month, last_day_of_month).strftime('%Y-%m-%d')
            })))
        self.write({'detail_field': activity_values})


class ProjectActivity(models.Model):
    _name = "project.activity"
    _description = "Project Activity"

    project_id = fields.Many2one('project.project', string="Project")
    month = fields.Selection(
        [('1', 'January'), ('2', 'February'), ('3', 'March'), ('4', 'April'), ('5', 'May'), ('6', 'June'),
         ('7', 'July'), ('8', 'August'), ('9', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December')],
        string='Month', required=True, readonly=True)
    year = fields.Char(string='Year', required=True, readonly=True)
    from_date = fields.Date(string='From Date', required=True, readonly=True)
    to_date = fields.Date(string='To Date', required=True, readonly=True)
