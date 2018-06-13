# -*- coding: utf-8 -*-
import time

from odoo.exceptions import ValidationError
from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class LeaveRequestApplication(models.Model):
    _name = 'leaveapp.leaverequestapplication'

    name = fields.Many2one("res.users", string ="申请人", required = True)
    manager = fields.Many2one("hr.employee", string ="主管", readonly = True)
    # days = fields.Float(string="天数", required = True)
    days = fields.Integer(string="天数", required=True, help="天数只能是整数", states={'draft': [('readonly', False)]}, readonly=True)
    # startDate = fields.Date(string="开始日期", required = True, default = fields.Datetime.now())
    startDate = fields.Date(string="开始日期", required=True, states={'draft': [('readonly', False)]}, readonly=True)
    endDate = fields.Date(string="结束日期", required=True)
    # reason = fields.Text(string="请假事由")
    reason = fields.Text(string="请假事由", default="", required=True, states={'draft': [('readonly', False)]}, readonly=True)
    accept_reason = fields.Text(string="同意理由", default = "同意")
    current_name = fields.Many2one("hr.employee", string = "当前登录人", compute ="_get_current_name")
    is_manager = fields.Boolean(compute="_get_is_manager")

    @api.constrains("days", "startDate", "reason")
    def _check_something(self):
        for record in self:
            # 当前时间
            currentDate = int(time.strftime("%Y%m%d", time.localtime()))
            # 选择的开始时间
            date = int(record.startdate[0:4] + record.startdate[5:7] + record.startdate[8:10])
            if record.days < 0 or record.days == 0:
                raise ValidationError("天数不能小于等于0")
            if date < currentDate:
                raise ValidationError("开始日期不能早于当前时间")

    def send(self):
        self.sended = True
        return self.sended

    def confirm(self):
        self.state = "confirmed"
        return self.state

    state = fields.Selection([
        ('draft', "草稿"),
        ('confirmed', "待审核"),
        ('accepted', "批准"),
        ('rejected', "拒绝"),
    ], string="状态", default = "draft", readonly = True)

    @api.model  # 使用新的 api
    def _get_default_name(self):
        uid = self.env.uid
        res = self.env["resource.resource"].search([("user_id", "=", uid)])
        name = res.name
        employee = self.env["hr.employee"].search([("name_related", "=", name)])
        return employee

    @api.model
    def _get_default_manager(self):  # 单记录 recordset 可以直接用点记号读取属性值
        uid = self.env.uid
        res = self.env["resource.resource"].search([("user_id", "=", uid)])
        name = res.name
        employee = self.env["hr.employee"].search([("name_related", "=", name)])
        _logger.info("myinfo{}".format(employee.parent_id))
        return employee.parent_id  # 似乎有这种数字引用方法值得我们注意

    # _defaults = {
    #     "name": _get_default_name,
    #     "manager": _get_default_manager,
    # }

    def _get_is_manager(self):  ### 这里 return 不起作用
        print(self.current_name, self.manager, self.env.uid)
        if self.current_name == self.manager:
            self.is_manager = True
        else:
            self.is_manager = False

    def _get_current_name(self):
        uid = self.env.uid
        res = self.env["resource.resource"].search([("user_id", "=", uid)])
        name = res.name
        employee = self.env["hr.employee"].search([("name_related", "=", name)])
        self.current_name = employee

    ##############################
    def draft(self, cr, uid, ids, context=None):
        if context is None:
            context = {}

        self.write(cr, uid, ids, {"state" : "draft"}, context = context)
        return True

    def confirm(self, cr, uid, ids, context=None):
        if context is None:
            context = {}

        self.write(cr, uid, ids, {"state" : "confirmed"}, context = context)
        return True

    def accept(self, cr, uid, ids, context=None):
        if context is None:
            context = {}

        self.write(cr, uid, ids, {"state" : "accepted"}, context = context)
        print("你的请假单被批准了")
        return True

    def reject(self, cr, uid, ids, context=None):
        if context is None:
            context = {}

        self.write(cr, uid, ids, {"state" : "rejected"}, context = context)
        print("抱歉，你的请假单没有被批准。")
        return True

