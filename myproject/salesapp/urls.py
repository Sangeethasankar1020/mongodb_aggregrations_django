from django.urls import path
from . import views

urlpatterns = [
    path('api/insert-sales-data/', views.insert_sales_data, name="insert_sales_data"),
    path('api/insert-supplier/', views.insert_supplier_data, name='insert_supplier_data'),
    path('api/sales-data/', views.get_sales_data, name="get_sales_data"),
    path('api/lookup-supplier/', views.lookup_supplier_info, name="lookup_supplier_info"),
    path('api/unwind-tags/', views.unwind_tags, name="unwind_tags"),
    path('api/set-unset-example/', views.set_and_unset_example, name="set_and_unset_example"),
    path('api/check-tags-array/', views.check_tags_array, name="check_tags_array"),
]
