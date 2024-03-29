from django.db.models.signals import post_save
from django.shortcuts import render, reverse, redirect
from django.views import View
from django.core.mail import send_mail, EmailMultiAlternatives, mail_managers, EmailMessage
from django.views.generic import DetailView, View


from .models import Appointment
from .models import *
from datetime import datetime
from django.utils import timezone


# Create your views here.




class NewsItems(DetailView):
    model = Appointment
    template_name = 'news.html'
    context_object_name = 'news'
    queryset = Appointment.objects.order_by('-dateCreation')
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_in_page'] = self.paginate_by
        return context







class AppointmentView(View):
    model = Appointment
    template_name = 'news_item.html'
    context_object_name = 'news'

class Search(View):
    model = Appointment
    template_name = 'search.html'
    context_object_name = 'post_search'
    ordering = ['-dateCreation']
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filter = self.filter_class(self.request.GET, queryset=queryset)
        return self.filter.qs.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filter
        context['list_in_page'] = self.paginate_by
        context['all_posts'] = Appointment.objects.all()
        return context


class myMail(DetailView):
    model = Appointment
    context_object_name = 'Appointment'
    template_name = 'appointments_created.html'
    def get(self, request, *args, **kwargs):
        return render(request, 'make_appointment.html', {})

    def post(self, request, html_content=None, *args, **kwargs):
        appointment = Appointment(date=datetime.strptime(request.POST['date'], '%Y-%m-%d'),
                                  client_name=request.POST['client_name'], message=request.POST['MESSAGE'], )
        appointment().save()

        msg = EmailMultiAlternatives(subject=f'{appointment.client_name} {appointment.date.strftime("%Y-%M-%d")}',
                                     body=appointment.messsage, from_email='denisevostyanov7@gmail.com',
                                     to=['denisevostyanov7@gmail.com'], )

        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return redirect('appointment:make_appointment')

    def notify_managers_appointment(sender, instance, created, **kwargs):
        subject = f'{instance.client_name} {instance.date.strftime("%d %m %Y")}'

        mail_managers(
            subject=subject,
            message=instance.message,
        )

    post_save.connect(notify_managers_appointment, sender=Appointment)

    def notify_managers_appointment(sender, instance, created, **kwargs):
        if created:
            subject = f'{instance.client_name} {instance.date.strftime("%d %m %Y")}'
        else:
            subject = f'Appointment changed for {instance.client_name} {instance.date.strftime("%d %m %Y")}'

        mail_managers(
            subject=subject,
            message=instance.message,
        )

        def send_email(subject, body, recipient):
            email = EmailMessage(subject, body, to=[recipient])
            email.send()

        def send_newsletter():
            categories = Category.objects.all()
            for category in categories:
                new_articles = Article.objects.filter(category=category,
                                                      pub_date__gte=timezone.now() - timezone.timedelta(days=7))
                for user in UserProfile.objects.filter(subscribed_categories=category):
                    subject = f"Новые статьи в категории {category.name}"
                    body = "Новые статьи:\n\n"
                    for article in new_articles:
                        body += f"- {article.title}: {article.content[:50]}...\n"
                    body += "\nПосмотреть все статьи: <ссылка на страницу со статьями>"
                    send_email(subject, body, user.user.email)





