from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from datetime import datetime
import textwrap, requests, os


page_number = 1





def draw_wrapped_line(pdf, text, length, x_pos, y_pos, y_offset):
    '''
    This function is for wrapping text.
    Input:
        pdf - pdf object
        text - the text you want to wrap
        length - the number of characters that should be on each line.
        x_pos - value for x-axis
        y_pos - value for y-axis
        y_offset - amount of space that should be between each line of text.
        w_type - defines how the text should be displayed, either centered aligned or left aligned, take canter or left as value

    Output: None
    '''

    if len(text) > length:
        wraps = textwrap.wrap(text, length)
        for x in range(len(wraps)):
            pdf.drawString(x_pos, y_pos, wraps[x])
            y_pos += y_offset
    else:
        pdf.drawString(x_pos, y_pos, text)
    
    return pdf





def add_another_page(pdf, item_list, currency, document, document_type):
    global page_number
    page_number += 1

    # another page
    pdf.showPage()
    pdf.translate(cm, cm)
    pdf.setPageSize((A4[0], A4[1]))
    pdf.setLineWidth(0.5)


    pdf.setFillColor(colors.black)

    pdf.rect(10, 10, 530, 25, fill=1)
    pdf.setFillColor(colors.white)
    pdf.setFont('Helvetica-Bold', 10)

    pdf.drawString(35, 25, "Qty")
    pdf.drawString(150, 25, "Description")
    pdf.drawString(350, 25, "Unit Price")
    pdf.drawString(470, 25, "Amount")

    pdf.setFillColor(colors.black)

    pdf.setFont('Helvetica', 10)
    pdf.drawString(250, 800, f"Page {page_number}")

    item_len = len(item_list)

    start_y = 40

    if item_len <= 20:
        
        for item in item_list:
            pdf.drawString(40, start_y+10, str(item["quantity"]))
            pdf.drawString(80, start_y+10, str(item["name"]))
            pdf.drawRightString(430, start_y+10, str(item["sales_price"]))
            pdf.drawRightString(535, start_y+10, str(item["amount"]))
                
            start_y += 20

        pdf.line(10, 10, 10, start_y)
        pdf.line(70, 10, 70, start_y)
        pdf.line(320, 10, 320, start_y)
        pdf.line(450, 10, 450, start_y)
        pdf.line(540, 10, 540, start_y)
        pdf.line(10, start_y, 540, start_y)



        pdf = total_box(pdf, start_y, currency, document_type, document)

    else:
        i = 0
        for item in item_list:
            if i == 36:
                break

            pdf.drawString(40, start_y+10, str(item["quantity"]))
            pdf.drawString(80, start_y+10, str(item["name"]))
            pdf.drawRightString(430, start_y+10, str(item["sales_price"]))
            pdf.drawRightString(535, start_y+10, str(item["amount"]))
                
            start_y += 20
            i += 1
        
        pdf.line(10, 10, 10, start_y)
        pdf.line(70, 10, 70, start_y)
        pdf.line(320, 10, 320, start_y)
        pdf.line(450, 10, 450, start_y)
        pdf.line(540, 10, 540, start_y)
        pdf.line(10, start_y, 540, start_y)

        
        pdf, start_y = add_another_page(pdf, item_list[36:], currency, document, document_type)


    return pdf, start_y






def total_box(pdf, start_y, currency, document_type, document):
    if document_type == "invoice":
        # it will have sub total
        pdf.drawRightString(440, start_y+20, "Subtotal")
        pdf.drawRightString(535, start_y+20, f"{document['sub_total']}")
        # tax, additional charges, discount_amount
        pdf.drawRightString(440, start_y+40, "Tax")
        pdf.drawRightString(535, start_y+40, f"{document['tax']}")
        pdf.drawRightString(440, start_y+60, "Additional Charges")
        pdf.drawRightString(535, start_y+60, f"{document['add_charges']}")
        pdf.drawRightString(440, start_y+85, "Discount Amount")
        pdf.drawRightString(535, start_y+85, f"{document.get('discount_amount', '0')}")

        pdf.setFillColor(colors.ReportLabFidRed)
        pdf.setFont('Helvetica-Bold', 13)
        pdf.drawRightString(440, start_y+120, f"{document_type.upper()} TOTAL")
        pdf.drawRightString(535, start_y+120, f"{currency} {document['grand_total']}")
        


    else:
        # tax, additional charges, discount_amount
        pdf.drawRightString(440, start_y+20, "Tax")
        pdf.drawRightString(535, start_y+20, f"{document['tax']}")
        pdf.drawRightString(440, start_y+40, "Additional Charges")
        pdf.drawRightString(535, start_y+40, f"{document['add_charges']}")
        pdf.drawRightString(440, start_y+65, "Discount Amount")
        pdf.drawRightString(535, start_y+65, f"{document.get('discount_amount', '0')}")

        pdf.setFillColor(colors.ReportLabFidRed)
        pdf.setFont('Helvetica-Bold', 13)
        pdf.drawRightString(440, start_y+100, f"{document_type.upper()} TOTAL")
        pdf.drawRightString(535, start_y+100, f"{currency} {document['grand_total']}")

    pdf.setFillColor(colors.ReportLabFidRed)
    pdf.setFont('Helvetica-Bold', 10)
    pdf.line(10, start_y+160, 550, start_y+160)
    pdf.drawString(10, start_y+180, "TERMS & CONDITION")
    pdf.setFillColor(colors.black)
    pdf.setFont('Helvetica', 10)
    pdf = draw_wrapped_line(pdf, document["terms"].title(), 100, 10, start_y+200, 15)

    pdf.drawImage("app/pdf/logo_27_down.png", -35, 745, width=620, height=70)
            
    return pdf
















