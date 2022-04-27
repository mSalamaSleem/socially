from django.shortcuts import render
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
#
# # authorize razorpay client with API Keys.
# razorpay_client = razorpay.Client(
#     auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
#
#
# def homepage(request):
#     currency = 'INR'
#     amount = 10000  # Rs. 100
#
#     # Create a Razorpay Order
#     razorpay_order = razorpay_client.order.create(dict(amount=amount,
#                                                        currency=currency,
#                                                        payment_capture='0'))
#
#     # order id of newly created order.
#     razorpay_order_id = razorpay_order['id']
#     callback_url = 'paymenthandler/'
#
#     # we need to pass these details to frontend.
#     context = {'razorpay_order_id': razorpay_order_id, 'razorpay_merchant_key': settings.RAZOR_KEY_ID,
#                'razorpay_amount': amount, 'currency': currency, 'callback_url': callback_url}
#
#     return render(request, 'membership/plans.html', context=context)
#
#
# # we need to csrf_exempt this url as
# # POST request will be made by Razorpay
# # and it won't have the csrf token.
# @csrf_exempt
# def paymenthandler(request):
#     # only accept POST request.
#     if request.method == "POST":
#         try:
#
#             # get the required parameters from post request.
#             payment_id = request.POST.get('razorpay_payment_id', '')
#             razorpay_order_id = request.POST.get('razorpay_order_id', '')
#             signature = request.POST.get('razorpay_signature', '')
#             params_dict = {
#                 'razorpay_order_id': razorpay_order_id,
#                 'razorpay_payment_id': payment_id,
#                 'razorpay_signature': signature
#             }
#
#             # verify the payment signature.
#             result = razorpay_client.utility.verify_payment_signature(
#                 params_dict)
#             if result is None:
#                 amount = 10000  # Rs. 100
#                 try:
#
#                     # capture the payemt
#                     razorpay_client.payment.capture(payment_id, amount)
#                     print(f"ssssssssssss {request.POST}")
#                     # render success page on successful caputre of payment
#                     return render(request, 'membership/paymentsuccess.html')
#                 except:
#                     print(f"fffffffffff {request.POST}")
#                     # if there is an error while capturing payment.
#                     return render(request, 'membership/paymentfail.html')
#             else:
#
#                 # if signature verification fails.
#                 return render(request, 'membership/paymentfail.html')
#         except:
#
#             # if we don't find the required parameters in POST data
#             return HttpResponseBadRequest()
#     else:
#         # if other than POST request is made.
#         return HttpResponseBadRequest()


def home(request):
    if request.method == "POST":
        name = request.POST.get('name')
        amount = 50000

        client = razorpay.Client(
            auth=("rzp_test_vz1CP5QLynEHCM", "T4fAGC4nVSl7NqIL6FAEkF5a"))

        try:
            payment = client.order.create({'amount': amount, 'currency': 'INR',
                                       'payment_capture': '1'})
            print('ssssssssssssssss')
        except:
            print('fffffffffff')
    return render(request, 'membership/plans.html')


@csrf_exempt
def success(request):
    return render(request, "membership/paymentsuccess.html")
