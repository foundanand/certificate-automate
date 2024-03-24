from PyPDF2 import PdfWriter, PdfReader
import io
import os
import pandas as pd
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A2, A3, A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from certificate_mail import send_mail

# NAME_FONT = pdfmetrics.registerFont(TTFont('Great Vibes 400', 'greatvibes.ttf'))
# NAME_FONT = pdfmetrics.registerFont(TTFont('Poppins', 'Poppins Regular 400.ttf'))
NAME_FONT = pdfmetrics.registerFont(TTFont('Book-Antiqua', 'Book-Antiqua.ttf'))
FILEPATH = "FinGenAI_List_Certificate.xlsx"
# EMAIL_ID = "anand.lahoti2021@vitbhopal.ac.in"
# PER_NAME = "Anand Lahoti"
CERTIFICATE = "certificate 4.pdf"
EVENT_NAME  = "FinGenAI"
CERTIFICATE_FOLDER = f"event_certificate/{EVENT_NAME}"
FONT_NAME = "Book-Antiqua"

def make_certificate(PER_NAME, FONT_NAME=FONT_NAME):

    PER_NAME = ' '.join(word.capitalize() for word in PER_NAME.split())

    # create a new PDF with Reportlab
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=A2)
    # can.setFillColorRGB(0, 0, 0)
    can.setFillColor(HexColor('#FFFFFF'))
    # Check the length of the name and adjust the font size
    if len(PER_NAME) > 19:
        can.setFont(FONT_NAME, 40)  #Reduce the font size if the name is too long
    else:
        can.setFont(FONT_NAME, 54)
    # can.setFont('Great Vibes 400', 54)
    fName = can.drawString(264, 345, PER_NAME)
    can.save()
    # move to the beginning of the StringIO buffer
    packet.seek(0)

    # create a new PDF with Reportlab
    new_pdf = PdfReader(packet)
    # read your existing PDF
    existing_pdf = PdfReader(open(CERTIFICATE, "rb"))
    output = PdfWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.pages[0]
    page.merge_page(new_pdf.pages[0])
    output.add_page(page)
    # finally, write "output" to a real file
    # Create directory if it doesn't exist
    if not os.path.exists(CERTIFICATE_FOLDER):
        os.makedirs(CERTIFICATE_FOLDER)



    output_stream = open(os.path.join(CERTIFICATE_FOLDER, f"{PER_NAME}_{EVENT_NAME}.pdf"), "wb")
    output.write(output_stream)
    output_stream.close()

# make_certificate(PER_NAME)
# send_mail(EMAIL_ID, PER_NAME, EVENT_NAME, CERTIFICATE_FOLDER, CERTIFICATE)
#
df = pd.read_excel(FILEPATH)
name_list = df.to_dict(orient='records')

for names in name_list:
    pdfGen = {'name': names['name'], 'email': names['email_id']}

    PER_NAME = pdfGen['name']
    EMAIL_ID = pdfGen['email']
    make_certificate(PER_NAME)
    # send_mail(EMAIL_ID, PER_NAME, EVENT_NAME, CERTIFICATE_FOLDER, CERTIFICATE)
    print(PER_NAME)
