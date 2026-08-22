from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import AdministratorOnly

from .models import PolicyVersion, RegularOpening
from .serializers import (
    CalendarExceptionSerializer,
    PolicyVersionSerializer,
    RegularOpeningSerializer,
)


class PolicyView(APIView):
    permission_classes = [AdministratorOnly]

    def get(self, request):
        policy = PolicyVersion.objects.first()
        return Response(PolicyVersionSerializer(policy).data if policy else None)

    def post(self, request):
        serializer = PolicyVersionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RegularOpeningView(APIView):
    permission_classes = [AdministratorOnly]

    def put(self, request, weekday):
        opening, _ = RegularOpening.objects.get_or_create(weekday=weekday)
        serializer = RegularOpeningSerializer(opening, data={**request.data, "weekday": weekday})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class CalendarExceptionView(APIView):
    permission_classes = [AdministratorOnly]

    def post(self, request):
        serializer = CalendarExceptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
