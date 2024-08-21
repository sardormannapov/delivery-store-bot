from datetime import datetime

import config.config as c
import xlsxwriter
import pandas
import repository.repository as repo
import numpy as np



excel_error_data_list = []

catalog_sheet_name = "Kataloglar"
catalog_id_field_name = 'ID'
catalog_name_uz_field_name = 'Katalog nomi uzbek tilida'
catalog_name_ru_field_name = 'Katalog nomi rus tilida'
catalog_name_en_field_name = 'Katalog nomi ingliz tilida'
catalog_photo_field_name = 'Katalog rasmi'

subcatalog_sheet_name = "SubKataloglar"
subcatalog_id_field_name = 'ID'
subcatalog_name_uz_field_name = 'SubKatalog nomi uzbek tilida'
subcatalog_name_ru_field_name = 'SubKatalog nomi rus tilida'
subcatalog_name_en_field_name = 'SubKatalog nomi ingliz tilida'
subcatalog_photo_field_name = 'SubKatalog rasmi'
subcatalog_catalog_id_field_name = 'Katalog ID'

product_sheet_name = "Taomlar"
product_id_field_name = 'ID'
product_name_uz_field_name = 'Taom nomi uzbek tilida'
product_name_ru_field_name = 'Taom nomi rus tilida'
product_name_en_field_name = 'Taom nomi ingliz tilida'
product_photo_field_name = 'Taom rasmi'
product_price_field_name = 'Taom narxi'
product_special_sign_uz_field_name = 'Taom maxsus belgisi uz tilida'
product_special_sign_ru_field_name = 'Taom maxsus belgisi ru tilida'
product_special_sign_en_field_name = 'Taom maxsus belgisi ingliz tilida'
product_ingredients_uz_field_name = 'Taom mahsulotlari uzbek tilida'
product_ingredients_ru_field_name = 'Taom mahsulotlari rus tilida'
product_ingredients_en_field_name = 'Taom mahsulotlari ingliz tilida'
product_category_id_field_name = 'SubKatalog ID'


