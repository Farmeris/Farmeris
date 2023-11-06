from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from login_app.models import UserProfile  # Update the import statement
from user_profile.forms import UserProfileForm
from add_product_main.models import Polozka, Transport, TransportLoc, Cena, AdditionalImage, PolozkaTransport, Availability
from add_product_main.forms import PictureForm, PolozkaForm, CenaForm, TransportForm
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.template.defaultfilters import slugify
from .utils import is_valid_image
from django.contrib import messages
from PIL import Image
import os
import uuid

# Create your views here.
def is_valid_image(file):
    #Check if the given file is a valid image.
    try:
        # Open the image file using Pillow
        image = Image.open(file)
        image.verify()  # Verify if it's a valid image
        return True
    except:
        return False

@login_required
def pridaj_polozku(request, username):
    user_profile = get_object_or_404(UserProfile, user__username=username)
    transportloc_list = TransportLoc.objects.filter(user_profile=user_profile)
    transport_list = Transport.objects.filter(user_profile=user_profile)
    readonly_cena = True

    context = {
            'username': username,
            'user_profile': user_profile,
            'transport_list': transport_list,
            'transportloc_list': transportloc_list,
            'readonly_cena': readonly_cena,
        }

    if request.user != user_profile.user:
        return render(request, 'access_denied.html')

    #if 'nazov_produktu' in request.method == 'POST':
    if request.method == 'POST':
        nazov_produktu = request.POST['nazov_produktu']
        info_nazov_produktu = request.POST['info_nazov_produktu']
        info_produktu = request.POST['info_produktu']
        image_file = request.FILES.get('image', None)
        amount = request.POST['amount']
        unit = request.POST['unit']
        price = request.POST['price']
        currency = request.POST['currency']

        # Create the transport instance
        transport_type = request.POST.get('transport_type')  
        transport_price = request.POST.get('transport_price')
        transport_unit = request.POST.get('unit')  
        transport_amount = request.POST.get('transport_amount')
        transport_currency = request.POST.get('currency')
        transport_notes = request.POST.get('transport_notes', '')

        # Extract availability details
        availability_start_date = request.POST.get('availability_start_date', None)
        availability_end_date = request.POST.get('availability_end_date', None)
        available_until_out_of_stock = request.POST.get('available_until_out_of_stock') == 'on'  # assuming it's a checkbox
        raw_stock_count = request.POST.get('stock_count', '9999')
        stock_count = int(raw_stock_count) if raw_stock_count.strip() else 9999

        #JS
        required_fields = ['nazov_produktu', 'info_produktu', 'amount', 'unit', 'price', 'currency', 'transport_type']
        missing_fields = [field for field in required_fields if not request.POST.get(field)]
        if missing_fields:
            missing_fields_str = ', '.join(missing_fields)
            return HttpResponseBadRequest(f"Missing required fields: {missing_fields_str}.")

        # Check file extension
        if image_file and not any([image_file.name.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif']]):
            return HttpResponseBadRequest("Invalid file extension.")

        # Validate the content type
        valid_content_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif']
        if image_file and image_file.content_type not in valid_content_types:
            return HttpResponseBadRequest("Unsupported file type.")

        # Use Pillow to check if it's a valid image
        if image_file and not is_valid_image(image_file):
            return HttpResponseBadRequest("Invalid image file.")
        
        if not (nazov_produktu and amount and unit and price and currency and info_produktu and transport_type):
            return HttpResponseBadRequest("Missing required fields.")
        
        existing_product = Polozka.objects.filter(user_profile=user_profile, nazov_produktu=nazov_produktu).exists()
        if existing_product:
            return HttpResponseBadRequest("A product with the same name already exists for this user.")
        
        product = Polozka.objects.create(
            user_profile=user_profile,
            nazov_produktu=nazov_produktu,
            info_nazov_produktu=info_nazov_produktu,
            info_produktu=info_produktu,
            image=image_file,
        )
        cena = Cena.objects.create(
            user_profile=user_profile, 
            polozka=product,
            amount=amount,
            unit=unit,
            price=price,
            currency=currency
        )
        # Create the Availability instance
        if availability_start_date or availability_end_date or available_until_out_of_stock or stock_count:
            availability = Availability.objects.create(
                user_profile=user_profile,
                polozka=product,
                availability_start_date=availability_start_date if availability_start_date else None,
                availability_end_date=availability_end_date if availability_end_date else None,
                available_until_out_of_stock=available_until_out_of_stock,
                stock_count=stock_count
            )
        # Check if the necessary transport fields are filled
        create_transport_loc = transport_type and transport_price and transport_unit and transport_amount and transport_currency

        if create_transport_loc:
            existing_transport_loc = TransportLoc.objects.filter(
                user_profile=user_profile,
                polozka=product,
                transport_type=transport_type,
                price=transport_price,
                unit=transport_unit,
                amount=transport_amount,
                currency=transport_currency,
                transport_notes=transport_notes
            ).first()

            if existing_transport_loc:
                # If an existing transport with the same parameters is found, use it
                transport_loc = existing_transport_loc
            else:
                # If not, create a new transport instance
                transport_loc = TransportLoc.objects.create(
                    user_profile=user_profile,
                    polozka=product,
                    transport_type=transport_type,
                    transport_notes=transport_notes,
                    price=transport_price,
                    currency=transport_currency,
                    amount=transport_amount,
                    unit=transport_unit,
                    position=transportloc_list.count() + 1
                )
        # Associating checked transports (from the Transport model) with the new Polozka
        selected_transports = request.POST.getlist('transport_selected') # Get all checked Transport IDs
        if not selected_transports and not create_transport_loc:
            return HttpResponseBadRequest("No transport for the product was selected/added, and the product was created without any transport info.")

        for transport_id in selected_transports:
            transport = get_object_or_404(Transport, id=transport_id, user_profile=user_profile)
            # Assuming you have a model or relationship to link Polozka with Transport
            # Modify this line as per your model structure
            PolozkaTransport.objects.create(polozka=product, transport=transport)

        return redirect('add_product_main:user_zobraz_polozku', username=username, nazov_produktu=nazov_produktu)  
    else:
        return render(request, 'polozka_pridanie.html', context)

@login_required
def pridaj_dopravu(request, username):
    user_profile = get_object_or_404(UserProfile, user__username=username)
    transport_list = Transport.objects.filter(user_profile=user_profile)

    context = {
        'username': username,
        'user_profile': user_profile,
        'transport_list': transport_list,
    }

    if request.user != user_profile.user:
        return render(request, 'access_denied.html')

    if request.method == 'POST':
        transport_type = request.POST.get('transport_type', None)
        price = request.POST.get('transport_price', None)  # use get method
        currency = request.POST.get('currency', None)      # use get method
        amount = request.POST.get('transport_amount', None)  # use get method
        unit = request.POST.get('unit', None)              # use get method
        transport_notes = request.POST.get('transport_notes', '')

        # Check if price and amount are set by the user
        if not price or not amount:
            messages.warning(request, "Please set both price and amount.")
            return render(request, 'doprava_pridanie.html', context)

        # Check for duplicates
        duplicate_transport = Transport.objects.filter(
            user_profile=user_profile,
            transport_type=transport_type,
            price=price,
            currency=currency,
            amount=amount,
            unit=unit
        ).exists()

        if duplicate_transport:
            messages.warning(request, "This transport configuration already exists.")
            return render(request, 'doprava_pridanie.html', context)

        # If everything's fine, add the transport
        position = transport_list.count() + 1
        Transport.objects.create(
            user_profile=user_profile,
            transport_type=transport_type,
            transport_notes=transport_notes,
            price=price,
            currency=currency,
            amount=amount,
            unit=unit,
            position=position
        )

        return redirect('add_product_main:user_pridaj_dopravu', username=username)

    else:
        # Handle the GET request and render the form
        return render(request, 'doprava_pridanie.html', context)

@login_required
def delete_transport_loc(request, username, transportloc_id):
    user_profile = get_object_or_404(UserProfile, user__username=username)
    transport_loc = get_object_or_404(TransportLoc, id=transportloc_id, user_profile=user_profile)

    # Save the referring URL
    referer_url = request.META.get('HTTP_REFERER', None)

    if request.user == user_profile.user:
        transport_loc.delete()

    if referer_url:
        return HttpResponseRedirect(referer_url)
    else:
        return redirect('add_product_main:user_pridaj_dopravu', username=username)

@login_required
def delete_transport(request, username, transport_id):
    user_profile = get_object_or_404(UserProfile, user__username=username)
    transport = get_object_or_404(Transport, id=transport_id, user_profile=user_profile)

    if request.user == user_profile.user:
        transport.delete()

    return redirect('add_product_main:user_pridaj_dopravu', username=username)
    
@login_required
def select_transport(request, username, nazov_produktu, transport_id):
    user_profile = get_object_or_404(UserProfile, user__username=username)
    transport = get_object_or_404(Transport, id=transport_id)
    polozka = get_object_or_404(Polozka, nazov_produktu=nazov_produktu)

    if request.user == user_profile.user:
        PolozkaTransport.objects.create(polozka=polozka, transport=transport)

    return redirect('add_product_main:user_zobraz_polozku', username=username, nazov_produktu=nazov_produktu)
    
@login_required
def deselect_transport(request, username, nazov_produktu, transport_id):
    user_profile = get_object_or_404(UserProfile, user__username=username)
    polozka = get_object_or_404(Polozka, nazov_produktu=nazov_produktu)
    transport = get_object_or_404(Transport, id=transport_id)

    # Check if the user is the owner of the product (Polozka)
    if request.user == user_profile.user:
        try:
            # Try to get the PolozkaTransport object with the given product and transport
            polozka_transport = PolozkaTransport.objects.get(polozka=polozka, transport=transport)
            # If the object exists, delete it to de-associate the transport from the product
            polozka_transport.delete()
        except PolozkaTransport.DoesNotExist:
            # If the PolozkaTransport object does not exist, do nothing or handle the error as needed.
            pass

    # Redirect the user to a different view after de-associating the transport option
    return redirect('add_product_main:user_zobraz_polozku', username=username, nazov_produktu=nazov_produktu)
    
def delete_picture(request, username, product_id):
    product = get_object_or_404(Polozka, id=product_id, user_profile__user__username=username)

    if request.user != product.user_profile.user:
        return HttpResponseForbidden()

    # Delete the picture from the database
    product.image.delete(save=True)

    return redirect('add_product_main:user_zobraz_polozku', username=username, nazov_produktu=product.nazov_produktu)

def add_picture(request, username, nazov_produktu):
    # Get the Polozka object
    polozka = Polozka.objects.get(user_profile__user__username=username, nazov_produktu=nazov_produktu)

    if request.method == 'POST':
        form = PictureForm(request.POST, request.FILES)
        if form.is_valid():
            # Get the uploaded image from the form
            image = form.cleaned_data['image']

            # Check content type for added security
            valid_content_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif']
            if image.content_type not in valid_content_types:
                form.add_error('image', 'Unsupported file type.')
                return render(request, 'add_picture.html', {'form': form, 'polozka': polozka})

            # Use Pillow to check if it's a valid image
            if not is_valid_image(image):
                form.add_error('image', 'Invalid image file.')
                return render(request, 'add_picture.html', {'form': form, 'polozka': polozka})

            # Save the image to the Polozka object
            polozka.image = image
            polozka.save()

            # Redirect to the view that displays the Polozka details
            return redirect('add_product_main:user_zobraz_polozku', username=username, nazov_produktu=nazov_produktu)
    else:
        form = PictureForm()

    return render(request, 'add_picture.html', {'form': form, 'polozka': polozka})

@login_required
def delete_cena(request, username, nazov_produktu, cena_id):
    user_profile = get_object_or_404(UserProfile, user__username=username)
    cena = get_object_or_404(Cena, id=cena_id, polozka__user_profile=user_profile)

    if request.user == user_profile.user:
        cena.delete()

    return redirect('add_product_main:user_zobraz_polozku', username=username, nazov_produktu=cena.polozka.nazov_produktu)

def zobraz_polozku(request, username, nazov_produktu, anchor=None):
    user_profile = get_object_or_404(UserProfile, user__username=username)
    #user = get_object_or_404(User, username=username)
    polozka = get_object_or_404(Polozka, user_profile=user_profile, nazov_produktu=nazov_produktu)  
    if polozka and polozka.image:
        image_url = polozka.image.url
    else:
        image_url = None
    filename = os.path.basename(polozka.image.name) if polozka.image else None

    is_owner = False  # Initialize is_owner to False by default

    if request.user.is_authenticated and request.user == user_profile.user:
        is_owner = True  # Set is_owner to True if the current user is the owner of the Polozka

    if username != polozka.user_profile.user.username:
        polozka = None
        return HttpResponseBadRequest("Polozka tohto pouzivatela neexistuje.")
    
    polozka_transport_list = []
    filtered_transport_list = []
    if polozka:
        polozka_transportloc_list = polozka.transportloc_set.all()
    else:
        polozka_transportloc_list = []
        
    if polozka:
        # Query the TransportLoc objects related to the Polozka
        polozka_transportloc_list = polozka.transportloc_set.all()
        # Retrieve the associated transports for the polozka
        #polozka_transport_list = polozka.polozkatransport_set.filter(transport__user_profile__user=request.user)
        polozka_transport_list = polozka.polozkatransport_set.all()

        # Filter the transport options that are already displayed
        displayed_transport_list = [polozka_transport.transport for polozka_transport in polozka_transport_list]

        # Filter the global transport options to exclude the ones already displayed
        filtered_transport_list = Transport.objects.exclude(id__in=[transport.id for transport in displayed_transport_list])
        filtered_transportloc_list = TransportLoc.objects.exclude(id__in=[transportloc.id for transportloc in polozka_transportloc_list])

        # Get the main image URL if it exists
        #if polozka.additional_images.exists():
        #    additional_image = polozka.additional_images.first()
        #    image_url = additional_image.image.url
        

    cena_id = request.session.get('cena_id')

    if 'amount' in request.method == 'POST':
        if 'delete_picture' in request.POST and is_owner:
            # Delete the picture from the database
            if polozka.image:
                polozka.image.delete(save=True)
            # Redirect back to the same view after successful deletion
            return redirect('add_product_main:user_zobraz_polozku', username=username, nazov_produktu=nazov_produktu)

        elif 'delete_cena' in request.POST:
            cena_id = request.POST['delete_cena']
            cena = get_object_or_404(Cena, id=cena_id)
            cena.delete()
        else:
            amount = request.POST['amount']
            unit = request.POST['unit']
            price = request.POST['price']
            currency = request.POST['currency']

            cena = Cena.objects.create(
                user_profile=polozka.user_profile,
                polozka=polozka,
                amount=amount,
                unit=unit,
                price=price,
                currency=currency
            )

        return redirect('add_product_main:user_zobraz_polozku', username=username, nazov_produktu=nazov_produktu)
    
    chat_messages = []
    ceny = []

    if polozka:
        ceny = Cena.objects.filter(polozka=polozka)
        # Retrieve chat_messages for the polozka
        chat_messages = polozka.chat_messages.order_by('created_at') 

        if request.user.is_authenticated:
            is_owner = request.user == user_profile.user

            if is_owner:
                # Filter chat messages for each sender separately
                unique_senders = chat_messages.values_list('sender', flat=True).distinct()
                filtered_messages = []
                for sender in unique_senders:
                    sender_messages = chat_messages.filter(sender=sender)
                    filtered_messages.append(sender_messages.latest('created_at'))
                chat_messages = filtered_messages
            else:
                # Filter chat messages for the logged-in user
                chat_messages = chat_messages.filter(sender=request.user)

    context = {
        'username': username,
        'polozka': polozka,
        'user_profile': polozka.user_profile if polozka else None,
        'info_nazov_produktu': polozka.info_nazov_produktu if polozka else None,
        'info_produktu': polozka.info_produktu if polozka else None,
        'nazov_produktu': nazov_produktu,
        'chat_messages': chat_messages,
        'anchor': anchor,
        'ceny': ceny,
        'polozka_transport_list': polozka_transport_list,
        'filtered_transport_list': filtered_transport_list,
        'polozka_transportloc_list': polozka_transportloc_list,
        'image_url': image_url,
        'filename': filename,
        'is_owner': is_owner,
    }

    return render(request, 'polozka_zobrazenie.html', context)

