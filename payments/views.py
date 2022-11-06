from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.conf import settings
from rest_framework.reverse import reverse
import stripe

ITEMS = [
    {
        "id": 123,
        "price": 895,
        "image_url": "https://media.istockphoto.com/id/1192094401/photo/delicious-vegetarian-pizza-on-white.jpg?s=612x612&w=0&k=20&c=Qsm2ikAI0Oz5JMu2COCmAODV_5U7YZtipj8Ic7BtJF8=",
        "name": "Pizza Proshute Kerpudhe Familjare",
        "quantity": 2,
    },
    {
        "id": 111,
        "price": 245,
        "image_url": "https://st2.depositphotos.com/1328914/5423/i/950/depositphotos_54233583-stock-photo-greek-gyros-with-tzatziki-sauce.jpg",
        "name": "Sufllaqe mish patate salce kosi",
        "quantity": 3,
    },
]


def get_payment_success(request):
    return render(request, "payments/payment_success.html")


def get_payment_cancel(request):
    return render(request, "payments/payment_cancel.html")


def get_config(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        return JsonResponse(
            {
                "publicKey": settings.STRIPE_PUBLISHABLE_KEY,
            }
        )
    return JsonResponse({"message": "Method not allowed"}, status=405)


def get_shopping_cart(request):
    total = sum(item["price"] * item["quantity"] for item in ITEMS)
    return render(
        request,
        "payments/cart.html",
        context={
            "items": ITEMS,
            "total": total,
        },
    )


def get_checkout_session(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY

    success_url = reverse("payments-success", request=request)
    cancel_url = reverse("payments-cancel", request=request)

    try:
        items = [
            {
                "quantity": item["quantity"],
                "price_data": {
                    "currency": "eur",
                    "product_data": {
                        "name": item["name"],
                        "images": [item["image_url"]],
                    },
                    "unit_amount": item["price"],
                },
            }
            for item in ITEMS
        ]
        # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
        checkout_session = stripe.checkout.Session.create(
            success_url=success_url + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=cancel_url,
            payment_method_types=["card"],
            mode="payment",
            line_items=items,
        )
        return JsonResponse({"sessionId": checkout_session["id"]})
    except Exception as e:
        return JsonResponse({"error": str(e)})
