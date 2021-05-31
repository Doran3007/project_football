from django.contrib import admin
from .models import Club, Staff, Trophy, Stadium
from django.utils.safestring import mark_safe


class previewAdmin(admin.ModelAdmin):
    readonly_fields = ["preview"]

    def preview(self, obj):
        return mark_safe(f'<img src="{obj.logo.url}" style="max-height: 200px;">')
    preview.short_description = 'Image'


# Register your models here.
admin.site.register(Club, previewAdmin)
admin.site.register(Staff, previewAdmin)
admin.site.register(Trophy, previewAdmin)
admin.site.register(Stadium, previewAdmin)