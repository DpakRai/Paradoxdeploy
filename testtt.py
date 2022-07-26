# def create_payment_intent(price,meta_data=None):
#     import stripe
#     stripe.api_key = "sk_test_51KTMNcSJ7XYjnhJesJFzKbx7t16uAhjIq9xPOCyRxy7u0ZppNYWwx4ah8H3YzfQoMKKm8K1SkhQwQZyrErYlvLjG003I5HezGI"
#     return stripe.PaymentIntent.create(
#         amount=price,
#         currency="usd",
#         payment_method_types=["card"],
#         metadata = meta_data
#         )

# def confirm_payment(id):
#     import stripe
#     stripe.api_key = "sk_test_51KTMNcSJ7XYjnhJesJFzKbx7t16uAhjIq9xPOCyRxy7u0ZppNYWwx4ah8H3YzfQoMKKm8K1SkhQwQZyrErYlvLjG003I5HezGI"
#     intent=stripe.PaymentIntent.retrieve(id)
#     status=intent.get('status')
#     if status!='succeeded':
#         raise Exception("Payment Incomplete")
#     return intent

from geopy.distance import distance as geopy_distance
start = (27.69454874365567, 85.31147118571127)
end = (27.695093788577893, 85.31004961502003)
d = geopy_distance(start, end)
print(d.meters)
print(d.miles)