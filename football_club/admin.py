from django.contrib import admin
from .models import Club, Staff, Trophy, Stadium
from django.utils.safestring import mark_safe


class ClubAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ["preview"]

    def preview(self, obj):
        return mark_safe(f'<img src="{obj.logo.url}" style="max-height: 200px;">')
    preview.short_description = 'Image'



class StaffAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("second_name",)}
    readonly_fields = ["preview"]

    def preview(self, obj):
        return mark_safe(f'<img src="{obj.logo.url}" style="max-height: 200px;">')
    preview.short_description = 'Image'


class TrophyAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ["preview"]

    def preview(self, obj):
        return mark_safe(f'<img src="{obj.logo.url}" style="max-height: 200px;">')
    preview.short_description = 'Image'


class StadiumAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ["preview"]

    def preview(self, obj):
        return mark_safe(f'<img src="{obj.logo.url}" style="max-height: 200px;">')
    preview.short_description = 'Image'


# Register your models here.
admin.site.register(Club, ClubAdmin )
admin.site.register(Staff, StaffAdmin)
admin.site.register(Trophy, TrophyAdmin)
admin.site.register(Stadium, StadiumAdmin)