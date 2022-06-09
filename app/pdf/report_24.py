from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from datetime import datetime
import textwrap


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
    width = pdf._pagesize[0]
    height = pdf._pagesize[1]

    for i in range(0, int(height), 150):
        pdf.drawImage("app/pdf/logo_24_star.png", 20, 20+i, 100, 100)
        pdf.drawImage("app/pdf/logo_24_star.png", 300, 20+i, 100, 100)
        pdf.drawImage("app/pdf/logo_24_star.png", 150, 100+i, 100, 100)
        pdf.drawImage("app/pdf/logo_24_star.png", 450, 100+i, 100, 100)


    fill_colour = colors.Color(34/255, 64/255, 103/255)
    stroke_colour = colors.Color(114/255, 159/255, 207/255)


    pdf.setFillColor(fill_colour)
    pdf.setStrokeColor(stroke_colour)
    
    pdf.setFont('Helvetica-Bold', 10)

    pdf.setLineWidth(2)
    pdf.line(10, 5, 540, 5)
    pdf.line(10, 35, 540, 35)
    pdf.setLineWidth(1)

    pdf.drawString(35, 25, "QTY")
    pdf.drawString(150, 25, "DESCRIPTION")
    pdf.drawRightString(420, 25, "UNIT PRICE")
    pdf.drawRightString(width-60, 25, "AMOUNT")

    pdf.setFillColor(colors.black)

    pdf.setFont('Helvetica', 10)
    pdf.drawString(250, 800, f"Page {page_number}")

    item_len = len(item_list)

    start_y = 40

    if item_len <= 20:
        
        for item in item_list:
            pdf.drawString(40, start_y+10, str(item["quantity"]))
            pdf.drawString(80, start_y+10, str(item["name"]))
            pdf.drawRightString(420, start_y+10, str(item["sales_price"]))
            pdf.drawRightString(535, start_y+10, str(item["amount"]))
                
            start_y += 20



        pdf = total_box(pdf, start_y, currency, document_type, document)

    else:
        i = 0
        for item in item_list:
            if i == 36:
                break

            pdf.drawString(40, start_y+10, str(item["quantity"]))
            pdf.drawString(80, start_y+10, str(item["name"]))
            pdf.drawRightString(420, start_y+10, str(item["sales_price"]))
            pdf.drawRightString(535, start_y+10, str(item["amount"]))
                
            start_y += 20
            i += 1


        
        pdf, start_y = add_another_page(pdf, item_list[36:], currency, document, document_type)


    return pdf, start_y






def total_box(pdf, start_y, currency, document_type, document):
    fill_colour = colors.Color(34/255, 64/255, 103/255)
    width = pdf._pagesize[0]
    pdf.drawImage("app/pdf/logo_24_down.png", -30, 525, width=width, height=290)
    pdf.drawImage("app/pdf/logo_24_star.png", 150, 510, 100, 100)
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

        pdf.setFillColor(fill_colour)
        pdf.setFont('Helvetica-Bold', 13)
        pdf.drawRightString(440, start_y+120, "TOTAL")
        pdf.drawRightString(535, start_y+120, f"{currency} {document['grand_total']}")
        


    else:
        # tax, additional charges, discount_amount
        pdf.drawRightString(440, start_y+20, "Tax")
        pdf.drawRightString(535, start_y+20, f"{document['tax']}")
        pdf.drawRightString(440, start_y+40, "Additional Charges")
        pdf.drawRightString(535, start_y+40, f"{document['add_charges']}")
        pdf.drawRightString(440, start_y+65, "Discount Amount")
        pdf.drawRightString(535, start_y+65, f"{document.get('discount_amount', '0')}")

        pdf.setFillColor(fill_colour)
        pdf.setFont('Helvetica-Bold', 13)
        pdf.drawRightString(440, start_y+100, "TOTAL")
        pdf.drawRightString(535, start_y+100, f"{currency} {document['grand_total']}")

    pdf.setFillColor(colors.black)
    pdf.setFont('Helvetica', 10)
    pdf = draw_wrapped_line(pdf, document["terms"].title(), 100, 15, 720, 15)
    pdf.drawString(250, 800, f"Page {page_number}")

            
    return pdf
















