from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .forms import PropertyForm, PropertyImageFormSet
from django.contrib.auth.decorators import login_required
from .models import Property, PropertyImage
from django.contrib.auth import login
from .user_forms import SignupForm 
from django.contrib import messages
from .models import UserProfile, Property
from django.contrib.auth.models import User
from .forms import EditProfileForm, CommentForm
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db.models import Count

def home(request):
    properties = Property.objects.all()

    title = request.GET.get('title')
    city = request.GET.get('city')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    bedrooms = request.GET.get('bedrooms')
    listing_type = request.GET.get('listing_type')
    properties = Property.objects.annotate(total_likes=Count('likes'))

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
    if listing_type in ['rent', 'sale']:
        properties = properties.filter(listing_type=listing_type)

    # PAGINATION ici
    paginator = Paginator(properties, 20)  # 20 biens par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'properties/home.html', {'page_obj': page_obj})

def property_detail(request, pk):
    prop = get_object_or_404(Property, pk=pk)
    comments = prop.comments.all().order_by('-created_at')
    form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.property = prop
            comment.user = request.user
            comment.save()
            return redirect('property_detail', pk=pk)

    return render(request, 'properties/detail.html', {
        'property': prop,
        'form': form,
        'comments': comments,
    })

@login_required
def toggle_like(request, pk):
    prop = get_object_or_404(Property, pk=pk)
    if request.user in prop.likes.all():
        prop.likes.remove(request.user)
        liked = False
    else:
        prop.likes.add(request.user)
        liked = True
    return JsonResponse({'liked': liked, 'likes_count': prop.total_likes()})
@login_required
def add_property(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        formset = PropertyImageFormSet(request.POST, request.FILES, queryset=PropertyImage.objects.none())

        if form.is_valid() and formset.is_valid():
            property_instance = form.save(commit=False)
            property_instance.owner = request.user  # ✅ Associer le bien à l'utilisateur
            property_instance.save()

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

@login_required
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


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # en attendant validation e-mail
            user.save()

            # Génére un token
            current_site = get_current_site(request)
            subject = 'Activez votre compte Congo Immo'
            message = render_to_string('properties/activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })

            user.email_user(subject, message)


            # ⚠️ Avant de créer un UserProfile, on vérifie s’il existe déjà
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.phone_number = form.cleaned_data['phone_number']
            profile.save()

            # log / email d'activation ici...
            print(f"Email de confirmation envoyé à {user.email}")

            # 💬 Message utilisateur
            messages.success(request, f"Un email de confirmation a été envoyé à {user.email}. Veuillez vérifier votre boîte mail.")


            return redirect('email_verification_notice')

    else:
        form = SignupForm()
    
    return render(request, 'properties/signup.html', {'form': form})

def cgu_view(request):
    return render(request, 'cgu.html')

def email_verification_notice(request):
    return render(request, 'properties/email_verification_notice.html')

@require_POST
def resend_activation(request):
    email = request.POST.get('email')
    user = User.objects.filter(email=email, is_active=False).first()

    if user:
        current_site = get_current_site(request)
        subject = 'Activez votre compte Congo Immo'
        message = render_to_string('properties/activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })
        user.email_user(subject, message)
        messages.success(request, "Un nouvel email d’activation a été envoyé.")
    else:
        messages.error(request, "Aucun utilisateur inactif trouvé avec cet email.")

    return redirect('email_verification_notice')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        user.userprofile.is_email_verified = True
        user.userprofile.save()
        messages.success(request, 'Votre compte a été activé avec succès.')
        return redirect('home')
    else:
        return render(request, 'properties/activation_invalid.html')
    
@login_required
def profile_view(request):
    return render(request, 'properties/profile.html')


@login_required
def my_properties(request):
    properties = Property.objects.filter(owner=request.user)
    paginator = Paginator(properties, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'properties/my_properties.html', {'page_obj': page_obj,'user': request.user})

@login_required
def edit_profile_view(request):
    user = request.user
    profile = user.userprofile

    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            phone = form.cleaned_data.get('phone_number')
            if phone:
                profile.phone_number = phone
                profile.save()

            # Changement de mot de passe
            new_password = form.cleaned_data.get('new_password')
            if new_password:
                user.set_password(new_password)
                user.save()
                messages.success(request, "Profil et mot de passe mis à jour. Veuillez vous reconnecter.")
                return redirect('login')

            messages.success(request, "Profil mis à jour.")
            return redirect('profile')
    else:
        form = EditProfileForm(instance=user, initial={'phone_number': profile.phone_number})

    return render(request, 'properties/edit_profile.html', {'form': form})
@login_required
def delete_property(request, pk):
    prop = get_object_or_404(Property, id=pk, owner=request.user)
    prop.delete()
    messages.success(request, "Le bien a été supprimé.")
    return redirect('my_properties')
