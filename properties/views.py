from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Inquiry, Property, PropertyAmenity, PropertyHighlight, PropertyImage, PropertyLegalInfo, PropertyNearby, VideoViewingRequest
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout

def home(request):
    properties = Property.objects.filter(status='available').prefetch_related('amenities').order_by('-created_at')

    context = {
        'property_type_choices': Property.PROPERTY_TYPES,
        'region_choices': Property.REGION,
        'construction_choices': Property.CONSTRUCTION,
        'properties': properties,
    }

    return render(request,'properties/home.html',context)

def property_detail(request, slug):

    property = get_object_or_404(Property.objects.prefetch_related('gallery','amenities','highlights','nearby_places','legal_info'),slug=slug)

    context = {
        'property': property
    }

    return render(request,'properties/property_detail.html',context)

@login_required(login_url='login')
def dashboard(request):
    total_listings = Property.objects.count()

    active_listings = Property.objects.filter(status='available').count()

    total_enquiries = Inquiry.objects.count()

    total_videoenquiries = VideoViewingRequest.objects.count()

    recent_properties = Property.objects.order_by("-created_at")[:5]

    recent_enquiries = Inquiry.objects.order_by("-created_at")[:5]

    region_stats = Property.objects.values('region').annotate(total=Count('id')).order_by('-total')

    context = {
        "total_listings": total_listings,
        "active_listings": active_listings,
        "total_enquiries": total_enquiries,
        "total_videoenquiries": total_videoenquiries,
        "recent_properties": recent_properties,
        "recent_enquiries": recent_enquiries,
        "region_stats": region_stats,
    }
    return render(request,"dashboard/dashboard.html", context)

@login_required(login_url='login')
def property_manage(request):
    total_properties = Property.objects.all()

    total_listings = Property.objects.count()

    context = {
        "total_properties": total_properties,
        "total_listings": total_listings,
        'status_choices': Property.STATUS,
        'region_choices': Property.REGION,
        'property_type_choices': Property.PROPERTY_TYPES,
    }
    return render(request,"dashboard/property_manage.html", context)

@login_required(login_url='login')
def enquiry_list(request):
    
    total_enquiries = Inquiry.objects.all().order_by('-created_at')

    context = {
        "total_enquiries": total_enquiries,
    }

    return render(request,"dashboard/enquiry_list.html", context)

@login_required(login_url='login')
def enquiry_detail(request, pk):

    enquiry = get_object_or_404(Inquiry.objects.select_related('property'),pk=pk)

    context = {
        'enquiry': enquiry,
    }

    return render(request,"dashboard/enquiry_detail.html", context)

@login_required(login_url='login')
def enquiry_delete(request, pk):
    """Delete a single enquiry and return to list."""
    enquiry = get_object_or_404(Inquiry, pk=pk)
    name    = enquiry.name
    enquiry.delete()
    messages.success(request, f'Enquiry from "{name}" deleted.')
    return redirect('enquiry_list')

