from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .forms import PropertyForm, PropertyImageFormSet

from .models import Property, PropertyImage


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
