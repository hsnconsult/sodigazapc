# -*- coding: utf-8 -*-

from datetime import date, datetime, timedelta
from operator import ne
from threading import Condition
from odoo import models, fields, api, _
import re

#les differents transient classes

#transient moyenpaiement
class ExpressdgMoyenpaiement(models.TransientModel):
    _name = "express_sdg.moyenpaiement"
    _description = "table avec données temporaires moyenpaiement"
    
    #fields
    date_debut = fields.Date(string="Début", required=True, default=fields.Date.today)
    date_fin = fields.Date(string="Fin", required=True, default=fields.Date.today)
    
    # object moyenpaiement
    def action_done_moyenpaiement(self):
        data = {"debut": self.date_debut,
                "fin":self.date_fin}
        action = self.env.ref("express_sdg.report_moyenpaiement").report_action(
            self, data=data
        )
        action.update({'close_on_report_download': True})
        return action
    
    #excel moyenpaiement
    def action_done_moyenpaiementxlsx(self):
        data = {"debut": self.date_debut,
                "fin":self.date_fin}
         
        return self.env.ref("express_sdg.report_moyenpaiementxlsx").report_action(self, data=data)                   
        
    #delete function  
    def deletedonnees(self):
        cr = self.env.cr       
        #Désactivation des contraintes sur les tables à synchroniser
        tablesync = ['pos_session','pos_order','pos_order_line','pos_payment',
                     'stock_picking','stock_move','stock_move_line','account_move',
                     'purchase_order_line','purchase_order',
                     'account_move_line','stock_quant','product_category','product_template','product_product',
                     'stock_valuation_layer','stock_production_lot']            
        for table in tablesync:
            cr.execute("alter table "+table+" disable trigger all")
        #suppression
        for table in tablesync:
            reqins = "DELETE FROM public."+table+" ;"
            
            requete = reqins       
            cr.execute(requete)
            cr.commit()
        #Réactivation des contraintes sur les tables à synchroniser
        tablesync = ['pos_session','pos_order','pos_order_line','pos_payment',
                     'stock_picking','stock_move','stock_move_line','account_move',
                     'purchase_order_line','purchase_order',
                     'account_move_line','stock_quant','product_category','product_template','product_product',
                     'stock_valuation_layer','stock_production_lot']
        for table in tablesync:
            cr.execute("alter table "+table+" enable trigger all")
    
#transient stocks
class ExpressdgStocks(models.TransientModel):
    _name = "express_sdg.stocks"
    _description = "table avec données temporaires stocks"
    
    #fields
    date_debut = fields.Date(string="Début", required=True, default=fields.Date.today)
    date_fin = fields.Date(string="Fin", required=True, default=fields.Date.today)
    entrepot = fields.Many2one('stock.warehouse', required=False, string="Entrepôt")
    famille = fields.Many2one('express_sdg.famille', required=False, string="Famille")
    rayon = fields.Many2one('express_sdg.rayon', required=False, string="Rayon")
    categorie_article= fields.Many2one('product.category', required=False, string="Catégorie Produit")
    produit=fields.Many2one('product.product', required=False, string="Produit")
    ouivoir=fields.Boolean(string="PCAL,VSCA")
    
    # object stocks
    def action_done_stocks(self):
        data = {"debut": self.date_debut,
                "fin":self.date_fin,
                "warehouse":self.entrepot.name,
                "entrepot":self.entrepot.lot_stock_id.id,
                "famille":self.famille.id,
                "rayon":self.rayon.id,
                "categorie":self.categorie_article.id,
                "famille_name":self.famille.name,
                "rayon_name":self.rayon.name,
                "categorie_name":self.categorie_article.name,
                "produit":self.produit.id,
                "produit_name":self.produit.name,
                "ouivoir":self.ouivoir}
        action = self.env.ref("express_sdg.report_stocks").report_action(
            self, data=data
        )
        action.update({'close_on_report_download': True})
        return action
    
    #excel stocks
    def action_done_stocksxlsx(self):
        data = {"debut": self.date_debut,
                "fin":self.date_fin,
                "warehouse":self.entrepot.name,
                "entrepot":self.entrepot.lot_stock_id.id,
                "famille":self.famille.id,
                "rayon":self.rayon.id,
                "categorie":self.categorie_article.id,
                "famille_name":self.famille.name,
                "rayon_name":self.rayon.name,
                "categorie_name":self.categorie_article.name,
                "produit":self.produit.id,
                "produit_name":self.produit.name,
                "ouivoir":self.ouivoir}
                
        return self.env.ref("express_sdg.report_stocksxlsx").report_action(self, data=data)                   
        
    
#transient ventespos
class ExpressdgStocks(models.TransientModel):
    _name = "express_sdg.ventespos"
    _description = "table avec données temporaires ventespos"
    
    #fields
    date_debut = fields.Date(string="Début", required=True, default=fields.Date.today)
    date_fin = fields.Date(string="Fin", required=True, default=fields.Date.today)
    caissiere = fields.Many2one('res.users', required=False, string="Caissière")
    famille = fields.Many2one('express_sdg.famille', required=False, string="Famille")
    rayon = fields.Many2one('express_sdg.rayon', required=False, string="Rayon")
    categorie_article= fields.Many2one('product.category', required=False, string="Catégorie Produit")
    point_vente=fields.Many2one('pos.config', required=False, string="Point de vente")
    produitv=fields.Many2one('product.product', required=False, string="Produit")
    # object ventespos
    def action_done_ventespos(self):
        data = {"debut": self.date_debut,
                "fin":self.date_fin,
                "caissiere":self.caissiere.id,
                "famille":self.famille.id,
                "rayon":self.rayon.id,
                "categorie":self.categorie_article.id,
                "caissiere_name":self.caissiere.name,
                "famille_name":self.famille.name,
                "rayon_name":self.rayon.name,
                "categorie_name":self.categorie_article.name,
                "produit":self.produitv.id,
                "produit_name":self.produitv.name,
                "pointdevente":self.point_vente.id,
                "pointdevente_name":self.point_vente.name}
        action = self.env.ref("express_sdg.report_ventespos").report_action(
            self, data=data
        )
        action.update({'close_on_report_download': True})
        return action

    #excel ventespos
    def action_done_ventesposxlsx(self):
        data = {"debut": self.date_debut,
                "fin":self.date_fin,
                "caissiere":self.caissiere.id,
                "famille":self.famille.id,
                "rayon":self.rayon.id,
                "categorie":self.categorie_article.id,
                "caissiere_name":self.caissiere.name,
                "famille_name":self.famille.name,
                "rayon_name":self.rayon.name,
                "categorie_name":self.categorie_article.name,
                "produit":self.produitv.id,
                "produit_name":self.produitv.name,
                "pointdevente":self.point_vente.id,
                "pointdevente_name":self.point_vente.name}
                
        return self.env.ref("express_sdg.report_ventesposxlsx").report_action(self, data=data)