@login_required(login_url='login')
def property_add(request):

    if request.method == "POST":

        title = request.POST.get("title")

        slug = slugify(title)

        # Prevent duplicate slugs
        original_slug = slug
        counter = 1

        while Property.objects.filter(slug=slug).exists():
            slug = f"{original_slug}-{counter}"
            counter += 1

        property_obj = Property.objects.create(

            title=title,
            slug=slug,

            property_type=request.POST.get("property_type"),
            status=request.POST.get("status"),

            rera_number=request.POST.get("rera_number"),

            region=request.POST.get("region"),
            location=request.POST.get("location"),

            pincode=request.POST.get("pincode"),
            full_address=request.POST.get("full_address"),

            short_description=request.POST.get("short_description"),
            description=request.POST.get("description"),

            price=request.POST.get("price") or 0,
            price_label=request.POST.get("price_label"),

            bedrooms=request.POST.get("bedrooms") or 0,
            bathrooms=request.POST.get("bathrooms") or 0,

            builtup_area=request.POST.get("builtup_area") or 0,
            area_sqft=request.POST.get("area_sqft") or 0,

            furnishing_status=request.POST.get("furnishing_status"),
            construction_status=request.POST.get("construction_status"),

            year_built=request.POST.get("year_built") or None,

            parking_spaces=request.POST.get("parking_spaces") or 0,

            badge=request.POST.get("badge"),

            featured=bool(request.POST.get("featured")),
            verified=bool(request.POST.get("verified")),

            featured_image=request.FILES.get("featured_image"),

            # youtube_video=request.POST.get("youtube_video"),
            # virtual_tour_url=request.POST.get("virtual_tour_url"),

            brochure_pdf=request.FILES.get("brochure_pdf"),

            google_map_url=request.POST.get("google_map_url"),

            latitude=request.POST.get("latitude") or None,
            longitude=request.POST.get("longitude") or None,
        )

        # =====================================
        # SAVE AMENITIES
        # =====================================

        amenity_icons = request.POST.getlist("amenity_icon[]")
        amenity_names = request.POST.getlist("amenity_name[]")

        for icon, name in zip(amenity_icons, amenity_names):

            if name.strip():

                PropertyAmenity.objects.create(property=property_obj,icon=icon,name=name)

        # =====================================
        # SAVE HIGHLIGHTS
        # =====================================

        highlight_icons = request.POST.getlist("highlight_icon[]")
        highlight_titles = request.POST.getlist("highlight_title[]")
        highlight_descs = request.POST.getlist("highlight_desc[]")

        for icon, title, desc in zip(
            highlight_icons,
            highlight_titles,
            highlight_descs
        ):

            if title.strip():

                PropertyHighlight.objects.create(property=property_obj,icon=icon,title=title,description=desc)

        # =====================================
        # SAVE NEARBY PLACES
        # =====================================

        nearby_icons = request.POST.getlist("nearby_icon[]")
        nearby_names = request.POST.getlist("nearby_name[]")
        nearby_distances = request.POST.getlist("nearby_distance[]")
        nearby_descs = request.POST.getlist("nearby_desc[]")

        for icon, name, distance, desc in zip(
            nearby_icons,
            nearby_names,
            nearby_distances,
            nearby_descs
        ):

            if name.strip():

                PropertyNearby.objects.create(property=property_obj,icon=icon,place_name=name,distance=distance,short_description=desc)

        # =====================================
        # SAVE LEGAL INFORMATION
        # =====================================

        legal_icons = request.POST.getlist("legal_icon[]")
        legal_titles = request.POST.getlist("legal_title[]")
        legal_descs = request.POST.getlist("legal_desc[]")
        legal_statuses = request.POST.getlist("legal_status[]")

        for icon, title, desc, status in zip(
            legal_icons,
            legal_titles,
            legal_descs,
            legal_statuses
        ):

            if title.strip():

                PropertyLegalInfo.objects.create(property=property_obj,icon=icon,title=title,description=desc,status=status)

        # =====================================
        # SAVE GALLERY IMAGES
        # =====================================

        gallery_images = request.FILES.getlist("gallery_images")

        for image in gallery_images:

            PropertyImage.objects.create(property=property_obj,gallery_images=image)

        return redirect("property_manage")

    context = {
        'status_choices': Property.STATUS,
        'region_choices': Property.REGION,
        'property_type_choices': Property.PROPERTY_TYPES,
        'furnish_status': Property.FURNISHING,
        'construction_status': Property.CONSTRUCTION,
        'nearby_icons': PropertyNearby.ICON_CHOICES,
        'amenity_icons': PropertyAmenity.ICON_CHOICES,
        'key_highlight_icons': PropertyHighlight.ICON_CHOICES,
        'legal_icons': PropertyLegalInfo.ICON_CHOICES,
        'legal_status': PropertyLegalInfo.STATUS_CHOICES,
    }

    return render(request,"dashboard/property_form.html",context)

