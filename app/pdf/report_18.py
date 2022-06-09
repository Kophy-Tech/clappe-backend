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

    fill_color = colors.Color(16/255, 154/255, 179/255)

    # another page
    pdf.showPage()
    pdf.translate(cm, cm)
    pdf.setPageSize((A4[0], A4[1]))

    width = pdf._pagesize[0]

    pdf.setFillColor(fill_color)
    pdf.setStrokeColor(fill_color)
    pdf.setLineWidth(1.5)
    pdf.line(10, 5, 540, 5)
    pdf.setFont('Helvetica', 10)


    pdf.drawString(10, 25, "DESCRIPTION")
    pdf.drawRightString(330, 25, "UNIT PRICE")
    pdf.drawString(400, 25, "QTY")
    pdf.drawRightString(width-55, 25, "AMOUNT")

    pdf.setStrokeColor(colors.black)

    pdf.setLineWidth(1.5)
    pdf.setFont('Helvetica', 10)
    pdf.setFillColor(colors.black)
    pdf.drawString(250, 800, f"Page {page_number}")

    item_len = len(item_list)

    start_y = 40

    if item_len <= 20:
        
        for item in item_list:
            pdf.drawString(10, start_y+10, str(item["name"]))
            pdf.drawRightString(330, start_y+10, str(item["sales_price"]))
            pdf.drawString(410, start_y+10, str(item["quantity"]))
            pdf.drawRightString(width-55, start_y+10, str(item["amount"]))
                
            start_y += 20

        pdf = total_box(pdf, start_y, currency, document_type, document)

    else:
        i = 0
        for item in item_list:
            if i == 36:
                break

            pdf.drawString(10, start_y+10, str(item["name"]))
            pdf.drawRightString(330, start_y+10, str(item["sales_price"]))
            pdf.drawString(410, start_y+10, str(item["quantity"]))
            pdf.drawRightString(width-55, start_y+10, str(item["amount"]))
                
            start_y += 20
            i += 1
        
        pdf, start_y = add_another_page(pdf, item_list[36:], currency, document, document_type)


    return pdf, start_y






def total_box(pdf, start_y, currency, document_type, document):
    fill_color = colors.Color(16/255, 154/255, 179/255)
    if document_type == "invoice":
        # it will have sub total
        pdf.setFillColor(fill_color)
        pdf.drawRightString(440, start_y+20, "SUBTOTAL")
        pdf.drawRightString(440, start_y+40, "Tax")
        pdf.drawRightString(440, start_y+60, "Additional Charges")
        pdf.drawRightString(440, start_y+85, "Discount Amount")
        pdf.setFont('Helvetica', 15)
        pdf.drawRightString(440, start_y+120, "TOTAL")
        pdf.setFont('Helvetica', 10)
        pdf.setFillColor(colors.black)
        pdf.drawRightString(535, start_y+20, f"{document['sub_total']}")
        pdf.drawRightString(535, start_y+40, f"{document['tax']}")
        pdf.drawRightString(535, start_y+60, f"{document['add_charges']}")
        pdf.drawRightString(535, start_y+85, f"{document.get('discount_amount', '0')}")

        pdf.setFont('Helvetica', 13)
        pdf.drawRightString(535, start_y+120, f"{currency} {document['grand_total']}")
        


    else:

        # tax, additional charges, discount_amount
        pdf.setFillColor(fill_color)
        pdf.drawRightString(440, start_y+20, "Tax")
        pdf.drawRightString(440, start_y+40, "Additional Charges")
        pdf.drawRightString(440, start_y+65, "Discount Amount")
        pdf.setFont('Helvetica', 15)
        pdf.drawRightString(440, start_y+100, "TOTAL")
        pdf.setFont('Helvetica', 10)
        pdf.setFillColor(colors.black)
        pdf.drawRightString(535, start_y+20, f"{document['tax']}")
        pdf.drawRightString(535, start_y+40, f"{document['add_charges']}")
        pdf.drawRightString(535, start_y+65, f"{document.get('discount_amount', '0')}")

        pdf.setFont('Helvetica', 13)
        pdf.drawRightString(535, start_y+100, f"{currency} {document['grand_total']}")

    pdf.setFont('Helvetica-Bold', 10)
    fill_color = colors.Color(0, 0, 0, 0.4)
    pdf.setFillColor(fill_color)
    pdf.drawString(10, 750, "TERMS & CONDITION")
    pdf.setFillColor(colors.black)
    pdf.setFont('Helvetica', 10)
    pdf = draw_wrapped_line(pdf, document["terms"].title(), 100, 10, 765, 15)
            
    return pdf

