#transient peremption
class ExpressdgPeremption(models.TransientModel):
    _name = "express_sdg.peremption"
    _description = "table avec données temporaires peremption"
    
    #fields
    date_debut = fields.Date(string="Début", required=True, default=fields.Date.today)
    date_fin = fields.Date(string="Fin", required=True, default=fields.Date.today)
    entrepot = fields.Many2one('stock.warehouse', required=False, string="Entrepôt")
    famille = fields.Many2one('express_sdg.famille', required=False, string="Famille")
    rayon = fields.Many2one('express_sdg.rayon', required=False, string="Rayon")
    categorie_article= fields.Many2one('product.category', required=False, string="Catégorie Produit")
    produit=fields.Many2one('product.product', required=False, string="Produit")
    lot=fields.Many2one('stock.production.lot', required=False, string="Lot")
    # object peremption
    def action_done_peremption(self):
        data = {"debut": self.date_debut,
                "fin":self.date_fin,
                "entrepot":self.entrepot.lot_stock_id.id,
                "famille":self.famille.id,
                "rayon":self.rayon.id,
                "categorie":self.categorie_article.id,
                "entrepot_name":self.entrepot.name,
                "famille_name":self.famille.name,
                "rayon_name":self.rayon.name,
                "categorie_name":self.categorie_article.name,
                "produit":self.produit.id,
                "produit_name":self.produit.name,
                "lot":self.lot.id,
                "lot_name":self.lot.name}
        action = self.env.ref("express_sdg.report_peremption").report_action(
            self, data=data
        )
        action.update({'close_on_report_download': True})
        return action
    
    #excel peremption
    def action_done_peremptionxlsx(self):
        data = {"debut": self.date_debut,
                "fin":self.date_fin,
                "entrepot":self.entrepot.lot_stock_id.id,
                "famille":self.famille.id,
                "rayon":self.rayon.id,
                "categorie":self.categorie_article.id,
                "entrepot_name":self.entrepot.name,
                "famille_name":self.famille.name,
                "rayon_name":self.rayon.name,
                "categorie_name":self.categorie_article.name,
                "produit":self.produit.id,
                "produit_name":self.produit.name,
                "lot":self.lot.id,
                "lot_name":self.lot.name}
                
        return self.env.ref("express_sdg.report_peremptionxlsx").report_action(self, data=data)

#les differents abstract classes
# debut histoavxlsx
class ExpressdgHistoavxlsxabstract(models.AbstractModel):
    _name = "report.express_sdg.report_histoav_templatexlsx"
    _inherit="report.report_xlsx.abstract"
    _description = "table avec données pour le template report_histoav_templatexlsx"
    
    def _get_report_values(self, docids, data=None):
        print('docids',docids)
        print('kiiiii',docids[0])
        return{
            "docids":docids,
            "lui":docids.ids
        }
    def generate_xlsx_report(self, workbook, data, docids):
        
        lines=self._get_report_values(docids)
        # print(lines)
        # print('\nnopeopoepeoeoeoepeoe')
        # print('nope',lines)
        # print('nope2',lines['lui'])
        selected_records=self.env['product.template'].browse(lines['lui'])
        # print('\nnnowa',selected_records)
        # print('\nplus tard',self.env['product.template'].search([('id', 'in', lines['lui'])]))       
        # print('\nseul',self.env['product.template'].search_read([('id', 'in', lines['lui'])]))       
        force=[]
        for record in selected_records:
            val={
                "id":record.id,
                "nom":record.name,
                "order_ids":record.order_ids,
                "pc_ids":record.pc_ids,
            }
            force.append(val)
        # print('\nforce',force)
        bolth = workbook.add_format({'bold': 1,'align': 'center','fg_color': 'green','border': 1})
        boltd = workbook.add_format({'border': 1})
        my_format=workbook.add_format({'border': 1,'num_format':'dd/mm/yyyy'})
        boltdsep = workbook.add_format({'border': 1,'num_format':'# ##0'})
        ident = workbook.add_format({'bold': 1,'border': 1,'align': 'center','valign': 'vcenter','fg_color': 'yellow'})
        identbo = workbook.add_format({'bold': 1,'border': 1,'align': 'center','valign': 'vcenter','fg_color': 'orange'})
        for produit in force:
            # print(force['nom'])"'"+produit['nom']+"'"
            # sheetlib=force['nom']
            worksheet = workbook.add_worksheet(produit['nom'])
            worksheet.set_column(0, 4, 15)
            col=0
            row=2
            worksheet.merge_range(0, col,0,col+4, produit['nom'],identbo)
            worksheet.merge_range(1, col,1,col+2, "Historique des prix d'achat",ident)
            worksheet.merge_range(1, col+3,1,col+4, 'Historique des prix de vente',ident)
            worksheet.write(row, col, 'Fournisseur',bolth)
            worksheet.write(row, col + 1, 'Prix',bolth)
            worksheet.write(row, col + 2, 'Date',bolth)
            worksheet.write(row, col+3, 'Prix',bolth)
            worksheet.write(row, col + 4, 'Date',bolth)
            for order in produit['order_ids']:
                row+=1
                # print(order.partner_id)
                worksheet.write(row, col, order.partner_id.name,boltd)
                worksheet.write(row, col+1, order.price_unit,boltdsep)
                worksheet.write(row, col+2, order.date_planned,my_format)       
            row2=2   
            for sell in produit['pc_ids']:
                row2+=1
                worksheet.write(row2, col+3, sell.track_pvtmp,boltdsep)
                worksheet.write(row2, col+4, sell.datepc,my_format) 
        # selected_ids=self.env.context.get('active_ids',[])
        # selected_records=self.env['product.template'].browse(selected_ids)
        # print(selected_ids)
        # print(selected_records)
        # domain = []
        # print('\nlalalaallalalalalalalala',self.active_id)
        # print('\nidsssssssss',self.active_ids)
        # for produit in self.env['product.template'].search(domain):
        #     for order in produit['order_ids']:
        #         row+=1
        #         worksheet.write(row, col, order['price_unit'],boltd)
        #         worksheet.write(row, col+1, order['date_planned'],boltd)
        #         print(order['price_unit'])
                
        #     for sell in produit['pc_ids']:
        #         row+=1
        #         worksheet.write(row, col, sell['track_pvtmp'],boltd)
        #         worksheet.write(row, col+1, sell['datepc'],boltd)     
# fin histoavxlsx

# debut peremption
class ExpressdgPeremptionabstract(models.AbstractModel):
    _name = "report.express_sdg.report_peremption_template"
    _description = "table avec données pour le template report_peremption_template"

    def _get_report_values(self, docids, data=None):
        argu=(data.get("debut"),data.get("fin"),)
        condition=""
        if data.get("entrepot"):
            condition+=" and l.id="+str(data.get("entrepot"))
        if data.get("rayon"):
            condition+=" and r.id="+str(data.get("rayon")) 
        if data.get("famille"):
            condition+=" and f.id="+str(data.get("famille"))
        if data.get("categorie"):
            condition+=" and c.id="+str(data.get("categorie"))
        if data.get("produit"):
            condition+=" and p.id="+str(data.get("produit"))
        if data.get("lot"):
            condition+=" and lot.id="+str(data.get("lot"))
        queryq="""SELECT p.id as produit_id, t.name as produit,
        c.id as c_id,c.name as categorie,
        r.id as r_id,r.name as rayon,
        f.id as f_id,f.name as famille, 
        q.location_id, 
        sum(q.quantity) as stockglobal, 
        l.complete_name,w.name as magasin_name, 
        lot.name as lot_name,lot.id as lot_id, 
        lot.expiration_date
        FROM public.product_product p,
        public.product_template t,
        public.stock_quant q,
        public.stock_location l,
        public.stock_warehouse w,
        public.stock_production_lot lot,
        express_sdg_rayon r, express_sdg_famille f,
        product_category c
        where p.product_tmpl_id=t.id and 
        q.product_id=p.id and 
        q.quantity >0 and
        q.location_id=l.id and
        l.id=w.lot_stock_id and
        q.lot_id=lot.id and
        lot.expiration_date::date between %s and %s
        and c.id=t.categ_id and r.id=t.idrayon 
        and f.id=t.idfamille """+condition+""" 
        group by lot.id,p.id,t.name,q.location_id,
        l.complete_name,w.name,lot.name,
        lot.expiration_date,
        c.id,c.name,r.id,r.name,f.id,f.name
        order by lot.expiration_date"""        
        self.env.cr.execute(queryq, argu)
        rec=self.env.cr.dictfetchall()
        return {
            "docs": rec,
            "data": data,
        }