@login_required(login_url='login')
def property_edit(request, pk):
    
    property_obj = get_object_or_404(Property, pk=pk)

    if request.method == "POST":
        property_obj.title = request.POST.get("title") 
        property_obj.property_type = request.POST.get("property_type") 
        property_obj.status = request.POST.get("status") 
        property_obj.region = request.POST.get("region") 
        property_obj.badge = request.POST.get("badge"),
        property_obj.location = request.POST.get("location") 
        property_obj.pincode = request.POST.get("pincode") 
        property_obj.full_address = request.POST.get("full_address") 
        property_obj.short_description = request.POST.get("short_description") 
        property_obj.description = request.POST.get("description") 
        property_obj.price = request.POST.get("price") or 0 
        property_obj.price_label = request.POST.get("price_label") 
        property_obj.bedrooms = request.POST.get("bedrooms") or 0 
        property_obj.bathrooms = request.POST.get("bathrooms") or 0 
        property_obj.builtup_area = request.POST.get("builtup_area") or 0 
        property_obj.area_sqft = request.POST.get("area_sqft") or 0 
        property_obj.furnishing_status = request.POST.get("furnishing_status") 
        property_obj.construction_status = request.POST.get("construction_status") 
        property_obj.year_built = request.POST.get("year_built") or None 
        property_obj.parking_spaces = request.POST.get("parking_spaces") or 0 
        property_obj.badge = request.POST.get("badge") 
        property_obj.featured = bool(request.POST.get("featured")) 
        property_obj.verified = bool(request.POST.get("verified")) 
        # property_obj.youtube_video = request.POST.get("youtube_video") 
        # property_obj.virtual_tour_url = request.POST.get("virtual_tour_url") 
        property_obj.google_map_url = request.POST.get("google_map_url") 
        property_obj.latitude = request.POST.get("latitude") or None 
        property_obj.longitude = request.POST.get("longitude") or None 
        
        # Replace Featured Image only if new image uploaded 
        
        if request.FILES.get("featured_image"): 
            property_obj.featured_image = request.FILES.get( "featured_image" )

        property_obj.save() 
            
        # Replace Brochure only if uploaded 
        
        if request.FILES.get("brochure_pdf"): 
            property_obj.brochure_pdf = request.FILES.get( "brochure_pdf" ) 
            property_obj.save() 
            
        # ---------------------------------- # DELETE OLD RELATED RECORDS # ---------------------------------- 
        
        property_obj.amenities.all().delete() 
        property_obj.highlights.all().delete() 
        property_obj.nearby_places.all().delete() 
        property_obj.legal_info.all().delete() 
        
        # ---------------------------------- # SAVE AMENITIES AGAIN # ---------------------------------- 
        
        amenity_icons = request.POST.getlist( "amenity_icon[]" ) 
        amenity_names = request.POST.getlist( "amenity_name[]" ) 

        for icon, name in zip( amenity_icons, amenity_names ): 
            if name.strip(): 
                PropertyAmenity.objects.create( property=property_obj, icon=icon, name=name ) 
                
        # ---------------------------------- # SAVE HIGHLIGHTS AGAIN # ---------------------------------- 
        
        highlight_icons = request.POST.getlist( "highlight_icon[]" ) 
        highlight_titles = request.POST.getlist( "highlight_title[]" ) 
        highlight_descs = request.POST.getlist( "highlight_desc[]" ) 

        for icon, title, desc in zip( highlight_icons, highlight_titles, highlight_descs ): 
            if title.strip(): 
                PropertyHighlight.objects.create( property=property_obj, icon=icon, title=title, description=desc ) 
            
        # ---------------------------------- # SAVE NEARBY AGAIN # ---------------------------------- 
        
        nearby_icons = request.POST.getlist( "nearby_icon[]" ) 
        nearby_names = request.POST.getlist( "nearby_name[]" ) 
        nearby_distances = request.POST.getlist( "nearby_distance[]" ) 
        nearby_descs = request.POST.getlist( "nearby_desc[]" ) 
        for icon, name, distance, desc in zip( nearby_icons, nearby_names, nearby_distances, nearby_descs ): 
            if name.strip(): 
                PropertyNearby.objects.create( property=property_obj, icon=icon, place_name=name, distance=distance, short_description=desc ) 
                
        # ---------------------------------- # SAVE LEGAL INFO AGAIN # ---------------------------------- 
        
        legal_icons = request.POST.getlist( "legal_icon[]" ) 
        legal_titles = request.POST.getlist( "legal_title[]" ) 
        legal_descs = request.POST.getlist( "legal_desc[]" ) 
        legal_statuses = request.POST.getlist( "legal_status[]" ) 
        for icon, title, desc, status in zip( legal_icons, legal_titles, legal_descs, legal_statuses ): 
            if title.strip(): 
                PropertyLegalInfo.objects.create( property=property_obj, icon=icon, title=title, description=desc, status=status ) 
            
        # ---------------------------------- # ADD NEW GALLERY IMAGES # ---------------------------------- 
            
        gallery_images = request.FILES.getlist( "gallery_images" ) 
        
        for image in gallery_images: 
            PropertyImage.objects.create( property=property_obj, gallery_images=image )
             
        return redirect( "property_manage" ) 
    
    context = { 
        'property': property_obj, 
        'status_choices': Property.STATUS, 
        'region_choices': Property.REGION, 
        'property_type_choices': Property.PROPERTY_TYPES, 
        'furnish_status': Property.FURNISHING, 
        'construction_status': Property.CONSTRUCTION, 
        'nearby_icons': PropertyNearby.ICON_CHOICES, 
        'amenity_icons': PropertyAmenity.ICON_CHOICES, 
        'key_highlight_icons': PropertyHighlight.ICON_CHOICES, 
        'legal_icons': PropertyLegalInfo.ICON_CHOICES, 
        'legal_status': PropertyLegalInfo.STATUS_CHOICES, 
        } 
    
    return render( request, "dashboard/property_form.html", context )

