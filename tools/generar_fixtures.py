# -*- coding: utf-8 -*-

# open all lines of file
import datetime
import json
import os
import csv
from django.template.defaultfilters import slugify

def generate_category(category, index):
    category_data = {
        'model': 'catalogue.category',
        'pk': index,
        'fields': {
            'name': category,
            'description': category,
            'slug': slugify(category),
            'full_name': category,
            'depth': 1,
            'path':'%04d' % index
        }
    }
    return category_data

def generate_product(product, description, index):
    product_data = {
        'model': 'catalogue.product',
        'pk': index,
        'fields': {
            'upc': index,
            'title': product,
            'description': description,
            'slug': slugify(product),
            'product_class': 1,
            'date_created': str(datetime.datetime.now()),
            'date_updated': str(datetime.datetime.now()),
            'status':'created',
            'is_discountable': False
        }
    }
    return product_data

def generate_productclass():
    class_data = {
        'model': 'catalogue.productclass',
        'pk': 1,
        'fields': {
            'name': 'Piezas',
            'slug': 'piezas',
            'requires_shipping': True,
            'track_stock': False
        }
    }
    return class_data

def generate_prodcateg(index, product_index, category_index):
    prodcateg_data = {
        'model': 'catalogue.productcategory',
        'pk': index,
        'fields': {
            'product': product_index,
            'category': category_index,
            'is_canonical': False
        }
    }
    return prodcateg_data

def generate_prodquestion(index, product_index, question, type):
    prodquestion_data = {
        'model': 'catalogue.productquestion',
        'pk': index,
        'fields': {
            'product': product_index,
            'text': question,
            'type': type
        }
    }
    return prodquestion_data

with open("productclass.json", "w") as outfile:
    json.dump([generate_productclass(),], outfile)

with open("podrecambios.csv") as f:
    contentreader = csv.reader(f, delimiter=',', quotechar='"')
    categories = []
    products = []
    question_types = {'SI/NO':'boolean', 'TEXTO':'text', 'FOTOS':'photo'}    

    created_categories = {}
    created_products = {}

    index = 1
    product_index = 1
    prodcateg_index = 1
    prodquestion_index = 1

    for row in contentreader:
        current_category = row[1]
        if current_category not in created_categories.keys():
            category = generate_category(current_category, index)
            created_categories[current_category] = index
            categories.append(category)
            index += 1

        # create the products for the category
        current_product = row[2]
        prodkey = current_category+"_"+current_product
        if prodkey not in created_products.keys():
            # product
            description = row[5]
            product = generate_product(current_product, description, product_index)
            products.append(product)
            created_products[prodkey] = product_index

            # product category
            current_categ_index = created_categories[current_category]
            prodcateg = generate_prodcateg(prodcateg_index, product_index, current_categ_index)
            products.append(prodcateg)

            prodcateg_index += 1
            product_index += 1

        # product question
        question = row[3]
        question_type = row[4]
        if question_type in question_types:
            final_question_type = question_types[question_type]
        else:
            final_question_type = ''

        if question:
            current_product_index = created_products[prodkey]
            prodquestion = generate_prodquestion(prodquestion_index, current_product_index, question, final_question_type)
            prodquestion_index += 1
            products.append(prodquestion)
       

    # write files
    with open("categories.json", "w") as outfile:
        json.dump(categories, outfile)
    with open("products.json", "w") as outfile:
        json.dump(products, outfile)
