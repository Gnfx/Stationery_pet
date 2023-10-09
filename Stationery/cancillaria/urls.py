from django.urls import path
from cancillaria.views import *
from django.conf.urls.static import static

urlpatterns = [
    path('', index_template, name='index_сancillaria'),
    path('list/', cancillaria_template, name='list_сancillaria'),
    path('httpresponse/', index),
    path('add/', cancillaria_add, name='add_сancillaria'),
    path('list/<int:cancillaria_id>/', cancillaria_detail, name='one_сancillaria'),
    path('supplier/add/', supplier_form, name='add_supp'),
    path('supplier/list/', supplier_list, name='list_supp'),

    path('supplier/view/list/', SupplierListView.as_view(), name='list_supp_view'),
    path('supplier/view/add/', SupplierCreateView.as_view(), name='add_supp_view'),
    path('supplier/view/<int:supplier_id>', SupplierDetailView.as_view(), name='info_supp_view'),
    path('supplier/view/edit/<int:pk>', SupplierUpdateView.as_view(), name='edit_supp_view'),
    path('supplier/view/del/<int:pk>', SupplierDeleteView.as_view(), name='del_supp_view'),
    path('registration/', user_registration, name='regis'),
    path('login/', user_login, name='log in'),
    path('logout/', user_logout, name='log out'),
    path('email/', contact_email, name='contact_email'),
    path('api/list/', cancillaria_api_list, name='cancillaria_api_list'),
    path('api/detail/<int:pk>', cancillaria_api_detail, name='cancillaria_api_detail'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