# fin peremption

# debut peremptionxlsx
class ExpressdgPeremptionxlsxabstract(models.AbstractModel):
    _name = "report.express_sdg.report_peremption_templatexlsx"
    _inherit="report.report_xlsx.abstract"
    _description = "table avec données pour le template report_peremption_templatexlsx"
    
    def generate_xlsx_report(self, workbook, data, lines):
        argu=(data.get("debut"),data.get("fin"),)
        condition=""
        if data.get("entrepot"):
            condition+=" and l.id="+str(data.get("entrepot"))
        if data.get("rayon"):
            condition+=" and r.id="+str(data.get("rayon")) 
        if data.get("famille"):
            condition+=" and f.id="+str(data.get("famille"))
        if data.get("categorie"):
            condition+=" and c.id="+str(data.get("categorie"))
        if data.get("produit"):
            condition+=" and p.id="+str(data.get("produit"))
        if data.get("lot"):
            condition+=" and lot.id="+str(data.get("lot"))
        queryq="""SELECT p.id as produit_id, t.name as produit,
        c.id as c_id,c.name as categorie,
        r.id as r_id,r.name as rayon,
        f.id as f_id,f.name as famille, 
        q.location_id, 
        sum(q.quantity) as stockglobal, 
        l.complete_name,w.name as magasin_name, 
        lot.name as lot_name,lot.id as lot_id, 
        lot.expiration_date::date
        FROM public.product_product p,
        public.product_template t,
        public.stock_quant q,
        public.stock_location l,
        public.stock_warehouse w,
        public.stock_production_lot lot,
        express_sdg_rayon r, express_sdg_famille f,
        product_category c
        where p.product_tmpl_id=t.id and 
        q.product_id=p.id and 
        q.quantity >0 and
        q.location_id=l.id and
        l.id=w.lot_stock_id and
        q.lot_id=lot.id and
        lot.expiration_date::date between %s and %s
        and c.id=t.categ_id and r.id=t.idrayon 
        and f.id=t.idfamille """+condition+""" 
        group by lot.id,p.id,t.name,q.location_id,
        l.complete_name,w.name,lot.name,
        lot.expiration_date,
        c.id,c.name,r.id,r.name,f.id,f.name
        order by lot.expiration_date"""        
        self.env.cr.execute(queryq, argu)
        rec=self.env.cr.dictfetchall()
        #document excel
        ident = workbook.add_format({'bold': 1,'border': 1,'align': 'center','valign': 'vcenter','fg_color': 'yellow'})
        bold = workbook.add_format({'bold': True, 'align': 'center','fg_color': '#2F75B5','border': 1})
        boldata = workbook.add_format({'align': 'center','fg_color': '#2A83G9','border': 1})
        bolth = workbook.add_format({'bold': 1,'align': 'center','fg_color': 'green','border': 1})
        boltd = workbook.add_format({'border': 1})
        my_format=workbook.add_format({'border': 1,'num_format':'dd/mm/yyyy'})
        worksheet = workbook.add_worksheet('Données')
        worksheet.set_column(0, 0, 10)
        worksheet.set_column(1, 1, 50)
        worksheet.set_column(2, 3, 15)
        worksheet.set_column(4, 4, 30)
        worksheet.set_column(5, 5, 10)
        worksheet.set_column(6, 7, 15)
        worksheet.set_column(8, 8, 20)
        col=0
        row=1
        worksheet.merge_range(0, col + 6,0, col + 7, 'Magasin', ident)
        worksheet.write(row, col, 'Lot',bolth)
        worksheet.write(row, col + 1, 'Produit',bolth)
        worksheet.write(row, col + 2, 'Rayon',bolth)
        worksheet.write(row, col + 3, 'Famille',bolth)
        worksheet.write(row, col + 4, 'Catégorie',bolth)
        worksheet.write(row, col + 5, 'Stock',bolth)
        worksheet.write(row, col + 6, 'nom',bolth)
        worksheet.write(row, col + 7, 'code',bolth)
        worksheet.write(row, col + 8, 'Date Expiration',bolth)     
        for line in rec:
            row+=1
            worksheet.write(row, col, line['lot_name'],boltd)
            worksheet.write(row, col+1, line.get("produit"),boltd)
            worksheet.write(row, col+2, line['rayon'],boltd)
            worksheet.write(row, col+3, line.get("famille"),boltd)
            worksheet.write(row, col+4, line['categorie'],boltd)
            worksheet.write(row, col+5, line.get("stockglobal"),boltd)
            worksheet.write(row, col+6, line['magasin_name'],boltd)
            worksheet.write(row, col+7, line.get("complete_name"),boltd)
            worksheet.write(row, col+8, line['expiration_date'],my_format)
        worksheet2 = workbook.add_worksheet('Paramètres')
        worksheet2.set_column(0, 1, 15)      
        worksheet2.write('A1', 'Date de début', bold)
        worksheet2.write('A2', 'Date de fin', bold)
        worksheet2.write('A3', 'Entrepôt', bold)
        worksheet2.write('A4', 'Famille', bold)
        worksheet2.write('A5', 'Rayon', bold)
        worksheet2.write('A6', 'Catégorie', bold)
        worksheet2.write('A7', 'Produit', bold)
        worksheet2.write('A8', 'Lot', bold)
        worksheet2.write('B1', data.get("debut"),boldata)
        worksheet2.write('B2', data.get("fin"),boldata)
        worksheet2.write('B3', data.get("entrepot_name"),boldata)
        worksheet2.write('B4', data.get("famille_name"),boldata)
        worksheet2.write('B5', data['rayon_name'],boldata)
        worksheet2.write('B6', data['categorie_name'],boldata)
        worksheet2.write('B7', data['produit_name'],boldata)
        worksheet2.write('B8', data['lot_name'],boldata)
# fin peremptionxlsx

