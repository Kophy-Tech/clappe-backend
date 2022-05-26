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
    pdf.setLineWidth(0.5)

    width = pdf._pagesize[0]
    height = pdf._pagesize[1]

    body_color = colors.Color(254/255,244/255,247/255)
    pdf.setFillColor(body_color)
    pdf.rect(-30, -30, width=width, height=height, stroke=0, fill=1)


    pdf.setFillColor(colors.black)


    pdf.setFont('Helvetica-Bold', 10)

    pdf.drawString(35, 25, "Qty")
    pdf.drawString(150, 25, "Description")
    pdf.drawRightString(420, 25, "Unit Price")
    pdf.drawRightString(520, 25, "Amount")

    pdf.setFillColor(colors.black)

    pdf.setFont('Helvetica', 10)
    pdf.drawString(250, 800, f"Page {page_number}")

    item_len = len(item_list)

    start_y = 40

    if item_len <= 20:

        fake_start_y = 40
        for _ in item_list:
            fake_start_y += 20

        pdf = total_box(pdf, fake_start_y, currency, document_type, document)

        pdf.setFillColor(colors.black)
        
        for item in item_list:
            pdf.drawString(40, start_y+10, str(item["quantity"]))
            pdf.drawString(80, start_y+10, str(item["name"]))
            pdf.drawRightString(420, start_y+10, str(item["sales_price"]))
            pdf.drawRightString(520, start_y+10, str(item["amount"]))
                
            start_y += 20



        # pdf = total_box(pdf, start_y, currency, document_type, document)

    else:
        i = 0
        for item in item_list:
            if i == 36:
                break

            pdf.drawString(40, start_y+10, str(item["quantity"]))
            pdf.drawString(80, start_y+10, str(item["name"]))
            pdf.drawRightString(420, start_y+10, str(item["sales_price"]))
            pdf.drawRightString(520, start_y+10, str(item["amount"]))
                
            start_y += 20
            i += 1

        
        pdf, start_y = add_another_page(pdf, item_list[36:], currency, document, document_type)


    return pdf, start_y






def total_box(pdf, start_y, currency, document_type, document):
    pdf.drawImage("app/pdf/logo_42_down.png", -35, 415, width=610, height=400)
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
        pdf.setFont('Helvetica-Bold', 20)
        pdf.drawRightString(440, start_y+120, "Total")
        pdf.setFont('Helvetica-Bold', 15)
        pdf.drawRightString(535, start_y+120, f"{currency} {document['grand_total']}")
        


    else:
        # tax, additional charges, discount_amount
        pdf.drawRightString(440, start_y+20, "Tax")
        pdf.drawRightString(535, start_y+20, f"{document['tax']}")
        pdf.drawRightString(440, start_y+40, "Additional Charges")
        pdf.drawRightString(535, start_y+40, f"{document['add_charges']}")
        pdf.drawRightString(440, start_y+65, "Discount Amount")
        pdf.drawRightString(535, start_y+65, f"{document['discount_amount']}")


        pdf.setFillColor(colors.black)
        pdf.setFont('Helvetica-Bold', 20)
        pdf.drawRightString(440, start_y+100, "Total")
        pdf.setFont('Helvetica-Bold', 15)
        pdf.drawRightString(535, start_y+100, f"{currency} {document['grand_total']}")

    pdf.setFillColor(colors.white)
    pdf.setFont('Helvetica', 10)
    pdf.drawString(10, 680, document["terms"].capitalize())

    
            
    return pdf
















