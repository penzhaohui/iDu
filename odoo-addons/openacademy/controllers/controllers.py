# -*- coding: utf-8 -*-
from odoo import api, http, SUPERUSER_ID, _
import logging


_logger = logging.getLogger(__name__)

# db = 'dev'
# cr = odoo.registry(db).cursor()
# env = api.Environment(cr, SUPERUSER_ID, {})

class Openacademy(http.Controller):
    @http.route('/openacademy/openacademy/', auth='public', website=True)
    def index(self, **kw):
        Teachers = http.request.env['openacademy.teacher']
        return http.request.render('openacademy.index', {
            # 'teachers': ["Diana Padilla", "Jody Caroll", "Lester Vaughn"],
            'teachers': Teachers.search([])
        })

    @http.route('/openacademy/<name>/', auth='public', website=True)
    def teacher(self, name):
        return '<h1>{}</h1>'.format(name)

    @http.route('/openacademy/<int:id>/', auth='public', website=True)
    def teacher(self, id):
        return '<h1>{} ({})</h1>'.format(id, type(id).__name__)

    @http.route('/openacademy/<model("openacademy.teacher"):teacher>/', auth='public', website=True)
    def teacher(self, teacher):
        return http.request.render('openacademy.biography', {
            'person': teacher
        })

    # @http.route('/openacademy/teachers1/', auth='public', website=True)
    # def teacher1(self, **kw):
    #     # env['openacademy.teacher'].getAllTeacher1()
    #     return ''

    @http.route('/w/download', type='http', auth='public', csrf=False)
    def w_download_attachment(self, **kwargs):
        attachment_id = kwargs.get('attachment_id')     #取得前端传回来的id
        # 根据id取得数据库中对应的附件，其中datas就是我们的附件数据
        attachment = request.env['ir.attachment'].sudo().search_read(
            [('id', '=', int(attachment_id))],
            ["name", "datas", "res_model", "res_id", "type", "url"]
        )
        if attachment:
            attachment = attachment[0]
        else:
            return redirect('/w/download')

        res_id = attachment['res_id']
        if attachment["type"] == "url":
            if attachment["url"]:
                return redirect(attachment["url"])
            else:
                return request.not_found()
        elif attachment["datas"]:
            data = StringIO(base64.standard_b64decode(attachment["datas"]))
            return http.send_file(data, filename=attachment['name'], as_attachment=True)
        else:
            return request.not_found()