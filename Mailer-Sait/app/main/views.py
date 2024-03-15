from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import Filters, AddFilter
from .mailer import Mailer

mailer = Mailer(server='imap.mail.ru', user_email='', password='')


@login_required
def index(request):
    if request.method == 'POST':
        form = AddFilter(request.POST)
        if form.is_valid():
            form.save()
            form_val = form.data
            print(form_val)
            return redirect('/')
    else:
        form = AddFilter()

    parent_folders = mailer.get_parent_folders()

    last_mail = mailer.get_last_10_emails

    return render(request, 'main/index.html', {'form': form, 'parent_folders': parent_folders, 'last_mail': last_mail})


@login_required
def detail(request, mail_id):
    emails = mailer.get_last_10_emails()
    mail_id_str = str(mail_id)
    selected_email = None
    for email in emails:
        if str(email['id']) == mail_id_str.strip():
            selected_email = email
            break

    if selected_email is None:
        return render(request, 'main/index.html', status=404)

    context = {
        'email': selected_email,
    }

    return render(request, 'main/detail.html', context)
