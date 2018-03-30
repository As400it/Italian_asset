# -*- coding: utf-8 -*-
# Copyright 2017 Marco Calcagni - Dinamiche Aziendali srl
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models
from odoo.exceptions import Warning as UserError
from odoo.tools.translate import _


class ItAssetType(models.Model):
    _name = "it.asset.type"
    name = fields.Char(string='Asset', track_visibility='always', required=True)

class ItFiscalGroup(models.Model):
    _name = "it.fiscal.group"
    name = fields.Char(string='Asset', track_visibility='always', required=True)

class ItFiscalType(models.Model):
    _name = "it.fiscal.type"
    name = fields.Char(string='Asset', track_visibility='always', required=True)

class ItFiscalCategory(models.Model):
    _name = "it.fiscal.category"
    name = fields.Char(string='Asset', track_visibility='always', required=True)

class ItCategory(models.Model):
    _name = "it.category"
    name = fields.Char(string='Category', track_visibility='always', required=True, help="Tipo ammortamento Civilistico, fiscale, Gestionale")

class AssetClassTag(models.Model):
    _name = 'asset.class.tag'
    _description = 'Asset Class Tags'
    name = fields.Char(string='Asset Class Tag', index=True, required=True)
    color = fields.Integer('Color Index')

class ItAsset(models.Model):
    _name = "it.asset"

    name = fields.Char(string='Asset', track_visibility='always',
                       required=True)
    # natura del cespite materiale , imm, ecc ,
    type = fields.Many2one(comodel_name='it.asset.type', string='name',)
    # codice e sottocodice per raggruppamenti logici
    asset_code = fields.Char('Code')
    asset_subcode = fields.Char('Sub code')
    # classificazione
    asset_class_ids = fields.Many2many('asset.class.tag',
                                        string='Asset Class Tags')
    #cespite in funzione
    asset_in_use = fields.Boolean("in use")
    # dati fiscali
    fiscal_group = fields.Many2one(comodel_name='it.fiscal.group', string='name',)
    fiscal_type = fields.Many2one(comodel_name='it.fiscal.type', string='name',)
    fiscal_category = fields.Many2one(comodel_name='it.fiscal.category', string='name',)
    # localizzazione del cespite dove si trova
    asset_sn = fields.Char("Serial number")
    asset_qty = fields.Integer(string="Quantity",  default=0, help="")
    # company
    company_id = fields.Many2one('res.company', string='Company', required=True,
                                 default=lambda self: self.env.user.company_id)
    # active odoo
    active = fields.Boolean(default=True)

class ItAssetMove(models.Model):
    _name = "it.asset.move"
    # qui ci vanno i dati che hanno creato il cespite es. acquisto
    # vendita, rivalutazione ecc.

    name = fields.Char(string='Name', track_visibility='always', required=True)
    invoice_nr = fields.Char(string='Invoice number', track_visibility='always')
    date_invoice = fields.Date(string='Invoice Date', track_visibility='onchange')
    partner = fields.Many2one('res.partner', string='Partner', help='Vendor or Customer')
    value_asset = fields.Float(string='Value on Invoice', help='Invoice value or asset value')
    move_type = fields.Selection(
        [('1', 'Incremento'),
         ('2', 'Alienazione'),
         ('3', "Incremento successivo all'esercizio di acquisizione"),
         ('4', "Alienazione parziale"),
         ('5', "Spese di manutenzione")],)
    # partecipa al valore del cespite
    asset_variation = fields.Boolean(default=True, help="partecipa al valore del cespite")


class ItAssetRule(models.Model):
    _name = "it.asset.rule"
    # qui ci vanno le regolepercalcolare l'ammortamento

    # immateriali vanno per %
    # quote costanti
    # quote crescenti
    # quote decrescenti
    # piano di ammortamento
    # calcolo sul valore cespite
    # calcolo sul residuo
    # sul valore per percentuale
    # rule_line ??


