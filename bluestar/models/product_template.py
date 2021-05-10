# # -*- coding: utf-8 -*-
#
# from odoo import models, fields, api
# from odoo.exceptions import UserError
# from odoo.http import request
# import logging
import os.path
# import sys
# import xlrd
# import logging.config
import pandas as pd
#
#
# class Sequence(models.Model):
#     _name = 'product.sequence'
#     _description = 'Sequence'
#
#     name = fields.Char()
#     sequence = fields.Integer(default=1)
#
#
# class ProductExport(models.Model):
#     _inherit = 'product.template'
#
#     def import_products(self, start, end):
#         for next_call_number in range(start, end):
#             filename = os.path.dirname(os.path.realpath(__file__)) + "/excel/" + "Part" + str(
#                 next_call_number) + "-split-excel" + ".xlsx"
#             line_vals = []
#             line_vals = self._load(filename)
#
#             if line_vals:
#                 self.env['product.template'].create(line_vals)
#             else:
#                 raise UserError('No records found.')
#
#         return end
#
#     #     def import_products(self):
#     #         _logger = self.Logger(os.path.dirname(os.path.realpath(__file__)) + "/logs/app.log")
#     #         seq_date = True
#     #         next_call_number = self.env['ir.sequence'].next_by_code('next_call_number', sequence_date=seq_date) or False
#
#     #         if next_call_number == False:
#     #             _logger.debug('Sequence cannot be retrieved.')
#     #             raise UserError('Sequence cannot be retrieved.')
#
#     #         filename = os.path.dirname(os.path.realpath(__file__)) + "/excel/" + "Part" + str(next_call_number) + "-split-excel" + ".xlsx"
#
#     #         _logger.debug('Filename:{0}'.format(filename))
#
#     #         line_vals = self._load(filename)
#
#     #         if line_vals:
#     #             self.env['product.template'].create(line_vals)
#     #             return next_call_number
#     #         else:
#     #             _logger.debug('No records found.')
#     #             raise UserError('No records found.')
#
#     def _load(self, filename):
#         try:
#             book = xlrd.open_workbook(filename=filename)
#         except FileNotFoundError:
#             #             _logger.debug('No such file or directory found. \n%s.' % filename)
#             raise UserError('No such file or directory found. \n%s.' % filename)
#         except xlrd.biffh.XLRDError:
#             #             _logger.debug('Only excel files are supported.')
#             raise UserError('Only excel files are supported.')
#
#         line_vals = []
#         for sheet in book.sheets():
#             try:
#                 if sheet.name == 'Sheet1':
#                     for row in range(sheet.nrows):
#                         if row >= 1:
#                             row_values = sheet.row_values(row)
#                             #                             vals = self._get_product_from_sheet(row_values)
#                             vals = self._get_product_from_sheet(
#                                 row_values[0],
#                                 row_values[1],
#                                 row_values[2],
#                                 row_values[3],
#                                 row_values[4],
#                                 row_values[5],
#                                 row_values[6]
#                             )
#
#                             if vals == True:
#                                 continue
#
#                             line_vals.append(vals)
#
#             except IndexError:
#                 pass
#
#         return line_vals
#
#     def _get_product_from_sheet(self, default_code, name, gross_price, market_code, factor, weight, volume):
#         ProductTemplate = self.env['product.template'].search([('default_code', '=', default_code)])
#         market_code = self.env['product.template.market.code'].search([('name', '=', market_code)])
#         if ProductTemplate:
#             return True
#
#         #         if not market_code:
#         #             factor_id = self.env['product.template.sales.factor'].search([('name', '=', factor)]).id
#         #             market_code = self.env['product.template.market.code'].create({'factor_id': factor_id, 'name': market_code})
#
#         product = {
#             "default_code": default_code,
#             "name": name,
#             "gross_price": gross_price,
#             "market_code": market_code.id,
#             "weight": weight,
#             "volume": volume
#         }
#         return product
#
#     def convert_csv_to_excel(self, start, end):
#         for i in range(start, end):
#             filename = os.path.dirname(os.path.realpath(__file__)) + "/excel/" + "Part" + str(i) + "-split-excel"
#
#             if not os.path.isfile(filename + ".xlsx"):
#                 self._convert(filename)
#
#     def _convert(self, filename):
#         read_file = pd.read_csv(filename + ".csv")
#         read_file.to_excel(filename + ".xlsx", index=None, header=True)
#
#     # ================== Logger ================================
#     def Logger(self, file_name):
#         formatter = logging.Formatter(fmt='%(asctime)s %(module)s,line: %(lineno)d %(levelname)8s | %(message)s',
#                                       datefmt='%Y/%m/%d %H:%M:%S')  # %I:%M:%S %p AM|PM format
#         logging.basicConfig(filename='%s.log' % (file_name),
#                             format='%(asctime)s %(module)s,line: %(lineno)d %(levelname)8s | %(message)s',
#                             datefmt='%Y/%m/%d %H:%M:%S', filemode='w', level=logging.INFO)
#         log_obj = logging.getLogger()
#         log_obj.setLevel(logging.DEBUG)
#         # log_obj = logging.getLogger().addHandler(logging.StreamHandler())
#
#         # console printer
#         screen_handler = logging.StreamHandler(stream=sys.stdout)  # stream=sys.stdout is similar to normal print
#         screen_handler.setFormatter(formatter)
#         logging.getLogger().addHandler(screen_handler)
#
#         log_obj.info("Logger object created successfully..")
#         return log_obj

class ProductExport():
    def convert_csv_to_excel(self, start, end):

        for i in range(start, end):
                filename = os.path.dirname(os.path.realpath(__file__)) + "/excel/" + "Part" + str(i) + "-split-excel" + ".csv"

                if os.path.isfile(filename):
                    os.remove(filename)
                    # read_file = pd.read_csv(filename + ".csv")
                    # read_file.to_excel(filename + ".xlsx", index=None, header=True)

        def _convert(self, filename):
            read_file = pd.read_csv(filename + ".csv")
            read_file.to_excel(filename + ".xlsx", index=None, header=True)

if __name__ == '__main__':
    md = ProductExport()
    md.convert_csv_to_excel(1, 410)
