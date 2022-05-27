from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfbase.pdfmetrics import stringWidth
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
    pdf.setLineWidth(0.1)
    width = pdf._pagesize[0]

    pdf.drawImage("app/pdf/logo_1_body.png", -30, -30, width=width, height=300)
    pdf.drawImage("app/pdf/logo_1_body.png", -30, 250, width=width, height=300)
    pdf.drawImage("app/pdf/logo_1_body.png", -30, 530, width=width, height=300)

    
    other_color = colors.Color(144/255, 147/255, 161/255)

    pdf.drawImage("app/pdf/logo_1_table.png", 10, 10, width=510, height=35)
    
    pdf.setFillColor(other_color)
    pdf.setFont('Helvetica', 10)
    pdf.drawString(250, 800, f"Page {page_number}")

    item_len = len(item_list)

    start_y = 50

    if item_len <= 20:
        
        for item in item_list:
            pdf.drawString(30, start_y+10, str(item["quantity"]))
            pdf.drawString(120, start_y+10, str(item["name"]))
            pdf.drawRightString(380, start_y+10, str(item["sales_price"]))
            pdf.drawRightString(507, start_y+10, str(item["amount"]))
                
            start_y += 20


        pdf = total_box(pdf, start_y, currency, document_type, document)

    else:
        i = 0
        for item in item_list:
            if i == 36:
                break

            pdf.drawString(30, start_y+10, str(item["quantity"]))
            pdf.drawString(120, start_y+10, str(item["name"]))
            pdf.drawRightString(380, start_y+10, str(item["sales_price"]))
            pdf.drawRightString(507, start_y+10, str(item["amount"]))
                
            start_y += 20
            i += 1
    

        
        pdf, start_y = add_another_page(pdf, item_list[36:], currency, document, document_type)


    return pdf, start_y






def total_box(pdf, start_y, currency, document_type, document):
    other_color = colors.Color(144/255, 147/255, 161/255)
    fill_colour = colors.Color(213/255, 85/255, 43/255)
    width = pdf._pagesize[0]
    
    if document_type == "invoice":
        # it will have sub total
        pdf.setFillColor(other_color)
        pdf.drawRightString(380, start_y+20, "Subtotal")
        pdf.drawRightString(380, start_y+40, "Tax")
        pdf.drawRightString(380, start_y+60, "Additional Charges")
        pdf.drawRightString(380, start_y+85, "Discount Amount")

        # tax, additional charges, discount_amount
        pdf.drawRightString(507, start_y+20, f"{document['sub_total']}")
        pdf.drawRightString(507, start_y+40, f"{document['tax']}")
        pdf.drawRightString(507, start_y+60, f"{document['add_charges']}")
        pdf.drawRightString(507, start_y+85, f"{document.get('discount_amount', '0')}")


        pdf.setFillColor(fill_colour)
        pdf.setFont('Helvetica-Bold', 20)
        pdf.drawRightString(380, start_y+125, "TOTAL")
        pdf.setFont('Helvetica-Bold', 15)
        pdf.drawRightString(507, start_y+125, f"{currency} {document['grand_total']}")
        


    else:
        # tax, additional charges, discount_amount
        pdf.setFillColor(other_color)
        pdf.drawRightString(380, start_y+20, "Tax")
        pdf.drawRightString(380, start_y+40, "Additional Charges")
        pdf.drawRightString(380, start_y+65, "Discount Amount")

        pdf.drawRightString(507, start_y+20, f"{document['tax']}")
        pdf.drawRightString(507, start_y+40, f"{document['add_charges']}")
        pdf.drawRightString(507, start_y+65, f"{document.get('discount_amount', '0')}")

        
        pdf.setFillColor(fill_colour)
        pdf.setFont('Helvetica-Bold', 20)
        pdf.drawRightString(380, start_y+105, "TOTAL")
        pdf.setFont('Helvetica-Bold', 15)
        pdf.drawRightString(507, start_y+105, f"{currency} {document['grand_total']}")



    pdf.drawImage("app/pdf/logo_1_down.png", -10, 700, width=560, height=100)
    pdf.setFont('Helvetica', 10)
    pdf.setFillColor(other_color)
    pdf = draw_wrapped_line(pdf, document["terms"].title(), 100, 30, 765, 15)
    pdf.drawString(250, 800, f"Page {page_number}")
            
    return pdf

























