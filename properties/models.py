from django.db import models


class Property(models.Model):

    PROPERTY_TYPES = [
        ('villa', 'Villa'),
        ('apartment', 'Apartment'),
        ('plot', 'Plot'),
        ('commercial', 'Commercial'),
    ]

    STATUS = [
        ('available', 'Available'),
        ('sold', 'Sold'),
        ('reserved', 'Reserved'),
    ]

    FURNISHING = [
        ('fully', 'Fully Furnished'),
        ('semi', 'Semi Furnished'),
        ('unfurnished', 'Unfurnished'),
    ]

    CONSTRUCTION = [
        ('ready', 'Ready To Move'),
        ('under_construction', 'Under Construction'),
        ('new_launch', 'New Launch'),
    ]

    REGION = [
        ('north goa', 'North Goa'),
        ('south goa', 'South Goa'),
        ('kushavati', 'Kushavati')
    ]

    title = models.CharField(max_length=255)

    slug = models.SlugField(unique=True)

    property_type = models.CharField(max_length=30,choices=PROPERTY_TYPES)

    rera_number = models.CharField(max_length=50)

    status = models.CharField(max_length=20,choices=STATUS,default='available')

    region = models.CharField(max_length=30, choices=REGION)

    location = models.CharField(max_length=200)

    pincode = models.CharField(max_length=10)

    full_address = models.TextField("Full Address", help_text="Enter your complete address")

    short_description = models.TextField()

    description = models.TextField()

    price = models.DecimalField(max_digits=15,decimal_places=2)

    price_label = models.CharField(max_length=20)

    bedrooms = models.PositiveIntegerField(default=0)

    bathrooms = models.PositiveIntegerField(default=0)

    builtup_area = models.PositiveIntegerField()

    area_sqft = models.PositiveIntegerField()

    furnishing_status = models.CharField(max_length=20,choices=FURNISHING,blank=True)

    construction_status = models.CharField(max_length=30,choices=CONSTRUCTION,blank=True)

    year_built = models.PositiveIntegerField(null=True,blank=True)

    parking_spaces = models.PositiveIntegerField(default=0)

    badge = models.CharField(max_length=10)

    featured = models.BooleanField(default=False)

    verified = models.BooleanField(default=True)

    featured_image = models.ImageField(upload_to='properties/')

    youtube_video = models.URLField(blank=True)

    virtual_tour_url = models.URLField(blank=True)

    brochure_pdf = models.FileField(upload_to='brochures/',blank=True)

    google_map_url = models.URLField(blank=True)

    latitude = models.DecimalField(max_digits=10,decimal_places=7,null=True,blank=True)

    longitude = models.DecimalField(max_digits=10,decimal_places=7,null=True,blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class PropertyImage(models.Model):

    property = models.ForeignKey(Property,on_delete=models.CASCADE,related_name='gallery')

    gallery_images = models.ImageField(upload_to='properties/gallery/')

    sort_order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.property.title
    
class PropertyAmenity(models.Model):

    ICON_CHOICES = [
        ('♾️', 'Swimming Pool'),
        ('🌬️', 'Central AC'),
        ('📶', 'Wifi'),
        ('🏥', 'Hospital'),
        ('🛒', 'Shopping'),
        ('🌧️', 'Waterfall'),
        ('🚗', 'Parking'),
        ('🌿', 'Garden'),
        ('🚿', 'Shower'),
        ('🛁', 'Jacuzzi '),
        ('🌅', 'Sea-View '),
        ('🚿', 'TV'),
        ('💧', 'Water'),
        ('⚡', 'Backup'),
    ]

    property = models.ForeignKey(Property,on_delete=models.CASCADE,related_name='amenities')

    icon = models.CharField(max_length=20,choices=ICON_CHOICES)

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class PropertyHighlight(models.Model):

    ICON_CHOICES = [
        ('♾️', 'Swimming Pool'),
        ('🌬️', 'Central AC'),
        ('📶', 'Wifi'),
        ('🏥', 'Hospital'),
        ('🛒', 'Shopping'),
        ('🌧️', 'Waterfall'),
        ('🚗', 'Parking'),
        ('🌿', 'Garden'),
        ('🚿', 'Shower'),
        ('🛁', 'Jacuzzi '),
        ('🌅', 'Sea-View '),
        ('🚿', 'TV'),
        ('💧', 'Water'),
        ('⚡', 'Backup'),
        ('🏠', 'Home'),
        ('🔒', 'Secure'),
        ('☀️', 'Sun'),
        ('🏖️', 'Beach'),

    ]

    property = models.ForeignKey(Property,on_delete=models.CASCADE,related_name='highlights')

    icon = models.CharField(max_length=10,choices=ICON_CHOICES)

    title = models.CharField(max_length=255)

    description = models.TextField(blank=True)

    def __str__(self):
        return self.title
    
class PropertyNearby(models.Model):

    ICON_CHOICES = [
        ('🏖️', 'Beach'),
        ('🌊', 'Waterfront'),
        ('✈️', 'Airport'),
        ('🏥', 'Hospital'),
        ('🛒', 'Shopping'),
        ('🌧️', 'Waterfall'),
    ]

    property = models.ForeignKey(Property,on_delete=models.CASCADE,related_name='nearby_places')

    icon = models.CharField(max_length=10,choices=ICON_CHOICES)

    place_name = models.CharField(max_length=100)

    distance = models.CharField(max_length=20)

    short_description = models.CharField(max_length=50)

    def __str__(self):
        return self.place_name
    
class PropertyLegalInfo(models.Model):

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('approved', 'Approved'),
        ('verified', 'Verified'),
        ('clear', 'Clear'),
        ('available', 'Available'),
    ]

    ICON_CHOICES = [
        ('📄', 'Document'),
        ('🌊', 'Sea'),
        ('🔍', 'Glass'),
        ('🏛️', 'Building'),
        ('🏗️', 'Construction'),
        ('🌍', 'Earth'),
        ('🚗', 'Parking'),
    ]

    property = models.ForeignKey(Property,on_delete=models.CASCADE,related_name='legal_info')

    icon = models.CharField(max_length=10,choices=ICON_CHOICES)

    title = models.CharField(max_length=50)

    description = models.TextField(max_length=100)

    status = models.CharField(max_length=20,choices=STATUS_CHOICES)

    display_order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

class Inquiry(models.Model):

    property = models.ForeignKey(Property,on_delete=models.CASCADE,related_name='inquiries')

    name = models.CharField(max_length=100)

    phone = models.CharField(max_length=20)

    email = models.EmailField(blank=True)

    view_type = models.CharField(max_length=50)

    message = models.TextField(blank=True)

    is_contacted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class VideoViewingRequest(models.Model):

    PLATFORM_CHOICES = [
        ('WhatsApp Video', 'WhatsApp Video'),
        ('Google Meet', 'Google Meet'),
        ('Zoom', 'Zoom'),
        ('FaceTime', 'FaceTime'),
    ]

    property = models.ForeignKey(Property,on_delete=models.CASCADE,related_name='video_requests')

    name = models.CharField(max_length=150)

    phone = models.CharField(max_length=20)

    preferred_date = models.DateField()

    preferred_time = models.CharField(max_length=50)

    platform = models.CharField(max_length=50,choices=PLATFORM_CHOICES)

    status = models.CharField(max_length=20,default='Pending')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.property.title}"