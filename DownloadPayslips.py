import imaplib
import email
import os
import config


imap_url = 'imap.gmail.com'
attachments_dir = 'E:/Documents/University/Report Automator/'


def start():
    try:
        connection = authentication()
    except Exception as e:
        print(e)

    remove_files()

    result, data = connection.uid('search', None, '(HEADER Subject "Revel payslip")')    # returning id's from emails that contain "Revel payslip" in the subject
    ids = data[0]
    id_list = ids.split()
    latest_mail_id = [id_list[-1], id_list[-2]]   # getting two most recent payslips

    for id in latest_mail_id:
        result, data = connection.uid('fetch', id, '(RFC822)')
        raw = email.message_from_bytes(data[0][1])
        get_attachments(raw, id)


def remove_files():
    for file in os.listdir(attachments_dir):
        file_path = os.path.join(attachments_dir, file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)


def get_attachments(msg, id):
    for part in msg.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        sub_file_name = part.get_filename()
        file_name = sub_file_name[:13] + id.decode("utf-8") + sub_file_name[13:]    # making filename unique

        if bool(file_name):
            filePath = os.path.join(attachments_dir, file_name)
            with open(filePath, 'wb') as f:
                f.write(part.get_payload(decode=True))
        else:
            print("no attachment")
    print("Download Success!")


def authentication():
    connection = imaplib.IMAP4_SSL(imap_url)    # connecting to gmail sever
    connection.login(config.EMAIL_ADDRESS, config.PASSWORD)    # login to sever
    connection.select('INBOX')     # selecting INBOX
    return connection
