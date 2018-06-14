# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _

class Course(models.Model):
    _name = 'openacademy.course'
    _description = "Course"
    # _inherits = {'product.template': 'product_tmpl_id'}
    _inherit = ['mail.thread']
    # _inherit = 'product.template'

    # Only Manager role can access name?
    name = fields.Char(string="Title", required=True)
    type = fields.Selection(string='Inventory of', selection='_selection_type',
        required=True,
        default='none',
        help="Refere to the sample code: addons/stock/models/stock_inventory.py")

    def _selection_type(self):
        """ Get the list of filter allowed according to the options checked
        in 'Settings\Warehouse'. """
        res_filter = [
            ('none', 'All products'),
            ('category', 'One product category'),
            ('product', 'One product only'),
            ('partial', 'Select products manually')]

        if self.user_has_groups('stock.group_tracking_owner'):
            res_filter += [('owner', 'One owner only'), ('product_owner', 'One product for a specific owner')]
        if self.user_has_groups('stock.group_production_lot'):
            res_filter.append(('lot', 'One Lot/Serial Number'))
        return res_filter

    no = fields.Char(string="NO", required=True)
    # Only Manager role can access credit?
    credit = fields.Integer(string="Credit", required=True, groups="openacademy.group_openacademy_manager")
    #credit = fields.Integer(string="Credit", required=True, groups="base.user_root")
    # credit = fields.Integer(string="Credit", required=True)
    description = fields.Text()
    teacher_id = fields.Many2one('openacademy.teacher', string="Teacher")
    responsible_id = fields.Many2one('res.users',
                                      ondelete='set null', string="Responsible", index=True, groups="openacademy.group_openacademy_manager")
    # responsible_id = fields.Many2one('res.users',
    #                                  ondelete='set null', string="Responsible", index=True)
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




