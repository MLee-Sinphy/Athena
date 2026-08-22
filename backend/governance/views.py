from django.db.models import Count
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import AdministratorOnly, PasswordChanged
from circulation.models import Loan

from .models import AuditEntry
from .serializers import AuditEntrySerializer, FeedbackSerializer, RatingSerializer
from .services import submit_return_feedback


class FeedbackView(APIView):
    permission_classes = [PasswordChanged]

    def post(self, request, loan_id):
        serializer = FeedbackSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        rating = submit_return_feedback(loan_id, request.user.id, **serializer.validated_data)
        return Response(
            RatingSerializer(rating).data if rating else {}, status=status.HTTP_201_CREATED
        )


class AuditListView(APIView):
    permission_classes = [AdministratorOnly]

    def get(self, request):
        return Response({"results": AuditEntrySerializer(AuditEntry.objects.all(), many=True).data})


class CirculationAnalyticsView(APIView):
    permission_classes = [AdministratorOnly]

    def get(self, request):
        returned = Loan.objects.filter(returned_on__isnull=False)
        by_title = list(
            returned.values("reservation__title_id", "reservation__title__name")
            .annotate(loan_count=Count("id"))
            .order_by("reservation__title_id")
        )
        by_category = list(
            returned.values("reservation__title__category")
            .annotate(loan_count=Count("id"))
            .order_by("reservation__title__category")
        )
        by_period = list(
            returned.values("returned_on").annotate(loan_count=Count("id")).order_by("returned_on")
        )
        return Response({"by_title": by_title, "by_category": by_category, "by_period": by_period})
