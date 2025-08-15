from rest_framework import viewsets
from .models import Listing, Booking
from .serializers import ListingSerializer, BookingSerializer
import os
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Payment
from .serializers import PaymentSerializer

CHAPA_SECRET_KEY = os.getenv("CHAPA_SECRET_KEY")
CHAPA_BASE_URL = os.getenv("CHAPA_BASE_URL", "https://api.chapa.co/v1")

class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


class InitiatePaymentView(generics.CreateAPIView):
    serializer_class = PaymentSerializer

    def create(self, request, *args, **kwargs):
        booking_reference = request.data.get("booking_reference")
        amount = request.data.get("amount")

        payload = {
            "amount": str(amount),
            "currency": "ETB",  # Change currency if needed
            "tx_ref": booking_reference,
            "callback_url": "http://localhost:8000/api/payments/verify/",
            "return_url": "http://localhost:8000/payment-success/",
            "customization[title]": "Travel Booking Payment",
            "customization[description]": "Secure payment for booking"
        }

        headers = {
            "Authorization": f"Bearer {CHAPA_SECRET_KEY}"
        }

        chapa_url = f"{CHAPA_BASE_URL}/transaction/initialize"
        r = requests.post(chapa_url, headers=headers, data=payload)

        if r.status_code == 200:
            data = r.json()
            payment = Payment.objects.create(
                booking_reference=booking_reference,
                amount=amount,
                transaction_id=data["data"]["tx_ref"],
                status="Pending"
            )
            return Response({
                "payment_url": data["data"]["checkout_url"],
                "transaction_id": payment.transaction_id
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Payment initiation failed"}, status=status.HTTP_400_BAD_REQUEST)


class VerifyPaymentView(generics.GenericAPIView):
    def get(self, request, tx_ref):
        headers = {
            "Authorization": f"Bearer {CHAPA_SECRET_KEY}"
        }
        r = requests.get(f"{CHAPA_BASE_URL}/transaction/verify/{tx_ref}", headers=headers)

        if r.status_code == 200:
            data = r.json()
            try:
                payment = Payment.objects.get(transaction_id=tx_ref)
                if data["data"]["status"] == "success":
                    payment.status = "Completed"
                else:
                    payment.status = "Failed"
                payment.save()
                return Response({"status": payment.status})
            except Payment.DoesNotExist:
                return Response({"error": "Payment not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "Verification failed"}, status=status.HTTP_400_BAD_REQUEST)
