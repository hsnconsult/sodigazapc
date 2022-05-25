# -*- coding: utf-8 -*-

from datetime import date, datetime, timedelta
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import re
import time

class ProductConfigurationSuite(models.Model):
    _inherit = 'purchase.order.line'
    
    #fields
    ptmpl_id=fields.Many2one('product.template',related="product_id.product_tmpl_id")
    
class ProductConfigurationSuite2(models.Model):
    _inherit = 'stock.production.lot'
    
    #fields
    stocklot=fields.Float('Stock du lot',digits=(16,2),compute='_isdastocklot',readonly=True,store=True,compute_sudo=True)
    #fonctions
    @api.depends('product_qty')
    def _isdastocklot(self):
        for rec in self:
            if rec.product_qty > 0:
                rec.stocklot = True
            else:
                rec.stocklot = False 
    
class ProductConfigurationCategory(models.Model):
    _inherit = 'product.category'
    
    #fields
    stock_minimal=fields.Float(string="Stock minimal")
   
     
class ProductConfiguration(models.Model):
    _inherit = 'product.template'
    
    #fields
    stock_minimaltmp=fields.Boolean(string="Stock minimal temp", compute='_istmpmin',readonly=True,store=True,compute_sudo=True)
    taxetmp=fields.Integer(string="Taxe temp", compute='_istaxetmp',readonly=True,store=True,compute_sudo=True)
    taxetmpwell=fields.Integer(string="Taxe Achat", compute='_istaxetmpwell',readonly=True,store=True,compute_sudo=True)
    idfamille=fields.Many2one('express_sdg.famille','Famille',required=False)
    idrayon=fields.Many2one('express_sdg.rayon','Rayon',required=False)
    order_ids = fields.One2many(string="Achats", comodel_name='purchase.order.line', inverse_name='ptmpl_id')
    pc_ids = fields.One2many(string="PrixVente", comodel_name='express_sdg.pricechange', inverse_name='ptmplid')
    #Stock minimal
    stock_minimal=fields.Float(string="Stock minimal")
    
    #fonctions
    @api.depends('stock_minimal','qty_available')
    def _istmpmin(self):
        for rec in self:
            if rec.qty_available <= rec.stock_minimal:
                rec.stock_minimaltmp = True
            else:
                rec.stock_minimaltmp = False
                  
    @api.onchange('list_price')
    def change_pv(self):
        newvalue = self.list_price
        oldvalue = self._origin.list_price
        protempid= self._origin.id 
        if(oldvalue!=newvalue):
            ki=self.env['express_sdg.pricechange']
            val={
            'track_pvtmp': oldvalue,
            'ptmplid': protempid
            }
            ki.create(val)
        else: 
            raise UserError(_("Le prix est toujours le même!"))  
        
    @api.depends('taxes_id')
    def _istaxetmp(self):
        for rec in self:
            if rec.taxes_id:
                rec.taxetmp = 1
            else:
                rec.taxetmp = 0
    
    @api.depends('supplier_taxes_id')
    def _istaxetmpwell(self):
        for rec in self:
            if rec.supplier_taxes_id:
                if rec.supplier_taxes_id.amount:
                    rec.taxetmpwell = rec.supplier_taxes_id.amount
                else:
                    rec.taxetmpwell = 0
            else:
                rec.taxetmpwell = 0
        
               
class PriceChange(models.Model):
    _name= 'express_sdg.pricechange'
    _description = 'la table contenant les pricechange'
    
    # static guys
    def get_dateop(self):
        return fields.Datetime.to_string(datetime.now())
    
    #fields
    ptmplid = fields.Many2one('product.template',"Article",required=False)
    user_id = fields.Many2one('res.users',"Utilisateur",required=True, default=lambda self:self.env.user)
    datepc = fields.Datetime(string="Date", required=True, default=get_dateop)
    track_pvtmp= fields.Float('Prix')
             
            
class ProductFamille(models.Model):
    _name = "express_sdg.famille"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'la table contenant les familles'
    
    #fields
    name = fields.Char(string="Famille", required=True)
    description = fields.Text("Description Famille",required=False,tracking=True)
    famille_ids = fields.One2many(string="Articlesfamille", comodel_name='product.template', inverse_name='idfamille')
    
    
class ProductRayon(models.Model):
    _name = "express_sdg.rayon"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'la table contenant les rayons'
    
    #fields
    name = fields.Char(string="Rayon", required=True)
    description = fields.Text("Description Rayon",required=False,tracking=True)
    rayon_ids = fields.One2many(string="Articlesrayon", comodel_name='product.template', inverse_name='idrayon')