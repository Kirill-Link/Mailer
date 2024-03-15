import imaplib
import shlex
from email import policy
from email.parser import BytesParser
import html2text

from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

from imap_tools.imap_utf7 import encode, decode


def get_email_body(msg):
    # Проверка на наличие многокомпонентного содержимого
    if msg.is_multipart():
        # Проход по всем частям сообщения
        for part in msg.iter_parts():
            # Выбираем текстовую часть
            if part.get_content_type() == 'text/plain':
                # Используем html2text для удаления HTML-тегов
                body = part.get_payload(decode=True).decode(part.get_content_charset(), 'ignore')
                return html2text.html2text(body)
    else:
        # Для простых текстовых сообщений
        # Используем html2text для удаления HTML-тегов
        body = msg.get_payload(decode=True).decode(msg.get_content_charset(), 'ignore')
        return html2text.html2text(body)

def clean_email_id(raw_id):
    try:
        # Декодируем байтовую строку в обычную строку
        decoded_id = raw_id.decode('utf-8')

        # Преобразуем строку в целое число
        email_id = int(decoded_id)

        return email_id
    except (UnicodeDecodeError, ValueError):
        # Обработка ошибок, если не удается декодировать или преобразовать
        return None



class Mailer:

    def __init__(self, server, user_email, password):
        self.mail = imaplib.IMAP4_SSL(server)
        self.mail.login(user_email, password)
        self.mail.select('inbox')

    def create_folder(self, parent_folder, folder_name):
        self.mail.create(f'{parent_folder}/{folder_name}')

    def get_parent_folders(self):
        find_folder = []
        for folder in self.mail.list(directory='.')[1]:
            folder_name = shlex.split(decode(folder))[-1]
            if '/' not in folder_name:
                find_folder.append(folder_name)

        return find_folder

    def create_client_folder(self, folder_name):
        self.mail.create(folder_name)

    def get_client_folders(self, parent_folder):
        find_folders = []
        status, folder_list = self.mail.list(directory=f'"{parent_folder}"')

        if status == "OK":
            for folder in folder_list:
                folder_name = shlex.split(folder.decode())[-1]

                if '/' in folder_name and folder_name.startswith(parent_folder):
                    child_folder = folder_name[len(parent_folder) + 1:]
                    find_folders.append(child_folder)

        # Проверка наличия папки и создание, если её нет
        if not find_folders:
            self.create_client_folder(parent_folder)  # Метод create_folder должен быть определен в вашем классе

        return find_folders

    def is_folder_exists(self, parent_folder, folder_name, create_if_not_exists=True):
        # Получаем список всех доступных папок
        status, folder_list = self.mail.list()

        # Проверяем, существует ли указанная папка
        for folder_info in folder_list:
            _, _, current_folder = folder_info.decode().partition(' "/" ')
            if current_folder == folder_name:
                return True

        # Если папка не найдена и create_if_not_exists=True, создаем папку
        if create_if_not_exists:
            self.mail.create(f'{parent_folder}/{folder_name}')
            return True

        return False

    def get_last_10_emails(self):
        emails = []

        # Получение последних 10 UID писем в папке "inbox"
        status, messages = self.mail.search(None, "ALL")
        mail_ids = messages[0].split() if status == "OK" else []

        # Получение деталей каждого письма и добавление в список
        for i in range(max(0, len(mail_ids) - 10), len(mail_ids)):
            status, msg_data = self.mail.fetch(mail_ids[i], "(RFC822)")
            raw_email = msg_data[0][1]

            # Парсинг письма
            msg = BytesParser(policy=policy.default).parsebytes(raw_email)

            # Декодирование тела письма
            if msg.is_multipart():
                # Если письмо состоит из нескольких частей
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8')
                        break
            else:
                # Если письмо состоит из одной части
                body = msg.get_payload(decode=True).decode(msg.get_content_charset() or 'utf-8')

            # Собираем информацию о письме в словарь
            email_info = {
                'id': clean_email_id(mail_ids[i]),  # Очищаем ID письма
                'subject': msg['subject'],
                'from': msg['from'],
                'date': msg['date'],
                'body': body,
            }

            emails.append(email_info)

        # Преобразование дат в объекты datetime с осведомлением о смещении
        for email in emails:
            email['date'] = parsedate_to_datetime(email['date']).replace(tzinfo=timezone.utc)

        # Сортировка писем по дате в убывающем порядке
        emails.sort(key=lambda x: x['date'], reverse=True)

        return emails

    def close_mail_connect(self):
        self.mail.close()
        self.mail.logout()
