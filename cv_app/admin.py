from django.contrib import admin
from .models import CV, LanguageEntry, Certificate, Experience, ExperienceDescription, Education, Skill, SkillCategory, VisitLog, PrintClickLog, DownloadClickLog

class LanguageEntryInline(admin.TabularInline):
    model = LanguageEntry
    extra = 1

class CertificateInline(admin.TabularInline):
    model = Certificate
    extra = 1

class ExperienceDescriptionInline(admin.TabularInline):
    model = ExperienceDescription
    extra = 1

def duplicate_experience(modeladmin, request, queryset):
    for experience in queryset:
        # Duplicate the experience
        experience.pk = None
        experience.save()
        # Duplicate descriptions
        for desc in experience.descriptions.all():
            desc.pk = None
            desc.experience = experience
            desc.save()

duplicate_experience.short_description = "Duplicate selected experiences"

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('cv', 'job_title', 'company', 'start_month', 'start_year', 'end_month', 'end_year')
    list_filter = ('cv',)
    ordering = ('-start_year', '-start_month')
    inlines = [ExperienceDescriptionInline]
    actions = [duplicate_experience]

class EducationInline(admin.TabularInline):
    model = Education
    extra = 1

@admin.register(CV)
class CVAdmin(admin.ModelAdmin):
    list_display = ('country_code', 'title', 'created_at')
    inlines = [LanguageEntryInline, CertificateInline, EducationInline]

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    ordering = ('order',)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.order = Skill.objects.filter(category=obj.category).count() + 1
        super().save_model(request, obj, form, change)

@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ('title_en', 'title_fr', 'title_ar', 'title_es', 'order')
    ordering = ('order',)
    fieldsets = (
        ('English Title', {
            'fields': ('title_en',)
        }),
        ('Translations', {
            'fields': ('title_fr', 'title_ar', 'title_es'),
            'description': 'Fill the translations for each language.'
        }),
        ('Order', {
            'fields': ('order',),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.order = SkillCategory.objects.count() + 1
        super().save_model(request, obj, form, change)


# Register analytics models with basic admin
@admin.register(VisitLog)
class VisitLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'ip_address', 'cv_lang')
    list_filter = ('cv_lang', 'timestamp')
    ordering = ('-timestamp',)
    search_fields = ('ip_address', 'user_agent')


@admin.register(PrintClickLog)
class PrintClickLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'ip_address', 'cv_lang')
    list_filter = ('cv_lang', 'timestamp')
    ordering = ('-timestamp',)
    search_fields = ('ip_address', 'user_agent')


@admin.register(DownloadClickLog)
class DownloadClickLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'ip_address', 'cv_lang')
    list_filter = ('cv_lang', 'timestamp')
    ordering = ('-timestamp',)
    search_fields = ('ip_address', 'user_agent')


from django.urls import path
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.contrib.admin import AdminSite
from django.template.response import TemplateResponse
from django.db.models.functions import TruncDay
from django.db.models import Count
import datetime

class CustomAdminSite(AdminSite):
    site_header = "CV Project Admin"
    site_title = "CV Admin Portal"
    index_title = "Welcome to CV Admin"

    @method_decorator(never_cache)
    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        # Add the default admin app list to the context so it shows the models
        app_list = self.get_app_list(request)
        extra_context['app_list'] = app_list
        return TemplateResponse(request, "admin/custom_index.html", extra_context)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('analytics/visits-data/', self.admin_view(self.analytics_visits_data), name='analytics_visits_data'),
            path('analytics/print-data/', self.admin_view(self.analytics_print_data), name='analytics_print_data'),
            path('analytics/download-data/', self.admin_view(self.analytics_download_data), name='analytics_download_data'),
        ]
        return custom_urls + urls

    def analytics_visits_data(self, request):
        today = datetime.date.today()
        start_date = today - datetime.timedelta(days=30)
        data = (
            VisitLog.objects.filter(timestamp__date__gte=start_date)
            .annotate(day=TruncDay('timestamp'))
            .values('day')
            .annotate(count=Count('id'))
            .order_by('day')
        )
        labels = [entry['day'].strftime('%Y-%m-%d') for entry in data]
        counts = [entry['count'] for entry in data]
        return JsonResponse({'labels': labels, 'counts': counts})

    def analytics_print_data(self, request):
        today = datetime.date.today()
        start_date = today - datetime.timedelta(days=30)
        data = (
            PrintClickLog.objects.filter(timestamp__date__gte=start_date)
            .annotate(day=TruncDay('timestamp'))
            .values('day')
            .annotate(count=Count('id'))
            .order_by('day')
        )
        labels = [entry['day'].strftime('%Y-%m-%d') for entry in data]
        counts = [entry['count'] for entry in data]
        return JsonResponse({'labels': labels, 'counts': counts})

    def analytics_download_data(self, request):
        today = datetime.date.today()
        start_date = today - datetime.timedelta(days=30)
        data = (
            DownloadClickLog.objects.filter(timestamp__date__gte=start_date)
            .annotate(day=TruncDay('timestamp'))
            .values('day')
            .annotate(count=Count('id'))
            .order_by('day')
        )
        labels = [entry['day'].strftime('%Y-%m-%d') for entry in data]
        counts = [entry['count'] for entry in data]
        return JsonResponse({'labels': labels, 'counts': counts})

# Instantiate custom admin site
custom_admin_site = CustomAdminSite(name='custom_admin')

# Register models with custom admin site
custom_admin_site.register(CV, CVAdmin)
custom_admin_site.register(Experience, ExperienceAdmin)
custom_admin_site.register(Skill, SkillAdmin)
custom_admin_site.register(SkillCategory, SkillCategoryAdmin)
custom_admin_site.register(VisitLog, VisitLogAdmin)
custom_admin_site.register(PrintClickLog, PrintClickLogAdmin)
custom_admin_site.register(DownloadClickLog, DownloadClickLogAdmin)
