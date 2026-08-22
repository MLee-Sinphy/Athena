from django.core.files.storage import default_storage
from django.db.models import Count, Q
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import AdministratorOnly, PasswordChanged

from .models import BookCopy, BookTitle, CopyState
from .serializers import (
    AdminBookImageSerializer,
    AdminCopySerializer,
    AdminTitleSerializer,
    CatalogTitleDetailSerializer,
    CatalogTitleSerializer,
)


class CatalogListView(APIView):
    permission_classes = [PasswordChanged]

    def get(self, request):
        titles = BookTitle.objects.prefetch_related("tags").annotate(
            available_copies=Count("copies", filter=Q(copies__state=CopyState.AVAILABLE))
        )
        query = request.query_params.get("q", "").strip()
        if query:
            tag_query = query[1:] if query.startswith("#") else query
            titles = titles.filter(
                Q(name__icontains=query)
                | Q(author__icontains=query)
                | Q(isbn__icontains=query)
                | Q(category__icontains=query)
                | Q(description__icontains=query)
                | Q(tags__name__iexact=tag_query)
                | Q(tag_suggestions__name__iexact=tag_query)
            ).distinct()
        paginator = PageNumberPagination()
        paginator.page_size = 24
        paginator.page_size_query_param = "page_size"
        paginator.max_page_size = 100
        page = paginator.paginate_queryset(titles, request, view=self)
        serializer = CatalogTitleSerializer(page, many=True, context={"request": request})
        return paginator.get_paginated_response(serializer.data)


class CatalogDetailView(APIView):
    permission_classes = [PasswordChanged]

    def get(self, request, title_id):
        title = get_object_or_404(BookTitle.objects.prefetch_related("tags", "copies"), pk=title_id)
        title.available_copies = title.copies.filter(state=CopyState.AVAILABLE).count()
        return Response(CatalogTitleDetailSerializer(title, context={"request": request}).data)


class AdminTitleView(APIView):
    permission_classes = [AdministratorOnly]

    def post(self, request):
        serializer = AdminTitleSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AdminTitleDetailView(APIView):
    permission_classes = [AdministratorOnly]

    def get_object(self, title_id):
        return get_object_or_404(BookTitle, pk=title_id)

    def get(self, request, title_id):
        return Response(
            AdminTitleSerializer(self.get_object(title_id), context={"request": request}).data
        )

    def patch(self, request, title_id):
        serializer = AdminTitleSerializer(
            self.get_object(title_id), data=request.data, partial=True, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, title_id):
        self.get_object(title_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AdminCopyView(APIView):
    permission_classes = [AdministratorOnly]

    def post(self, request):
        serializer = AdminCopySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AdminCopyDetailView(APIView):
    permission_classes = [AdministratorOnly]

    def get_object(self, copy_id):
        return get_object_or_404(BookCopy, pk=copy_id)

    def get(self, request, copy_id):
        return Response(AdminCopySerializer(self.get_object(copy_id)).data)

    def patch(self, request, copy_id):
        copy = self.get_object(copy_id)
        before = AdminCopySerializer(copy).data
        serializer = AdminCopySerializer(copy, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        copy = serializer.save()
        from governance.services import record_audit

        record_audit(
            request.user,
            "book_copy_changed",
            copy,
            dict(before),
            dict(serializer.data),
            request.data.get("reason", ""),
        )
        return Response(serializer.data)

    def delete(self, request, copy_id):
        self.get_object(copy_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProtectedMediaView(APIView):
    permission_classes = [PasswordChanged]

    def get(self, request, name):
        if not name.startswith(("covers/", "books/")) or not default_storage.exists(name):
            raise Http404
        return FileResponse(default_storage.open(name, "rb"), as_attachment=False)


class AdminBookImageView(APIView):
    permission_classes = [AdministratorOnly]

    def post(self, request):
        serializer = AdminBookImageSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