# debut moyenpaiement
class ExpressdgMoyenpaiementabstract(models.AbstractModel):
    _name = "report.express_sdg.report_moyenpaiement_template"
    _description = "table avec données pour le template report_moyenpaiement_template"

    def _get_report_values(self, docids, data=None):
        docs = []
        query = """ SELECT ppm.name as moyenpaiement,sum(pp.amount) as montant
            FROM public.pos_payment as pp,
                public.pos_payment_method as ppm
            WHERE pp.payment_method_id=ppm.id and 
            pp.payment_date::date between %s and %s
            group by ppm.name """
        self.env.cr.execute(query, (data.get("debut"),data.get("fin"),))
        for rec in self.env.cr.dictfetchall():
            val = {
                "moyenpaiement": rec.get("moyenpaiement"),
                "montant": rec.get("montant"),
            }
            docs.append(val)
        return {
            "docs": docs,
            "data": data,
        }
# fin moyenpaiement

# debut moyenpaiementxlsx
class ExpressdgMoyenpaiementxlsxabstract(models.AbstractModel):
    _name = "report.express_sdg.report_moyenpaiement_templatexlsx"
    _inherit="report.report_xlsx.abstract"
    _description = "table avec données pour le template report_moyenpaiement_templatexlsx"
    
    def generate_xlsx_report(self, workbook, data, lines):
        query = """ SELECT ppm.name as moyenpaiement,sum(pp.amount) as montant
            FROM public.pos_payment as pp,
            public.pos_payment_method as ppm
            WHERE pp.payment_method_id=ppm.id and 
            pp.payment_date::date between %s and %s
            group by ppm.name """
        self.env.cr.execute(query, (data.get("debut"),data.get("fin"),))
        result = self.env.cr.dictfetchall()
        #document excel
        bold = workbook.add_format({'bold': True, 'align': 'center','fg_color': '#2F75B5','border': 1})
        boldata = workbook.add_format({'align': 'center','fg_color': '#2A83G9','border': 1})
        bolth = workbook.add_format({'bold': 1,'align': 'center','fg_color': 'green','border': 1})
        boltd = workbook.add_format({'border': 1})
        worksheet = workbook.add_worksheet('Données')
        worksheet.set_column(0, 1, 20)
        col=0
        row=0
        worksheet.write(row, col, 'Moyen de paiement',bolth)
        worksheet.write(row, col + 1, 'Montant',bolth)
        for line in result:
            row+=1
            worksheet.write(row, col, line['moyenpaiement'],boltd)
            worksheet.write(row, col+1, line.get("montant"),boltd)
        worksheet2 = workbook.add_worksheet('Paramètres')
        worksheet2.set_column(0, 1, 15)     
        worksheet2.write('A1', 'Date de début', bold)
        worksheet2.write('A2', 'Date de fin', bold)
        worksheet2.write('B1', data.get("debut"),boldata)
        worksheet2.write('B2', data.get("fin"),boldata)
# fin moyenpaiementxlsx

# debut ventespos
class ExpressdgVentesposabstract(models.AbstractModel):
    _name = "report.express_sdg.report_ventespos_template"
    _description = "table avec données pour le template report_ventespos_template"

    def _get_report_values(self, docids, data=None):
        condition=""
        if data.get("caissiere"):
            condition+=" and rl.caissier_id="+str(data.get("caissiere"))
        if data.get("rayon"):
            condition+=" and rl.rayonid="+str(data.get("rayon")) 
        if data.get("famille"):
            condition+=" and rl.familleid="+str(data.get("famille"))
        if data.get("categorie"):
            condition+=" and rl.categorieid="+str(data.get("categorie"))
        if data.get("produit"):
            condition+=" and rl.product_id="+str(data.get("produit"))
        if data.get("pointdevente"):
            condition+=" and rl.pdv_id="+str(data.get("pointdevente"))
        queryq="""with purchaselineforder as (SELECT 
        svl.product_id,sum(-svl.quantity) as quantity,
        sum(svl.unit_cost),sum(-svl.value) as value
        FROM public.stock_valuation_layer svl, public.product_product p
        where description like '%POS%'
        and svl.product_id = p.id
        and svl.create_date::date between '"""+str(data.get("debut"))+"""' and '"""+str(data.get("fin"))+"""' 
        group by svl.product_id
        order by quantity,product_id),
        orderlineforder as (SELECT 
        pt.taxetmpwell,pol.product_id,sum(pol.qty) as qtv,
        esr.id as rayonid,esf.id as familleid,
        pc.id as categorieid,pt.name as produit,
        esr.name as rayon,pt.default_code,
        esf.name as famille,pc.name as categorie,
        (sum(pol.price_subtotal_incl)-sum(pol.price_subtotal))::decimal(16,2) as mtaxe,
        sum(pol.price_subtotal)::decimal(16,2) as tht,
        sum(pol.price_subtotal_incl)::decimal(16,2) as ttc
        FROM public.pos_order po,
        public.pos_order_line pol, 
        public.product_product pp,
        public.product_template pt,
        public.product_category pc,
        public.express_sdg_rayon esr,
        public.express_sdg_famille esf,
        public.res_users ru,
        public.pos_session pos,
        public.pos_config poc
        where po.id=pol.order_id
        and po.session_id=pos.id
        and pos.config_id=poc.id
        and pp.id=pol.product_id
        and po.state='done'
        and pp.product_tmpl_id=pt.id
        and pt.categ_id=pc.id
        and esr.id=pt.idrayon
        and esf.id=pt.idfamille
        and ru.id=po.user_id
        and po.date_order::date between '"""+str(data.get("debut"))+"""' and '"""+str(data.get("fin"))+"""'
        group by pt.taxetmpwell,pol.product_id,rayonid,familleid,categorieid,produit,
        rayon,famille,categorie,pt.name,pt.default_code
        order by product_id),
        purchaseline as(select 
        row_number() over() as yea,plf.* 
        from purchaselineforder plf where plf.quantity!=0),
        orderline as (select 
        row_number() over() as yea,olf.* 
        from orderlineforder olf where olf.qtv!=0),
        resultline as
        (select ol.product_id,ol.taxetmpwell,ol.qtv,
        ol.rayonid,ol.familleid,ol.categorieid,ol.produit,ol.rayon,ol.famille,ol.categorie,
        ol.mtaxe,ol.tht,ol.ttc,pl.value as caht,(pl.value*ol.taxetmpwell/100)::decimal(16,2) as mtaxeca,
        (pl.value+(pl.value*ol.taxetmpwell/100))::decimal(16,2) as catc, 
        (ol.tht-pl.value)::decimal(16,2) as mgt, ((ol.tht-pl.value)/ol.qtv)::decimal(16,2) as mgu, ol.default_code
        from orderline ol,purchaseline pl
        where ol.product_id=pl.product_id)
        select rl.product_id,rl.default_code,rl.taxetmpwell,sum(rl.qtv) as qtv,
        rl.rayonid,rl.familleid,rl.categorieid,rl.rayon,
        rl.famille,rl.categorie,sum(rl.mtaxe) as mtaxe,sum(rl.tht) as tht,sum(rl.ttc) as ttc,
        sum(rl.caht) as caht,sum(rl.mtaxeca) as mtaxeca,sum(rl.catc) as catc,sum(rl.mgt) as mgt,(sum(rl.mgt)/sum(rl.qtv))::decimal(16,2) as mgu,rl.produit
        from resultline rl
        where 1=1 """+condition+"""  
        group by rl.product_id,rl.taxetmpwell,
        rl.rayonid,rl.familleid,rl.categorieid,rl.rayon,
        rl.famille,rl.categorie,rl.produit,rl.default_code
        order by produit""" 
        self.env.cr.execute(queryq)
        rec=self.env.cr.dictfetchall()
        print(rec)
        return {
            "docs": rec,
            "data": data,
        }
