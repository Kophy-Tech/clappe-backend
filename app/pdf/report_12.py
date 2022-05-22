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
    pdf.setLineWidth(2)
    width = pdf._pagesize[0]
    
    pdf.drawImage("app/pdf/logo_12.png", -30, -30, width=185, height=850)

    bold_color = colors.Color(42/255, 96/255, 153/255)
    stroke_color = colors.Color(162/255, 72/255, 128/255)


    pdf.setFillColor(bold_color)
    pdf.setStrokeColor(stroke_color)
    
    pdf.setFont('Helvetica-Bold', 10)

    pdf.setFillColor(bold_color)
    pdf.setLineWidth(2)
    pdf.setStrokeColor(stroke_color)
    pdf.line(10, 10, 540, 10)
    pdf.line(10, 40, 540, 40)
    pdf.setStrokeColor(colors.black)

    pdf.drawString(10, 30, "QTY")
    pdf.drawString(130, 30, "DESCRIPTION")
    pdf.drawRightString(400, 30, "UNIT PRICE")
    pdf.drawRightString(width-60, 30, "AMOUNT")


    #     pdf.setFillColor(bold_color)
    pdf.setLineWidth(2)
    # pdf.setStrokeColor(stroke_color)
    # pdf.line(10, 230, 540, 230)
    # pdf.line(10, 258, 540, 258)
    # pdf.setStrokeColor(colors.black)

    # pdf.drawString(10, 247, "QTY")
    # pdf.drawString(130, 247, "DESCRIPTION")
    # pdf.drawRightString(400, 247, "UNIT PRICE")
    # pdf.drawRightString(width-60, 247, "AMOUNT")

    pdf.setFillColor(colors.black)

    pdf.setFont('Helvetica', 10)
    pdf.drawString(250, 800, f"Page {page_number}")

    item_len = len(item_list)

    start_y = 55

    if item_len <= 20:
        
        for item in item_list:
            pdf.drawString(15, start_y+10, str(item["quantity"]))
            pdf.drawString(70, start_y+10, str(item["name"]))
            pdf.drawRightString(400, start_y+10, str(item["sales_price"]))
            pdf.drawRightString(width-60, start_y+10, str(item["amount"]))
                
            start_y += 20



        pdf = total_box(pdf, start_y, currency, document_type, document)

    else:
        i = 0
        for item in item_list:
            if i == 36:
                break

            pdf.drawString(15, start_y+10, str(item["quantity"]))
            pdf.drawString(70, start_y+10, str(item["name"]))
            pdf.drawRightString(400, start_y+10, str(item["sales_price"]))
            pdf.drawRightString(width-60, start_y+10, str(item["amount"]))
                
            start_y += 20
            i += 1


        
        pdf, start_y = add_another_page(pdf, item_list[36:], currency, document, document_type)


    return pdf, start_y






def total_box(pdf, start_y, currency, document_type, document):
    bold_color = colors.Color(42/255, 96/255, 153/255)
    stroke_color = colors.Color(162/255, 72/255, 128/255)
    pdf.setLineWidth(2)
    pdf.setStrokeColor(stroke_color)
    pdf.line(10, start_y, 540, start_y)
    pdf.setStrokeColor(colors.black)
    if document_type == "invoice":
        # it will have sub total
        pdf.drawRightString(400, start_y+20, "Subtotal")
        pdf.drawRightString(535, start_y+20, f"{document['sub_total']}")
        # tax, additional charges, discount_amount
        pdf.drawRightString(400, start_y+40, "Tax")
        pdf.drawRightString(535, start_y+40, f"{document['tax']}")
        pdf.drawRightString(400, start_y+60, "Additional Charges")
        pdf.drawRightString(535, start_y+60, f"{document['add_charges']}")
        pdf.drawRightString(400, start_y+85, "Discount Amount")
        pdf.drawRightString(535, start_y+85, f"{document['discount_amount']}")

        pdf.setFillColor(bold_color)
        # pdf.rect(120, start_y+95, 530, 35, fill=1, stroke=0)
        pdf.setFont('Helvetica-Bold', 15)
        # pdf.setFillColor(colors.white)
        pdf.drawRightString(400, start_y+120, "TOTAL")

        pdf.drawRightString(535, start_y+120, f"{currency} {document['grand_total']}")
        


    else:
        # tax, additional charges, discount_amount
        pdf.drawRightString(400, start_y+20, "Tax")
        pdf.drawRightString(535, start_y+20, f"{document['tax']}")
        pdf.drawRightString(400, start_y+40, "Additional Charges")
        pdf.drawRightString(535, start_y+40, f"{document['add_charges']}")
        pdf.drawRightString(400, start_y+65, "Discount Amount")
        pdf.drawRightString(535, start_y+65, f"{document['discount_amount']}")

        pdf.setFillColor(bold_color)
        # pdf.rect(120, start_y+75, 530, 35, fill=1, stroke=0)
        pdf.setFont('Helvetica-Bold', 15)
        # pdf.setFillColor(colors.white)
        pdf.drawRightString(400, start_y+100, "TOTAL")

        pdf.drawRightString(535, start_y+100, f"{currency} {document['grand_total']}")

    pdf.setFont('Helvetica-Bold', 10)
    pdf.setFillColor(bold_color)
    pdf.drawString(10, 750, "Terms & Conditions")
    pdf.setFillColor(colors.black)
    pdf.setFont('Helvetica', 10)
    pdf = draw_wrapped_line(pdf, document["terms"].title(), 300, 10, 765, 15)

            
    return pdf
