@login_required(login_url='login')
def image_delete(request, pk):

    image = get_object_or_404(PropertyImage,pk=pk)

    property_id = image.property.id

    # Delete physical file from media folder
    if image.gallery_images:
        image.gallery_images.delete(save=False)

    # Delete database record
    image.delete()

    return redirect('property_edit',pk=property_id)

@login_required(login_url='login')
def property_delete(request, pk):

    property_obj = get_object_or_404(Property, pk=pk)

    property_obj.delete()

    return redirect('property_manage')

@login_required(login_url='login')
def submit_enquiry(request):

    if request.method == "POST":

        property_obj = None

        property_id = request.POST.get('property_id')

        if property_id:
            property_obj = Property.objects.get(id=property_id)

        lead = Inquiry.objects.create(

            name=request.POST.get('name'),

            phone=request.POST.get('phone'),

            email=request.POST.get('email'),

            property=property_obj,

            view_type=request.POST.get('viewing_type'),

            message=request.POST.get('message')

        )

        send_mail(
            subject='New GoaNest Lead',

            message=f"""
            New enquiry received

            Name: {lead.name}
            Phone: {lead.phone}
            Email: {lead.email}

            Property: {lead.property.title if lead.property else 'Any Property'}

            Viewing Type: {lead.view_type}

            Message: {lead.message} """,

            from_email=None,

            recipient_list=[
                'devwithsagar@gmail.com'
            ],

            fail_silently=False
        )


        return JsonResponse({
            'success': True
        })

    return JsonResponse({
        'success': False
    })

@login_required(login_url='login')
def submit_video_viewing(request):

    if request.method == "POST":

        property_obj = Property.objects.get(id=request.POST.get('property_id'))

        booking = VideoViewingRequest.objects.create(

            property=property_obj,

            name=request.POST.get('name'),

            phone=request.POST.get('phone'),

            preferred_date=request.POST.get('preferred_date'),

            preferred_time=request.POST.get('preferred_time'),

            platform=request.POST.get('platform')

        )

        send_mail(
            subject=
            'New Video Viewing Request',

            message=f"""
                Property: {property_obj.title}

                Name: {booking.name}

                Phone: {booking.phone}

                Date: {booking.preferred_date}

                Time: {booking.preferred_time}

                Platform: {booking.platform} """,

            from_email=None,

            recipient_list=[
                'devwithsagar@gmail.com'
            ],

            fail_silently=False
        )

        return JsonResponse({
            'success': True
        })

    return JsonResponse({
        'success': False
    })

@login_required(login_url='login')
def videoviewing_list(request):
    
    total_enquiries = VideoViewingRequest.objects.all().order_by('-created_at')

    context = {
        "total_enquiries": total_enquiries,
    }

    return render(request,"dashboard/videoviewing_list.html", context)

@login_required(login_url='login')
def video_enquiry_delete(request, pk):
    """Delete a single enquiry and return to list."""
    video_enquiry = get_object_or_404(VideoViewingRequest, pk=pk)
    name    = video_enquiry.name
    video_enquiry.delete()
    messages.success(request, f'Enquiry from "{name}" deleted.')
    return redirect('videoviewing_list')

def login_view(request):

    # Already logged in
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:
            login(request, user)
            return redirect('dashboard')
        
        messages.error(
            request,
            "Incorrect username or password. Please try again."
        )

    return render(request,'dashboard/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')