# fin ventespos

# debut ventesposxlsx
class ExpressdgVentesposxlsxabstract(models.AbstractModel):
    _name = "report.express_sdg.report_ventespos_templatexlsx"
    _inherit="report.report_xlsx.abstract"
    _description = "table avec données pour le template report_ventespos_templatexlsx"
    
    def generate_xlsx_report(self, workbook, data, lines):
        condition=""
        if data.get("caissiere"):
            condition+=" and rl.caissier_id="+str(data.get("caissiere"))
        if data.get("rayon"):
            condition+=" and rl.rayonid="+str(data.get("rayon")) 
        if data.get("famille"):
            condition+=" and rl.familleid="+str(data.get("famille"))
        if data.get("categorie"):
            condition+=" and rl.categorieid="+str(data.get("categorie"))
        if data.get("produit"):
            condition+=" and rl.product_id="+str(data.get("produit"))
        if data.get("pointdevente"):
            condition+=" and rl.pdv_id="+str(data.get("pointdevente"))
        queryq="""with purchaselineforder as (SELECT 
        svl.product_id,sum(-svl.quantity) as quantity,
        sum(svl.unit_cost),sum(-svl.value) as value
        FROM public.stock_valuation_layer svl, public.product_product p
        where description like '%POS%'
        and svl.product_id = p.id
        and svl.create_date::date between '"""+str(data.get("debut"))+"""' and '"""+str(data.get("fin"))+"""' 
        group by svl.product_id
        order by quantity,product_id),
        orderlineforder as (SELECT 
        pt.taxetmpwell,pol.product_id,sum(pol.qty) as qtv,
        esr.id as rayonid,esf.id as familleid,
        pc.id as categorieid,pt.name as produit,
        esr.name as rayon,pt.default_code,
        esf.name as famille,pc.name as categorie,
        (sum(pol.price_subtotal_incl)-sum(pol.price_subtotal))::decimal(16,2) as mtaxe,
        sum(pol.price_subtotal)::decimal(16,2) as tht,
        sum(pol.price_subtotal_incl)::decimal(16,2) as ttc
        FROM public.pos_order po,
        public.pos_order_line pol, 
        public.product_product pp,
        public.product_template pt,
        public.product_category pc,
        public.express_sdg_rayon esr,
        public.express_sdg_famille esf,
        public.res_users ru,
        public.pos_session pos,
        public.pos_config poc
        where po.id=pol.order_id
        and po.session_id=pos.id
        and pos.config_id=poc.id
        and pp.id=pol.product_id
        and po.state='done'
        and pp.product_tmpl_id=pt.id
        and pt.categ_id=pc.id
        and esr.id=pt.idrayon
        and esf.id=pt.idfamille
        and ru.id=po.user_id
        and po.date_order::date between '"""+str(data.get("debut"))+"""' and '"""+str(data.get("fin"))+"""'
        group by pt.taxetmpwell,pol.product_id,rayonid,familleid,categorieid,produit,
        rayon,famille,categorie,pt.name,pt.default_code
        order by product_id),
        purchaseline as(select 
        row_number() over() as yea,plf.* 
        from purchaselineforder plf where plf.quantity!=0),
        orderline as (select 
        row_number() over() as yea,olf.* 
        from orderlineforder olf where olf.qtv!=0),
        resultline as
        (select ol.product_id,ol.taxetmpwell,ol.qtv,
        ol.rayonid,ol.familleid,ol.categorieid,ol.produit,ol.rayon,ol.famille,ol.categorie,
        ol.mtaxe,ol.tht,ol.ttc,pl.value as caht,(pl.value*ol.taxetmpwell/100)::decimal(16,2) as mtaxeca,
        (pl.value+(pl.value*ol.taxetmpwell/100))::decimal(16,2) as catc, 
        (ol.tht-pl.value)::decimal(16,2) as mgt, ((ol.tht-pl.value)/ol.qtv)::decimal(16,2) as mgu, ol.default_code
        from orderline ol,purchaseline pl
        where ol.product_id=pl.product_id)
        select rl.product_id,rl.default_code,rl.taxetmpwell,sum(rl.qtv) as qtv,
        rl.rayonid,rl.familleid,rl.categorieid,rl.rayon,
        rl.famille,rl.categorie,sum(rl.mtaxe) as mtaxe,sum(rl.tht) as tht,sum(rl.ttc) as ttc,
        sum(rl.caht) as caht,sum(rl.mtaxeca) as mtaxeca,sum(rl.catc) as catc,sum(rl.mgt) as mgt,(sum(rl.mgt)/sum(rl.qtv))::decimal(16,2) as mgu,rl.produit
        from resultline rl
        where 1=1 """+condition+"""  
        group by rl.product_id,rl.taxetmpwell,
        rl.rayonid,rl.familleid,rl.categorieid,rl.rayon,
        rl.famille,rl.categorie,rl.produit,rl.default_code
        order by produit"""     
        self.env.cr.execute(queryq)
        rec=self.env.cr.dictfetchall()
        #document excel
        bold = workbook.add_format({'bold': True, 'align': 'center','fg_color': '#2F75B5','border': 1})
        boldata = workbook.add_format({'align': 'center','fg_color': '#2A83G9','border': 1})
        bolth = workbook.add_format({'bold': 1,'align': 'center','fg_color': 'green','border': 1})
        boltd = workbook.add_format({'border': 1})
        boltdsep = workbook.add_format({'border': 1,'num_format':'# ##0'})
        worksheet = workbook.add_worksheet('Données')
        worksheet.set_column(0, 0, 20)
        worksheet.set_column(1, 1, 50)
        worksheet.set_column(2, 3, 15)
        worksheet.set_column(4, 4, 30)
        worksheet.set_column(5, 5, 15)
        worksheet.set_column(6, 13, 20)
        col=0
        row=0
        worksheet.write(row, col, 'Référence interne',bolth)
        worksheet.write(row, col+1, 'Produit',bolth)
        worksheet.write(row, col + 2, 'Rayon',bolth)
        worksheet.write(row, col + 3, 'Famille',bolth)
        worksheet.write(row, col + 4, 'Catégorie',bolth)
        worksheet.write(row, col + 5, 'Quantité vendue',bolth)
        worksheet.write(row, col + 6, 'Total Vente HT',bolth)
        worksheet.write(row, col + 7, 'Montant TVA Vente',bolth)
        worksheet.write(row, col + 8, 'Total Vente TTC',bolth)
        worksheet.write(row, col + 9, 'Total Coût Achat HT',bolth)
        worksheet.write(row, col + 10, 'Montant TVA Achat',bolth)
        worksheet.write(row, col + 11, 'Total Coût Achat TTC',bolth)
        worksheet.write(row, col + 12, 'Marge totale',bolth)
        worksheet.write(row, col + 13, 'Marge unitaire',bolth)      
        for line in rec:
            row+=1
            worksheet.write(row, col, line['default_code'],boltd)
            worksheet.write(row, col+1, line['produit'],boltd)
            worksheet.write(row, col+2, line.get("rayon"),boltd)
            worksheet.write(row, col+3, line['famille'],boltd)
            worksheet.write(row, col+4, line.get("categorie"),boltd)
            worksheet.write(row, col+5, line['qtv'],boltdsep)
            worksheet.write(row, col+6, line.get("tht"),boltdsep)
            worksheet.write(row, col+7, line['mtaxe'],boltdsep)
            worksheet.write(row, col+8, line.get("ttc"),boltdsep)
            worksheet.write(row, col+9, line['caht'],boltdsep)
            worksheet.write(row, col+10, line.get("mtaxeca"),boltdsep)
            worksheet.write(row, col+11, line['catc'],boltdsep)
            worksheet.write(row, col+12, line.get("mgt"),boltdsep)
            worksheet.write(row, col+13, line.get("mgu"),boltdsep)           
        worksheet2 = workbook.add_worksheet('Paramètres')
        worksheet2.set_column(0, 1, 15)     
        worksheet2.write('A1', 'Date de début', bold)
        worksheet2.write('A2', 'Date de fin', bold)
        worksheet2.write('A3', 'Caissière', bold)
        worksheet2.write('A4', 'Famille', bold)
        worksheet2.write('A5', 'Rayon', bold)
        worksheet2.write('A6', 'Catégorie', bold)
        worksheet2.write('A7', 'Produit', bold)
        worksheet2.write('A8', 'Point de vente', bold)
        worksheet2.write('B1', data.get("debut"),boldata)
        worksheet2.write('B2', data.get("fin"),boldata)
        worksheet2.write('B3', data.get("caissiere_name"),boldata)
        worksheet2.write('B4', data.get("famille_name"),boldata)
        worksheet2.write('B5', data['rayon_name'],boldata)
        worksheet2.write('B6', data['categorie_name'],boldata)
        worksheet2.write('B7', data['produit_name'],boldata)
        worksheet2.write('B8', data['pointdevente_name'],boldata)
