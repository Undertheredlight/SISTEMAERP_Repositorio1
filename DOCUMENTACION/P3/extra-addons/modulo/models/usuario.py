
from odoo import models, fields, api


class ModuloUsuario(models.Model):
    _name="modulo.usuarios"
    _descripcion="Creacion de usuarios"

    name=fields.Char(String="Nombre de usuario")
    edad= fields.Integer(String="Edad")
    direccion=fields.Char(String="Dirección")
    telefono= fields.Integer(String="Teléfono")
    mail=fields.Char(String="Correo")
    producto=fields.Many2one('modulo.producto',String="Producto seleccionado")
    descripcion_producto = fields.Text(string="Descripción de la Licencia")
    nombre_producto = fields.Char(string="Nombre del producto")
    precio_producto=fields.Monetary(currency_field='currency_id', string="Precio", required=True)
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)

    @api.onchange('producto')
    def _onchange_producto(self):
        self.descripcion_producto = self.producto.descripcion_licencia
        self.nombre_producto = self.producto.name
        self.precio_producto = self.producto.precio_licencia

