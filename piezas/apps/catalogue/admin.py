from django.contrib import admin
from django.db.models import get_model
import models

admin.site.register(models.Model)
admin.site.register(models.Version)
admin.site.register(models.Bodywork)
admin.site.register(models.Engine)
admin.site.register(models.Product)
admin.site.register(models.ProductQuestion)
admin.site.register(models.SearchRequest)
admin.site.register(models.SearchItemRequest)
admin.site.register(models.SearchItemRequestAnswers)
admin.site.register(models.Quote)
admin.site.register(models.QuoteItem)

