from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .forms import PropertyForm, PropertyImageFormSet
from django.contrib.auth.decorators import login_required
from .models import Property, PropertyImage
from django.contrib.auth import login
from .forms_copy import SignUpForm 

def home(request):
    properties = Property.objects.all()

    title = request.GET.get('title')
    city = request.GET.get('city')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    bedrooms = request.GET.get('bedrooms')

    if title:
        properties = properties.filter(title__icontains=title)
    if city:
        properties = properties.filter(city__name__icontains=city)
    if min_price:
        properties = properties.filter(price__gte=min_price)
    if max_price:
        properties = properties.filter(price__lte=max_price)
    if bedrooms:
        properties = properties.filter(bedrooms=bedrooms)

    # PAGINATION ici
    paginator = Paginator(properties, 20)  # 20 biens par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'properties/home.html', {'page_obj': page_obj})

def property_detail(request, pk):
    prop = Property.objects.get(id=pk)
    return render(request, 'properties/detail.html', {'property': prop})

def add_property(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        formset = PropertyImageFormSet(request.POST, request.FILES, queryset=PropertyImage.objects.none())

        if form.is_valid() and formset.is_valid():
            property_instance = form.save()

            for image_form in formset:
                if image_form.cleaned_data.get('image'):
                    PropertyImage.objects.create(
                        property=property_instance,
                        image=image_form.cleaned_data['image']
                    )

            return redirect('home')
    else:
        form = PropertyForm()
        formset = PropertyImageFormSet(queryset=PropertyImage.objects.none())

    return render(request, 'properties/add_property.html', {
        'form': form,
        'formset': formset
    })

def edit_property(request, pk):
    prop = get_object_or_404(Property, pk=pk,  owner=request.user)

    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=prop)
        formset = PropertyImageFormSet(request.POST, request.FILES, queryset=PropertyImage.objects.filter(property=prop))

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('property_detail', pk=prop.pk)
    else:
        form = PropertyForm(instance=prop)
        formset = PropertyImageFormSet(queryset=PropertyImage.objects.filter(property=prop))

    return render(request, 'properties/edit_property.html', {
        'form': form,
        'formset': formset,
        'property': prop,
    })

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})

@login_required
def my_properties(request):
    properties = Property.objects.filter(owner=request.user)
    paginator = Paginator(properties, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'properties/my_properties.html', {'page_obj': page_obj})