def create_excel_template_file(repo):
    # current_time=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    workbook = xlsxwriter.Workbook('get_db.xlsx')
    worksheet_catalog = workbook.add_worksheet(catalog_sheet_name)
    bold = workbook.add_format({'bold': True})
    worksheet_catalog.write('A1', catalog_id_field_name, bold)
    worksheet_catalog.write('B1', catalog_name_uz_field_name, bold)
    worksheet_catalog.write('C1', catalog_name_ru_field_name, bold)
    worksheet_catalog.write('D1', catalog_name_en_field_name, bold)
    worksheet_catalog.write('E1', catalog_photo_field_name, bold)
    data = repo.category.get_list_without_lang(0, 1000000000000)
    if len(data["body"]) != 0:
        for i in range(len(data["body"])):
            worksheet_catalog.write(i + 1, 0, data["body"][i]["id"])
            worksheet_catalog.write(i + 1, 1, data["body"][i]["category_name"]["uz"])
            worksheet_catalog.write(i + 1, 2, data["body"][i]["category_name"]["ru"])
            worksheet_catalog.write(i + 1, 3, data["body"][i]["category_name"]["en"])
            worksheet_catalog.write(i + 1, 4, data["body"][i]["photo"])
    worksheet_subcatalog = workbook.add_worksheet(subcatalog_sheet_name)
    bold = workbook.add_format({'bold': True})
    worksheet_subcatalog.write('A1', subcatalog_id_field_name, bold)
    worksheet_subcatalog.write('B1', subcatalog_name_uz_field_name, bold)
    worksheet_subcatalog.write('C1', subcatalog_name_ru_field_name, bold)
    worksheet_subcatalog.write('D1', subcatalog_name_en_field_name, bold)
    worksheet_subcatalog.write('E1', subcatalog_photo_field_name, bold)
    worksheet_subcatalog.write('F1', subcatalog_catalog_id_field_name, bold)
    data = repo.subcategory.get_list(0, 1000000000000)
    if len(data["body"]) != 0:
        for i in range(len(data["body"])):
            worksheet_subcatalog.write(i + 1, 0, data["body"][i]["id"])
            worksheet_subcatalog.write(i + 1, 1, data["body"][i]["subcategory_name"]["uz"])
            worksheet_subcatalog.write(i + 1, 2, data["body"][i]["subcategory_name"]["ru"])
            worksheet_subcatalog.write(i + 1, 3, data["body"][i]["subcategory_name"]["en"])
            worksheet_subcatalog.write(i + 1, 4, data["body"][i]["photo"])
            worksheet_subcatalog.write(i + 1, 5, data["body"][i]["category_id"])

    worksheet_product = workbook.add_worksheet(product_sheet_name)
    bold = workbook.add_format({'bold': True})
    worksheet_product.write('A1', product_id_field_name, bold)
    worksheet_product.write('B1', product_name_uz_field_name, bold)
    worksheet_product.write('C1', product_name_ru_field_name, bold)
    worksheet_product.write('D1', product_name_en_field_name, bold)
    worksheet_product.write('E1', product_special_sign_uz_field_name, bold)
    worksheet_product.write('F1', product_special_sign_ru_field_name, bold)
    worksheet_product.write('G1', product_special_sign_en_field_name, bold)
    worksheet_product.write('H1', product_price_field_name, bold)
    worksheet_product.write('I1', product_ingredients_uz_field_name, bold)
    worksheet_product.write('J1', product_ingredients_ru_field_name, bold)
    worksheet_product.write('K1', product_ingredients_en_field_name, bold)
    worksheet_product.write('L1', product_photo_field_name, bold)
    worksheet_product.write('M1', product_category_id_field_name, bold)
    data = repo.product.get_list(0, 1000000000000)
    if len(data["body"]) != 0:
        for i in range(len(data["body"])):
            worksheet_product.write(i + 1, 0, data["body"][i]["id"])
            worksheet_product.write(i + 1, 1, data["body"][i]["product_name"]["uz"])
            worksheet_product.write(i + 1, 2, data["body"][i]["product_name"]["ru"])
            worksheet_product.write(i + 1, 3, data["body"][i]["product_name"]["en"])
            worksheet_product.write(i + 1, 4, data["body"][i]["special_sign"]["uz"])
            worksheet_product.write(i + 1, 5, data["body"][i]["special_sign"]["ru"])
            worksheet_product.write(i + 1, 6, data["body"][i]["special_sign"]["en"])
            worksheet_product.write(i + 1, 7, data["body"][i]["price"])
            worksheet_product.write(i + 1, 8, data["body"][i]["ingredients"]["uz"])
            worksheet_product.write(i + 1, 9, data["body"][i]["ingredients"]["ru"])
            worksheet_product.write(i + 1, 10, data["body"][i]["ingredients"]["en"])
            worksheet_product.write(i + 1, 11, data["body"][i]["photo"])
            worksheet_product.write(i + 1, 12, data["body"][i]["subcategory_id"])
    workbook.close()

def read_excel_file(repo,log, path):
    catalog_error_data_list = read_excel_catalogs(repo,log, path)
    subcatalog_error_data_list = read_excel_subcatalogs(repo,log, path)
    product_error_data_list = read_excel_products(repo,log, path)
    if bool(catalog_error_data_list) or bool(subcatalog_error_data_list) or bool(product_error_data_list):
        return dict(catalog_error_data_list=catalog_error_data_list,
                    subcatalog_error_data_list=subcatalog_error_data_list,
                    product_error_data_list=product_error_data_list)


