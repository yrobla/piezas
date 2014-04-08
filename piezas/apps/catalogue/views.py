from django.http import HttpResponse
from django.utils import simplejson
from piezas.apps.catalogue.models import ProductQuestion
from django.views.generic import View
import json

class ProductQuestionsView(View):
    def get(self, request, *args, **kwargs):
        current_product = kwargs['pk']

        # retrieve all questions for this product
        try:
            questions = ProductQuestion.objects.filter(product=current_product)
            current_session = request.session.get('search_data', None)
            if current_session:
                current_data = json.loads(current_session)
            else:
                current_data = {}

            result = []
            for question in questions:
                result_item = {}
                result_item["id"] = question.id
                result_item["type"] = question.type
                result_item["text"] = question.text
                result_item["options"] = question.options

                # check if we have value in session
                question_key = 'question_'+str(question.id)
                if question_key in current_data:
                    result_item["value"] = current_data[question_key]

                result.append(result_item)
 
        except Exception as e:
            result = None

        return HttpResponse(simplejson.dumps(result), mimetype='application/json')
