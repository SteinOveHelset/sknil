import stripe
import json
import djstripe

from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from apps.bookmark.models import Bookmark

from djstripe.models import Product

@login_required
def dashboard(request):
    bookmarks = request.user.bookmarks.all().order_by('-created_at')[0:5]
    categories = request.user.categories.all().order_by('-created_at')[0:5]

    context = {
        'bookmarks': bookmarks,
        'categories': categories
    }

    return render(request, 'dashboard/dashboard.html', context)

@login_required
def create_sub(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        payment_method = data['payment_method']
        stripe.api_key = djstripe.settings.STRIPE_SECRET_KEY

        payment_method_obj = stripe.PaymentMethod.retrieve(payment_method)
        djstripe.models.PaymentMethod.sync_from_stripe_data(payment_method_obj)

        try:
            customer = stripe.Customer.create(
                payment_method=payment_method,
                email=request.user.email,
                invoice_settings={
                    'default_payment_method': payment_method
                }
            )

            djstripe_customer = djstripe.models.Customer.sync_from_stripe_data(customer)

            subscription = stripe.Subscription.create(
                customer=customer.id,
                items=[
                    {
                        "price": data["price_id"]
                    }
                ],
                expand=["latest_invoice.payment_intent"]
            )

            djstripe_subscription = djstripe.models.Subscription.sync_from_stripe_data(subscription)

            request.user.userprofile.subscription = subscription.id
            request.user.userprofile.save()

            return JsonResponse(subscription)
        except Exception as e:
            return JsonResponse({'error': (e.args[0])}, status=403)
    else:
        return HttpResponse('Request method not allowed')

@login_required
def plans(request):
    products = Product.objects.all()

    context = {
        'products': products
    }

    return render(request, 'dashboard/plans.html', context)

@login_required
def complete(request):
    return render(request, 'dashboard/complete.html')

@login_required
def settings(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        username = request.POST.get('username', '')

        user = request.user

        if username != request.user.username:
            users = User.objects.filter(username=username)

            if len(users):
                messages.error(request, 'The username already exists!')
            else:
                user.username = username

        user.first_name = first_name
        user.last_name = last_name
        user.save()

        messages.success(request, 'The changes was saved!')

        return redirect('settings')

    return render(request, 'dashboard/settings.html')