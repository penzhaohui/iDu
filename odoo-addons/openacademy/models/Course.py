# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions

class Course(models.Model):
    _name = 'openacademy.course'
    name = fields.Char(string="Title", required=True)
    no = fields.Char(string="NO", required=True)
    credit = fields.Integer(string="Credit", required=True)
    description = fields.Text()
    teacher = fields.Char(string="Teacher", required=False)
    responsible_id = fields.Many2one('res.users',
                                     ondelete='set null', string="Responsible", index=True)
    session_ids = fields.One2many(
        'openacademy.session', 'course_id', string="Sessions")

    @api.multi
    def copy(self, default=None):
        default = dict(default or {})

        copied_count = self.search_count(
            [('name', '=like', u"Copy of {}%".format(self.name))])
        if not copied_count:
            new_name = u"Copy of {}".format(self.name)
        else:
            new_name = u"Copy of {} ({})".format(self.name, copied_count)

        default['name'] = new_name
        return super(Course, self).copy(default)

    _sql_constraints = [
        ('name_description_check',
         'CHECK(name != description)',
         "The title of the course should not be the description"),

        ('name_unique',
         'UNIQUE(name)',
         "The course title must be unique"),
    ]

    WORKFLOW_STATE_SELECTION = [
        ('init', '初始'),
        ('start', '开始'),
        ('confirm', '确认'),
        ('complete', '完成'),
    ]

    state = fields.Selection(WORKFLOW_STATE_SELECTION, default='init', string="状态", readonly=True)

    # 注意使用新版本定义方法是，需要添加装饰器@api.one/@api.multi
    # 将state 置于开始状态
    @api.one
    def do_start(self):
        print "------------self.state = 'start'"
        self.state = 'start'
        return True

    # 将state 置于确认状态
    @api.one
    def do_confirm(self):
        print "------------self.state = 'confirm'"
        self.state = 'confirm'
        return True

    # 将state 置于完成状态
    @api.one
    def do_complete(self):
        print "------------self.state = 'complete'"
        self.state = 'complete'
        return True

    # 将state 置于取消状态
    @api.one
    def do_cancel(self):
        print "------------self.state = 'init'"
        self.state = 'init'
        return True


class Teacher(models.Model):
    _name = 'openacademy.teacher'

    firstName = fields.Char(string="First Name", required=True)
    lastName = fields.Char(string="Last Name", required=True)

