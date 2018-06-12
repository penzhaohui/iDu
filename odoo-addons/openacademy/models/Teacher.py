# -*- coding: utf-8 -*-
from odoo import models, fields, api
import psycopg2

import logging
_logger = logging.getLogger(__name__)

class Teacher(models.Model):
    _name = 'openacademy.teacher'

    name = fields.Char(string="Name", required=True)
    firstName = fields.Char(string="First Name", required=True)
    lastName = fields.Char(string="Last Name", required=True)
    biography = fields.Html()
    # course_ids = fields.One2many('openacademy.course', 'teacher_id', string="Courses")
    course_ids = fields.One2many('openacademy.course', 'teacher_id', string="Courses")

    @api.multi
    def getAllTeacher1(self):
        db = psycopg2.connect("dbname=dev user=postgres")  # 查找名叫 test4 的数据库  postgres  是数据库的超级用户名称
        vals = db.cursor()
        vals.execute("SELECT name,firstName,lastName FROM openacademy_teacher")  # 执行sql语句查询数据
        tables = vals.fetchall()  # 返回查询结果

    @api.multi
    def getAllTeacher2(self):
        sql = "SELECT name,firstName,lastName FROM openacademy_teacher"
        self.env.cr.execute(sql)  # 执行SQL语句
        dicts = self.env.cr.dictfetchall()  # 获取SQL的查询结果

    @api.constrains('name')
    def action(self):
        print "The server action will return one URL action soon!!!"
        _logger.info("The server action will return one URL action soon!!!")
        return {
            "type": "ir.actions.act_url",
            "url": "http://odoo.com",
            "target": "self",
        }
