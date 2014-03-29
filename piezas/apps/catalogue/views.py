from django.http import HttpResponse
from django.utils import simplejson
from piezas.apps.catalogue.models import ProductQuestion

def ProductQuestionsView(request, *args, **kwargs):
    current_product = kwargs['pk']

    # retrieve all questions for this product
    try:
        questions = ProductQuestion.objects.filter(product=current_product)

        result = []
        for question in questions:
            result_item = {}
            result_item["id"] = question.id
            result_item["type"] = question.type
            result_item["text"] = question.text
            result.append(result_item)
 
    except Exception as e:
        result = None

    return HttpResponse(simplejson.dumps(result), mimetype='application/json')
