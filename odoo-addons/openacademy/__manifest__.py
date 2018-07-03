# -*- coding: utf-8 -*-
{
    'name': "Open Academy",

    'summary': """
        这个模块主要模拟在线课程管理 """,

    'description': """
        这是我的第一个练习Odoo Module
        参考资料：          
        1. https://www.cnblogs.com/odoouse/p/5995413.html
        2. https://www.odoo.com/documentation/11.0/howtos/backend.html#build-an-odoo-module
    """,

    'author': "peter.peng",
    'website': "http://www.transtrue.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'eGovment',
    'version': '1.1',
    'ico': 'static/description/icon.png',
    'application': 'true',
    # any module necessary for this one to work correctly
    'depends': ['base', 'website', 'mail','base_action_rule'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/course_views.xml',
        'views/course_workflow.xml',
        'views/session_views.xml',
        'views/teacher_views.xml',
        'views/partner_views.xml',
        'views/region_views.xml',
        'views/widget_views.xml',
        'views/templates.xml',
        'views/menu_views.xml',
        'views/scheduler_scheduled_actions.xml',
    ],
    'qweb': ['static/src/xml/tree_view_button.xml'],
    # only loaded in demonstration mode
    'demo': [
        'demo/course_demo.xml',
        # 'demo/partner_demo.xml',
        'demo/teacher_demo.xml',
    ],
}