from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from datetime import datetime
import textwrap, requests, os


page_number = 1



def draw_image(pdf, image_url, email, x, y, image_type):
    r = requests.get(image_url)
    if r.status_code == 200:
        with open(f"{email}_{image_type}.png", 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)

        pdf.saveState()
        pdf.rotate(180)
        if image_type == "logo":
            pdf.drawImage(f"{email}_{image_type}.png", -x, -y, 100, 100)
        else:
            pdf.drawImage(f"{email}_{image_type}.png", -x, -y, 160, 50)
        pdf.restoreState()
        
        os.remove(f"{email}_{image_type}.png")

    return pdf





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
    pdf.setLineWidth(1.5)


    pdf.rect(10, 10, 530, 25)
    
    pdf.setFont('Times-Bold', 10)
    pdf.drawString(35, 25, "QTY")
    pdf.drawString(80, 25, "DESCRIPTION")
    pdf.drawString(350, 25, "UNIT PRICE")
    pdf.drawString(470, 25, "AMOUNT")

    pdf.setFont('Times-Roman', 10)
    pdf.drawString(250, 800, f"Page {page_number}")

    item_len = len(item_list)

    start_y = 40

    if item_len <= 22:
        
        for item in item_list:
            pdf.drawString(40, start_y+10, str(item["quantity"]))
            pdf.drawString(80, start_y+10, str(item["name"]))
            pdf.drawRightString(410, start_y+10, str(item["sales_price"]))
            pdf.drawRightString(515, start_y+10, str(item["amount"]))
                
            start_y += 25

        pdf.line(10, 35, 10, start_y)
        pdf.line(540, 35, 540, start_y)
        pdf.line(10, start_y, 540, start_y)



        pdf = total_box(pdf, start_y, currency, document_type, document)

    else:
        i = 0
        for item in item_list:
            if i == 32:
                break

            pdf.drawString(40, start_y+10, str(item["quantity"]))
            pdf.drawString(80, start_y+10, str(item["name"]))
            pdf.drawRightString(410, start_y+10, str(item["sales_price"]))
            pdf.drawRightString(515, start_y+10, str(item["amount"]))
                
            start_y += 25
            i += 1

        pdf.line(10, 35, 10, start_y)
        pdf.line(540, 35, 540, start_y)
        pdf.line(10, start_y, 540, start_y)
        
        pdf, start_y = add_another_page(pdf, item_list[32:], currency, document, document_type)


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
        pdf.drawRightString(535, start_y+85, f"{document['discount_amount']}")

        pdf.setFillColor(colors.black)
        pdf.setLineWidth(3)
        pdf.rect(10, start_y+100, 530, 40)
        pdf.setFont('Times-Roman', 25)
        pdf.drawString(20, start_y+125, "TOTAL")
        pdf.drawRightString(535, start_y+125, f"{currency} {document['grand_total']}")
        


    else:
        # tax, additional charges, discount_amount
        pdf.drawRightString(440, start_y+20, "Tax")
        pdf.drawRightString(535, start_y+20, f"{document['tax']}")
        pdf.drawRightString(440, start_y+40, "Additional Charges")
        pdf.drawRightString(535, start_y+40, f"{document['add_charges']}")
        pdf.drawRightString(440, start_y+65, "Discount Amount")
        pdf.drawRightString(535, start_y+65, f"{document['discount_amount']}")

        pdf.setFillColor(colors.black)
        pdf.setLineWidth(3)
        pdf.rect(10, start_y+100, 530, 40)
        pdf.setFont('Times-Roman', 25)
        pdf.drawString(20, start_y+125, "TOTAL")
        pdf.drawRightString(535, start_y+125, f"{currency} {document['grand_total']}")


    pdf.setFont('Times-Bold', 10)
    pdf.drawString(10, 750, "Terms   &    Conditions")
    pdf.setFillColor(colors.black)
    pdf.setFont('Times-Roman', 10)
    pdf = draw_wrapped_line(pdf, document["terms"].title(), 100, 10, 765, 15)
            
    return pdf

