def get_report_18(buffer, document, currency, document_type, request, logo):

    now = datetime.now().strftime("%Y-%m-%d %H-%M-%S")

    file_name = f"{document_type.title()} for {request.user.email} - {now}.pdf"

    # create file
    pdf = canvas.Canvas(buffer, bottomup=0)
    pdf.translate(cm, cm)
    pdf.setPageSize((A4[0], A4[1]))

    width = pdf._pagesize[0]
    pdf.setTitle(document_type.title())

    fill_color = colors.Color(16/255, 154/255, 179/255)


    pdf.setLineWidth(1.5)
    
    pdf.setFillColor(fill_color)
    pdf.rect(-30, -30, 600, 150, stroke=0, fill=1)
    pdf.setFillColor(colors.white)
    pdf.setFont('Helvetica', 25)
    pdf.drawString(0, 50, document_type.upper())

    pdf.setFont('Helvetica', 10)
    pdf.drawRightString(470, 20, f"{document_type.title()} #")
    pdf.drawRightString(470, 40, f"{document_type.title()} Date")
    pdf.drawRightString(470, 60, "Due Date")

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

    pdf.drawRightString(width - 55, 20, f"{document[doc_number_key]}")
    pdf.drawRightString(width - 55, 40, f"{document[doc_date_key]}")
    pdf.drawRightString(width - 55, 60, f"{document['due_date']}")


    pdf.setFillColor(colors.black)

    fill_color = colors.Color(16/255, 154/255, 179/255)
    pdf.setFillColor(fill_color)
    pdf.drawString(10, 150, "FROM")
    pdf.drawString(140, 150, "BILL TO")
    pdf.drawString(280, 150, "SHIP TO")
    pdf.drawRightString(width-55, 150, f"{document_type.upper()} TOTAL")
    pdf.setFillColor(colors.black)
    pdf.setFont('Helvetica', 10)
    pdf = draw_wrapped_line(pdf, request.user.business_name.title(), 20, 10, 170, 10)
    pdf = draw_wrapped_line(pdf, request.user.address.capitalize(), 100, 10, 180, 10)
    pdf = draw_wrapped_line(pdf, request.user.phone_number, 100, 10, 190, 10)
    pdf = draw_wrapped_line(pdf, document["bill_to"], 25, 140, 170, 10)
    pdf = draw_wrapped_line(pdf, document["ship_to"], 25, 280, 170, 10)
    pdf.setFont('Helvetica', 20)
    pdf.setFillColor(fill_color)
    pdf.drawRightString(width-55, 180, f"{currency} {document['grand_total']}")


    pdf.setFont('Helvetica', 10)
    
    pdf.setLineWidth(1.5)
    pdf.setStrokeColor(fill_color)

    pdf.line(10, 230, 540, 230)

    pdf.drawString(10, 250, "DESCRIPTION")
    pdf.drawRightString(330, 250, "UNIT PRICE")
    pdf.drawString(400, 250, "QTY")
    pdf.drawRightString(width-55, 250, "AMOUNT")

    pdf.setFillColor(colors.black)

    pdf.drawString(250, 800, f"Page {page_number}")

    item_list = document["item_list"]
    item_len = len(item_list)

    start_y = 270

    if item_len <= 20:
        # it will spill to another page
        for item in item_list:
            pdf.drawString(10, start_y, str(item["name"]))
            pdf.drawRightString(330, start_y, str(item["sales_price"]))
            pdf.drawString(410, start_y, str(item["quantity"]))
            pdf.drawRightString(width-55, start_y, str(item["amount"]))
                
            start_y += 20

        pdf = total_box(pdf, start_y, currency, document_type, document)

    else:
        i = 0
        for item in item_list:
            if i == 23:
                break

            pdf.drawString(10, start_y, str(item["name"]))
            pdf.drawRightString(330, start_y, str(item["sales_price"]))
            pdf.drawString(410, start_y, str(item["quantity"]))
            pdf.drawRightString(width-55, start_y, str(item["amount"]))
                
            start_y += 20
            i += 1

        pdf, start_y = add_another_page(pdf, item_list[23:], currency, document, document_type)


    
    pdf.save()


    return file_name