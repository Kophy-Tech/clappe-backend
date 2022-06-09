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

    body_color = colors.Color(246/255, 241/255, 211/255)
    pdf.setFillColor(body_color)
    pdf.rect(-30, -30, width=width, height=height, stroke=0, fill=1)


    pdf.setFillColor(colors.black)


    pdf.setFont('Helvetica-Bold', 10)

    pdf.rect(10, 10, 530, 25, fill=0)
    pdf.setFillColor(colors.black)

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

        pdf.setFillColor(colors.black)
        
        for item in item_list:
            pdf.drawString(40, start_y+10, str(item["quantity"]))
            pdf.drawString(80, start_y+10, str(item["name"]))
            pdf.drawRightString(420, start_y+10, str(item["sales_price"]))
            pdf.drawRightString(520, start_y+10, str(item["amount"]))
                
            start_y += 20

        pdf.line(10, 10, 10, start_y)
        pdf.line(70, 10, 70, start_y)
        pdf.line(450, 10, 450, start_y)
        pdf.line(540, 10, 540, start_y)

        pdf = total_box(pdf, start_y, currency, document_type, document, 40)



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


        pdf.line(10, 10, 10, start_y)
        pdf.line(70, 10, 70, start_y)
        pdf.line(450, 10, 450, start_y)
        pdf.line(540, 10, 540, start_y)
        pdf.line(10, start_y, 540, start_y)

        
        pdf, start_y = add_another_page(pdf, item_list[36:], currency, document, document_type)


    return pdf, start_y






def total_box(pdf, start_y, currency, document_type, document, y_start):
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

        pdf.setFillColor(colors.black)
        pdf.setFont('Helvetica-Bold', 20)
        pdf.drawRightString(440, start_y+120, f"{document_type.split(' ')[0].upper()} TOTAL")
        pdf.setFont('Helvetica-Bold', 13)
        pdf.drawRightString(535, start_y+120, f"{currency} {document['grand_total']}")

        pdf.line(10, y_start, 10, start_y+140)
        pdf.line(70, y_start, 70, start_y+140)
        pdf.line(450, y_start, 450, start_y+140)
        pdf.line(540, y_start, 540, start_y+140)

        pdf.drawImage("app/pdf/logo_9_down.png", 170, start_y+140, width=200, height=50)
        
        pdf.line(10, start_y+140, 540, start_y+140)


    else:
        # tax, additional charges, discount_amount
        pdf.drawRightString(440, start_y+20, "Tax")
        pdf.drawRightString(535, start_y+20, f"{document['tax']}")
        pdf.drawRightString(440, start_y+40, "Additional Charges")
        pdf.drawRightString(535, start_y+40, f"{document['add_charges']}")
        pdf.drawRightString(440, start_y+65, "Discount Amount")
        pdf.drawRightString(535, start_y+65, f"{document.get('discount_amount', '0')}")


        pdf.setFillColor(colors.black)
        pdf.setFont('Helvetica-Bold', 20)
        pdf.drawRightString(440, start_y+100, f"{document_type.split(' ')[0].upper()} TOTAL")
        pdf.setFont('Helvetica-Bold', 13)
        pdf.drawRightString(535, start_y+100, f"{currency} {document['grand_total']}")

        pdf.line(10, y_start, 10, start_y+120)
        pdf.line(70, y_start, 70, start_y+120)
        pdf.line(450, y_start, 450, start_y+120)
        pdf.line(540, y_start, 540, start_y+120)

        pdf.drawImage("app/pdf/logo_9_down.png", 170, start_y+120, width=200, height=50)

        pdf.line(10, start_y+120, 540, start_y+120)

    pdf.setFont('Helvetica-Bold', 10)
    pdf.drawString(10, 760, "Terms & Conditions")
    pdf.setFont('Helvetica', 10)
    pdf.drawString(10, 780, document["terms"].capitalize())

    
            
    return pdf
















