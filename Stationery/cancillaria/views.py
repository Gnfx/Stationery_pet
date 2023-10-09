from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Cancillaria, Supplier, Order, Pos_order, Chegue
from .forms import CancillariaForm, SupplierForm, RegistrationForm, LoginForm, ContactForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .utils import Default_value
from django.urls import reverse, reverse_lazy
from django.core.paginator import Paginator
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.core.mail import send_mail, send_mass_mail
from django.conf import settings
from django.http import JsonResponse
from .serializers import CancillariaSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import viewsets
from basket.forms import BasketAddProductForm


def index(request):
    print(request)
    return HttpResponse('Hello Django')


def cancillaria(request):
    cancillarias = Cancillaria.objects.all()
    responce = '<h1>Список канцтоваров</h1>'

    for item in cancillarias:
        responce += f'<div>\n<p>{item.name}</p>\n<p>{item.price}</p></div>'
    return HttpResponse(responce)


def index_template(request):
    return render(request, 'cancillaria/index.html')


def cancillaria_template(request):
    context = {'title': 'Канцтовары'}
    cancillarias = Cancillaria.objects.all()
    paginator = Paginator(cancillarias, 3)
    page_num = request.GET.get('page', 1)
    page_object = paginator.get_page(page_num)
    context['page_obj'] = page_object
    if request.method == "GET":
        cancillaria_id = request.GET.get('id', 1)
        try:
            cancillaria_one = Cancillaria.objects.get(pk=cancillaria_id)
        except:
            pass
        else:
            context['cancillaria_one'] = cancillaria_one

        context['name'] = request.GET.get('name', 'History')

    elif request.method == "POST":
        cancillaria_id = request.POST.get('id', 1)
        try:
            cancillaria_one = Cancillaria.objects.get(pk=cancillaria_id)
        except:
            pass
        else:
            context['cancillaria_one'] = cancillaria_one

        context['name'] = request.POST.get('name', 'History')

    return render(
        request=request,
        template_name='cancillaria/cancillaria-all.html',
        context=context
    )


@permission_required('cancillaria.add_cancillaria')
def cancillaria_add(request):
    if request.method == "POST":
        context = dict()
        context['name'] = request.POST.get('name')
        context['description'] = request.POST.get('description')
        context['price'] = request.POST.get('price')
        context['photo'] = request.POST.get('photo')

        Cancillaria.objects.create(
            name=context['name'],
            description=context['description'],
            price=context['price'],
            photo=context['photo'],
        )
        return HttpResponseRedirect('/cancillaria/list/')
    else:
        cancillariaform = CancillariaForm()
        context = {'form': cancillariaform}
        return render(request, "cancillaria/cancillaria-add.html", context=context)


@login_required
def cancillaria_detail(request, cancillaria_id):
    basket_form = BasketAddProductForm
    cancillaria = get_object_or_404(Cancillaria, pk=cancillaria_id)
    return render(request, 'cancillaria/cancillaria-info.html',
                  {'cancillaria_item': cancillaria, 'basket_form': basket_form})


def supplier_list(request):
    # suppliers = Supplier.objects.filter(exist=True).order_by('title')
    return render(request, 'cancillaria/supplier/supplier-list.html')
    # {'supplier': suppliers, 'title': 'Список поставщиков из функции'})


class SupplierListView(ListView, Default_value):
    model = Supplier
    template_name = 'cancillaria/supplier/supplier-list.html'
    context_object_name = 'supplier'
    # extra_context = {'title': 'Список поставщиков из класса'}

    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)

        context = self.add_title_context(context=context, title_name='Страница поставщиков')
        context['info'] = 'Поставщики которые с нами работают'
        return context

    def get_queryset(self):
        return Supplier.objects.filter(exist=True).order_by('title')


class SupplierDetailView(DetailView):
    model = Supplier
    template_name = 'cancillaria/supplier/supplier-info.html'

    context_object_name = 'one_supplier'
    pk_url_kwarg = 'supplier_id'


def supplier_form(request):
    if request.method == "POST":
        form = SupplierForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)

            Supplier.objects.create(
                title=form.cleaned_data['title'],
                agent_name=form.cleaned_data['agent_name'],
                agent_firstname=form.cleaned_data['agent_firstname'],
                agent_patronymic=form.cleaned_data['agent_patronymic'],
                exist=form.cleaned_data['exist'],
            )
            return redirect('list_supp')
        else:
            context = {'form': form}
            return render(request, 'cancillaria/supplier/supplier-add.html', context)

    else:
        form = SupplierForm()
        context = {'form': form}
        return render(request, 'cancillaria/supplier/supplier-add.html', context)


class SupplierCreateView(CreateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'cancillaria/supplier/supplier-add.html'

    context_object_name = 'form'
    success_url = reverse_lazy('list_supp_view')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class SupplierUpdateView(UpdateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'cancillaria/supplier/supplier-edit.html'
    context_object_name = 'from'

    @method_decorator(permission_required('cancillaria.change_supplier'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class SupplierDeleteView(DeleteView):
    model = Supplier
    success_url = reverse_lazy('list_supp_view')

    @method_decorator(permission_required('cancillaria.delete_supplier'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


def user_registration(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            print(user)
            return redirect('index_сancillaria')
    else:
        form = RegistrationForm()
        return render(request, 'cancillaria/auth/registration.html', {'form': form})


def user_login(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            print('is_anon', request.user.is_anonymous)
            print('is_auth', request.user.is_authenticated)
            login(request, user)
            print('is_anon', request.user.is_anonymous)
            print('is_auth', request.user.is_authenticated)
            print(user)
            return redirect('index_сancillaria')
    else:
        form = LoginForm()
        return render(request, 'cancillaria/auth/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('log in')


def contact_email(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            mail = send_mail(
                form.cleaned_data['subject'],
                form.cleaned_data['content'],
                settings.EMAIL_HOST_USER,
                ['gnfx@mail.ru'],
                fail_silently=False
            )
            if mail:
                return redirect('index_сancillaria')
    else:
        form = ContactForm()
    return render(request, 'cancillaria/email.html', {'form': form})


@api_view(['GET', 'POST'])
def cancillaria_api_list(request):
    if request.method == "GET":
        cancillaria_list = Cancillaria.objects.all()
        serializer = CancillariaSerializer(cancillaria_list, many=True)
        return Response({'cancillaria_list': serializer.data})
    elif request.method == "POST":
        serializer = CancillariaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def cancillaria_api_detail(request, pk, format=None):
    cancillaria_obj = get_object_or_404(Cancillaria, pk=pk)
    if cancillaria_obj.exist:
        if request.method == 'GET':
            serializer = CancillariaSerializer(cancillaria_obj)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CancillariaSerializer(cancillaria_obj, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Данные успешно изменены', 'cancillaria': serializer.data})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            cancillaria_obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
