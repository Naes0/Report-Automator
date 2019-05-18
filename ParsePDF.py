import os
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO

attachments_dir = 'E:/Documents/University/Report Automator/'
os.chdir(attachments_dir)   # change working directory to where the pdf's are


def parse_and_calc():
    payslips_list = create_payslip_list()
    payslips = strip_and_split(payslips_list)

    total_pay = 0.0
    total_hours = 0.0
    message = ""

    try:
        for payslip in payslips:
            total_pay += float((payslip[55])[1:])   # getting pay from payslip and eliminating "$"
            if "Sunday" in payslip:
                total_hours += float(payslip[94]) + float(payslip[95])
            else:
                total_hours += float(payslip[92])
        message = "Total Pay: ${}\nTotal Hours: {}".format(total_pay, total_hours)
    except ValueError as err:
        print("error parsing and calculating")
        message = str(err)
    return message


# looping through pdf files returning text values
def create_payslip_list():
    payslips = []
    for file in os.listdir():
        file_path = os.path.join(attachments_dir, file)
        payslips.append(convert_pdf_to_txt(file_path))
    return payslips


# adapted from https://stackoverflow.com/questions/26494211/extracting-text-from-a-pdf-file-using-pdfminer-in-python
def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages,
                                  password=password, caching=caching,
                                  check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()
    fp.close()
    device.close()
    retstr.close()
    return text


def strip_and_split(payslips_list):
    payslips_list[0].strip()
    payslip_1 = payslips_list[0].split()
    payslips_list[1].strip()
    payslip_2 = payslips_list[1].split()
    payslips = [payslip_1, payslip_2]
    return payslips
