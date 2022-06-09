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
    pdf.setLineWidth(0.1)


    fill_colour = colors.Color(61/255, 205/255, 33/255)
    
    pdf.setFont('Helvetica-Bold', 10)
    
    
    pdf.setFillColor(fill_colour)
    pdf.rect(10, 10, 530, 25, fill=1, stroke=0)
    pdf.setFillColor(colors.white)

    pdf.drawString(35, 25, "QTY")
    pdf.drawString(90, 25, "DESCRIPTION")
    pdf.drawRightString(400, 25, "UNIT PRICE")
    pdf.drawRightString(535, 25, "AMOUNT")

    pdf.setFont('Helvetica', 10)
    pdf.setFillColor(colors.black)
    pdf.drawString(250, 800, f"Page {page_number}")

    item_len = len(item_list)

    start_y = 50

    stroke_color = colors.Color(0, 0, 0, 0.1)
    pdf.setStrokeColor(stroke_color)

    if item_len <= 20:
        
        for item in item_list:
            pdf.drawString(40, start_y+10, str(item["quantity"]))
            pdf.drawString(90, start_y+10, str(item["name"]))
            pdf.drawRightString(400, start_y+10, str(item["sales_price"]))
            pdf.drawRightString(535, start_y+10, str(item["amount"]))
            pdf.line(10, start_y+15, 540, start_y+15)
                
            start_y += 25

        pdf = total_box(pdf, start_y, currency, document_type, document)

    else:
        i = 0
        for item in item_list:
            if i == 36:
                break

            pdf.drawString(40, start_y+10, str(item["quantity"]))
            pdf.drawString(90, start_y+10, str(item["name"]))
            pdf.drawRightString(400, start_y+10, str(item["sales_price"]))
            pdf.drawRightString(535, start_y+10, str(item["amount"]))

            pdf.line(10, start_y+15, 540, start_y+15)
                
            start_y += 25
            i += 1

        
        pdf, start_y = add_another_page(pdf, item_list[36:], currency, document, document_type)


    return pdf, start_y






def total_box(pdf, start_y, currency, document_type, document):
    fill_colour = colors.Color(61/255, 205/255, 33/255)
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
        pdf.setFont('Helvetica-Bold', 23)
        pdf.drawString(10, start_y+120, f"{document_type.split(' ')[0].upper()} TOTAL")
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
        pdf.setFont('Helvetica-Bold', 23)
        pdf.drawString(10, start_y+100, f"{document_type.split(' ')[0].upper()} TOTAL")
        pdf.drawRightString(535, start_y+100, f"{currency} {document['grand_total']}")


    pdf.setFont('Helvetica-Bold', 10)
    pdf.setFillColor(fill_colour)
    pdf.drawString(10, 750, "Terms & Conditions")
    pdf.setFillColor(colors.black)
    pdf.setFont('Helvetica', 10)
    pdf = draw_wrapped_line(pdf, document["terms"].title(), 100, 10, 765, 15)
            
    return pdf

























def get_report_30(buffer, document, currency, document_type, request, logo):

    now = datetime.now().strftime("%Y-%m-%d %H-%M-%S")

    file_name = f"{document_type.title()} for {request.user.email} - {now}.pdf"

    # create file
    pdf = canvas.Canvas(buffer, bottomup=0)
    pdf.translate(cm, cm)
    pdf.setPageSize((A4[0], A4[1]))

    width = pdf._pagesize[0]
    pdf.setTitle(document_type.title())

    fill_colour = colors.Color(61/255, 205/255, 33/255)
    pdf.setLineWidth(1.5)
    pdf.setStrokeColor(fill_colour)
    pdf.setFillColor(fill_colour)
            

    pdf.setFont('Helvetica', 10)

    pdf.rect(10, 0, 350, 50)
    
    pdf.drawString(15, 15, f"{document_type.split(' ')[0].upper()} #")
    pdf.drawString(200, 15, f"{document_type.split(' ')[0].upper()} DATE")
    pdf.drawString(15, 40, "DUE DATE")

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

    pdf.setFillColor(colors.black)

    pdf.drawString(95, 15, f"{document[doc_number_key]}")
    pdf.drawString(300, 15, f"{document[doc_date_key]}")
    pdf.drawString(85, 40, f"{document['due_date']}")


    
    pdf.setFont('Helvetica-Bold', 10)
    pdf.setFillColor(fill_colour)
    pdf.drawString(10, 100, "BILL TO")
    pdf.drawString(190, 100, "SHIP TO")
    pdf.setFillColor(colors.black)
    pdf.setFont('Helvetica', 10)
    pdf = draw_wrapped_line(pdf, document["bill_to"], 40, 10, 115, 10)
    pdf = draw_wrapped_line(pdf, document["ship_to"], 40, 190, 115, 10)


    pdf.setFont('Helvetica-Bold', 10)
    pdf.drawRightString(width-55, 100, request.user.business_name.title())
    pdf.setFont('Helvetica', 10)
    pdf = draw_wrapped_line(pdf, request.user.address.capitalize(), 40, 380, 120, 10)
    pdf.drawRightString(width-55, 150, request.user.email)
    pdf.drawRightString(width-55, 165, request.user.phone_number)




    pdf.setFont('Helvetica-Bold', 10)
    
    
    pdf.setFillColor(fill_colour)
    pdf.rect(10, 190, 530, 25, fill=1, stroke=0)
    pdf.setFillColor(colors.white)

    pdf.drawString(35, 205, "QTY")
    pdf.drawString(90, 205, "DESCRIPTION")
    pdf.drawRightString(400, 205, "UNIT PRICE")
    pdf.drawRightString(535, 205, "AMOUNT")

    pdf.setFont('Helvetica', 10)

    pdf.setFillColor(colors.black)

    pdf.drawString(250, 800, f"Page {page_number}")

    item_list = document["item_list"]
    item_len = len(item_list)

    start_y = 235
    stroke_color = colors.Color(0, 0, 0, 0.1)
    pdf.setStrokeColor(stroke_color)

    if item_len <= 20:
        # it will spill to another page
        for item in item_list:
            pdf.drawString(35, start_y, str(item["quantity"]))
            pdf.drawString(90, start_y, str(item["name"]))
            pdf.drawRightString(400, start_y, str(item["sales_price"]))
            pdf.drawRightString(535, start_y, str(item["amount"]))

            pdf.line(10, start_y+9, 540, start_y+9)
                
            start_y += 25

        pdf = total_box(pdf, start_y, currency, document_type, document)

    else:
        i = 0
        for item in item_list:
            if i == 22:
                break

            pdf.drawString(35, start_y, str(item["quantity"]))
            pdf.drawString(90, start_y, str(item["name"]))
            pdf.drawRightString(400, start_y, str(item["sales_price"]))
            pdf.drawRightString(535, start_y, str(item["amount"]))

            pdf.line(10, start_y+9, 540, start_y+9)
                
            start_y += 25
            i += 1
        

        pdf, start_y = add_another_page(pdf, item_list[22:], currency, document, document_type)


    
    pdf.save()


    return file_name