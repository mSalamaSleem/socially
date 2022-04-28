from django.shortcuts import render
from membership.models import Customer
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest, Http404


def home(request):
    if request.method == "POST":
        name = request.POST.get('name')
        amount = 50000

    # make integration call to razorpay api to create a payment object and get the payment_id
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        payment = client.order.create(dict(amount=amount, currency='INR', receipt='order_rcptid_11', payment_capture='1'))
        payment_id = payment['id']

    # create a customer object in the database
        customer = Customer(user=request.user, name=name, payment_id=payment_id, ismember=True)
        customer.save()

    # redirect to the payment page
        return render(request, 'home/profile.html', {'payment_id': payment_id})
    else:
        return render(request, 'membership/plans.html')


# @csrf_exempt
# def payment_status(request):
#     if request.method == "POST":
#         payment_id = request.POST.get('razorpay_payment_id')
#         razorpay_order_id = request.POST.get('razorpay_order_id')
#         razorpay_signature = request.POST.get('razorpay_signature')
#         try:
#             customer = Customer.objects.get(payment_id=payment_id)
#         except Customer.DoesNotExist:
#             return HttpResponseBadRequest()
#         client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
#         try:
#             response = client.utility.verify_payment_signature(razorpay_order_id, razorpay_signature)
#         except Exception:
#             return HttpResponseBadRequest()
#         if response:
#             customer.ismember = True
#             customer.save()
#             return render(request, 'membership/paymentsuccess.html')
#         return HttpResponseBadRequest()
#     else:
#         return HttpResponseBadRequest()


# def payment_status_check(request):
#     return render(request, 'payment_status_check.html')
#
#
# def payment_status_check_success(request):
#     return render(request, 'payment_status_check_success.html')
#
#
# def payment_status_check_failure(request):
#     return render(request, 'payment_status_check_failure.html')
#
#
# def payment_failure(request):
#     return render(request, 'payment_failure.html')
#
#
# def payment_success(request):
#     return render(request, 'payment_success.html')
#
#
# def payment_cancelled(request):
#     return render(request, 'payment_cancelled.html')
#
#
# def payment_error(request):
#     return render(request, 'payment_error.html')
#
#
# def payment_pending(request):
#     return render(request, 'payment_pending.html')
#
#
# def payment_expired(request):
#     return render(request, 'payment_expired.html')
#
#
# def payment_captured(request):
#     return render(request, 'payment_captured.html')
#
#
# def payment_authorized(request):
#     return render(request, 'payment_authorized.html')
#
#
# def payment_failed(request):
#     return render(request, 'payment_failed.html')
#
#
# def payment_refunded(request):
#     return render(request, 'payment_refunded.html')
#
#
# def payment_settled(request):
#     return render(request, 'payment_settled.html')
#
#
# def payment_disbursed(request):
#     return render(request, 'payment_disbursed.html')
#
#
# def payment_reversed(request):
#     return render(request, 'payment_reversed.html')
#
#
# def payment_initiated(request):
#     return render(request, 'payment_initiated.html')
#
#
# def payment_authorized(request):
#     return render(request, 'payment_authorized.html')