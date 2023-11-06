from django.contrib import admin
from add_product_main.models import Polozka
from add_product_main.models import Transport
from add_product_main.models import TransportLoc
from add_product_main.models import PolozkaTransport
from add_product_main.models import AdditionalImage
from django.utils.safestring import mark_safe


#class TransportInline(admin.TabularInline):
#    model = PolozkaTransport
#    extra = 0

class AdditionalImageInline(admin.TabularInline):
    model = AdditionalImage
    extra = 0

class TransportLocInline(admin.TabularInline):
    model = TransportLoc
    extra = 0

class PolozkaTransportInline(admin.TabularInline):
    model = PolozkaTransport
    extra = 0

class TransportAdmin(admin.ModelAdmin):
    list_display = ('transport_name', 'user_profile')
    search_fields = ('user_profile__user__username', 'transport_name')

    def get_username(self, obj):
        return obj.user_profile.user.username

    get_username.short_description = 'Username'

class TransportLocAdmin(admin.ModelAdmin):
    list_display = ('transport_name', 'user_profile', 'transport_type', 'price', 'currency')
    search_fields = ('transport_name', 'user_profile__user__username')

    def get_username(self, obj):
        return obj.user_profile.user.username

    get_username.short_description = 'Username'

# Registering the TransportLoc model
admin.site.register(TransportLoc, TransportLocAdmin)

class PolozkaAdmin(admin.ModelAdmin):
    list_display = ('nazov_produktu', 'user_profile', 'get_transport_names', 'get_transport_locs', 'display_main_image','display_additional_images')
    search_fields = ('nazov_produktu', 'user_profile__user__username')
    inlines = [PolozkaTransportInline, AdditionalImageInline]
    readonly_fields = ('display_main_image','display_additional_images')

    def get_transport_names(self, obj):
        transport_names = obj.polozkatransport_set.values_list('transport__transport_name', flat=True)
        return ', '.join(transport_names)

    get_transport_names.short_description = 'Transport Names'

    def get_transport_locs(self, obj):
        transport_locs = TransportLoc.objects.filter(polozka=obj).values_list('transport_name', flat=True)
        return ', '.join(transport_locs)

    get_transport_locs.short_description = 'TransportLoc Names'

    def display_main_image(self, obj):
        # Retrieve the main image associated with the Polozka object
        main_image = obj.image
        if main_image and main_image.name:
            return main_image.name
        return 'No image available'

    display_main_image.short_description = 'Main Image'

    def display_additional_images(self, obj):
        # Retrieve the first AdditionalImage associated with the Polozka object
        additional_image = obj.additional_images.first()
        if additional_image and additional_image.image:
            return additional_image.image.name
        return 'No image available'

    display_additional_images.short_description = 'AdditionalImages Image'

    def created_by(self, obj):
        return obj.user_profile.user.username

    created_by.admin_order_field = 'user_profile__user__username'  # Enable sorting by user_profile


admin.site.register(Transport, TransportAdmin)
admin.site.register(Polozka, PolozkaAdmin)
