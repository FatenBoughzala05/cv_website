from django.db import models

# -------------------------
# Country-specific CV
# -------------------------
class CV(models.Model):
    COUNTRY_CHOICES = [
        ("tn", "Tunisian"),
        ("fr", "French"),
        ("en", "English"),
        ("ca", "Canadian English"),
        ("ar", "Arabic"),
        ("es", "Spanish"),
    ]
    country_code = models.CharField(max_length=2, choices=COUNTRY_CHOICES, unique=True)
    title = models.CharField(max_length=255, blank=True)  # optional title
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_country_code_display()} CV"


# -------------------------
# Languages
# -------------------------
class LanguageEntry(models.Model):
    cv = models.ForeignKey(CV, on_delete=models.CASCADE, related_name="languages")
    language_name = models.CharField(max_length=100)  # e.g., "Arabic", "Arabe"
    level = models.CharField(max_length=50)           # e.g., Native, Intermédiaire

    def __str__(self):
        return f"{self.language_name}: {self.level}"


# -------------------------
# Certificates
# -------------------------
class Certificate(models.Model):
    cv = models.ForeignKey(CV, on_delete=models.CASCADE, related_name='certificates')
    name = models.CharField(max_length=200)
    issuer = models.CharField(max_length=200)
    url = models.URLField(blank=True, null=True)  # optional link

    def __str__(self):
        return f"{self.name} - {self.issuer}"



# -------------------------
# Experience
# -------------------------
class Experience(models.Model):
    MONTH_CHOICES = [
        ("01", "January"),
        ("02", "February"),
        ("03", "March"),
        ("04", "April"),
        ("05", "May"),
        ("06", "June"),
        ("07", "July"),
        ("08", "August"),
        ("09", "September"),
        ("10", "October"),
        ("11", "November"),
        ("12", "December"),
    ]

    MONTH_NAMES = {
        'en': {
            '01': 'January',
            '02': 'February',
            '03': 'March',
            '04': 'April',
            '05': 'May',
            '06': 'June',
            '07': 'July',
            '08': 'August',
            '09': 'September',
            '10': 'October',
            '11': 'November',
            '12': 'December',
        },
        'fr': {
            '01': 'Janvier',
            '02': 'Février',
            '03': 'Mars',
            '04': 'Avril',
            '05': 'Mai',
            '06': 'Juin',
            '07': 'Juillet',
            '08': 'Août',
            '09': 'Septembre',
            '10': 'Octobre',
            '11': 'Novembre',
            '12': 'Décembre',
        },
        'es': {
            '01': 'Enero',
            '02': 'Febrero',
            '03': 'Marzo',
            '04': 'Abril',
            '05': 'Mayo',
            '06': 'Junio',
            '07': 'Julio',
            '08': 'Agosto',
            '09': 'Septiembre',
            '10': 'Octubre',
            '11': 'Noviembre',
            '12': 'Diciembre',
        },
        'ar': {
            '01': 'يناير',
            '02': 'فبراير',
            '03': 'مارس',
            '04': 'أبريل',
            '05': 'مايو',
            '06': 'يونيو',
            '07': 'يوليو',
            '08': 'أغسطس',
            '09': 'سبتمبر',
            '10': 'أكتوبر',
            '11': 'نوفمبر',
            '12': 'ديسمبر',
        },
        'ca': {
            '01': 'January',
            '02': 'February',
            '03': 'March',
            '04': 'April',
            '05': 'May',
            '06': 'June',
            '07': 'July',
            '08': 'August',
            '09': 'September',
            '10': 'October',
            '11': 'November',
            '12': 'December',
        },
        'tn': {
            '01': 'Janvier',
            '02': 'Février',
            '03': 'Mars',
            '04': 'Avril',
            '05': 'Mai',
            '06': 'Juin',
            '07': 'Juillet',
            '08': 'Août',
            '09': 'Septembre',
            '10': 'Octobre',
            '11': 'Novembre',
            '12': 'Décembre',
        },
    }

    cv = models.ForeignKey(CV, on_delete=models.CASCADE, related_name="experiences")
    job_title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    start_month = models.CharField(max_length=2, choices=MONTH_CHOICES)
    start_year = models.IntegerField()
    end_month = models.CharField(max_length=2, choices=MONTH_CHOICES, blank=True, null=True)
    end_year = models.IntegerField(blank=True, null=True)

    second_start_month = models.CharField(max_length=2, choices=MONTH_CHOICES, blank=True, null=True)
    second_start_year = models.IntegerField(blank=True, null=True)
    second_end_month = models.CharField(max_length=2, choices=MONTH_CHOICES, blank=True, null=True)
    second_end_year = models.IntegerField(blank=True, null=True)
    # descriptions handled by ExperienceDescription

    @property
    def month_dict(self):
        return self.MONTH_NAMES.get(self.cv.country_code, self.MONTH_NAMES['en'])

    @property
    def date_range(self):
        month_dict = self.month_dict
        start = f"{month_dict.get(self.start_month)} {self.start_year}"
        if self.end_month and self.end_year:
            end = f"{month_dict.get(self.end_month)} {self.end_year}"
        else:
            end = "Present"
        return f"{start} - {end}"

    @property
    def second_date_range(self):
        if self.second_start_month and self.second_start_year and self.second_end_month and self.second_end_year:
            month_dict = self.month_dict
            start = f"{month_dict.get(self.second_start_month)} {self.second_start_year}"
            end = f"{month_dict.get(self.second_end_month)} {self.second_end_year}"
            return f"{start} - {end}"
        return ""

    def __str__(self):
        return f"{self.job_title} at {self.company} ({self.date_range})"

    class Meta:
        ordering = ['-start_year', '-start_month']


class ExperienceDescription(models.Model):
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE, related_name='descriptions')
    description = models.TextField()

    def __str__(self):
        return self.description[:50]

# -------------------------
# Academic Background
# -------------------------
class Education(models.Model):
    cv = models.ForeignKey(CV, on_delete=models.CASCADE, related_name="educations")
    degree_name = models.CharField(max_length=255)
    institution = models.CharField(max_length=255)
    year = models.IntegerField()
    description = models.TextField(blank=True)  # optional, translated

    def __str__(self):
        return f"{self.degree_name} ({self.year})"


class SkillCategory(models.Model):
    title_en = models.CharField(max_length=200, default='')  # English title
    title_fr = models.CharField(max_length=200, default='')  # French translation
    title_ar = models.CharField(max_length=200, default='')  # Arabic translation
    title_es = models.CharField(max_length=200, default='')  # Spanish translation
    order = models.IntegerField(default=0)

    def get_title(self, lang='en'):
        if lang == 'fr':
            return self.title_fr or self.title_en
        elif lang == 'ar':
            return self.title_ar or self.title_en
        elif lang == 'es':
            return self.title_es or self.title_en
        else:
            return self.title_en

    def __str__(self):
        return self.title_en


class Skill(models.Model):
    category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=200)  # skill name stays in English
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.name


# -------------------------  
# Analytics/Tracking Models
# -------------------------
class VisitLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    cv_lang = models.CharField(max_length=10, blank=True)  # e.g., 'en', 'fr'

    def __str__(self):
        return f"Visit at {self.timestamp} from {self.ip_address}"


class PrintClickLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    cv_lang = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return f"Print click at {self.timestamp} from {self.ip_address}"


class DownloadClickLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    cv_lang = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return f"Download click at {self.timestamp} from {self.ip_address}"

