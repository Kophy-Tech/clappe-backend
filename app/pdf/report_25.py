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

    blue_color = colors.Color(165/255, 243/255, 253/155)
    yellow_color = colors.Color(253/255, 247/255, 155/255)


    pdf.setFont('Helvetica', 10)

    pdf.setFillColor(blue_color)
    pdf.rect(40, 10, width=450, height=30, stroke=0, fill=1)
    pdf.setFillColor(colors.black)

    pdf.drawString(60, 25, "Qty")
    pdf.drawString(200, 25, "Description")
    pdf.drawRightString(400, 25, "Unit Price")
    pdf.drawRightString(485, 25, "Amount")

    pdf.setStrokeColor(colors.white)
    pdf.line(90, 10, 90, 40)
    pdf.line(345, 10, 345, 40)
    pdf.line(410, 10, 410, 40)

    pdf.setStrokeColor(colors.black)

    pdf.setFillColor(colors.black)

    pdf.setFont('Helvetica', 10)
    pdf.drawString(250, 800, f"Page {page_number}")

    item_len = len(item_list)

    start_y = 50

    if item_len <= 20:
        
        for item in item_list:
            pdf.drawString(60, start_y+10, str(item["quantity"]))
            pdf.drawString(200, start_y+10, str(item["name"]))
            pdf.drawRightString(400, start_y+10, str(item["sales_price"]))
            pdf.drawRightString(485, start_y+10, str(item["amount"]))
                
            start_y += 20



        pdf = total_box(pdf, start_y, currency, document_type, document)

    else:
        i = 0
        for item in item_list:
            if i == 36:
                break

            pdf.drawString(60, start_y+10, str(item["quantity"]))
            pdf.drawString(200, start_y+10, str(item["name"]))
            pdf.drawRightString(400, start_y+10, str(item["sales_price"]))
            pdf.drawRightString(485, start_y+10, str(item["amount"]))
                
            start_y += 20
            i += 1

        
        pdf, start_y = add_another_page(pdf, item_list[36:], currency, document, document_type)


    return pdf, start_y






def total_box(pdf, start_y, currency, document_type, document):
    pdf.drawImage("app/pdf/logo_25_down.png", -35, 515, width=610, height=300)

    if document_type == "invoice":
        # it will have sub total
        pdf.drawRightString(400, start_y+20, "Subtotal")
        pdf.drawRightString(485, start_y+20, f"{document['sub_total']}")
        # tax, additional charges, discount_amount
        pdf.drawRightString(400, start_y+40, "Tax")
        pdf.drawRightString(485, start_y+40, f"{document['tax']}")
        pdf.drawRightString(400, start_y+60, "Additional Charges")
        pdf.drawRightString(485, start_y+60, f"{document['add_charges']}")
        pdf.drawRightString(400, start_y+85, "Discount Amount")
        pdf.drawRightString(485, start_y+85, f"{document.get('discount_amount', '0')}")

        pdf.setFillColor(colors.black)
        pdf.setFont('Helvetica-Bold', 20)
        pdf.drawRightString(400, start_y+120, f"{document_type.title()} Total")
        pdf.setFont('Helvetica-Bold', 15)
        pdf.drawRightString(485, start_y+120, f"{currency} {document['grand_total']}")
        


    else:
        # tax, additional charges, discount_amount
        pdf.drawRightString(400, start_y+20, "Tax")
        pdf.drawRightString(485, start_y+20, f"{document['tax']}")
        pdf.drawRightString(400, start_y+40, "Additional Charges")
        pdf.drawRightString(485, start_y+40, f"{document['add_charges']}")
        pdf.drawRightString(400, start_y+65, "Discount Amount")
        pdf.drawRightString(485, start_y+65, f"{document.get('discount_amount', '0')}")


        pdf.setFillColor(colors.black)
        pdf.setFont('Helvetica', 20)
        pdf.drawRightString(400, start_y+100, f"{document_type.title()} Total")
        # pdf.setFont('Helvetica', 15)
        pdf.drawRightString(485, start_y+100, f"{currency} {document['grand_total']}")

    pdf.setFillColor(colors.black)
    pdf.setFont('Helvetica', 10)
    pdf.drawString(10, 680, "Terms & Conditions")
    pdf.drawString(10, 700, document["terms"].capitalize())
    # pdf.drawRightString(540, 790, document[doc_number_key])

    
            
    return pdf
















