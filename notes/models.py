from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.utils.html import mark_safe
import markdown
import markdown.extensions.fenced_code
import markdown.extensions.codehilite
import markdown.extensions.tables
import markdown.extensions.toc
from django.db.models.signals import pre_save, post_save
import joblib
from sentiment_model.sentiment_formatting import formatted_text


def generate_unique_slug(_class, field):
    origin_slug = slugify(field)
    unique_slug = origin_slug
    numb = 1
    while _class.objects.filter(slug=unique_slug).exists():
        unique_slug = '%s-%d' % (origin_slug, numb)
        numb += 1
    return unique_slug

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    note_title = models.CharField(max_length=200)
    note_content = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=200, unique=True)
    sentiment = models.CharField(max_length=200, default='Neutral')

    def get_message_as_markdown(self):
        return mark_safe(
            markdown.markdown(
                self.note_content,
                output_format="html5"
            )
        )

    def __str__(self):
        return self.note_title

    def save(self, *args, **kwargs):
        title = self.note_title
        if self.slug:
            if slugify(title) != self.slug:
                self.slug = generate_unique_slug(Note, title)
        else:
            self.slug = generate_unique_slug(Note, title)

        model = joblib.load('sentiment_model/sentiment_model.sav')
        self.sentiment = model.predict(formatted_text(self.note_content))[0]
        print(self.sentiment)
        super(Note, self).save(*args, **kwargs)

# def note_pre_save(sender, instance, *args, **kwargs):
#     print('note pre save')
#     print(args, kwargs)
#     print('pre saved')
#     instance.sentiment = 'sad'
#     instance.save()

# pre_save.connect(note_pre_save, sender=Note)

# def note_post_save(sender, instance, created, *args, **kwargs):
#     print('note post save')
#     print(args, kwargs)
#     if created:
#         print('just created')
#         instance.sentiment = 'sad'
#         instance.save()

# post_save.connect(note_post_save, sender=Note)
