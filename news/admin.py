from django.contrib import admin
from django.utils.safestring import mark_safe
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import News, Category


class NewsAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = News
        fields = '__all__'


class NewsAdmin(admin.ModelAdmin):
    form = NewsAdminForm
    list_display = ('id', 'title', 'created_at', 'category', 'update_at', 'is_published', 'get_photo')
    list_display_links = ('title', 'id')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'category')
    fields = ('title', 'category', 'content', 'photo', 'get_photo', 'views', 'created_at', 'update_at')
    readonly_fields = ('get_photo', 'views', 'created_at', 'update_at')

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{ obj.photo.url }" width="80">')

    get_photo.short_description = 'Фото'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)


admin.site.register(News, NewsAdmin)
admin.site.register(Category, CategoryAdmin)

admin.site.site_title = 'Админка'
admin.site.site_header = 'Админка'
