# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _

class Course(models.Model):
    _name = 'openacademy.course'
    _description = "Course"
    # _inherits = {'product.template': 'product_tmpl_id'}
    _inherit = ['mail.thread']
    _table = 'openacademy_course_table'
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
    color = fields.Char(string="Color", help="Choose your color")
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

    attachments = fields.Many2many('ir.attachment', compute='_get_attachment_ids', string=u'附件')
    def _get_attachment_ids(self):
        att_model = self.env['ir.attachment']  # 获取附件模型
        for obj in self:
            query = [('res_model', '=', self._name), ('res_id', '=', obj.id)]  # 根据res_model和res_id查询附件
            obj.attachments = att_model.search(query)  # 取得附件list

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

    def invoke_jsonrpc(self):

        import xmlrpclib
        import datetime
        HOST = 'localhost'
        PORT = 8069
        root = 'http://%s:%d/xmlrpc/' % (HOST, PORT)
        dbname = 'demo'
        user = 'admin'
        pwd = 'admin'

        uid = xmlrpclib.ServerProxy(root + 'common').login(dbname, user, pwd)  # common是服务，login 是方法
        print "Logged in as %s (uid: %d)" % (user, uid)

        date = datetime.datetime.now()
        detester = date.strftime('%Y-%m-%d %H:%M:%S')

        # 调用openacademy.course对象的create方法在数据库中插入一名课程
        sock = xmlrpclib.ServerProxy(root + 'object')
        args = {
            'name': '测试' + detester,
            'no': 'C0001',
            'credit': 10,
            'teacher': 'Peter.Peng',
            'lang': 'en_US'
        }

        course_id = sock.execute(dbname, uid, pwd, 'openacademy.course', 'create',args)

        values = {
            'name': '更新'
        }
        result1 = sock.execute(dbname, uid, pwd, 'openacademy.course', 'write', course_id, values)
        print(result1)

        args = [('name', '=', '更新')]
        result2 = sock.execute(dbname, uid, pwd, 'openacademy.course', 'search', args)
        print(result2)

        # 读取字段记录
        fields = ['name', 'no', 'credit', 'teacher']
        data = sock.execute(dbname, uid, pwd, 'openacademy.course', 'read', course_id, fields)
        print(data)

        # 查找所有字段，无需传ID
        data1 = sock.execute(dbname, uid, pwd, 'openacademy.course', 'search_read')
        print(data1)

        print 'deleteID', course_id
        result = sock.execute(dbname, uid, pwd, 'openacademy.course', 'unlink', course_id)
        print result

        return

    def invoke_xmlrpc(self):
        print("invoke rpc sample successfully!")

        import xmlrpclib
        import datetime
        username = 'admin'  # 用户登录名
        pwd = 'admin'  # 用户的登录密码，测试时请换成自己的密码
        dbname = 'demo'  # 数据库帐套名，测试时请换成自己的帐套名

        # 第一步，取得uid
        sock_common = xmlrpclib.ServerProxy('http://localhost:8069/xmlrpc/common')
        uid = sock_common.login(dbname, username, pwd)
        print 'uid:', uid

        # replace localhost with the address of the server
        sock = xmlrpclib.ServerProxy('http://localhost:8069/xmlrpc/object')

        date = datetime.datetime.now()
        detester = date.strftime('%Y-%m-%d %H:%M:%S')

        # 调用openacademy.course对象的create方法在数据库中插入一名课程
        course = {
            'name': '测试' + detester,
            'no': 'C0001',
            'credit': 10,
            'teacher': 'Peter.Peng',
            'lang': 'en_US'
        }

        course_id = sock.execute(dbname, uid, pwd, 'openacademy.course', 'create', course)

        # 删除一条或多条记录
        updateID = []
        updateID.append(course_id)

        values = {
            'name': '更新'
        }
        result1 = sock.execute(dbname, uid, pwd, 'openacademy.course', 'write', updateID, values)

        args = [('name', '=', '更新')]
        result2 = sock.execute(dbname, uid, pwd, 'openacademy.course', 'search', args)
        print(result2)

        # 读取字段记录
        fields = ['name', 'no', 'credit', 'teacher']
        data = sock.execute(dbname, uid, pwd, 'openacademy.course', 'read', updateID, fields)
        print(data)

        # 查找所有字段，无需传ID
        data1 = sock.execute(dbname, uid, pwd, 'openacademy.course', 'search_read')
        print(data1)

        deleteID = updateID
        print 'deleteID', deleteID
        result = sock.execute(dbname, uid, pwd, 'openacademy.course', 'unlink', deleteID)

        return