def get_report_27(buffer, document, currency, document_type, request, logo):

    now = datetime.now().strftime("%Y-%m-%d %H-%M-%S")

    file_name = f"{document_type.title()} for {request.user.email} - {now}.pdf"

    # create file
    pdf = canvas.Canvas(buffer, bottomup=0)
    pdf.translate(cm, cm)
    pdf.setPageSize((A4[0], A4[1]))

    width = pdf._pagesize[0]
    pdf.setTitle(document_type.title())


    pdf.setLineWidth(0.5)

    pdf.drawImage("app/pdf/logo_27_up.png", -30, -30, width=600, height=100)
            


    pdf.setFont('Helvetica-Bold', 20)
    pdf.setFillColor(colors.ReportLabFidRed)
    pdf = draw_wrapped_line(pdf, request.user.business_name.title(), 100, 10, 90, 10)
    pdf.setFillColor(colors.black)

    pdf.setFont('Helvetica', 10)
    pdf = draw_wrapped_line(pdf, request.user.address.capitalize(), 100, 10, 110, 10)
    pdf = draw_wrapped_line(pdf, request.user.email, 100, 10, 125, 10)
    pdf = draw_wrapped_line(pdf, request.user.phone_number, 100, 10, 140, 10)

    
    pdf.setFont('Helvetica-Bold', 10)
    pdf.setFillColor(colors.ReportLabFidRed)
    pdf.rect(10, 160, 530, 23, fill=1)
    pdf.rect(350, 220, 190, 23, fill=1)
    pdf.line(10, 160, 10, 270)
    pdf.line(180, 160, 180, 270)
    pdf.line(350, 160, 350, 270)
    pdf.line(440, 160, 440, 270)
    pdf.line(540, 160, 540, 270)
    pdf.line(10, 270, 540, 270)
    pdf.setFillColor(colors.white)
    pdf.drawString(80, 175, "Bill To")
    pdf.drawString(240, 175, "Ship To")
    pdf.setFillColor(colors.black)
    pdf.setFont('Helvetica', 10)
    pdf = draw_wrapped_line(pdf, document["bill_to"], 40, 20, 200, 10)
    pdf = draw_wrapped_line(pdf, document["ship_to"], 40, 190, 200, 10)

    pdf.setFont('Helvetica-Bold', 10)
    pdf.setFillColor(colors.white)
    pdf.drawRightString(420, 175, f"{document_type.split(' ')[0].title()} #")
    pdf.drawRightString(520, 175, f"{document_type.split(' ')[0].title()} Date")
    pdf.drawRightString(420, 235, "Due Date")
    pdf.setFillColor(colors.black)
    pdf.setFont('Helvetica', 10)

    documents = {'invoice': "invoice_number",
                "proforma invoice": "invoice_number",
                "purchase order": "po_number",
                "estimate": "estimate_number",
                "quote": "quote_number",
                "receipt": "receipt_number",
                "credit note": "cn_number",
                "delivery note": "dn_number"
                }

    doc_number_key = documents[document_type]
    doc_date_key = doc_number_key.replace('number', 'date')

    pdf.setFont('Helvetica', 10)

    pdf.drawCentredString(400, 200, f"{document[doc_number_key]}")
    pdf.drawCentredString(490, 200, f"{document[doc_date_key]}")
    pdf.drawCentredString(400, 260, f"{document['due_date']}")


    pdf.setFont('Helvetica-Bold', 10)
    

    pdf.setFillColor(colors.black)
    pdf.rect(10, 290, 530, 25, fill=1)
    pdf.setFillColor(colors.white)

    pdf.drawString(35, 305, "Qty")
    pdf.drawString(150, 305, "Description")
    pdf.drawString(350, 305, "Unit Price")
    pdf.drawString(470, 305, "Amount")


    pdf.setFillColor(colors.black)
    pdf.setFont('Helvetica', 10)

    pdf.drawString(250, 800, f"Page {page_number}")

    item_list = document["item_list"]
    item_len = len(item_list)

    start_y = 335

    if item_len <= 10:
        # it will spill to another page
        for item in item_list:
            pdf.drawString(40, start_y, str(item["quantity"]))
            pdf.drawString(80, start_y, str(item["name"]))
            pdf.drawRightString(430, start_y, str(item["sales_price"]))
            pdf.drawRightString(535, start_y, str(item["amount"]))
                
            start_y += 20

        pdf.line(10, 290, 10, start_y)
        pdf.line(70, 290, 70, start_y)
        pdf.line(320, 290, 320, start_y)
        pdf.line(450, 290, 450, start_y)
        pdf.line(540, 290, 540, start_y)
        pdf.line(10, start_y, 540, start_y)

        pdf = total_box(pdf, start_y, currency, document_type, document)

    else:
        i = 0
        for item in item_list:
            if i == 22:
                break

            pdf.drawString(40, start_y, str(item["quantity"]))
            pdf.drawString(80, start_y, str(item["name"]))
            pdf.drawRightString(430, start_y, str(item["sales_price"]))
            pdf.drawRightString(535, start_y, str(item["amount"]))
                
            start_y += 20
            i += 1
        
        pdf.line(10, 290, 10, start_y)
        pdf.line(70, 290, 70, start_y)
        pdf.line(320, 290, 320, start_y)
        pdf.line(450, 290, 450, start_y)
        pdf.line(540, 290, 540, start_y)
        pdf.line(10, start_y, 540, start_y)

        pdf, start_y = add_another_page(pdf, item_list[22:], currency, document, document_type)


    
    pdf.save()


    return file_name