def get_report_42(buffer, document, currency, document_type, request):

    now = datetime.now().strftime("%Y-%m-%d %H-%M-%S")

    file_name = f"{document_type.title()} for {request.user.email} - {now}.pdf"

    # create file
    pdf = canvas.Canvas(buffer, bottomup=0)
    pdf.translate(cm, cm)
    pdf.setPageSize((A4[0], A4[1]))

    width = pdf._pagesize[0]
    height = pdf._pagesize[1]

    
    pdf.setTitle(document_type.title())


    pdf.setLineWidth(0.5)
    body_color = colors.Color(254/255,244/255,247/255)
    pdf.setFillColor(body_color)
    pdf.rect(-30, -30, width=width, height=height, stroke=0, fill=1)
    pdf.drawImage("app/pdf/logo_42_up.png", -30, -30, width=600, height=360)

    fill_color = colors.Color(250/255, 166/255, 74/255)

    pdf.setFillColor(colors.white)
    pdf.setFont('Helvetica', 30)
    pdf.drawRightString(width-55, 15, f"{document_type.title()}")

    pdf.setFont('Helvetica', 10)
    pdf.setFillColor(colors.black)
    pdf = draw_wrapped_line(pdf, request.user.business_name.title(), 100, 110, 150, 10)
    pdf.setFont('Helvetica', 10)
    pdf = draw_wrapped_line(pdf, request.user.address.capitalize(), 30, 110, 160, 10)
    pdf = draw_wrapped_line(pdf, request.user.email, 100, 110, 200, 10)
    pdf = draw_wrapped_line(pdf, request.user.phone_number, 100, 110, 210, 10)
    
    pdf.setFont('Helvetica-Bold', 10)
    pdf.setFillColor(fill_color)
    pdf.drawString(110, 130, "From")
    pdf.drawString(250, 130, "Bill To")
    pdf.drawString(390, 130, "Ship To")
    pdf.setFillColor(colors.black)
    pdf.setFont('Helvetica', 10)
    pdf = draw_wrapped_line(pdf, document["bill_to"], 20, 250, 150, 10)
    pdf = draw_wrapped_line(pdf, document["ship_to"], 20, 390, 150, 10)

    pdf.setFont('Helvetica-Bold', 10)
    pdf.setFillColor(fill_color)
    
    pdf.drawString(200, 70, f"{document_type.split(' ')[0].title()} #")
    pdf.drawString(300, 70, f"{document_type.split(' ')[0].title()} Date")
    pdf.drawString(400, 70, "Due Date")
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

    # pdf.setFillColor(colors.white)
    pdf.drawString(200, 85, f"{document[doc_number_key]}")
    pdf.drawString(300, 85, f"{document[doc_date_key]}")
    pdf.setFillColor(colors.black)
    pdf.drawString(400, 85, f"{document['due_date']}")


    pdf.setFont('Helvetica-Bold', 10)
    
    pdf.setFillColor(fill_color)

    pdf.drawString(15, 250, "Qty")
    pdf.drawString(150, 250, "Description")
    pdf.drawRightString(420, 250, "Unit Price")
    pdf.drawRightString(520, 250, "Amount")


    pdf.setFillColor(colors.black)
    pdf.setFont('Helvetica', 10)

    pdf.drawString(250, 800, f"Page {page_number}")

    item_list = document["item_list"]
    item_len = len(item_list)

    start_y = 280

    if item_len <= 15:
        # it will spill to another page
        fake_start_y = 280
        for _ in item_list:
            fake_start_y += 20

        pdf = total_box(pdf, fake_start_y, currency, document_type, document)

        pdf.setFillColor(colors.black)
        for item in item_list:
            pdf.drawString(17, start_y, str(item["quantity"]))
            pdf.drawString(80, start_y, str(item["name"]))
            pdf.drawRightString(420, start_y, str(item["sales_price"]))
            pdf.drawRightString(520, start_y, str(item["amount"]))
                
            start_y += 20



    else:
        i = 0
        for item in item_list:
            if i == 23:
                break

            pdf.drawString(17, start_y, str(item["quantity"]))
            pdf.drawString(80, start_y, str(item["name"]))
            pdf.drawRightString(420, start_y, str(item["sales_price"]))
            pdf.drawRightString(520, start_y, str(item["amount"]))
                
            start_y += 20
            i += 1


        pdf, start_y = add_another_page(pdf, item_list[23:], currency, document, document_type)


    
    pdf.save()


    return file_name