def get_report_25(buffer, document, currency, document_type, request):

    now = datetime.now().strftime("%Y-%m-%d %H-%M-%S")

    file_name = f"{document_type.title()} for {request.user.email} - {now}.pdf"

    # create file
    pdf = canvas.Canvas(buffer, bottomup=0)
    pdf.translate(cm, cm)
    pdf.setPageSize((A4[0], A4[1]))

    width = pdf._pagesize[0]
    
    pdf.setTitle(document_type.title())


    pdf.setLineWidth(1.5)

    blue_color = colors.Color(165/255, 243/255, 253/155)
    yellow_color = colors.Color(253/255, 247/255, 155/255)
            


    pdf.setFont('Helvetica-Bold', 20)
    pdf.setFillColor(colors.black)
    
    pdf.setFillColor(blue_color)
    pdf.rect(120, 18, 300, 30, fill=1, stroke=0)
    pdf.setFillColor(colors.black)
    pdf.drawCentredString(270, 40, request.user.business_name.title())
    pdf.setFont('Helvetica', 10)
    pdf.drawCentredString(270, 70, request.user.address.capitalize())
    pdf.drawCentredString(270, 85, request.user.email)
    pdf.drawCentredString(270, 100, request.user.phone_number)


    pdf.setFillColor(yellow_color)
    pdf.rect(40, 130, width=450, height=30, stroke=0, fill=1)
    # pdf.setFillColor(colors.black)
    
    pdf.setFont('Helvetica', 10)
    pdf.setFillColor(colors.black)
    pdf.drawString(45, 150, "Bill To")
    pdf.drawString(185, 150, "Ship To")
    pdf.setFillColor(colors.black)
    pdf.setFont('Helvetica', 10)
    pdf = draw_wrapped_line(pdf, document["bill_to"], 30, 45, 175, 10)
    pdf = draw_wrapped_line(pdf, document["ship_to"], 30, 185, 175, 10)

    pdf.setFont('Helvetica', 10)
    # pdf.setFillColor(colors.white)
    
    pdf.setFillColor(colors.black)
    pdf.drawRightString(400, 150, f"{document_type.split(' ')[0].title()} #")
    pdf.drawRightString(400, 175, f"{document_type.split(' ')[0].title()} Date")
    pdf.drawRightString(400, 195, "Due Date")
    pdf.setFillColor(colors.black)
    pdf.setFont('Helvetica', 10)

    pdf.setStrokeColor(colors.white)
    pdf.line(180, 130, 180, 160)
    pdf.line(320, 130, 320, 160)
    pdf.line(405, 130, 405, 160)

    pdf.setStrokeColor(colors.black)

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

    pdf.setFillColor(colors.black)
    pdf.drawRightString(485, 150, f"{document[doc_number_key]}")
    pdf.drawRightString(485, 170, f"{document[doc_date_key]}")
    pdf.drawRightString(485, 190, f"{document['due_date']}")
    # pdf.drawString(250, 220, f"{document['due_date']}")


    # pdf.setFont('Helvetica', 10)
    
    pdf.setFillColor(blue_color)
    pdf.rect(40, 240, width=450, height=30, stroke=0, fill=1)
    pdf.setFillColor(colors.black)
    pdf.drawString(60, 260, "Qty")
    pdf.drawString(200, 260, "Description")
    pdf.drawRightString(400, 260, "Unit Price")
    pdf.drawRightString(485, 260, "Amount")

    pdf.setStrokeColor(colors.white)
    pdf.line(90, 240, 90, 270)
    pdf.line(345, 240, 345, 270)
    pdf.line(410, 240, 410, 270)

    pdf.setStrokeColor(colors.black)


    # pdf.setFillColor(colors.black)
    # pdf.setFont('Helvetica', 10)

    pdf.drawString(250, 800, f"Page {page_number}")

    item_list = document["item_list"]
    item_len = len(item_list)

    start_y = 290

    if item_len <= 10:
        # it will spill to another page
        for item in item_list:
            pdf.drawString(60, start_y, str(item["quantity"]))
            pdf.drawString(110, start_y, str(item["name"]))
            pdf.drawRightString(400, start_y, str(item["sales_price"]))
            pdf.drawRightString(485, start_y, str(item["amount"]))
                
            start_y += 20


        pdf = total_box(pdf, start_y, currency, document_type, document)

    else:
        i = 0
        for item in item_list:
            if i == 23:
                break

            pdf.drawString(60, start_y, str(item["quantity"]))
            pdf.drawString(110, start_y, str(item["name"]))
            pdf.drawRightString(400, start_y, str(item["sales_price"]))
            pdf.drawRightString(485, start_y, str(item["amount"]))
                
            start_y += 20
            i += 1


        pdf, start_y = add_another_page(pdf, item_list[23:], currency, document, document_type)


    
    pdf.save()


    return file_name