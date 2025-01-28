
from odoo import models, fields, api


class ModuloProducto(models.Model):
    _name="modulo.producto"
    _descripcion="Licencia de productos"
    
    name=fields.Char(string="Nombre de Licencia")
    precio_licencia=fields.Monetary(currency_field='currency_id', string="Precio", required=True)
    descripcion_licencia=fields.Text(string="Descripción de la Licencia")
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)