def get_report_24(buffer, document, currency, document_type, request, logo):

    now = datetime.now().strftime("%Y-%m-%d %H-%M-%S")

    file_name = f"{document_type.title()} for {request.user.email} - {now}.pdf"

    # create file
    pdf = canvas.Canvas(buffer, bottomup=0)
    pdf.translate(cm, cm)
    pdf.setPageSize((A4[0], A4[1]))

    width = pdf._pagesize[0]
    height = pdf._pagesize[1]
    pdf.setTitle(document_type.title())

    for i in range(0, int(height), 150):
        pdf.drawImage("app/pdf/logo_24_star.png", 20, 20+i, 100, 100)
        pdf.drawImage("app/pdf/logo_24_star.png", 300, 20+i, 100, 100)
        pdf.drawImage("app/pdf/logo_24_star.png", 150, 100+i, 100, 100)
        pdf.drawImage("app/pdf/logo_24_star.png", 450, 100+i, 100, 100)


    fill_colour = colors.Color(34/255, 64/255, 103/255)
    stroke_colour = colors.Color(114/255, 159/255, 207/255)

    pdf.setFillColor(fill_colour)
    pdf.setFont('Helvetica-Bold', 30)
    pdf.drawString(10, 20, f"{document_type.upper()}")



    pdf.setFont('Helvetica-Bold', 15)
    
    pdf.setFillColor(colors.black)
    pdf = draw_wrapped_line(pdf, request.user.business_name.title(), 100, 10, 60, 10)
    pdf.setFont('Helvetica', 10)
    pdf = draw_wrapped_line(pdf, request.user.address.capitalize(), 150, 10, 75, 10)
    pdf = draw_wrapped_line(pdf, request.user.email, 100, 10, 88, 10)
    pdf = draw_wrapped_line(pdf, request.user.phone_number, 100, 10, 101, 10)

    pdf.setStrokeColor(fill_colour)

    pdf.setFont('Helvetica-Bold', 10)
    pdf.setFillColor(fill_colour)
    pdf.drawString(10, 170, "BILL TO")
    pdf.drawString(190, 170, "SHIP TO")
    pdf.setFillColor(colors.black)
    pdf.setFont('Helvetica', 10)
    pdf = draw_wrapped_line(pdf, document["bill_to"], 40, 10, 190, 10)
    pdf = draw_wrapped_line(pdf, document["ship_to"], 40, 190, 190, 10)

    pdf.setFont('Helvetica-Bold', 10)
    pdf.setFillColor(fill_colour)
    pdf.drawRightString(470, 170, f"{document_type.split(' ')[0].upper()} #")
    pdf.drawRightString(470, 190, f"{document_type.split(' ')[0].upper()} DATE")
    pdf.drawRightString(470, 210, "DUE DATE")
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

    pdf.drawRightString(width - 55, 170, f"{document[doc_number_key]}")
    pdf.drawRightString(width - 55, 190, f"{document[doc_date_key]}")
    pdf.drawRightString(width - 55, 210, f"{document['due_date']}")


    

    pdf.setFont('Helvetica-Bold', 10)
    pdf.setStrokeColor(stroke_colour)
    
    pdf.setFillColor(fill_colour)
    pdf.setLineWidth(2)
    pdf.line(10, 230, 540, 230)
    pdf.line(10, 260, 540, 260)
    pdf.setLineWidth(1)

    pdf.drawString(35, 250, "QTY")
    pdf.drawString(150, 250, "DESCRIPTION")
    pdf.drawRightString(420, 250, "UNIT PRICE")
    pdf.drawRightString(width-60, 250, "AMOUNT")


    pdf.setFillColor(colors.black)
    pdf.setFont('Helvetica', 10)

    pdf.drawString(250, 800, f"Page {page_number}")

    item_list = document["item_list"]
    item_len = len(item_list)

    start_y = 280

    if item_len <= 10:
        # it will spill to another page
        for item in item_list:
            pdf.drawString(40, start_y, str(item["quantity"]))
            pdf.drawString(80, start_y, str(item["name"]))
            pdf.drawRightString(420, start_y, str(item["sales_price"]))
            pdf.drawRightString(535, start_y, str(item["amount"]))
                
            start_y += 20

        pdf = total_box(pdf, start_y, currency, document_type, document)

    else:
        i = 0
        for item in item_list:
            if i == 23:
                break

            pdf.drawString(40, start_y, str(item["quantity"]))
            pdf.drawString(80, start_y, str(item["name"]))
            pdf.drawRightString(420, start_y, str(item["sales_price"]))
            pdf.drawRightString(535, start_y, str(item["amount"]))
                
            start_y += 20
            i += 1


        pdf, start_y = add_another_page(pdf, item_list[23:], currency, document, document_type)


    
    pdf.save()


    return file_name