def read_excel_catalogs(repo,log, path):
    catalog_error_data = []
    try:
        catalog_excel_data = pandas.read_excel(path, sheet_name=catalog_sheet_name, usecols=[
            catalog_id_field_name, catalog_name_uz_field_name, catalog_name_ru_field_name, catalog_name_en_field_name,
            catalog_photo_field_name])
    except Exception as err:
        log.error(err)
        return dict(error=err)
    catalog_df = pandas.DataFrame(catalog_excel_data)
    catalog_df = catalog_df.dropna(how='all')
    catalog_df[catalog_id_field_name].fillna(0)
    catalog_df[catalog_id_field_name].replace(np.nan, 0, inplace=True)
    catalog_df[catalog_name_uz_field_name].replace(np.nan, "", inplace=True)
    catalog_df[catalog_name_ru_field_name].replace(np.nan, "", inplace=True)
    catalog_df[catalog_name_en_field_name].replace(np.nan, "", inplace=True)
    catalog_df[catalog_photo_field_name].replace(np.nan, "", inplace=True)
    catalog_df = pandas.DataFrame(catalog_df)
    catalog_df[catalog_photo_field_name] = catalog_df[catalog_photo_field_name].astype("string")
    excel_catalog_id_list = []
    # if len( catalog_df.index ) == 0:
    #     return
    for i in catalog_df.index:
        excel_catalog_id_list.append(int(catalog_df[catalog_id_field_name][i]))
    db_data = repo.category.get_list_without_lang(0, 1000000000000)
    db_catalog_id_list = []
    for i in db_data["body"]:
        db_catalog_id_list.append(i["id"])
    for i in db_catalog_id_list:
        if i not in excel_catalog_id_list:
            repo.category.delete(i)
    for i in catalog_df.index:
        catalog = dict(id=int(catalog_df[catalog_id_field_name][i]),
                       uz="{0}".format(catalog_df[catalog_name_uz_field_name][i]).strip(),
                       ru="{0}".format(catalog_df[catalog_name_ru_field_name][i]).strip(),
                       en="{0}".format(catalog_df[catalog_name_en_field_name][i]).strip(),
                       photo="{0}".format(catalog_df[catalog_photo_field_name][i]).strip())
        data = repo.category.alter(catalog)
        if not data["success"]:
            if i != 0:
                catalog_error_data.append(i)
    return catalog_error_data

def read_excel_subcatalogs(repo,log, path):
    subcatalog_error_data = []
    try:
        subcatalog_excel_data = pandas.read_excel(path, sheet_name=subcatalog_sheet_name, usecols=[
            subcatalog_id_field_name, subcatalog_name_uz_field_name, subcatalog_name_ru_field_name,
            subcatalog_name_en_field_name,
            subcatalog_photo_field_name, subcatalog_catalog_id_field_name])
    except Exception as err:
       log.error(err)
       return dict(error=err)
    subcatalog_df = pandas.DataFrame(subcatalog_excel_data)
    subcatalog_df = subcatalog_df.dropna(how='all')
    subcatalog_df[subcatalog_id_field_name].fillna(0)
    subcatalog_df[subcatalog_id_field_name].replace(np.nan, 0, inplace=True)
    subcatalog_df[subcatalog_catalog_id_field_name].replace(np.nan, 0, inplace=True)
    subcatalog_df[subcatalog_name_uz_field_name].replace(np.nan, "", inplace=True)
    subcatalog_df[subcatalog_name_ru_field_name].replace(np.nan, "", inplace=True)
    subcatalog_df[subcatalog_name_en_field_name].replace(np.nan, "", inplace=True)
    subcatalog_df[subcatalog_photo_field_name].replace(np.nan, "", inplace=True)
    subcatalog_df = pandas.DataFrame(subcatalog_df)
    subcatalog_df[subcatalog_photo_field_name] = subcatalog_df[subcatalog_photo_field_name].astype("string")
    excel_subcatalog_id_list = []
    for i in subcatalog_df.index:
        excel_subcatalog_id_list.append(int(subcatalog_df[subcatalog_id_field_name][i]))
    db_data = repo.subcategory.get_list(0, 1000000000000)
    db_subcatalog_id_list = []
    for i in db_data["body"]:
        db_subcatalog_id_list.append(i["id"])
    for i in db_subcatalog_id_list:
        if i not in excel_subcatalog_id_list:
            repo.subcategory.delete(i)
    for i in subcatalog_df.index:
        subcatalog = dict(id=int(subcatalog_df[subcatalog_id_field_name][i]),
                          uz="{0}".format(subcatalog_df[subcatalog_name_uz_field_name][i]).strip(),
                          ru="{0}".format(subcatalog_df[subcatalog_name_ru_field_name][i]).strip(),
                          en="{0}".format(subcatalog_df[subcatalog_name_en_field_name][i]).strip(),
                          photo="{0}".format(subcatalog_df[subcatalog_photo_field_name][i]).strip(),
                          catalog_id=int(subcatalog_df[subcatalog_catalog_id_field_name][i]))
        data = repo.subcategory.alter(subcatalog)
        if not data["success"]:
            if i != 0:
                subcatalog_error_data.append(i)
    return subcatalog_error_data


