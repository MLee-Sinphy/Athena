from django.urls import path

from .views import (
    AdminBookImageView,
    AdminCopyDetailView,
    AdminCopyView,
    AdminTitleDetailView,
    AdminTitleView,
    CatalogDetailView,
    CatalogListView,
    ProtectedMediaView,
)

urlpatterns = [
    path("catalog/titles/", CatalogListView.as_view(), name="catalog-list"),
    path("catalog/titles/<int:title_id>/", CatalogDetailView.as_view(), name="catalog-detail"),
    path("catalog/media/<path:name>", ProtectedMediaView.as_view(), name="catalog-media"),
    path("admin/catalog/titles/", AdminTitleView.as_view(), name="admin-title"),
    path(
        "admin/catalog/titles/<int:title_id>/",
        AdminTitleDetailView.as_view(),
        name="admin-title-detail",
    ),
    path("admin/catalog/copies/", AdminCopyView.as_view(), name="admin-copy"),
    path("admin/catalog/images/", AdminBookImageView.as_view(), name="admin-book-image"),
    path(
        "admin/catalog/copies/<int:copy_id>/",
        AdminCopyDetailView.as_view(),
        name="admin-copy-detail",
    ),
]