class ItDepreciation(models.Model):
    _name = "it.depreciation"
    # qui ci va il tipo di ammortamento civilistico, fiscale, gestionale ecc
    name = fields.Char(string='Name', track_visibility='always', required=True,)
    category_id = fields.Many2one(comodel_name='it.category', string='name', )
    gratuitamete_devolvibile = fields.Boolean("Gratuitamete Devolvibile")
    cespite_promisquo = fields.Boolean("cespite promisquo")
    #escluso dal calcolo delle spese di manutenzione deducibili
    escluso_spe_man = fields.Boolean("escluso dal calcolo delle spese di manutenzione deducibili")
    # valore minimo ammortizzabile
    value_min_depreciation = fields.Float(string='Valore minimo ammortamento', help="Valore minimo per l'ammortamento")
    # deducibile in un esercizio
    one_year_cost = fields.Boolean("deducibile in un esercizio")
    asset_in_leasing = fields.Boolean("cespite in leasing")
    # valore cespite calcolato da asset move
    value_asset = fields.Float(string='Value on Invoice', help='Invoice value or asset value')
    # maggiorazione diminuzione rispetto al calcolo
    value_adjustement = fields.Float(string='Variazioni di Valore',
                                     help='Variazione al valore per ammortamenti maggiorati es. superammortamento')
    adjustement_note = fields.Char('Sub code')
    # valore residuo da ammortizzare
    value_residual = fields.Float(string='Valore residuo')
    date_next_depreciation = fields.Date(string='Data prossimo ammortamento', track_visibility='onchange')
    # data inizio ammortamnto
    date_start = fields.Date(string='Inizio Ammortamento', track_visibility='onchange')
    date_end = fields.Date(string='Fine Ammortamento', track_visibility='onchange')
    # cost calculation rule
    cost_rule = fields.Many2one(comodel_name='it.asset.rule', string='name',)
    # primo anno di ammortamento
    first_year = fields.Integer(string="First year", default=0, help="")
    # contro contabile
    account_depreciation = fields.Many2one('account.account', string='Depreciation Account')



class ItDepreciationLine(models.Model):
    _name = "it.depreciation.line"
    # qui ci vanno le quote di ammortamento calcolate x periodo
    name = fields.Char(string='Name', track_visibility='always', required=True,)
    # period ??
    date_start = fields.Date(string='Inizio Ammortamento', track_visibility='onchange')
    date_end = fields.Date(string='Fine Ammortamento', track_visibility='onchange')
    value = fields.Float(string='Valore Ammortamento')
    total_value_asset all epoca del calcolo
    move_id = fields.Many2one('account.move', string='Journal Entry',
        readonly=True, index=True, ondelete='restrict', copy=False,
        help="Link to the automatically generated Journal Items.")



# report
#
# -> cespite
# descrizione del cespite , classificazione fiscale, data acquisizione, data inizio amm.
#
# -> righe del cespite più
# data , descrizione, importo variazione, importo totale aggiornato (somma dei + o -)
# -> righe di ammortamento
# data, descrizione , fondo ammortamento ->[ %, quota di ammortamento, variazione , totale accantonamento] ,
#                     quota persa ->[%, importo variazione],  rimanente da ammortizzare.
#
# totale
# totale per categoria , totale generale
#  -> importo variazione, importo totale aggiornato , quota di ammortamento, variazione , totale accantonamento, importo variazione, rimanente da ammortizzare




# gruppoe specie in testata pagina
# righe
    # codice e descrizione cespite, tipo ammortamento, anno acquisto, importo acquisto, oneri diversi, rivalutazioni, importo non ammortizzabile
    # plusvalenze reinv.,  totale da ammortizzare
    # % amm. ammorttamento precedente, ammortamento indeducibile precedente , ammortamento ordinario, amm. anticipato, non ammortizzabile, ammortamento indeducibile
    # gg utilizzo, importo eliminazione, importo vendita, minusvalenza, plusvalenza, Plusvalenza da riportare, resuduo da ammortizzare.
# vedi documento    manuale flusso cespiti
