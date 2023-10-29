from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.http import JsonResponse
import json
from .models import Payment, Transaction
from django.db import transaction
from django.utils import timezone

@method_decorator(csrf_exempt, name='dispatch')
class RazorPayWebHookView(View):

    def get(self, request, *args, **kwargs):
       return JsonResponse({'status': 'ok'})

    def post(self, request):
        webhook_body = request.body.decode('utf-8')
        body = json.loads(webhook_body)
        try:
            entity = body['payload']['payment']['entity']
            razorpay_order_id = entity['order_id']
            razorpay_amount = entity['amount']
            verify = True
            if body['event'] == 'payment.captured' and verify:
                try:
                    payment = Payment.objects.get(rzp_order_id=razorpay_order_id)
                except Payment.DoesNotExist:
                    raise Exception('Payment not found')
                with transaction.atomic():
                    payment.order.status = "PROCESSING"
                    payment.order.is_payment_successful = True
                    payment.order.is_captured = True
                    payment.order.processed_on = timezone.now().date()
                    payment.order.save(force_update=True)
                    payment.status = 'CAPTURED'
                    payment.charged_value = (razorpay_amount / 100)
                    payment.save(force_update=True)
                    trans = Transaction()
                    trans.raw_data = body
                    trans.save(force_insert=True)
            else:
                return JsonResponse(
                    {
                        "status": "ok",
                        "message": "authotrized"
                    }
                )
            return JsonResponse({"status": "ok"})
        except Exception as e:
            print(e)
            return JsonResponse({"status": "Fail", "message": "invalid request {}".format(e)}, status=400)