def get_report_8(buffer, document, currency, document_type, request):

    now = datetime.now().strftime("%Y-%m-%d %H-%M-%S")

    file_name = f"{document_type.title()} for {request.user.email} - {now}.pdf"

    # create file
    pdf = canvas.Canvas(buffer, bottomup=0)
    pdf.translate(cm, cm)
    pdf.setPageSize((A4[0], A4[1]))

    width = pdf._pagesize[0]
    pdf.setTitle(document_type.title())


    pdf.setLineWidth(1.5)

    if request.user.logo_path:
        pdf = draw_image(pdf, request.user.logo_path, request.user.email, 540, 100, "logo")
            


    pdf.setFont('Helvetica', 40)
    pdf.saveState()
    pdf.rotate(180)
    pdf.drawImage("app/pdf/logo_8.png", -200, -25, 200, 30)
    pdf.restoreState()

    pdf.drawString(10, 60, f"{document_type.lower()}")

    pdf.setFont('Times-Roman', 13)
    pdf.drawString(10, 110, "FROM")
    pdf.setFont('Times-Bold', 10)
    pdf = draw_wrapped_line(pdf, request.user.business_name.title(), 100, 10, 130, 10)
    pdf.setFont('Times-Roman', 10)
    pdf = draw_wrapped_line(pdf, request.user.address.capitalize(), 100, 10, 145, 10)
    pdf = draw_wrapped_line(pdf, request.user.email, 100, 10, 160, 10)
    pdf = draw_wrapped_line(pdf, request.user.phone_number, 100, 10, 175, 10)


    
    pdf.setFont('Times-Roman', 15)
    pdf.drawString(10, 200, "BILL TO")
    pdf.drawString(190, 200, "SHIP TO")
    pdf.setFont('Times-Roman', 10)
    pdf = draw_wrapped_line(pdf, document["bill_to"], 40, 10, 225, 10)
    pdf = draw_wrapped_line(pdf, document["ship_to"], 40, 190, 225, 10)


    pdf.setFont('Times-Roman', 15)
    pdf.drawRightString(470, 140, f"{document_type.upper()} #")
    pdf.drawRightString(470, 160, f"{document_type.upper()} DATE")
    pdf.drawRightString(470, 180, "DUE DATE")

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

    pdf.setFont('Times-Roman', 10)

    pdf.drawRightString(width - 55, 140, f"{document[doc_number_key]}")
    pdf.drawRightString(width - 55, 160, f"{document[doc_date_key]}")
    pdf.drawRightString(width - 55, 180, f"{document['due_date']}")


    pdf.setFont('Times-Bold', 10)
    
    fill_colour = colors.Color(0, 0, 0, 0.04)
    pdf.setFillColor(fill_colour)
    pdf.setFillColor(colors.black)

    pdf.rect(10, 280, 530, 30)
    pdf.setFont('Times-Bold', 10)
    pdf.drawString(35, 300, "QTY")
    pdf.drawString(80, 300, "DESCRIPTION")
    pdf.drawString(350, 300, "UNIT PRICE")
    pdf.drawString(470, 300, "AMOUNT")

    pdf.setFont('Times-Roman', 10)

    pdf.drawString(250, 800, f"Page {page_number}")

    item_list = document["item_list"]
    item_len = len(item_list)

    start_y = 335

    if item_len <= 10:
        # it will spill to another page
        for item in item_list:
            pdf.drawString(40, start_y, str(item["quantity"]))
            pdf.drawString(80, start_y, str(item["name"]))
            pdf.drawRightString(410, start_y, str(item["sales_price"]))
            pdf.drawRightString(515, start_y, str(item["amount"]))

            if item != item_list[-1]:
                pdf.line(10, start_y+10, 540, start_y+10)
                
            start_y += 25

        pdf.line(10, 300, 10, start_y)
        pdf.line(540, 300, 540, start_y)
        pdf.line(10, start_y, 540, start_y)



        pdf = total_box(pdf, start_y, currency, document_type, document)

    else:
        i = 0
        for item in item_list:
            if i == 18:
                break

            pdf.drawString(40, start_y, str(item["quantity"]))
            pdf.drawString(80, start_y, str(item["name"]))
            pdf.drawRightString(410, start_y, str(item["sales_price"]))
            pdf.drawRightString(515, start_y, str(item["amount"]))

            if item != item_list[-1]:
                pdf.line(10, start_y+10, 540, start_y+10)
                
            start_y += 25
            i += 1
    
        pdf.line(10, 300, 10, start_y)
        pdf.line(540, 300, 540, start_y)
        pdf.line(10, start_y, 540, start_y)

        pdf, start_y = add_another_page(pdf, item_list[18:], currency, document, document_type)


    
    pdf.save()


    return file_name