# fin ventesposxlsx

# debut stocks
class ExpressdgStocksabstract(models.AbstractModel):
    _name = "report.express_sdg.report_stocks_template"
    _description = "table avec données pour le template report_stocks_template"

    def _get_report_values(self, docids, data=None):
        argu=(data.get("debut"),data.get("debut"),data.get("debut"),data.get("fin"),
              data.get("debut"),data.get("fin"),)
        condition=""
        condition2=""
        if data.get("entrepot"):
            condition+=" and s.location_id="+str(data.get("entrepot"))
            condition2+=" and s.location_dest_id="+str(data.get("entrepot"))
        if data.get("rayon"):
            condition+=" and r.id="+str(data.get("rayon")) 
            condition2+=" and r.id="+str(data.get("rayon"))
        if data.get("famille"):
            condition+=" and f.id="+str(data.get("famille"))
            condition2+=" and f.id="+str(data.get("famille")) 
        if data.get("categorie"):
            condition+=" and c.id="+str(data.get("categorie"))
            condition2+=" and c.id="+str(data.get("categorie"))
        if data.get("produit"):
            condition+=" and p.id="+str(data.get("produit"))
            condition2+=" and p.id="+str(data.get("produit")) 
        req="""with stinitentree as (
        SELECT s.product_id, sum(s.qty_done) as qty_done,
        lot.id as lot_id,lot.name as lot_name,sm.price_unit as price_unit,lot.use_date::date as dateuse
        FROM stock_move_line s, stock_move sm, stock_location l, 
        product_product p,product_template t, 
        product_category c, express_sdg_rayon r, 
        express_sdg_famille f,public.stock_production_lot lot
        WHERE s.location_dest_id = l.id 
        and sm.id=s.move_id
        and lot.id=s.lot_id
        AND l.usage = 'internal'
        AND p.product_tmpl_id = t.id
        and p.id=s.product_id
        and t.categ_id=c.id
        and r.id=t.idrayon
        and f.id=t.idfamille """+condition2+"""
        AND s.date::date<%s 
        GROUP BY s.product_id,lot.id,lot.name,sm.price_unit
        ),
        stinitsortie as  (
        SELECT s.product_id, sum(s.qty_done) as qty_done,
        lot.id as lot_id,lot.name as lot_name,lot.use_date::date as dateuse
        FROM stock_move_line s,stock_move sm, stock_location l,product_product p, product_template t, 
        product_category c, express_sdg_rayon r, express_sdg_famille f,public.stock_production_lot lot
        WHERE s.location_id = l.id
        and sm.id=s.move_id
        and lot.id=s.lot_id
        AND l.usage = 'internal'
        AND p.product_tmpl_id = t.id
        and p.id=s.product_id
        and t.categ_id=c.id
        and r.id=t.idrayon
        and f.id=t.idfamille """+condition+"""
        AND s.date::date<%s
        AND s.state = 'done'
        GROUP BY s.product_id,lot.id,lot.name
        ),
        stinit as (
        SELECT coalesce(se.product_id,ss.product_id) as product_id, coalesce(se.qty_done,0)-coalesce(ss.qty_done,0) as stockinit
        ,coalesce(se.lot_id,ss.lot_id) as lot_id,coalesce(se.lot_name,ss.lot_name) as lot_name,se.price_unit,coalesce(se.dateuse,ss.dateuse) as dateuse
        FROM stinitentree se
        FULL JOIN stinitsortie ss
        ON se.product_id = ss.product_id and se.lot_id=ss.lot_id
        ),
        entree as (
        SELECT s.product_id, sum(qty_done) as qte_entree
        ,lot.id as lot_id,lot.name as lot_name,sm.price_unit as price_unit,lot.use_date::date as dateuse
        FROM stock_move_line s, stock_location l,product_product p, product_template t, product_category c, express_sdg_rayon r, express_sdg_famille f
        ,public.stock_production_lot lot,stock_move sm
        WHERE s.location_dest_id = l.id
        and sm.id=s.move_id
        and lot.id=s.lot_id
        AND p.product_tmpl_id = t.id
        and p.id=s.product_id
        and t.categ_id=c.id
        and r.id=t.idrayon
        and f.id=t.idfamille """+condition2+"""
        AND l.usage = 'internal'
        AND s.date::date BETWEEN %s AND %s
        AND s.state = 'done'
        GROUP BY s.product_id,lot.id,lot.name,sm.price_unit
        ),
        sortie as (
        SELECT s.product_id, sum(qty_done) as qte_sortie
        ,lot.id as lot_id,lot.name as lot_name,lot.use_date::date as dateuse
        FROM stock_move_line s, stock_location l,product_product p, product_template t, product_category c, express_sdg_rayon r, express_sdg_famille f
        ,public.stock_production_lot lot,stock_move sm
        WHERE s.location_id = l.id
        and sm.id=s.move_id
        and lot.id=s.lot_id
        AND p.product_tmpl_id = t.id
        and p.id=s.product_id
        and t.categ_id=c.id
        and r.id=t.idrayon
        and f.id=t.idfamille """+condition+"""
        AND l.usage = 'internal'
        AND s.date::date BETWEEN %s AND %s
        AND s.state = 'done'
        GROUP BY s.product_id,lot.id,lot.name
        ),
        entreesortie as(
        SELECT coalesce(se.product_id, ss.product_id) as product_id, 
        coalesce(se.qte_entree,0) as qte_entree, coalesce(ss.qte_sortie,0) as qte_sortie
        ,coalesce(se.lot_id,ss.lot_id) as lot_id,coalesce(se.lot_name,ss.lot_name) as lot_name,se.price_unit,coalesce(se.dateuse,ss.dateuse) as dateuse
        FROM entree se
        FULL JOIN sortie ss
        ON se.product_id = ss.product_id and se.lot_id=ss.lot_id
        ),
        stockfinal as (
        SELECT coalesce(si.product_id, es.product_id) as product_id, 
        coalesce(si.lot_id, es.lot_id) as lot_id,
        coalesce(si.lot_name, es.lot_name) as lot_name,
        coalesce(si.stockinit,0) as stockinit, 
        coalesce(es.qte_entree,0) as qte_entree, coalesce(es.qte_sortie,0) as qte_sortie, 
        coalesce(si.stockinit,0)+coalesce(es.qte_entree,0)-coalesce(es.qte_sortie,0) as stockfinal
        ,coalesce(si.price_unit,es.price_unit) as price_unit,coalesce(si.dateuse,es.dateuse) as dateuse
        FROM stinit si
        FULL JOIN entreesortie es
        ON si.product_id = es.product_id and si.lot_id=es.lot_id
        )
        SELECT stf.lot_id,stf.lot_name,stf.product_id,t.default_code,t.name as produit,r.name as rayon,f.name as famille,c.name as categorie, 
        stf.stockinit,stf.qte_entree,
        stf.qte_sortie,stf.stockfinal,
        coalesce(stf.price_unit,0) as price_unit,stf.dateuse,
        coalesce(c.stock_minimal,0) as stockmin, coalesce(stf.price_unit,0)*coalesce(stf.stockfinal,0) as vsca
        from stockfinal stf,product_template t,
        express_sdg_rayon r, express_sdg_famille f,
        product_category c,product_product p where p.product_tmpl_id=t.id
        and c.id=t.categ_id and stf.product_id=p.id
        and r.id=t.idrayon and f.id=t.idfamille
        order by produit"""    
        self.env.cr.execute(req, argu)
        rec=self.env.cr.dictfetchall()
        return {
            "docs": rec,
            "data": data,
        }