def read_excel_products(repo,log, path):
    product_error_data = []
    try:
        product_excel_data = pandas.read_excel(path, sheet_name=product_sheet_name,
                                              usecols=[product_id_field_name,
                                                         product_name_uz_field_name,
                                                         product_photo_field_name,
                                                         product_name_ru_field_name,
                                                         product_name_en_field_name,
                                                         product_special_sign_uz_field_name,
                                                         product_special_sign_ru_field_name,
                                                         product_special_sign_en_field_name,
                                                         product_price_field_name,
                                                         product_category_id_field_name,
                                                         product_ingredients_uz_field_name,
                                                         product_ingredients_ru_field_name,
                                                         product_ingredients_en_field_name,
                                                         ]
                                              )
    except Exception as err:
        log.error(err)
        return dict(error=err)
    product_df = pandas.DataFrame(product_excel_data)
    product_df = product_df.dropna(how='all')
    product_df[product_id_field_name].fillna(0)
    product_df[product_category_id_field_name].fillna(0)
    product_df[product_price_field_name].fillna(0)
    product_df[product_id_field_name].replace(np.nan, 0, inplace=True)
    product_df[product_name_uz_field_name].replace(np.nan, "", inplace=True)
    product_df[product_name_ru_field_name].replace(np.nan, "", inplace=True)
    product_df[product_name_en_field_name].replace(np.nan, "", inplace=True)
    product_df[product_special_sign_uz_field_name].replace(np.nan, "", inplace=True)
    product_df[product_special_sign_ru_field_name].replace(np.nan, "", inplace=True)
    product_df[product_special_sign_en_field_name].replace(np.nan, "", inplace=True)
    product_df[product_photo_field_name].replace(np.nan, "", inplace=True)
    product_df[product_price_field_name].replace(np.nan, 0, inplace=True)
    product_df[product_ingredients_uz_field_name].replace(np.nan, "", inplace=True)
    product_df[product_ingredients_ru_field_name].replace(np.nan, "", inplace=True)
    product_df[product_ingredients_en_field_name].replace(np.nan, "", inplace=True)
    product_df[product_category_id_field_name].replace(np.nan, 0, inplace=True)
    product_df = pandas.DataFrame(product_df)
    product_df[product_photo_field_name] = product_df[product_photo_field_name].astype("string")
    excel_product_id_list = []
    for i in product_df.index:
        excel_product_id_list.append(int(product_df[product_id_field_name][i]))
    db_product_id_list = list()
    db_data = repo.product.get_list(0, 1000000000000)["body"]
    for i in db_data:
        db_product_id_list.append(i["id"])
    for i in db_product_id_list:
        if i not in excel_product_id_list:
            repo.product.delete(i)
    for i in product_df.index:
        product = dict(id=int(product_df[product_id_field_name][i]),
                       title_uz="{0}".format(product_df[product_name_uz_field_name][i]).strip(),
                       title_ru="{0}".format(product_df[product_name_ru_field_name][i]).strip(),
                       title_en="{0}".format(product_df[product_name_en_field_name][i]).strip(),
                       special_sign_uz="{0}".format(product_df[product_special_sign_uz_field_name][i]).strip(),
                       special_sign_ru="{0}".format(product_df[product_special_sign_ru_field_name][i]).strip(),
                       special_sign_en="{0}".format(product_df[product_special_sign_en_field_name][i]).strip(),
                       photo="{0}".format(product_df[product_photo_field_name][i]).strip(),
                       price=int(product_df[product_price_field_name][i]),
                       subcatalog_id=int(product_df[product_category_id_field_name][i]),
                       ingredient_uz="{0}".format(product_df[product_ingredients_uz_field_name][i]).strip(),
                       ingredient_ru="{0}".format(product_df[product_ingredients_ru_field_name][i]).strip(),
                       ingredient_en="{0}".format(product_df[product_ingredients_en_field_name][i]).strip()
                       )
        data = repo.product.alter(product)
        if not data["success"]:
            if i != 0:
                product_error_data.append(i)
    return product_error_data

# read_excel_file("get_db.xlsx")
# create_excel_template_file()
