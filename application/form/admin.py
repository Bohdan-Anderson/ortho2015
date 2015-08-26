from django.contrib import admin

from form.models import *

# class applicationAdmin(admin.ModelAdmin):

admin.site.register(Application)
admin.site.register(UploadedFile)