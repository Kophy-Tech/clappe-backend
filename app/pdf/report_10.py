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
    pdf.setPageSize((A4[0]+15, A4[1]))
    pdf.setLineWidth(0.1)


    fill_colour = colors.Color(0, 0, 0, 0.04)
    pdf.setFillColor(fill_colour)
    pdf.rect(10, 10, 530, 25, fill=1)
    pdf.setFillColor(colors.black)

    pdf.drawString(35, 25, "QTY")
    pdf.drawString(150, 25, "DESCRIPTION")
    pdf.drawString(350, 25, "UNIT PRICE")
    pdf.drawString(470, 25, "AMOUNT")

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
    fill_colour = colors.Color(0, 0, 0, 0.04)
    if document_type == "invoice":
        pdf.rect(450, start_y, 90, 95)
        # it will have sub total
        pdf.drawRightString(440, start_y+20, "Subtotal")
        pdf.drawRightString(535, start_y+20, f"{document['sub_total']}")
        pdf.line(450, start_y+25, 540, start_y+25)
        # tax, additional charges, discount_amount
        pdf.drawRightString(440, start_y+40, "Tax")
        pdf.drawRightString(535, start_y+40, f"{document['tax']}")
        pdf.line(450, start_y+50, 540, start_y+50)
        pdf.drawRightString(440, start_y+60, "Additional Charges")
        pdf.drawRightString(535, start_y+60, f"{document['add_charges']}")
        pdf.line(450, start_y+70, 540, start_y+70)
        pdf.drawRightString(440, start_y+85, "Discount Amount")
        pdf.drawRightString(535, start_y+85, f"{document['discount_amount']}")

        pdf.setFillColor(fill_colour)
        pdf.rect(450, start_y+95, 90, 35, fill=1)
        pdf.setFillColor(colors.black)
        pdf.setFont('Helvetica-Bold', 20)
        pdf.drawRightString(440, start_y+120, "Total")
        pdf.setFont('Helvetica-Bold', 15)
        pdf.drawRightString(535, start_y+120, f"{currency} {document['grand_total']}")
        


    else:
        pdf.rect(450, start_y, 90, 75)
        # tax, additional charges, discount_amount
        pdf.drawRightString(440, start_y+20, "Tax")
        pdf.drawRightString(535, start_y+20, f"{document['tax']}")
        pdf.line(450, start_y+25, 540, start_y+25)
        pdf.drawRightString(440, start_y+40, "Additional Charges")
        pdf.drawRightString(535, start_y+40, f"{document['add_charges']}")
        pdf.line(450, start_y+50, 540, start_y+50)
        pdf.drawRightString(440, start_y+65, "Discount Amount")
        pdf.drawRightString(535, start_y+65, f"{document['discount_amount']}")

        pdf.setFillColor(fill_colour)
        pdf.rect(450, start_y+75, 90, 35, fill=1)
        pdf.setFillColor(colors.black)
        pdf.setFont('Helvetica-Bold', 20)
        pdf.drawRightString(440, start_y+100, "Total")
        pdf.setFont('Helvetica-Bold', 15)
        pdf.drawRightString(535, start_y+100, f"{currency} {document['grand_total']}")


    pdf.setFont('Helvetica-Bold', 10)
    pdf.drawString(10, 750, "Terms & Conditions")
    pdf.setFont('Helvetica', 10)
    pdf = draw_wrapped_line(pdf, document["terms"].title(), 100, 10, 765, 15)
            
    return pdf

























