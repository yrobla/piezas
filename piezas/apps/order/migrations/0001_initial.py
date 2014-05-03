# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PaymentEventQuantity'
        db.create_table(u'order_paymenteventquantity', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(related_name='line_quantities', to=orm['order.PaymentEvent'])),
            ('line', self.gf('django.db.models.fields.related.ForeignKey')(related_name='payment_event_quantities', to=orm['order.Line'])),
            ('quantity', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'order', ['PaymentEventQuantity'])

        # Adding model 'ShippingEventQuantity'
        db.create_table(u'order_shippingeventquantity', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(related_name='line_quantities', to=orm['order.ShippingEvent'])),
            ('line', self.gf('django.db.models.fields.related.ForeignKey')(related_name='shipping_event_quantities', to=orm['order.Line'])),
            ('quantity', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'order', ['ShippingEventQuantity'])

        # Adding model 'Order'
        db.create_table(u'order_order', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=128, db_index=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
            ('basket_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='orders', null=True, on_delete=models.SET_NULL, to=orm['customuser.PiezasUser'])),
            ('billing_address', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['order.BillingAddress'], null=True, on_delete=models.SET_NULL, blank=True)),
            ('currency', self.gf('django.db.models.fields.CharField')(default='EUR', max_length=12)),
            ('total_incl_tax', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=2)),
            ('total_excl_tax', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=2)),
            ('shipping_incl_tax', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=12, decimal_places=2)),
            ('shipping_excl_tax', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=12, decimal_places=2)),
            ('shipping_address', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['order.ShippingAddress'], null=True, on_delete=models.SET_NULL, blank=True)),
            ('shipping_method', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('shipping_code', self.gf('django.db.models.fields.CharField')(default='', max_length=128, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('guest_email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('date_placed', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
        ))
        db.send_create_signal(u'order', ['Order'])

        # Adding model 'OrderNote'
        db.create_table(u'order_ordernote', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order', self.gf('django.db.models.fields.related.ForeignKey')(related_name='notes', to=orm['order.Order'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['customuser.PiezasUser'], null=True)),
            ('note_type', self.gf('django.db.models.fields.CharField')(max_length=128, null=True)),
            ('message', self.gf('django.db.models.fields.TextField')()),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'order', ['OrderNote'])

        # Adding model 'CommunicationEvent'
        db.create_table(u'order_communicationevent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order', self.gf('django.db.models.fields.related.ForeignKey')(related_name='communication_events', to=orm['order.Order'])),
            ('event_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['customer.CommunicationEventType'])),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'order', ['CommunicationEvent'])

        # Adding model 'ShippingAddress'
        db.create_table(u'order_shippingaddress', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('line1', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('line2', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('line3', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('line4', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('postcode', self.gf('oscar.models.fields.UppercaseCharField')(max_length=64, null=True, blank=True)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['address.Country'])),
            ('search_text', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('phone_number', self.gf('oscar.models.fields.PhoneNumberField')(max_length=128, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'order', ['ShippingAddress'])

        # Adding model 'BillingAddress'
        db.create_table(u'order_billingaddress', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('line1', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('line2', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('line3', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('line4', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('postcode', self.gf('oscar.models.fields.UppercaseCharField')(max_length=64, null=True, blank=True)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['address.Country'])),
            ('search_text', self.gf('django.db.models.fields.CharField')(max_length=1000)),
        ))
        db.send_create_signal(u'order', ['BillingAddress'])

        # Adding model 'Line'
        db.create_table(u'order_line', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order', self.gf('django.db.models.fields.related.ForeignKey')(related_name='lines', to=orm['order.Order'])),
            ('partner', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='order_lines', null=True, on_delete=models.SET_NULL, to=orm['partner.Partner'])),
            ('stockrecord', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['partner.StockRecord'], null=True, on_delete=models.SET_NULL, blank=True)),
            ('partner_name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('partner_sku', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('upc', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalogue.Product'], null=True, on_delete=models.SET_NULL, blank=True)),
            ('quantity', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            ('line_price_incl_tax', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=2)),
            ('line_price_excl_tax', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=2)),
            ('line_price_before_discounts_incl_tax', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=2)),
            ('line_price_before_discounts_excl_tax', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=2)),
            ('unit_cost_price', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=12, decimal_places=2, blank=True)),
            ('unit_price_incl_tax', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=12, decimal_places=2, blank=True)),
            ('unit_price_excl_tax', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=12, decimal_places=2, blank=True)),
            ('unit_retail_price', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=12, decimal_places=2, blank=True)),
            ('partner_line_reference', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('partner_line_notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('est_dispatch_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'order', ['Line'])

        # Adding model 'LinePrice'
        db.create_table(u'order_lineprice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order', self.gf('django.db.models.fields.related.ForeignKey')(related_name='line_prices', to=orm['order.Order'])),
            ('line', self.gf('django.db.models.fields.related.ForeignKey')(related_name='prices', to=orm['order.Line'])),
            ('quantity', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            ('price_incl_tax', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=2)),
            ('price_excl_tax', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=2)),
            ('shipping_incl_tax', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=12, decimal_places=2)),
            ('shipping_excl_tax', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=12, decimal_places=2)),
        ))
        db.send_create_signal(u'order', ['LinePrice'])

        # Adding model 'LineAttribute'
        db.create_table(u'order_lineattribute', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('line', self.gf('django.db.models.fields.related.ForeignKey')(related_name='attributes', to=orm['order.Line'])),
            ('option', self.gf('django.db.models.fields.related.ForeignKey')(related_name='line_attributes', null=True, on_delete=models.SET_NULL, to=orm['catalogue.Option'])),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'order', ['LineAttribute'])

        # Adding model 'ShippingEvent'
        db.create_table(u'order_shippingevent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order', self.gf('django.db.models.fields.related.ForeignKey')(related_name='shipping_events', to=orm['order.Order'])),
            ('event_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['order.ShippingEventType'])),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'order', ['ShippingEvent'])

        # Adding model 'ShippingEventType'
        db.create_table(u'order_shippingeventtype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('code', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=128)),
        ))
        db.send_create_signal(u'order', ['ShippingEventType'])

        # Adding model 'PaymentEvent'
        db.create_table(u'order_paymentevent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order', self.gf('django.db.models.fields.related.ForeignKey')(related_name='payment_events', to=orm['order.Order'])),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=2)),
            ('reference', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('event_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['order.PaymentEventType'])),
            ('shipping_event', self.gf('django.db.models.fields.related.ForeignKey')(related_name='payment_events', null=True, to=orm['order.ShippingEvent'])),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'order', ['PaymentEvent'])

        # Adding model 'PaymentEventType'
        db.create_table(u'order_paymenteventtype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
            ('code', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=128)),
        ))
        db.send_create_signal(u'order', ['PaymentEventType'])

        # Adding model 'OrderDiscount'
        db.create_table(u'order_orderdiscount', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order', self.gf('django.db.models.fields.related.ForeignKey')(related_name='discounts', to=orm['order.Order'])),
            ('category', self.gf('django.db.models.fields.CharField')(default='Basket', max_length=64)),
            ('offer_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('offer_name', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, db_index=True)),
            ('voucher_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('voucher_code', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, db_index=True)),
            ('frequency', self.gf('django.db.models.fields.PositiveIntegerField')(null=True)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=12, decimal_places=2)),
            ('message', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'order', ['OrderDiscount'])


    def backwards(self, orm):
        # Deleting model 'PaymentEventQuantity'
        db.delete_table(u'order_paymenteventquantity')

        # Deleting model 'ShippingEventQuantity'
        db.delete_table(u'order_shippingeventquantity')

        # Deleting model 'Order'
        db.delete_table(u'order_order')

        # Deleting model 'OrderNote'
        db.delete_table(u'order_ordernote')

        # Deleting model 'CommunicationEvent'
        db.delete_table(u'order_communicationevent')

        # Deleting model 'ShippingAddress'
        db.delete_table(u'order_shippingaddress')

        # Deleting model 'BillingAddress'
        db.delete_table(u'order_billingaddress')

        # Deleting model 'Line'
        db.delete_table(u'order_line')

        # Deleting model 'LinePrice'
        db.delete_table(u'order_lineprice')

        # Deleting model 'LineAttribute'
        db.delete_table(u'order_lineattribute')

        # Deleting model 'ShippingEvent'
        db.delete_table(u'order_shippingevent')

        # Deleting model 'ShippingEventType'
        db.delete_table(u'order_shippingeventtype')

        # Deleting model 'PaymentEvent'
        db.delete_table(u'order_paymentevent')

        # Deleting model 'PaymentEventType'
        db.delete_table(u'order_paymenteventtype')

        # Deleting model 'OrderDiscount'
        db.delete_table(u'order_orderdiscount')


    models = {
        u'address.country': {
            'Meta': {'ordering': "('-display_order', 'name')", 'object_name': 'Country'},
            'display_order': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0', 'db_index': 'True'}),
            'is_shipping_country': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'iso_3166_1_a2': ('django.db.models.fields.CharField', [], {'max_length': '2', 'primary_key': 'True'}),
            'iso_3166_1_a3': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'db_index': 'True'}),
            'iso_3166_1_numeric': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'printable_name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
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
        u'catalogue.productrecommendation': {
            'Meta': {'object_name': 'ProductRecommendation'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'primary': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'primary_recommendations'", 'to': u"orm['catalogue.Product']"}),
            'ranking': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'recommendation': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalogue.Product']"})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'customer.communicationeventtype': {
            'Meta': {'object_name': 'CommunicationEventType'},
            'category': ('django.db.models.fields.CharField', [], {'default': "u'Order related'", 'max_length': '255'}),
            'code': ('django.db.models.fields.SlugField', [], {'max_length': '128'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'email_body_html_template': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'email_body_template': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'email_subject_template': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'sms_template': ('django.db.models.fields.CharField', [], {'max_length': '170', 'null': 'True', 'blank': 'True'})
        },
        u'customuser.piezasuser': {
            'Meta': {'object_name': 'PiezasUser'},
            'cif': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'commercial_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'contact_person': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            'iban': ('django_iban.fields.IBANField', [], {'max_length': '34', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_validated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'promotional_code': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'social_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'customer'", 'max_length': '15'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"})
        },
        u'order.billingaddress': {
            'Meta': {'object_name': 'BillingAddress'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['address.Country']"}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'line1': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'line2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'line3': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'line4': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'postcode': ('oscar.models.fields.UppercaseCharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'search_text': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'})
        },
        u'order.communicationevent': {
            'Meta': {'ordering': "['-date_created']", 'object_name': 'CommunicationEvent'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'event_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['customer.CommunicationEventType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'communication_events'", 'to': u"orm['order.Order']"})
        },
        u'order.line': {
            'Meta': {'object_name': 'Line'},
            'est_dispatch_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'line_price_before_discounts_excl_tax': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '2'}),
            'line_price_before_discounts_incl_tax': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '2'}),
            'line_price_excl_tax': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '2'}),
            'line_price_incl_tax': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '2'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'lines'", 'to': u"orm['order.Order']"}),
            'partner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'order_lines'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['partner.Partner']"}),
            'partner_line_notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'partner_line_reference': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'partner_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'partner_sku': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalogue.Product']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'quantity': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'stockrecord': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['partner.StockRecord']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'unit_cost_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '2', 'blank': 'True'}),
            'unit_price_excl_tax': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '2', 'blank': 'True'}),
            'unit_price_incl_tax': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '2', 'blank': 'True'}),
            'unit_retail_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '2', 'blank': 'True'}),
            'upc': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'})
        },
        u'order.lineattribute': {
            'Meta': {'object_name': 'LineAttribute'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'line': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'attributes'", 'to': u"orm['order.Line']"}),
            'option': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'line_attributes'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['catalogue.Option']"}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'order.lineprice': {
            'Meta': {'ordering': "('id',)", 'object_name': 'LinePrice'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'line': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'prices'", 'to': u"orm['order.Line']"}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'line_prices'", 'to': u"orm['order.Order']"}),
            'price_excl_tax': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '2'}),
            'price_incl_tax': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '2'}),
            'quantity': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'shipping_excl_tax': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '12', 'decimal_places': '2'}),
            'shipping_incl_tax': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '12', 'decimal_places': '2'})
        },
        u'order.order': {
            'Meta': {'ordering': "['-date_placed']", 'object_name': 'Order'},
            'basket_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'billing_address': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['order.BillingAddress']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'currency': ('django.db.models.fields.CharField', [], {'default': "'EUR'", 'max_length': '12'}),
            'date_placed': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'guest_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '128', 'db_index': 'True'}),
            'shipping_address': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['order.ShippingAddress']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'shipping_code': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'blank': 'True'}),
            'shipping_excl_tax': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '12', 'decimal_places': '2'}),
            'shipping_incl_tax': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '12', 'decimal_places': '2'}),
            'shipping_method': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'total_excl_tax': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '2'}),
            'total_incl_tax': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '2'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'orders'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['customuser.PiezasUser']"})
        },
        u'order.orderdiscount': {
            'Meta': {'object_name': 'OrderDiscount'},
            'amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '12', 'decimal_places': '2'}),
            'category': ('django.db.models.fields.CharField', [], {'default': "'Basket'", 'max_length': '64'}),
            'frequency': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'offer_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'offer_name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'db_index': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'discounts'", 'to': u"orm['order.Order']"}),
            'voucher_code': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'db_index': 'True'}),
            'voucher_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'order.ordernote': {
            'Meta': {'object_name': 'OrderNote'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'note_type': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'notes'", 'to': u"orm['order.Order']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['customuser.PiezasUser']", 'null': 'True'})
        },
        u'order.paymentevent': {
            'Meta': {'ordering': "['-date_created']", 'object_name': 'PaymentEvent'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '2'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'event_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['order.PaymentEventType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lines': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['order.Line']", 'through': u"orm['order.PaymentEventQuantity']", 'symmetrical': 'False'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'payment_events'", 'to': u"orm['order.Order']"}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'shipping_event': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'payment_events'", 'null': 'True', 'to': u"orm['order.ShippingEvent']"})
        },
        u'order.paymenteventquantity': {
            'Meta': {'object_name': 'PaymentEventQuantity'},
            'event': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'line_quantities'", 'to': u"orm['order.PaymentEvent']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'line': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'payment_event_quantities'", 'to': u"orm['order.Line']"}),
            'quantity': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'order.paymenteventtype': {
            'Meta': {'ordering': "('name',)", 'object_name': 'PaymentEventType'},
            'code': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '128'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        u'order.shippingaddress': {
            'Meta': {'object_name': 'ShippingAddress'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['address.Country']"}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'line1': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'line2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'line3': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'line4': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'phone_number': ('oscar.models.fields.PhoneNumberField', [], {'max_length': '128', 'blank': 'True'}),
            'postcode': ('oscar.models.fields.UppercaseCharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'search_text': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'})
        },
        u'order.shippingevent': {
            'Meta': {'ordering': "['-date_created']", 'object_name': 'ShippingEvent'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'event_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['order.ShippingEventType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lines': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'shipping_events'", 'symmetrical': 'False', 'through': u"orm['order.ShippingEventQuantity']", 'to': u"orm['order.Line']"}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'shipping_events'", 'to': u"orm['order.Order']"})
        },
        u'order.shippingeventquantity': {
            'Meta': {'object_name': 'ShippingEventQuantity'},
            'event': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'line_quantities'", 'to': u"orm['order.ShippingEvent']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'line': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'shipping_event_quantities'", 'to': u"orm['order.Line']"}),
            'quantity': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'order.shippingeventtype': {
            'Meta': {'ordering': "('name',)", 'object_name': 'ShippingEventType'},
            'code': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '128'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'partner.partner': {
            'Meta': {'object_name': 'Partner'},
            'code': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '128'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'partners'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['customuser.PiezasUser']"})
        },
        u'partner.stockrecord': {
            'Meta': {'unique_together': "(('partner', 'partner_sku'),)", 'object_name': 'StockRecord'},
            'cost_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '2', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'low_stock_threshold': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_allocated': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_in_stock': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'partner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stockrecords'", 'to': u"orm['partner.Partner']"}),
            'partner_sku': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'price_currency': ('django.db.models.fields.CharField', [], {'default': "'EUR'", 'max_length': '12'}),
            'price_excl_tax': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '2', 'blank': 'True'}),
            'price_retail': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '2', 'blank': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stockrecords'", 'to': u"orm['catalogue.Product']"})
        },
        u'sites.site': {
            'Meta': {'ordering': "(u'domain',)", 'object_name': 'Site', 'db_table': "u'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['order']