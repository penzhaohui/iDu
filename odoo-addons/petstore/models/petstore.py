from odoo import models, api, fields

class Message(models.Model):
    _name = "petstore.message_of_the_day"
  
    message = fields.Text()
    color = fields.Char(size=20)

    @api.model
    # displays the last message in the message database
    def my_method(self):
        #return {"hello": "world","h" : "how"}
        return self.env['petstore.message_of_the_day'].search([('id','=','5')]).message



class Product(models.Model):
    _inherit = "product.product"
    # _name = "product.product"

    #name = fields.Char(string = "Product Name")
    max_quantity = fields.Float(string="Maximum Quantity")
    #

    @api.model
    def my_method(self):
        #import pdb; pdb.set_trace()
        #return {"he":"df"}  search_read instead of search
        return self.env['product.product'].search_read([('categ_id.name', '=', 'Pet Toys')])
