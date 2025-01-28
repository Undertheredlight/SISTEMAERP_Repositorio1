from odoo import models, fields, api
import datetime
from calendar import monthrange


class ModuloPagos(models.Model):
    _name="modulo.pagos"
    _descripcion="Pagos Realizados"


    name=fields.Char(string="ID", default="Nuevo")
    nombre_licencia=fields.Char(string="Nombre de la Licencia")
    fecha_pago=fields.Date(string="Fecha de pago")
    fecha_proximo_pago=fields.Date(string="Próximo pago")
    usuario=fields.Many2one("modulo.usuarios", string="Cliente")
    importe=fields.Monetary(currency_field='currency_id', string="Precio", required=True)
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)


    @api.onchange('usuario')
    def _onchange_usuario(self):
        self.nombre_licencia = self.usuario.nombre_producto
        self.importe = self.usuario.precio_producto

    @api.model_create_multi
    def create(self, vals_list):

        #print("Hola:", vals_list)
        for vals in vals_list:
            if not vals.get('name') or vals['name'] == "Nuevo":
                vals['name'] = self.env['ir.sequence'].next_by_code("modulo.pagos")


        return super().create(vals_list) 
    
    #@api.onchange('fecha_pago')
    #def _onchange_fecha(self):
    #    if self.fecha_pago:
    #        self.fecha_proximo_pago = self.fecha_pago+datetime.timedelta(days=30)

    @api.onchange('fecha_pago')
    def _onchange_fecha(self):
        if self.fecha_pago:
            # Obtener el año y mes de la fecha de pago
            anio = self.fecha_pago.year
            mes = self.fecha_pago.month
            
            # Si es diciembre, el próximo mes es enero del siguiente año
            if mes == 12:
                proximo_mes = 1
                proximo_ano = anio + 1
            else:
                proximo_mes = mes + 1
                proximo_ano = anio
            
            # Establecer el próximo pago como el primer día del siguiente mes
            self.fecha_proximo_pago = fields.Date.to_string(datetime.date(proximo_ano, proximo_mes, 1))
            
            # Prorrateo: calcular el número de días en el mes de la fecha de pago
            dias_en_mes = monthrange(self.fecha_pago.year, self.fecha_pago.month)[1]
            
            # Calcular el número de días hasta el próximo pago
            dias_restantes = dias_en_mes - self.fecha_pago.day
            
            # Si se tiene el importe completo para un mes completo, calcular el prorrateo
            if self.importe:
                importe_prorrateado = self.importe * (dias_restantes / dias_en_mes)
                self.importe = importe_prorrateado


            