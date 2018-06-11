# -*- coding: utf-8 -*-

from odoo import models, fields, api

# 主线模板
class BusTemplate(models.Model):
	_name = 'bus.template'

	name = fields.Char(string='名称', help='主线名称', readonly=False, required=True, index=True)
	summary = fields.Char(string='概要', help='概要说明', readonly=False, required=True, index=True)
	description = fields.Text(string='描述', help='具体的描述', readonly=False, required=True, index=True)
	recipient = fields.Char(string='接收者', help='主线的责任人', readonly=False, required=True, index=True)
	bus_ids = fields.One2many('bus.main', 'id', string="Main Bus")
	
# 主线节点模板
class BusNodeTemplate(models.Model):
	_name = 'bus.node.template'

	name = fields.Char(string='名称', help='主线名称', readonly=False, required=True, index=True)
	summary = fields.Char(string='概要', help='概要说明', readonly=False, required=True, index=True)
	description = fields.Text(string='描述', help='具体的描述', readonly=False, required=True, index=True)
	recipient = fields.Char(string='接收者', help='主线的责任人', readonly=False, required=True, index=True)

# 主线
class Bus(models.Model):
	_name = 'bus.main'
	
	name = fields.Char(string='名称', help='主线名称', readonly=False, required=True, index=True)
	summary = fields.Char(string='概要', help='概要说明', readonly=False, required=True, index=True)
	description = fields.Text(string='描述', help='具体的描述', readonly=False, required=True, index=True)
	recipient = fields.Char(string='接收者', help='主线的责任人', readonly=False, required=True, index=True)
	bus_template_id = fields.Many2one('bus.template', string="Bus Template")

# 主线节点
class BusNode(models.Model):
	_name = 'bus.node'

	bus_id = fields.Many2one("bus.main", string='Main Bus')
	parent_bus_node_id = fields.Many2one('bus.node', string='Parant Bus Node')
	name = fields.Char(string='名称', help='主线节点名称', readonly=False, required=True, index=True)

# 主线与业务实体的关联关系
class BusNodeAccessory(models.Model):
	_name = 'bus.node.accessory'

	bus_id = fields.Many2one("bus.main", string='Main Bus')
	bus_node_id = fields.Many2one('bus.node', string='Bus Node')
	bus_accessory_type = fields.Selection(selection=[(0, u'业务实体'),(1, u'自定义表单'),(2, u'文档'),(3, u'频道')])
	bus_entity_type = fields.Char()
	bus_entity_id = fields.Integer

# 主线状态
class BusStatus(models.Model):
	_name = 'bus.status'