def get_report_1(buffer, document, currency, document_type, request):

    now = datetime.now().strftime("%Y-%m-%d %H-%M-%S")

    file_name = f"{document_type.title()} for {request.user.email} - {now}.pdf"

    # create file
    pdf = canvas.Canvas(buffer, bottomup=0)
    pdf.translate(cm, cm)
    pdf.setPageSize((A4[0], A4[1]))

    width = pdf._pagesize[0]
    pdf.setTitle(document_type.title())

    pdf.drawImage("app/pdf/logo_1_body.png", -30, -30, width=width, height=300)
    pdf.drawImage("app/pdf/logo_1_body.png", -30, 250, width=width, height=300)
    pdf.drawImage("app/pdf/logo_1_body.png", -30, 530, width=width, height=300)


    pdf.setLineWidth(0.1)
            

    
    fill_colour = colors.Color(213/255, 85/255, 43/255)
    other_color = colors.Color(144/255, 147/255, 161/255)

    document_string_width = stringWidth(f"{document_type.upper()}", "Helvetica-Bold", 40)
    pdf.drawImage("app/pdf/logo_1_star.png", 270 - (document_string_width/2) - 60, -5, 40, 40)
    pdf.setFont('Helvetica-Bold', 40)
    pdf.drawCentredString(270, 30, f"{document_type.upper()}")
    pdf.drawImage("app/pdf/logo_1_star.png", 270 + (document_string_width/2) + 20, -5, 40, 40)


    pdf.setFillColor(fill_colour)
    business_string_width = stringWidth(request.user.business_name.upper(), "Helvetica-Bold", 20)
    address_string_width = stringWidth(request.user.address.capitalize(), "Helvetica", 10)
    width_to_use = business_string_width if business_string_width > address_string_width else address_string_width

    pdf.drawImage("app/pdf/logo_1_gun_left.png", 270 - (width_to_use/2)-150, 35, width=150, height=70)
    pdf.setFont('Helvetica-Bold', 20)
    pdf.drawCentredString(270, 60, request.user.business_name.title())
    pdf.setFont('Helvetica-Bold', 10)

    pdf.drawCentredString(270, 80, request.user.address.capitalize())
    pdf.drawCentredString(270, 95, request.user.email)
    pdf.drawCentredString(270, 110, request.user.phone_number)
    pdf.drawImage("app/pdf/logo_1_gun_right.png", 270 + (width_to_use/2), 40, width=150, height=60)

    
    pdf.drawImage("app/pdf/logo_1_line.png", 10, 130, width=200, height=15)
    pdf.drawImage("app/pdf/logo_1_line.png", 340, 130, width=170, height=15)

    pdf.drawString(10, 160, "BILL TO")
    pdf.drawString(200, 160, "SHIP TO")
    pdf.drawString(350, 160, f"{document_type.split(' ')[0].upper()} #")
    pdf.drawString(350, 180, f"{document_type.split(' ')[0].upper()} DATE")
    pdf.drawString(350, 200, "DUE DATE")

    
    pdf.setFont('Helvetica', 10)
    pdf.setFillColor(other_color)
    pdf = draw_wrapped_line(pdf, document["bill_to"], 35, 10, 180, 10)
    pdf = draw_wrapped_line(pdf, document["ship_to"], 30, 200, 180, 10)


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

    pdf.drawRightString(width - 85, 160, f"{document[doc_number_key]}")
    pdf.drawRightString(width - 85, 180, f"{document[doc_date_key]}")
    pdf.drawRightString(width - 85, 200, f"{document['due_date']}")

    pdf.setFont('Helvetica', 10)

    pdf.drawString(250, 800, f"Page {page_number}")


    pdf.drawImage("app/pdf/logo_1_table.png", 10, 230, width=510, height=35)


    item_list = document["item_list"]
    item_len = len(item_list)

    start_y = 280

    if item_len <= 20:
        # it will spill to another page
        for item in item_list:
            pdf.drawString(30, start_y, str(item["quantity"]))
            pdf.drawString(120, start_y, str(item["name"]))
            pdf.drawRightString(380, start_y, str(item["sales_price"]))
            pdf.drawRightString(507, start_y, str(item["amount"]))

            

            start_y += 20


        pdf = total_box(pdf, start_y, currency, document_type, document)

    else:
        i = 0
        for item in item_list:
            if i == 23:
                break

            pdf.drawString(30, start_y, str(item["quantity"]))
            pdf.drawString(120, start_y, str(item["name"]))
            pdf.drawRightString(380, start_y, str(item["sales_price"]))
            pdf.drawRightString(507, start_y, str(item["amount"]))
                
            start_y += 20
            i += 1


        pdf, start_y = add_another_page(pdf, item_list[23:], currency, document, document_type)


    
    pdf.save()


    return file_name