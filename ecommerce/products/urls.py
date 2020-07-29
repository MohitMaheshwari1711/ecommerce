from django.conf.urls import url

from .views import (
    ProductListView,
    ProductDetailSlugView,
    ProductListFilteredView,
    product_detail_api_view
    )

urlpatterns = [
    url(r'^$', ProductListView.as_view(), name='list'),
    url(r'^(?P<slug>[\w-]+)$', ProductDetailSlugView.as_view(), name='detail'),
]
