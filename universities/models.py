from django.db import models

class University(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    contact = models.CharField(max_length=100)
    total_departments = models.IntegerField()
    faculty = models.IntegerField()
    qs_ranking = models.IntegerField(null=True, blank=True)
    publications = models.IntegerField(default=0)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    admission_requirements = models.TextField()
    image = models.ImageField(upload_to='universities/', blank=True, null=True, help_text="Upload university image")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    google_maps_link = models.URLField(max_length=500, blank=True, null=True)
    website = models.URLField(max_length=500, blank=True, null=True)
    short_name = models.CharField(max_length=50, blank=True, null=True, help_text="e.g., BUET,BRACU,NSU,AIUB, UAP")
    course_type = models.CharField(max_length=50, blank=True, null=True)
    subject_group = models.CharField(max_length=50, blank=True, null=True)
    language = models.CharField(max_length=50, blank=True, null=True)
    institution_type = models.CharField(max_length=50, blank=True, null=True)
    CREDIT_CHOICES = [
        ('Open', 'Open Credit'),
        ('Closed', 'Closed Credit'),
    ]
    credit_system = models.CharField(max_length=10, choices=CREDIT_CHOICES, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Universities"
        ordering = ['name']


class Department(models.Model):
    university = models.ForeignKey(
        University,
        on_delete=models.CASCADE,
        related_name='departments',
    )
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(
        upload_to='departments/',
        blank=True,
        null=True,
        help_text='Optional image for this department',
    )

    def __str__(self):
        return f"{self.name} ({self.university.name})"

    class Meta:
        verbose_name_plural = "Departments"
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(
                fields=['university', 'name'],
                name='unique_department_name_per_university',
            ),
        ]


class Event(models.Model):
    # Links this event to a specific university
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_date = models.DateTimeField()
    location = models.CharField(max_length=200, help_text="e.g., Main Auditorium or Zoom Link")
    image = models.ImageField(
        upload_to='events/',
        blank=True,
        null=True,
        help_text='Optional banner or poster image',
    )

    def __str__(self):
        return f"{self.title} - {self.university.name}"

    class Meta:
        ordering = ['event_date']  # Shows the closest events first


class Admission(models.Model):
    # Links this admission cycle to a specific university
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='admissions')
    degree_level = models.CharField(max_length=100, help_text="e.g., Bachelor's Fall 2026")
    deadline = models.DateField()
    apply_link = models.URLField(blank=True, null=True)
    is_open = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.university.name} - {self.degree_level}"

    class Meta:
        ordering = ['deadline']  # Shows the most urgent deadlines first


class Scholarship(models.Model):
    """Merit or need-based aid programs managed from the staff dashboard."""

    university = models.ForeignKey(
        University,
        on_delete=models.CASCADE,
        related_name='scholarships',
    )
    title = models.CharField(max_length=200)
    tagline = models.CharField(
        max_length=300,
        blank=True,
        help_text='Short highlight (e.g. "Up to 100% tuition")',
    )
    description = models.TextField()
    deadline = models.DateField(null=True, blank=True, help_text='Optional application deadline')
    apply_link = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(
        default=False,
        help_text='Show in the home page “Featured scholarships” strip',
    )
    image = models.ImageField(
        upload_to='scholarships/',
        blank=True,
        null=True,
    )
    sort_order = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f"{self.title} — {self.university.name}"

    class Meta:
        ordering = ['sort_order', 'title']
        verbose_name_plural = 'Scholarships'


class FaqCategory(models.Model):
    """Groups FAQ entries (e.g. Admissions, Fees)."""

    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, blank=True)
    sort_order = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'FAQ categories'
        ordering = ['sort_order', 'name']

    def save(self, *args, **kwargs):
        from django.utils.text import slugify

        if not self.slug:
            base = slugify(self.name)[:80] or 'category'
            slug = base
            n = 1
            while FaqCategory.objects.exclude(pk=self.pk).filter(slug=slug).exists():
                slug = f'{base}-{n}'
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)


class FaqItem(models.Model):
    """Published Q&A for the public Help & FAQ page."""

    category = models.ForeignKey(
        FaqCategory,
        on_delete=models.CASCADE,
        related_name='items',
    )
    question = models.CharField(max_length=400)
    answer = models.TextField()
    sort_order = models.PositiveSmallIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.question[:60]

    class Meta:
        ordering = ['category', 'sort_order', 'pk']
        verbose_name_plural = 'FAQ items'