def get_report_12(buffer, document, currency, document_type, request):

    now = datetime.now().strftime("%Y-%m-%d %H-%M-%S")

    file_name = f"{document_type.title()} for {request.user.email} - {now}.pdf"

    # create file
    pdf = canvas.Canvas(buffer, bottomup=0)
    pdf.translate(cm, cm)
    pdf.setPageSize((A4[0], A4[1]))

    width = pdf._pagesize[0]
    pdf.setTitle(document_type.title())


    

    pdf.drawImage("app/pdf/logo_12.png", -30, -30, width=185, height=850)

    bold_color = colors.Color(42/255, 96/255, 153/255)
    stroke_color = colors.Color(162/255, 72/255, 128/255)

    if request.user.logo_path:
        pdf = draw_image(pdf, request.user.logo_path, request.user.email, 540, 100, "logo")


    pdf.setFont('Helvetica-Bold', 35)
    pdf.setFillColor(bold_color)
    pdf.drawString(10, 30, document_type.upper())

    
    pdf.setFillColor(colors.black)
    pdf.setFont('Helvetica-Bold', 15)
    pdf = draw_wrapped_line(pdf, request.user.business_name.title(), 100, 10, 80, 10)
    pdf.setFont('Helvetica', 10)
    pdf.setFillColor(colors.black)
    pdf.setFont('Helvetica', 10)
    pdf = draw_wrapped_line(pdf, request.user.address.capitalize(), 300, 10, 95, 10)
    pdf = draw_wrapped_line(pdf, request.user.email, 100, 10, 110, 10)
    pdf = draw_wrapped_line(pdf, request.user.phone_number, 100, 10, 125, 10)

    pdf.setStrokeColor(bold_color)

    pdf.setFont('Helvetica-Bold', 10)
    pdf.setFillColor(bold_color)
    pdf.drawString(10, 170, "BILL TO")
    pdf.drawString(200, 170, "SHIP TO")
    pdf.setFillColor(colors.black)
    pdf.setFont('Helvetica', 9)
    pdf = draw_wrapped_line(pdf, document["bill_to"], 30, 10, 185, 10)
    pdf = draw_wrapped_line(pdf, document["ship_to"], 30, 200, 185, 10)

    pdf.setFont('Helvetica-Bold', 10)
    pdf.setFillColor(bold_color)
    pdf.drawRightString(450, 170, f"{document_type.split(' ')[0].upper()} #")
    pdf.drawRightString(450, 190, f"{document_type.split(' ')[0].upper()} DATE")
    pdf.drawRightString(450, 210, "DUE DATE")
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

    pdf.setFont('Helvetica', 8)

    pdf.drawRightString(width - 55, 170, f"{document[doc_number_key]}")
    pdf.drawRightString(width - 55, 190, f"{document[doc_date_key]}")
    pdf.drawRightString(width - 55, 210, f"{document['due_date']}")


    

    pdf.setFont('Helvetica-Bold', 10)
    
    pdf.setFillColor(bold_color)
    pdf.setLineWidth(2)
    pdf.setStrokeColor(stroke_color)
    pdf.line(10, 230, 540, 230)
    pdf.line(10, 258, 540, 258)
    pdf.setStrokeColor(colors.black)

    pdf.drawString(10, 247, "QTY")
    pdf.drawString(130, 247, "DESCRIPTION")
    pdf.drawRightString(400, 247, "UNIT PRICE")
    pdf.drawRightString(width-60, 247, "AMOUNT")


    pdf.setFillColor(colors.black)
    pdf.setFont('Helvetica', 10)

    pdf.drawString(250, 800, f"Page {page_number}")

    item_list = document["item_list"]
    item_len = len(item_list)

    start_y = 280

    if item_len <= 10:
        # it will spill to another page
        for item in item_list:
            pdf.drawString(15, start_y, str(item["quantity"]))
            pdf.drawString(70, start_y, str(item["name"]))
            pdf.drawRightString(400, start_y, str(item["sales_price"]))
            pdf.drawRightString(width-60, start_y, str(item["amount"]))
                
            start_y += 20

        pdf = total_box(pdf, start_y, currency, document_type, document)

    else:
        i = 0
        for item in item_list:
            if i == 23:
                break

            pdf.drawString(15, start_y, str(item["quantity"]))
            pdf.drawString(70, start_y, str(item["name"]))
            pdf.drawRightString(400, start_y, str(item["sales_price"]))
            pdf.drawRightString(width-60, start_y, str(item["amount"]))
                
            start_y += 20
            i += 1


        pdf, start_y = add_another_page(pdf, item_list[23:], currency, document, document_type)


    
    pdf.save()


    return file_name