def get_report_9(buffer, document, currency, document_type, request, logo):

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
    body_color = colors.Color(246/255, 241/255, 211/255)
    pdf.setFillColor(body_color)
    pdf.rect(-30, -30, width=width, height=height, stroke=0, fill=1)
    pdf.drawImage("app/pdf/logo_9_up.png", -30, -30, width=width, height=200)

    # pdf.setFillColor(colors.white)
    # pdf.setFont('Helvetica', 30)
    # pdf.drawRightString(width-55, 15, f"{document_type.title()}")

    pdf.setFont('Helvetica', 20)
    pdf.setFillColor(colors.black)
    pdf.drawCentredString((width-50)/2, 70, request.user.business_name.capitalize())
    pdf.setFont('Helvetica', 10)
    pdf.drawCentredString((width-50)/2, 160, request.user.address.capitalize())
    pdf.drawCentredString((width-50)/2, 175, request.user.email)
    pdf.drawCentredString((width-50)/2, 190, request.user.phone_number)

    pdf.drawImage("app/pdf/logo_9_up_2.png", 150, 200 , width=250, height=50)
    
    pdf.setFont('Helvetica-Bold', 10)
    pdf.drawString(20, 250, "Bill To")
    pdf.drawString(200, 250, "Ship To")
    # pdf.setFillColor(colors.black)
    pdf.setFont('Helvetica', 10)
    pdf = draw_wrapped_line(pdf, document["bill_to"], 20, 20, 270, 10)
    pdf = draw_wrapped_line(pdf, document["ship_to"], 20, 200, 270, 10)

    pdf.setFont('Helvetica-Bold', 10)
    
    pdf.drawString(350, 250, f"{document_type.split(' ')[0].title()} Date")
    pdf.drawString(350, 280, "Due Date")
    pdf.drawString(200, 330, f"{document_type.split(' ')[0].title()} #")
    # pdf.setFillColor(colors.black)
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
    pdf.drawString(270, 330, f"{document[doc_number_key]}")
    pdf.drawRightString(520, 250, f"{document[doc_date_key]}")
    # pdf.setFillColor(colors.black)
    pdf.drawRightString(520, 280, f"{document['due_date']}")


    pdf.setFont('Helvetica-Bold', 10)
    
    # fill_colour = colors.Color(0, 0, 0, 0.04)
    # pdf.setFillColor(fill_colour)
    pdf.rect(10, 365, 530, 25, fill=0)
    pdf.setFillColor(colors.black)

    pdf.drawString(15, 380, "Qty")
    pdf.drawString(150, 380, "Description")
    pdf.drawRightString(420, 380, "Unit Price")
    pdf.drawRightString(520, 380, "Amount")


    # pdf.setFillColor(colors.black)
    pdf.setFont('Helvetica', 10)

    pdf.drawString(250, 800, f"Page {page_number}")

    item_list = document["item_list"]
    item_len = len(item_list)

    start_y = 410

    if item_len <= 15:
        # it will spill to another page


        # pdf.setFillColor(colors.black)
        for item in item_list:
            pdf.drawString(17, start_y, str(item["quantity"]))
            pdf.drawString(80, start_y, str(item["name"]))
            pdf.drawRightString(420, start_y, str(item["sales_price"]))
            pdf.drawRightString(520, start_y, str(item["amount"]))
                
            start_y += 20

        
        pdf.line(10, 365, 10, start_y)
        pdf.line(70, 365, 70, start_y)
        pdf.line(450, 365, 450, start_y)
        pdf.line(540, 365, 540, start_y)
        # pdf.line(10, start_y, 540, start_y)

        pdf = total_box(pdf, start_y, currency, document_type, document, 410)


    else:
        i = 0
        for item in item_list:
            if i == 17:
                break

            pdf.drawString(17, start_y, str(item["quantity"]))
            pdf.drawString(80, start_y, str(item["name"]))
            pdf.drawRightString(420, start_y, str(item["sales_price"]))
            pdf.drawRightString(520, start_y, str(item["amount"]))
                
            start_y += 20
            i += 1

        pdf.line(10, 365, 10, start_y)
        pdf.line(70, 365, 70, start_y)
        pdf.line(450, 365, 450, start_y)
        pdf.line(540, 365, 540, start_y)
        pdf.line(10, start_y, 540, start_y)

        pdf, start_y = add_another_page(pdf, item_list[17:], currency, document, document_type)


    
    pdf.save()


    return file_name