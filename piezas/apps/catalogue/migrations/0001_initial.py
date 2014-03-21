# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ProductRecommendation'
        db.create_table(u'catalogue_productrecommendation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('primary', self.gf('django.db.models.fields.related.ForeignKey')(related_name='primary_recommendations', to=orm['catalogue.Product'])),
            ('recommendation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalogue.Product'])),
            ('ranking', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
        ))
        db.send_create_signal(u'catalogue', ['ProductRecommendation'])

        # Adding model 'ProductClass'
        db.create_table(u'catalogue_productclass', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=128)),
            ('requires_shipping', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('track_stock', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'catalogue', ['ProductClass'])

        # Adding M2M table for field options on 'ProductClass'
        m2m_table_name = db.shorten_name(u'catalogue_productclass_options')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('productclass', models.ForeignKey(orm[u'catalogue.productclass'], null=False)),
            ('option', models.ForeignKey(orm[u'catalogue.option'], null=False))
        ))
        db.create_unique(m2m_table_name, ['productclass_id', 'option_id'])

        # Adding model 'Category'
        db.create_table(u'catalogue_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('path', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('depth', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('numchild', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=255, null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255)),
            ('full_name', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
        ))
        db.send_create_signal(u'catalogue', ['Category'])

        # Adding model 'ProductCategory'
        db.create_table(u'catalogue_productcategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalogue.Product'])),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalogue.Category'])),
            ('is_canonical', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
        ))
        db.send_create_signal(u'catalogue', ['ProductCategory'])

        # Adding model 'Product'
        db.create_table(u'catalogue_product', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('upc', self.gf('django.db.models.fields.CharField')(max_length=64, unique=True, null=True, blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='variants', null=True, to=orm['catalogue.Product'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=128, null=True, blank=True)),
            ('product_class', self.gf('django.db.models.fields.related.ForeignKey')(related_name='products', null=True, to=orm['catalogue.ProductClass'])),
            ('score', self.gf('django.db.models.fields.FloatField')(default=0.0, db_index=True)),
            ('rating', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, db_index=True, blank=True)),
            ('is_discountable', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'catalogue', ['Product'])

        # Adding M2M table for field product_options on 'Product'
        m2m_table_name = db.shorten_name(u'catalogue_product_product_options')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('product', models.ForeignKey(orm[u'catalogue.product'], null=False)),
            ('option', models.ForeignKey(orm[u'catalogue.option'], null=False))
        ))
        db.create_unique(m2m_table_name, ['product_id', 'option_id'])

        # Adding M2M table for field related_products on 'Product'
        m2m_table_name = db.shorten_name(u'catalogue_product_related_products')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_product', models.ForeignKey(orm[u'catalogue.product'], null=False)),
            ('to_product', models.ForeignKey(orm[u'catalogue.product'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_product_id', 'to_product_id'])

        # Adding model 'ContributorRole'
        db.create_table(u'catalogue_contributorrole', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('name_plural', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
        ))
        db.send_create_signal(u'catalogue', ['ContributorRole'])

        # Adding model 'Contributor'
        db.create_table(u'catalogue_contributor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255)),
        ))
        db.send_create_signal(u'catalogue', ['Contributor'])

        # Adding model 'ProductContributor'
        db.create_table(u'catalogue_productcontributor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalogue.Product'])),
            ('contributor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalogue.Contributor'])),
            ('role', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalogue.ContributorRole'], null=True, blank=True)),
        ))
        db.send_create_signal(u'catalogue', ['ProductContributor'])

        # Adding model 'ProductAttribute'
        db.create_table(u'catalogue_productattribute', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product_class', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='attributes', null=True, to=orm['catalogue.ProductClass'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('code', self.gf('django.db.models.fields.SlugField')(max_length=128)),
            ('type', self.gf('django.db.models.fields.CharField')(default='text', max_length=20)),
            ('option_group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalogue.AttributeOptionGroup'], null=True, blank=True)),
            ('entity_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalogue.AttributeEntityType'], null=True, blank=True)),
            ('required', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'catalogue', ['ProductAttribute'])

        # Adding model 'ProductAttributeValue'
        db.create_table(u'catalogue_productattributevalue', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('attribute', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalogue.ProductAttribute'])),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(related_name='attribute_values', to=orm['catalogue.Product'])),
            ('value_text', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('value_integer', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('value_boolean', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('value_float', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('value_richtext', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('value_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('value_option', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalogue.AttributeOption'], null=True, blank=True)),
            ('value_entity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalogue.AttributeEntity'], null=True, blank=True)),
            ('value_file', self.gf('django.db.models.fields.files.FileField')(max_length=255, null=True, blank=True)),
            ('value_image', self.gf('django.db.models.fields.files.ImageField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal(u'catalogue', ['ProductAttributeValue'])

        # Adding model 'AttributeOptionGroup'
        db.create_table(u'catalogue_attributeoptiongroup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal(u'catalogue', ['AttributeOptionGroup'])

        # Adding model 'AttributeOption'
        db.create_table(u'catalogue_attributeoption', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(related_name='options', to=orm['catalogue.AttributeOptionGroup'])),
            ('option', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'catalogue', ['AttributeOption'])

        # Adding model 'AttributeEntity'
        db.create_table(u'catalogue_attributeentity', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255, blank=True)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='entities', to=orm['catalogue.AttributeEntityType'])),
        ))
        db.send_create_signal(u'catalogue', ['AttributeEntity'])

        # Adding model 'AttributeEntityType'
        db.create_table(u'catalogue_attributeentitytype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'catalogue', ['AttributeEntityType'])

        # Adding model 'Option'
        db.create_table(u'catalogue_option', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('code', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=128)),
            ('type', self.gf('django.db.models.fields.CharField')(default='Required', max_length=128)),
        ))
        db.send_create_signal(u'catalogue', ['Option'])

        # Adding model 'ProductImage'
        db.create_table(u'catalogue_productimage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(related_name='images', to=orm['catalogue.Product'])),
            ('original', self.gf('django.db.models.fields.files.ImageField')(max_length=255)),
            ('caption', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('display_order', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'catalogue', ['ProductImage'])

        # Adding unique constraint on 'ProductImage', fields ['product', 'display_order']
        db.create_unique(u'catalogue_productimage', ['product_id', 'display_order'])

        # Adding model 'Brand'
        db.create_table(u'catalogue_brand', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, db_index=True, blank=True)),
        ))
        db.send_create_signal(u'catalogue', ['Brand'])

        # Adding model 'Model'
        db.create_table(u'catalogue_model', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('brand', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalogue.Brand'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, db_index=True, blank=True)),
        ))
        db.send_create_signal(u'catalogue', ['Model'])

        # Adding model 'Version'
        db.create_table(u'catalogue_version', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('model', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalogue.Model'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, db_index=True, blank=True)),
        ))
        db.send_create_signal(u'catalogue', ['Version'])

        # Adding model 'Bodywork'
        db.create_table(u'catalogue_bodywork', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, db_index=True, blank=True)),
        ))
        db.send_create_signal(u'catalogue', ['Bodywork'])

        # Adding model 'Engine'
        db.create_table(u'catalogue_engine', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, db_index=True, blank=True)),
        ))
        db.send_create_signal(u'catalogue', ['Engine'])

        # Adding model 'SearchRequest'
        db.create_table(u'catalogue_searchrequest', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('brand', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='product_brand', null=True, to=orm['catalogue.Brand'])),
            ('model', self.gf('smart_selects.db_fields.ChainedForeignKey')(blank=True, related_name='product_model', null=True, to=orm['catalogue.Model'])),
            ('version', self.gf('smart_selects.db_fields.ChainedForeignKey')(blank=True, related_name='product_version', null=True, to=orm['catalogue.Version'])),
            ('bodywork', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='product_bodywork', null=True, to=orm['catalogue.Bodywork'])),
            ('engine', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='product_engine', null=True, to=orm['catalogue.Engine'])),
            ('frameref', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('comments', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, db_index=True, blank=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='search_requests', null=True, to=orm['piezas.User'])),
            ('search_type', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('state', self.gf('django.db.models.fields.CharField')(default='pending', max_length=25)),
            ('expiration_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'catalogue', ['SearchRequest'])

        # Adding model 'SearchItemRequest'
        db.create_table(u'catalogue_searchitemrequest', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(related_name='product_category', to=orm['catalogue.Category'])),
            ('piece', self.gf('smart_selects.db_fields.ChainedForeignKey')(related_name='product_piece', to=orm['catalogue.Product'])),
            ('comments', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('quantity', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='search_product_requests', null=True, to=orm['piezas.User'])),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, db_index=True, blank=True)),
            ('search_request', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalogue.SearchRequest'], null=True, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(default='pending', max_length=25)),
        ))
        db.send_create_signal(u'catalogue', ['SearchItemRequest'])

        # Adding model 'Quote'
        db.create_table(u'catalogue_quote', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('search_request', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalogue.SearchRequest'])),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='quote_owner', null=True, to=orm['piezas.User'])),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, db_index=True, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(default='pending', max_length=25)),
            ('base_total_excl_tax', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=2)),
            ('base_total_incl_tax', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=2)),
            ('shipping_total_excl_tax', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=2)),
            ('shipping_total_incl_tax', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=2)),
            ('grand_total_excl_tax', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=2)),
            ('grand_total_incl_tax', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=2)),
            ('comments', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('warranty_days', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('shipping_days', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'catalogue', ['Quote'])

        # Adding model 'QuoteItem'
        db.create_table(u'catalogue_quoteitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('search_item_request', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalogue.SearchItemRequest'])),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='quote_item_owner', null=True, to=orm['piezas.User'])),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, db_index=True, blank=True)),
            ('quantity', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            ('base_total_excl_tax', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=2)),
            ('shipping_total_excl_tax', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=2)),
            ('state', self.gf('django.db.models.fields.CharField')(default='pending', max_length=25)),
            ('comments', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'catalogue', ['QuoteItem'])


    def backwards(self, orm):
        # Removing unique constraint on 'ProductImage', fields ['product', 'display_order']
        db.delete_unique(u'catalogue_productimage', ['product_id', 'display_order'])

        # Deleting model 'ProductRecommendation'
        db.delete_table(u'catalogue_productrecommendation')

        # Deleting model 'ProductClass'
        db.delete_table(u'catalogue_productclass')

        # Removing M2M table for field options on 'ProductClass'
        db.delete_table(db.shorten_name(u'catalogue_productclass_options'))

        # Deleting model 'Category'
        db.delete_table(u'catalogue_category')

        # Deleting model 'ProductCategory'
        db.delete_table(u'catalogue_productcategory')

        # Deleting model 'Product'
        db.delete_table(u'catalogue_product')

        # Removing M2M table for field product_options on 'Product'
        db.delete_table(db.shorten_name(u'catalogue_product_product_options'))

        # Removing M2M table for field related_products on 'Product'
        db.delete_table(db.shorten_name(u'catalogue_product_related_products'))

        # Deleting model 'ContributorRole'
        db.delete_table(u'catalogue_contributorrole')

        # Deleting model 'Contributor'
        db.delete_table(u'catalogue_contributor')

        # Deleting model 'ProductContributor'
        db.delete_table(u'catalogue_productcontributor')

        # Deleting model 'ProductAttribute'
        db.delete_table(u'catalogue_productattribute')

        # Deleting model 'ProductAttributeValue'
        db.delete_table(u'catalogue_productattributevalue')

        # Deleting model 'AttributeOptionGroup'
        db.delete_table(u'catalogue_attributeoptiongroup')

        # Deleting model 'AttributeOption'
        db.delete_table(u'catalogue_attributeoption')

        # Deleting model 'AttributeEntity'
        db.delete_table(u'catalogue_attributeentity')

        # Deleting model 'AttributeEntityType'
        db.delete_table(u'catalogue_attributeentitytype')

        # Deleting model 'Option'
        db.delete_table(u'catalogue_option')

        # Deleting model 'ProductImage'
        db.delete_table(u'catalogue_productimage')

        # Deleting model 'Brand'
        db.delete_table(u'catalogue_brand')

        # Deleting model 'Model'
        db.delete_table(u'catalogue_model')

        # Deleting model 'Version'
        db.delete_table(u'catalogue_version')

        # Deleting model 'Bodywork'
        db.delete_table(u'catalogue_bodywork')

        # Deleting model 'Engine'
        db.delete_table(u'catalogue_engine')

        # Deleting model 'SearchRequest'
        db.delete_table(u'catalogue_searchrequest')

        # Deleting model 'SearchItemRequest'
        db.delete_table(u'catalogue_searchitemrequest')

        # Deleting model 'Quote'
        db.delete_table(u'catalogue_quote')

        # Deleting model 'QuoteItem'
        db.delete_table(u'catalogue_quoteitem')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'catalogue.attributeentity': {
            'Meta': {'object_name': 'AttributeEntity'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entities'", 'to': u"orm['catalogue.AttributeEntityType']"})
        },
        u'catalogue.attributeentitytype': {
            'Meta': {'object_name': 'AttributeEntityType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'catalogue.attributeoption': {
            'Meta': {'object_name': 'AttributeOption'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'options'", 'to': u"orm['catalogue.AttributeOptionGroup']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'option': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'catalogue.attributeoptiongroup': {
            'Meta': {'object_name': 'AttributeOptionGroup'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'catalogue.bodywork': {
            'Meta': {'object_name': 'Bodywork'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'catalogue.brand': {
            'Meta': {'object_name': 'Brand'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'catalogue.category': {
            'Meta': {'ordering': "['full_name']", 'object_name': 'Category'},
            'depth': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'numchild': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'path': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'})
        },
        u'catalogue.contributor': {
            'Meta': {'object_name': 'Contributor'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'})
        },
        u'catalogue.contributorrole': {
            'Meta': {'object_name': 'ContributorRole'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'name_plural': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        u'catalogue.engine': {
            'Meta': {'object_name': 'Engine'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'catalogue.model': {
            'Meta': {'object_name': 'Model'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalogue.Brand']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'catalogue.option': {
            'Meta': {'object_name': 'Option'},
            'code': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '128'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'Required'", 'max_length': '128'})
        },
        u'catalogue.product': {
            'Meta': {'ordering': "['-date_created']", 'object_name': 'Product'},
            'attributes': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['catalogue.ProductAttribute']", 'through': u"orm['catalogue.ProductAttributeValue']", 'symmetrical': 'False'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['catalogue.Category']", 'through': u"orm['catalogue.ProductCategory']", 'symmetrical': 'False'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_discountable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'variants'", 'null': 'True', 'to': u"orm['catalogue.Product']"}),
            'product_class': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'products'", 'null': 'True', 'to': u"orm['catalogue.ProductClass']"}),
            'product_options': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['catalogue.Option']", 'symmetrical': 'False', 'blank': 'True'}),
            'rating': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'recommended_products': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['catalogue.Product']", 'symmetrical': 'False', 'through': u"orm['catalogue.ProductRecommendation']", 'blank': 'True'}),
            'related_products': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'relations'", 'blank': 'True', 'to': u"orm['catalogue.Product']"}),
            'score': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'status': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'upc': ('django.db.models.fields.CharField', [], {'max_length': '64', 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'catalogue.productattribute': {
            'Meta': {'ordering': "['code']", 'object_name': 'ProductAttribute'},
            'code': ('django.db.models.fields.SlugField', [], {'max_length': '128'}),
            'entity_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalogue.AttributeEntityType']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'option_group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalogue.AttributeOptionGroup']", 'null': 'True', 'blank': 'True'}),
            'product_class': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'attributes'", 'null': 'True', 'to': u"orm['catalogue.ProductClass']"}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'text'", 'max_length': '20'})
        },
        u'catalogue.productattributevalue': {
            'Meta': {'object_name': 'ProductAttributeValue'},
            'attribute': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalogue.ProductAttribute']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'attribute_values'", 'to': u"orm['catalogue.Product']"}),
            'value_boolean': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'value_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'value_entity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalogue.AttributeEntity']", 'null': 'True', 'blank': 'True'}),
            'value_file': ('django.db.models.fields.files.FileField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'value_float': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'value_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'value_integer': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'value_option': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalogue.AttributeOption']", 'null': 'True', 'blank': 'True'}),
            'value_richtext': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'value_text': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'catalogue.productcategory': {
            'Meta': {'ordering': "['-is_canonical']", 'object_name': 'ProductCategory'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalogue.Category']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_canonical': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalogue.Product']"})
        },
        u'catalogue.productclass': {
            'Meta': {'ordering': "['name']", 'object_name': 'ProductClass'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'options': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['catalogue.Option']", 'symmetrical': 'False', 'blank': 'True'}),
            'requires_shipping': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '128'}),
            'track_stock': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'catalogue.productcontributor': {
            'Meta': {'object_name': 'ProductContributor'},
            'contributor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalogue.Contributor']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalogue.Product']"}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalogue.ContributorRole']", 'null': 'True', 'blank': 'True'})
        },
        u'catalogue.productimage': {
            'Meta': {'ordering': "['display_order']", 'unique_together': "(('product', 'display_order'),)", 'object_name': 'ProductImage'},
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'display_order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'original': ('django.db.models.fields.files.ImageField', [], {'max_length': '255'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'images'", 'to': u"orm['catalogue.Product']"})
        },
        u'catalogue.productrecommendation': {
            'Meta': {'object_name': 'ProductRecommendation'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'primary': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'primary_recommendations'", 'to': u"orm['catalogue.Product']"}),
            'ranking': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'recommendation': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalogue.Product']"})
        },
        u'catalogue.quote': {
            'Meta': {'object_name': 'Quote'},
            'base_total_excl_tax': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '2'}),
            'base_total_incl_tax': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '2'}),
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'grand_total_excl_tax': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '2'}),
            'grand_total_incl_tax': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'quote_owner'", 'null': 'True', 'to': u"orm['piezas.User']"}),
            'search_request': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalogue.SearchRequest']"}),
            'shipping_days': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'shipping_total_excl_tax': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '2'}),
            'shipping_total_incl_tax': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '2'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'pending'", 'max_length': '25'}),
            'warranty_days': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'catalogue.quoteitem': {
            'Meta': {'object_name': 'QuoteItem'},
            'base_total_excl_tax': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '2'}),
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'quote_item_owner'", 'null': 'True', 'to': u"orm['piezas.User']"}),
            'quantity': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'search_item_request': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalogue.SearchItemRequest']"}),
            'shipping_total_excl_tax': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '2'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'pending'", 'max_length': '25'})
        },
        u'catalogue.searchitemrequest': {
            'Meta': {'object_name': 'SearchItemRequest'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'product_category'", 'to': u"orm['catalogue.Category']"}),
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'search_product_requests'", 'null': 'True', 'to': u"orm['piezas.User']"}),
            'piece': ('smart_selects.db_fields.ChainedForeignKey', [], {'related_name': "'product_piece'", 'to': u"orm['catalogue.Product']"}),
            'quantity': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'search_request': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalogue.SearchRequest']", 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'pending'", 'max_length': '25'})
        },
        u'catalogue.searchrequest': {
            'Meta': {'object_name': 'SearchRequest'},
            'bodywork': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'product_bodywork'", 'null': 'True', 'to': u"orm['catalogue.Bodywork']"}),
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'product_brand'", 'null': 'True', 'to': u"orm['catalogue.Brand']"}),
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'engine': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'product_engine'", 'null': 'True', 'to': u"orm['catalogue.Engine']"}),
            'expiration_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'frameref': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('smart_selects.db_fields.ChainedForeignKey', [], {'blank': 'True', 'related_name': "'product_model'", 'null': 'True', 'to': u"orm['catalogue.Model']"}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'search_requests'", 'null': 'True', 'to': u"orm['piezas.User']"}),
            'search_type': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'pending'", 'max_length': '25'}),
            'version': ('smart_selects.db_fields.ChainedForeignKey', [], {'blank': 'True', 'related_name': "'product_version'", 'null': 'True', 'to': u"orm['catalogue.Version']"})
        },
        u'catalogue.version': {
            'Meta': {'object_name': 'Version'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalogue.Model']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'piezas.user': {
            'Meta': {'object_name': 'User'},
            'cif': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'promotional_code': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'customer'", 'max_length': '15'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"})
        }
    }

    complete_apps = ['catalogue']