def get_report_10(buffer, document, currency, document_type, request):

    now = datetime.now().strftime("%Y-%m-%d %H-%M-%S")

    file_name = f"{document_type.title()} for {request.user.email} - {now}.pdf"

    # create file
    pdf = canvas.Canvas(buffer, bottomup=0)
    pdf.translate(cm, cm)
    pdf.setPageSize((A4[0], A4[1]))

    width = pdf._pagesize[0]
    pdf.setTitle(document_type.title())


    pdf.setLineWidth(0.1)

    if request.user.logo_path:
        pdf = draw_image(pdf, request.user.logo_path, request.user.email, 540, 140, "logo")
            


    pdf.setFont('Helvetica-Bold', 20)
    pdf.setFillColor(colors.ReportLabFidBlue)
    # pdf.setStrokeColor(colors.white)
    pdf.rect(0, 0, 550, 25, stroke=0, fill=1)
    pdf.setFillColor(colors.white)
    pdf = draw_wrapped_line(pdf, document["customer"]["business_name"].title(), 100, 10, 20, 10)
    pdf.drawRightString(width - 55, 20, f"{document_type.upper()}")
    pdf.setFillColor(colors.black)
    # pdf.setStrokeColor(colors.black)
    pdf.setFont('Helvetica', 10)
    pdf = draw_wrapped_line(pdf, document["customer"]["address"].capitalize(), 100, 10, 40, 10)
    pdf = draw_wrapped_line(pdf, document["customer"]["email"], 100, 10, 55, 10)
    pdf = draw_wrapped_line(pdf, document["customer"]["phone_number"], 100, 10, 70, 10)


    
    pdf.setFont('Helvetica-Bold', 10)
    pdf.drawString(10, 170, "Bill To")
    pdf.drawString(190, 170, "Ship To")
    pdf.setFont('Helvetica', 10)
    pdf = draw_wrapped_line(pdf, document["bill_to"], 40, 10, 185, 10)
    pdf = draw_wrapped_line(pdf, document["ship_to"], 40, 190, 185, 10)



    pdf.drawRightString(470, 170, f"{document_type.title()} #")
    pdf.drawRightString(470, 190, f"{document_type.title()} Date")
    pdf.drawRightString(470, 210, "Due Date")

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

    pdf.drawRightString(width - 55, 170, f"{document[doc_number_key]}")
    pdf.drawRightString(width - 55, 190, f"{document[doc_date_key]}")
    pdf.drawRightString(width - 55, 210, f"{document['due_date']}")


    pdf.setFont('Helvetica-Bold', 10)
    
    fill_colour = colors.Color(0, 0, 0, 0.04)
    pdf.setFillColor(fill_colour)
    pdf.rect(10, 230, 530, 25, fill=1)
    pdf.setFillColor(colors.black)

    pdf.drawString(35, 245, "QTY")
    pdf.drawString(150, 245, "DESCRIPTION")
    pdf.drawString(350, 245, "UNIT PRICE")
    pdf.drawString(470, 245, "AMOUNT")

    pdf.setFont('Helvetica', 10)

    pdf.drawString(250, 800, f"Page {page_number}")

    item_list = document["item_list"]
    item_len = len(item_list)

    start_y = 275

    if item_len <= 20:
        # it will spill to another page
        for item in item_list:
            pdf.drawString(40, start_y, str(item["quantity"]))
            pdf.drawString(80, start_y, str(item["name"]))
            pdf.drawRightString(430, start_y, str(item["sales_price"]))
            pdf.drawRightString(535, start_y, str(item["amount"]))
                
            start_y += 20

        pdf.line(10, 230, 10, start_y)
        pdf.line(70, 230, 70, start_y)
        pdf.line(320, 230, 320, start_y)
        pdf.line(450, 230, 450, start_y)
        pdf.line(540, 230, 540, start_y)
        pdf.line(10, start_y, 540, start_y)



        pdf = total_box(pdf, start_y, currency, document_type, document)

    else:
        i = 0
        for item in item_list:
            if i == 23:
                break

            pdf.drawString(40, start_y, str(item["quantity"]))
            pdf.drawString(80, start_y, str(item["name"]))
            pdf.drawRightString(430, start_y, str(item["sales_price"]))
            pdf.drawRightString(535, start_y, str(item["amount"]))
                
            start_y += 20
            i += 1
        
        pdf.line(10, 230, 10, start_y)
        pdf.line(70, 230, 70, start_y)
        pdf.line(320, 230, 320, start_y)
        pdf.line(450, 230, 450, start_y)
        pdf.line(540, 230, 540, start_y)
        pdf.line(10, start_y, 540, start_y)

        if item_len > 23:
            pdf, start_y = add_another_page(pdf, item_list[23:], currency, document, document_type)


    
    pdf.save()


    return file_name