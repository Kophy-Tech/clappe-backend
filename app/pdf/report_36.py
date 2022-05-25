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
    pdf.setLineWidth(0.1)
    width = pdf._pagesize[0]

    pdf.drawImage("app/pdf/logo_36_table.png", -13, -20, width=width-30, height=130)


    

    pdf.setFont('Helvetica', 10)
    pdf.drawString(250, 800, f"Page {page_number}")

    item_len = len(item_list)

    start_y = 60

    if item_len <= 20:
        
        for item in item_list:
            pdf.drawString(40, start_y+10, str(item["quantity"]))
            pdf.drawString(120, start_y+10, str(item["name"]))
            pdf.drawRightString(410, start_y+10, str(item["sales_price"]))
            pdf.drawRightString(507, start_y+10, str(item["amount"]))
                
            start_y += 20


        pdf = total_box(pdf, start_y, currency, document_type, document)

    else:
        i = 0
        for item in item_list:
            if i == 36:
                break

            pdf.drawString(40, start_y+10, str(item["quantity"]))
            pdf.drawString(120, start_y+10, str(item["name"]))
            pdf.drawRightString(410, start_y+10, str(item["sales_price"]))
            pdf.drawRightString(507, start_y+10, str(item["amount"]))
                
            start_y += 20
            i += 1
    

        
        pdf, start_y = add_another_page(pdf, item_list[36:], currency, document, document_type)


    return pdf, start_y






def total_box(pdf, start_y, currency, document_type, document):
    fill_colour = colors.Color(254/255, 224/255, 89/255)
    width = pdf._pagesize[0]
    pdf.drawImage("app/pdf/logo_36_down.png", -35, 595, width=width+10, height=220)
    if document_type == "invoice":
        # it will have sub total
        pdf.setFillColor(fill_colour)
        pdf.drawRightString(410, start_y+20, "Subtotal")
        pdf.drawRightString(410, start_y+40, "Tax")
        pdf.drawRightString(410, start_y+60, "Additional Charges")
        pdf.drawRightString(410, start_y+85, "Discount Amount")
        pdf.setFillColor(colors.black)
        # tax, additional charges, discount_amount
        pdf.drawRightString(507, start_y+20, f"{document['sub_total']}")
        pdf.drawRightString(507, start_y+40, f"{document['tax']}")
        pdf.drawRightString(507, start_y+60, f"{document['add_charges']}")
        pdf.drawRightString(507, start_y+85, f"{document['discount_amount']}")

 
        pdf.setFont('Helvetica-Bold', 15)
        pdf.drawRightString(507, start_y+125, f"{currency} {document['grand_total']}")
        


    else:
        # tax, additional charges, discount_amount
        pdf.setFillColor(fill_colour)
        pdf.drawRightString(410, start_y+20, "Tax")
        pdf.drawRightString(410, start_y+40, "Additional Charges")
        pdf.drawRightString(410, start_y+65, "Discount Amount")
        pdf.setFillColor(colors.black)

        pdf.drawRightString(507, start_y+20, f"{document['tax']}")
        pdf.drawRightString(507, start_y+40, f"{document['add_charges']}")
        pdf.drawRightString(507, start_y+65, f"{document['discount_amount']}")


        pdf.setFont('Helvetica-Bold', 15)
        pdf.drawRightString(535, start_y+105, f"{currency} {document['grand_total']}")

    pdf.drawImage("app/pdf/logo_36_total.png", 340, start_y+90, width=100, height=50)

    pdf.setFont('Helvetica', 10)
    pdf = draw_wrapped_line(pdf, document["terms"].title(), 100, 30, 765, 15)
    pdf.drawString(250, 800, f"Page {page_number}")
            
    return pdf

























def get_report_36(buffer, document, currency, document_type, request):

    now = datetime.now().strftime("%Y-%m-%d %H-%M-%S")

    file_name = f"{document_type.title()} for {request.user.email} - {now}.pdf"

    # create file
    pdf = canvas.Canvas(buffer, bottomup=0)
    pdf.translate(cm, cm)
    pdf.setPageSize((A4[0], A4[1]))

    width = pdf._pagesize[0]
    pdf.setTitle(document_type.title())


    pdf.setLineWidth(0.1)

    pdf.drawImage("app/pdf/logo_36_up.png", -30, -30, width=width, height=450)
            


    pdf.setFont('Helvetica-Bold', 20)
    fill_colour = colors.Color(254/255, 224/255, 89/255)
    
    pdf.setFillColor(fill_colour)

    pdf.drawCentredString(270, 60, request.user.business_name.title())
    pdf.setFont('Helvetica', 10)
    pdf.setFillColor(colors.black)
    pdf.drawCentredString(270, 80, request.user.address.capitalize())
    pdf.drawCentredString(270, 95, request.user.email)
    pdf.drawCentredString(270, 110, request.user.phone_number)
    pdf.setFillColor(colors.white)
    pdf.setFont('Helvetica-Bold', 30)
    pdf.drawCentredString(270, 20, f"{document_type.upper()}")
    pdf.setFillColor(colors.black)

    
    pdf.setFont('Helvetica', 10)
    pdf = draw_wrapped_line(pdf, document["bill_to"], 25, 30, 220, 10)
    pdf = draw_wrapped_line(pdf, document["ship_to"], 40, 160, 220, 10)


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

    pdf.drawRightString(width - 85, 200, f"{document[doc_number_key]}")
    pdf.drawRightString(width - 85, 220, f"{document[doc_date_key]}")
    pdf.drawRightString(width - 85, 240, f"{document['due_date']}")

    pdf.setFont('Helvetica', 10)

    pdf.drawString(250, 800, f"Page {page_number}")

    item_list = document["item_list"]
    item_len = len(item_list)

    start_y = 350

    if item_len <= 20:
        # it will spill to another page
        for item in item_list:
            pdf.drawString(40, start_y, str(item["quantity"]))
            pdf.drawString(120, start_y, str(item["name"]))
            pdf.drawRightString(410, start_y, str(item["sales_price"]))
            pdf.drawRightString(507, start_y, str(item["amount"]))

            start_y += 20


        pdf = total_box(pdf, start_y, currency, document_type, document)

    else:
        i = 0
        for item in item_list:
            if i == 20:
                break

            pdf.drawString(40, start_y, str(item["quantity"]))
            pdf.drawString(120, start_y, str(item["name"]))
            pdf.drawRightString(410, start_y, str(item["sales_price"]))
            pdf.drawRightString(507, start_y, str(item["amount"]))
                
            start_y += 20
            i += 1


        pdf, start_y = add_another_page(pdf, item_list[20:], currency, document, document_type)


    
    pdf.save()


    return file_name