from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from datetime import datetime


from app.pdf.utils import add_other_details, draw_wrapped_line

# sauce code: 138235

def get_report(buffer, document, currency, document_type, request, terms):

    now = datetime.now().strftime("%Y-%m-%d %H-%M-%S")

    documents = {'invoice': "invoice_number",
                "proforma invoice": "invoice_number",
                "purchase order": "po_number",
                "estimate": "estimate_number",
                "quote": "quote_number",
                "receipt": "receipt_number",
                "credit note": "cn_number",
                "delivery note": "dn_number"
                }

    # doc_number_key = documents[document_type]

    file_name = f"{document_type.title()} for {request.user.email} - {now}.pdf"

    # create file
    pdf = canvas.Canvas(buffer, bottomup=0)
    pdf.translate(cm, cm)
    pdf.setPageSize((A4[0]+15, A4[1]))

    # author info
    # pdf.setAuthor("Made by Pyaar")
    # pdf.setSubject("Report PDF.")
    pdf.setTitle(document_type.title())

    # setting a custom background color
    background_color = colors.Color(0.1, 0.1, 1)

    pdf.setFillColor(background_color)
    pdf.setLineWidth(0.1)
    pdf.setStrokeColor(background_color)



    # aspect for company name
    # pdf.rect(-15, 0, 280, 140)
    pdf.rect(-15, 0, 100, 100)
    pdf.drawString(10, 30, "logo")
    pdf.setFont('Times-Roman', 20)
    pdf = draw_wrapped_line(pdf, request.user.business_name, 100, 90, 20, 10)
    pdf.setFont('Times-Roman', 10)
    pdf = draw_wrapped_line(pdf, request.user.address, 100, 90, 30, 10)
    pdf = draw_wrapped_line(pdf, request.user.email, 100, 90, 40, 10)
    pdf = draw_wrapped_line(pdf, request.user.phone_number, 100, 90, 50, 10)
    # pdf.drawString(-10, 75, "space for the logo and merchant details")
    # pdf.rect(430, 20, 140, 50)

    # rectangle for date
    pdf.rect(430, 20, 140, 50)
    pdf.line(500, 20, 500, 70)
    pdf.line(430, 40, 570, 40)
    pdf.setFont('Times-Roman', 20)
    pdf.drawString(430, 15, f"{document_type.title()}")
    pdf.setFont('Times-Roman', 10)
    pdf.drawString(450, 35, "DATE")
    pdf.drawString(510, 35, "NUMBER")



    # rectangle for customer name details
    pdf.rect(-15, 140, 220, 100)
    pdf.line(-15, 165, 205, 165)
    pdf.drawString(-10, 155, f"{document_type.title()} To")



    # rectangle for 3 details
    pdf.rect(380, 180, 190, 60)
    # pdf.drawString(310, 195, "P.O. No.")
    pdf.line(380, 205, 570, 205)
    pdf.drawString(410, 195, "P.O. No.")
    pdf.line(380, 180, 380, 240)
    pdf.drawString(500, 195, "Project")
    pdf.line(470, 180, 470, 240)


    # big rectangle for the details
    pdf.rect(-15, 240, 585, 500)
    pdf.line(-15, 270, 570, 270)
    pdf.drawCentredString(9, 260, "Qty")
    pdf.line(30, 240, 30, 740)
    pdf.drawString(200, 260, "Description")
    pdf.line(400, 240, 400, 740)
    pdf.drawCentredString(445, 260, "Rate")
    pdf.line(490, 240, 490, 740)
    pdf.drawCentredString(530, 260, "Amount")

    
    # adding the additional details
    pdf = add_other_details(pdf, document, 268, document_type, currency, terms)


    
    pdf.save()


    return file_name