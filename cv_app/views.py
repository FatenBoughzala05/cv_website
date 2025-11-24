from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from django.conf import settings
import os
from io import BytesIO
from .models import CV, Skill, SkillCategory, VisitLog, PrintClickLog, DownloadClickLog
from django.views.decorators.csrf import csrf_exempt

def cv_home(request):
    return redirect('cv_view', lang='tn')


def download_cv(request):
    # Render your HTML
    html_string = render_to_string('index.html', {'user': request.user})

    # Define path to static CSS file
    css_path = os.path.join(settings.BASE_DIR, 'cv_app', 'static', 'css', 'download.css')

    # Open CSS file and read content
    with open(css_path) as f:
        css_content = f.read()

    # Inject CSS content inside a <style> tag in the HTML string
    html_with_css = f'<style>{css_content}</style>' + html_string

    # Create a BytesIO buffer to receive PDF data
    result = BytesIO()

    # Convert HTML to PDF using xhtml2pdf
    pdf_status = pisa.CreatePDF(
        src=html_with_css,
        dest=result,
        encoding='UTF-8',
        link_callback=lambda uri, rel: os.path.join(settings.BASE_DIR, 'cv_app', 'static', uri.replace(settings.STATIC_URL, ''))
    )

    if pdf_status.err:
        return HttpResponse('We had some errors while generating the PDF', status=500)

    # Get PDF data from BytesIO buffer
    pdf_file = result.getvalue()
    result.close()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="CV_Faten_Boughzala.pdf"'
    return response


def cv_view(request, lang="tn"):
    templates = {
        "en": "cv_en.html",
        "fr": "cv_fr.html",   # French/Canadian French
        "ar": "cv_ar.html",
        "es": "cv_es.html",
        "tn": "index.html",   # Tunisian default
        "ca": "cv_ca.html"    # Canadian French if needed
    }
    template = templates.get(lang, "index.html")
    
     # Get CV instance by country code
    cv = get_object_or_404(CV, country_code=lang)

    # Map country_code to translation language
    lang_map = {
        'tn': 'fr',
        'fr': 'fr',
        'en': 'en',
        'ca': 'en',
        'es': 'es',
        'ar': 'ar'
    }
    translation_lang = lang_map.get(lang, 'en')

    # Fetch related data
    languages = cv.languages.all()
    certificates = cv.certificates.all()
    experiences = cv.experiences.all()
    educations = cv.educations.all()
    skills = Skill.objects.all()  # universal skills
    skill_categories_translated = [{'title': category.get_title(translation_lang), 'skills': category.skills.all()} for category in SkillCategory.objects.all()]

    context = {
        'cv': cv,
        'languages': languages,
        'certificates': certificates,
        'experiences': experiences,
        'educations': educations,
        'skills': skills,
        'skill_categories_translated': skill_categories_translated,
        'lang': lang
    }

    return render(request, template, context)


def get_client_ip(request):
    """Utility to get client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def log_visit(request, lang):
    ip = get_client_ip(request)
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    VisitLog.objects.create(ip_address=ip, user_agent=user_agent, cv_lang=lang)


@csrf_exempt
def log_print_click(request):
    if request.method == 'POST':
        ip = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        lang = request.POST.get('lang', '')
        PrintClickLog.objects.create(ip_address=ip, user_agent=user_agent, cv_lang=lang)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'fail'}, status=400)


@csrf_exempt
def log_download_click(request):
    if request.method == 'POST':
        ip = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        lang = request.POST.get('lang', '')
        DownloadClickLog.objects.create(ip_address=ip, user_agent=user_agent, cv_lang=lang)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'fail'}, status=400)


# Modify cv_view to log visits
def cv_view(request, lang="tn"):
    templates = {
        "en": "cv_en.html",
        "fr": "cv_fr.html",   # French/Canadian French
        "ar": "cv_ar.html",
        "es": "cv_es.html",
        "tn": "index.html",   # Tunisian default
        "ca": "cv_ca.html"    # Canadian French if needed
    }
    template = templates.get(lang, "index.html")
    
     # Get CV instance by country code
    cv = get_object_or_404(CV, country_code=lang)

    # Log visit
    log_visit(request, lang)

    # Map country_code to translation language
    lang_map = {
        'tn': 'fr',
        'fr': 'fr',
        'en': 'en',
        'ca': 'en',
        'es': 'es',
        'ar': 'ar'
    }
    translation_lang = lang_map.get(lang, 'en')

    # Fetch related data
    languages = cv.languages.all()
    certificates = cv.certificates.all()
    experiences = cv.experiences.all()
    educations = cv.educations.all()
    skills = Skill.objects.all()  # universal skills
    skill_categories_translated = [{'title': category.get_title(translation_lang), 'skills': category.skills.all()} for category in SkillCategory.objects.all()]

    context = {
        'cv': cv,
        'languages': languages,
        'certificates': certificates,
        'experiences': experiences,
        'educations': educations,
        'skills': skills,
        'skill_categories_translated': skill_categories_translated,
        'lang': lang
    }

    return render(request, template, context)
