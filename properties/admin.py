from django.contrib import admin
from .models import (
    Property,
    PropertyImage,
    PropertyAmenity,
    PropertyHighlight,
    PropertyNearby,
    PropertyLegalInfo,
    Inquiry,
    VideoViewingRequest
)


# ==========================
# Inlines
# ==========================

class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1


class PropertyAmenityInline(admin.TabularInline):
    model = PropertyAmenity
    extra = 1


class PropertyHighlightInline(admin.TabularInline):
    model = PropertyHighlight
    extra = 1


class PropertyNearbyInline(admin.TabularInline):
    model = PropertyNearby
    extra = 1


class PropertyLegalInfoInline(admin.TabularInline):
    model = PropertyLegalInfo
    extra = 1


# ==========================
# Property Admin
# ==========================

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'property_type',
        'location',
        'price',
        'featured',
        'verified',
        'status'
    )

    list_filter = (
        'property_type',
        'status',
        'featured',
        'verified'
    )

    search_fields = (
        'title',
        'location'
    )

    prepopulated_fields = {
        'slug': ('title',)
    }

    inlines = [
        PropertyImageInline,
        PropertyAmenityInline,
        PropertyHighlightInline,
        PropertyNearbyInline,
        PropertyLegalInfoInline
    ]


# ==========================
# Inquiry Admin
# ==========================

@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'phone',
        'email',
        'property',
        'created_at'
    )

    search_fields = (
        'name',
        'phone',
        'email'
    )

    readonly_fields = (
        'created_at',
    )


# Optional standalone registration
admin.site.register(PropertyImage)
admin.site.register(PropertyAmenity)
admin.site.register(PropertyHighlight)
admin.site.register(PropertyNearby)
admin.site.register(PropertyLegalInfo)
admin.site.register(VideoViewingRequest)