# fin stocks

# debut stocksxlsx
class ExpressdgStocksxlsxabstract(models.AbstractModel):
    _name = "report.express_sdg.report_stocks_templatexlsx"
    _inherit="report.report_xlsx.abstract"
    _description = "table avec données pour le template report_stocks_templatexlsx"
    
    def generate_xlsx_report(self, workbook, data, lines):
        argu=(data.get("debut"),data.get("debut"),data.get("debut"),data.get("fin"),
              data.get("debut"),data.get("fin"),)
        condition=""
        condition2=""
        if data.get("entrepot"):
            condition+=" and s.location_id="+str(data.get("entrepot"))
            condition2+=" and s.location_dest_id="+str(data.get("entrepot"))
        if data.get("rayon"):
            condition+=" and r.id="+str(data.get("rayon")) 
            condition2+=" and r.id="+str(data.get("rayon"))
        if data.get("famille"):
            condition+=" and f.id="+str(data.get("famille"))
            condition2+=" and f.id="+str(data.get("famille")) 
        if data.get("categorie"):
            condition+=" and c.id="+str(data.get("categorie"))
            condition2+=" and c.id="+str(data.get("categorie"))
        if data.get("produit"):
            condition+=" and p.id="+str(data.get("produit"))
            condition2+=" and p.id="+str(data.get("produit")) 
        req="""with stinitentree as (
        SELECT s.product_id, sum(s.qty_done) as qty_done,
        lot.id as lot_id,lot.name as lot_name,sm.price_unit as price_unit,lot.use_date::date as dateuse
        FROM stock_move_line s, stock_move sm, stock_location l, 
        product_product p,product_template t, 
        product_category c, express_sdg_rayon r, 
        express_sdg_famille f,public.stock_production_lot lot
        WHERE s.location_dest_id = l.id 
        and sm.id=s.move_id
        and lot.id=s.lot_id
        AND l.usage = 'internal'
        AND p.product_tmpl_id = t.id
        and p.id=s.product_id
        and t.categ_id=c.id
        and r.id=t.idrayon
        and f.id=t.idfamille """+condition2+"""
        AND s.date::date<%s 
        GROUP BY s.product_id,lot.id,lot.name,sm.price_unit
        ),
        stinitsortie as  (
        SELECT s.product_id, sum(s.qty_done) as qty_done,
        lot.id as lot_id,lot.name as lot_name,lot.use_date::date as dateuse
        FROM stock_move_line s,stock_move sm, stock_location l,product_product p, product_template t, 
        product_category c, express_sdg_rayon r, express_sdg_famille f,public.stock_production_lot lot
        WHERE s.location_id = l.id
        and sm.id=s.move_id
        and lot.id=s.lot_id
        AND l.usage = 'internal'
        AND p.product_tmpl_id = t.id
        and p.id=s.product_id
        and t.categ_id=c.id
        and r.id=t.idrayon
        and f.id=t.idfamille """+condition+"""
        AND s.date::date<%s
        AND s.state = 'done'
        GROUP BY s.product_id,lot.id,lot.name
        ),
        stinit as (
        SELECT coalesce(se.product_id,ss.product_id) as product_id, coalesce(se.qty_done,0)-coalesce(ss.qty_done,0) as stockinit
        ,coalesce(se.lot_id,ss.lot_id) as lot_id,coalesce(se.lot_name,ss.lot_name) as lot_name,se.price_unit,coalesce(se.dateuse,ss.dateuse) as dateuse
        FROM stinitentree se
        FULL JOIN stinitsortie ss
        ON se.product_id = ss.product_id and se.lot_id=ss.lot_id
        ),
        entree as (
        SELECT s.product_id, sum(qty_done) as qte_entree
        ,lot.id as lot_id,lot.name as lot_name,sm.price_unit as price_unit,lot.use_date::date as dateuse
        FROM stock_move_line s, stock_location l,product_product p, product_template t, product_category c, express_sdg_rayon r, express_sdg_famille f
        ,public.stock_production_lot lot,stock_move sm
        WHERE s.location_dest_id = l.id
        and sm.id=s.move_id
        and lot.id=s.lot_id
        AND p.product_tmpl_id = t.id
        and p.id=s.product_id
        and t.categ_id=c.id
        and r.id=t.idrayon
        and f.id=t.idfamille """+condition2+"""
        AND l.usage = 'internal'
        AND s.date::date BETWEEN %s AND %s
        AND s.state = 'done'
        GROUP BY s.product_id,lot.id,lot.name,sm.price_unit
        ),
        sortie as (
        SELECT s.product_id, sum(qty_done) as qte_sortie
        ,lot.id as lot_id,lot.name as lot_name,lot.use_date::date as dateuse
        FROM stock_move_line s, stock_location l,product_product p, product_template t, product_category c, express_sdg_rayon r, express_sdg_famille f
        ,public.stock_production_lot lot,stock_move sm
        WHERE s.location_id = l.id
        and sm.id=s.move_id
        and lot.id=s.lot_id
        AND p.product_tmpl_id = t.id
        and p.id=s.product_id
        and t.categ_id=c.id
        and r.id=t.idrayon
        and f.id=t.idfamille """+condition+"""
        AND l.usage = 'internal'
        AND s.date::date BETWEEN %s AND %s
        AND s.state = 'done'
        GROUP BY s.product_id,lot.id,lot.name
        ),
        entreesortie as(
        SELECT coalesce(se.product_id, ss.product_id) as product_id, 
        coalesce(se.qte_entree,0) as qte_entree, coalesce(ss.qte_sortie,0) as qte_sortie
        ,coalesce(se.lot_id,ss.lot_id) as lot_id,coalesce(se.lot_name,ss.lot_name) as lot_name,se.price_unit,coalesce(se.dateuse,ss.dateuse) as dateuse
        FROM entree se
        FULL JOIN sortie ss
        ON se.product_id = ss.product_id and se.lot_id=ss.lot_id
        ),
        stockfinal as (
        SELECT coalesce(si.product_id, es.product_id) as product_id, 
        coalesce(si.lot_id, es.lot_id) as lot_id,
        coalesce(si.lot_name, es.lot_name) as lot_name,
        coalesce(si.stockinit,0) as stockinit, 
        coalesce(es.qte_entree,0) as qte_entree, coalesce(es.qte_sortie,0) as qte_sortie, 
        coalesce(si.stockinit,0)+coalesce(es.qte_entree,0)-coalesce(es.qte_sortie,0) as stockfinal
        ,coalesce(si.price_unit,es.price_unit) as price_unit,coalesce(si.dateuse,es.dateuse) as dateuse
        FROM stinit si
        FULL JOIN entreesortie es
        ON si.product_id = es.product_id and si.lot_id=es.lot_id
        )
        SELECT stf.lot_id,stf.lot_name,stf.product_id,t.default_code,t.name as produit,r.name as rayon,f.name as famille,c.name as categorie, 
        stf.stockinit,stf.qte_entree,
        stf.qte_sortie,stf.stockfinal,
        coalesce(stf.price_unit,0) as price_unit,stf.dateuse,
        coalesce(c.stock_minimal,0) as stockmin, coalesce(stf.price_unit,0)*coalesce(stf.stockfinal,0) as vsca
        from stockfinal stf,product_template t,
        express_sdg_rayon r, express_sdg_famille f,
        product_category c,product_product p where p.product_tmpl_id=t.id
        and c.id=t.categ_id and stf.product_id=p.id
        and r.id=t.idrayon and f.id=t.idfamille
        order by produit"""    
        self.env.cr.execute(req, argu)
        rec=self.env.cr.dictfetchall()
        #document excel
        ident = workbook.add_format({'bold': 1,'border': 1,'align': 'center','valign': 'vcenter','fg_color': 'yellow'})
        bold = workbook.add_format({'bold': True, 'align': 'center','fg_color': '#2F75B5','border': 1})
        boldata = workbook.add_format({'align': 'center','fg_color': '#2A83G9','border': 1})
        bolth = workbook.add_format({'bold': 1,'align': 'center','fg_color': 'green','border': 1})
        boltd = workbook.add_format({'border': 1})
        boltdsep = workbook.add_format({'border': 1,'num_format':'# ##0'})
        my_format=workbook.add_format({'border': 1,'num_format':'dd/mm/yyyy'})
        worksheet = workbook.add_worksheet('Données')
        worksheet.set_column(0, 0, 20)
        worksheet.set_column(1, 1, 10)
        worksheet.set_column(2, 2, 50)
        worksheet.set_column(3, 4, 15)
        worksheet.set_column(5, 5, 30)
        worksheet.set_column(6, 10, 10)
        worksheet.set_column(11, 11, 25)
        col=0
        row=1
        worksheet.merge_range(0, col + 7,0, col + 8, 'Mouvements', ident)
        worksheet.write(row, col, 'Référence interne',bolth)
        worksheet.write(row, col+1, 'Lot',bolth)
        worksheet.write(row, col + 2, 'Produit',bolth)
        worksheet.write(row, col + 3, 'Rayon',bolth)
        worksheet.write(row, col + 4, 'Famille',bolth)
        worksheet.write(row, col + 5, 'Catégorie',bolth)
        worksheet.write(row, col + 6, 'Stock initial',bolth)
        worksheet.write(row, col + 7, 'entrée',bolth)
        worksheet.write(row, col + 8, 'sortie',bolth)
        worksheet.write(row, col + 9, 'Stock final',bolth)
        worksheet.write(row, col + 10, 'Stock alerte',bolth)
        worksheet.write(row, col + 11, 'Date utilisation optimale',bolth)
        if data.get("ouivoir"):
            worksheet.set_column(12, 12, 10)
            worksheet.set_column(13, 13, 20)
            worksheet.write(row, col + 12, 'Pcal',bolth)
            worksheet.write(row, col + 13, 'Valorisation',bolth)
        
        for line in rec:
            row+=1
            worksheet.write(row, col, line['default_code'],boltd)
            worksheet.write(row, col+1, line['lot_name'],boltd)
            worksheet.write(row, col+2, line.get("produit"),boltd)
            worksheet.write(row, col+3, line['rayon'],boltd)
            worksheet.write(row, col+4, line.get("famille"),boltd)
            worksheet.write(row, col+5, line['categorie'],boltd)
            worksheet.write(row, col+6, line.get("stockinit"),boltdsep)
            worksheet.write(row, col+7, line['qte_entree'],boltdsep)
            worksheet.write(row, col+8, line.get("qte_sortie"),boltdsep)
            worksheet.write(row, col+9, line['stockfinal'],boltdsep)
            worksheet.write(row, col+10, line.get("stockmin"),boltdsep)
            worksheet.write(row, col+11, line.get("dateuse"),my_format)
            if data.get("ouivoir"):
                worksheet.write(row, col+12, line['price_unit'],boltdsep)
                worksheet.write(row, col+13, line.get("vsca"),boltdsep)
        worksheet2 = workbook.add_worksheet('Paramètres') 
        worksheet2.set_column(0, 1, 15)    
        worksheet2.write('A1', 'Date de début', bold)
        worksheet2.write('A2', 'Date de fin', bold)
        worksheet2.write('A3', 'Entrepôt', bold)
        worksheet2.write('A4', 'Famille', bold)
        worksheet2.write('A5', 'Rayon', bold)
        worksheet2.write('A6', 'Catégorie', bold)
        worksheet2.write('A7', 'Produit', bold)
        worksheet2.write('A8', 'PCAM,VSCA', bold)
        worksheet2.write('B1', data.get("debut"),boldata)
        worksheet2.write('B2', data.get("fin"),boldata)
        worksheet2.write('B3', data.get("warehouse"),boldata)
        worksheet2.write('B4', data.get("famille_name"),boldata)
        worksheet2.write('B5', data['rayon_name'],boldata)
        worksheet2.write('B6', data['categorie_name'],boldata)
        worksheet2.write('B7', data['produit_name'],boldata)
        worksheet2.write('B8', data['ouivoir'],boldata)    
# fin stocksxlsx