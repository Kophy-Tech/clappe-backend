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

    pdf.drawImage("app/pdf/logo_31_body.png", -28, -28, width=width-1, height=height)

    fill_colour = colors.Color(69/255, 100/255, 117/255)


    pdf.setFillColor(fill_colour)
    pdf.setStrokeColor(fill_colour)
    pdf.rect(70, 10, 470, 25, fill=1)
    pdf.setFillColor(colors.white)
    pdf.setFont('Helvetica-Bold', 10)

    pdf.drawString(75, 25, "Qty")
    pdf.drawString(150, 25, "Description")
    pdf.drawRightString(420, 25, "Unit Price")
    pdf.drawRightString(width-60, 25, "Amount")

    pdf.setFillColor(colors.black)

    pdf.setFont('Helvetica', 10)
    pdf.drawString(250, 800, f"Page {page_number}")

    item_len = len(item_list)

    start_y = 40

    if item_len <= 25:
        
        for item in item_list:
            pdf.drawString(80, start_y+10, str(item["quantity"]))
            pdf.drawString(130, start_y+10, str(item["name"]))
            pdf.drawRightString(420, start_y+10, str(item["sales_price"]))
            pdf.drawRightString(535, start_y+10, str(item["amount"]))
                
            start_y += 20


        pdf = total_box(pdf, start_y, currency, document_type, document)

    else:
        i = 0
        for item in item_list:
            if i == 36:
                break

            pdf.drawString(80, start_y+10, str(item["quantity"]))
            pdf.drawString(130, start_y+10, str(item["name"]))
            pdf.drawRightString(420, start_y+10, str(item["sales_price"]))
            pdf.drawRightString(535, start_y+10, str(item["amount"]))
                
            start_y += 20
            i += 1


        
        pdf, start_y = add_another_page(pdf, item_list[36:], currency, document, document_type)


    return pdf, start_y






def total_box(pdf, start_y, currency, document_type, document):
    fill_colour = colors.Color(69/255, 100/255, 117/255)
    if document_type == "invoice":
        # it will have sub total
        pdf.setFillColor(fill_colour)
        pdf.drawRightString(420, start_y+20, "Subtotal")
        pdf.drawRightString(420, start_y+40, "Tax")
        pdf.drawRightString(420, start_y+60, "Additional Charges")
        pdf.drawRightString(420, start_y+85, "Discount Amount")
        # tax, additional charges, discount_amount
        pdf.setFillColor(colors.black)
        pdf.drawRightString(535, start_y+20, f"{document['sub_total']}")
        pdf.drawRightString(535, start_y+40, f"{document['tax']}")
        pdf.drawRightString(535, start_y+60, f"{document['add_charges']}")
        pdf.drawRightString(535, start_y+85, f"{document['discount_amount']}")

        pdf.setFillColor(fill_colour)
        pdf.rect(70, start_y+95, 530, 25, fill=1)
        pdf.setFillColor(colors.white)
        pdf.setFont('Helvetica-Bold', 15)
        pdf.drawString(75, start_y+115, f"{document_type.title()} Total")
        pdf.drawRightString(535, start_y+115, f"{currency} {document['grand_total']}")
        


    else:
        # tax, additional charges, discount_amount
        pdf.setFillColor(fill_colour)
        pdf.drawRightString(420, start_y+20, "Tax")
        pdf.drawRightString(420, start_y+40, "Additional Charges")
        pdf.drawRightString(420, start_y+65, "Discount Amount")

        pdf.setFillColor(colors.black)
        pdf.drawRightString(535, start_y+20, f"{document['tax']}")
        pdf.drawRightString(535, start_y+40, f"{document['add_charges']}")
        pdf.drawRightString(535, start_y+65, f"{document['discount_amount']}")

        pdf.setFillColor(fill_colour)
        pdf.rect(70, start_y+75, 530, 25, fill=1)
        pdf.setFillColor(colors.white)
        pdf.setFont('Helvetica-Bold', 15)
        pdf.drawString(75, start_y+95, f"{document_type.split(' ')[0].title()} Total")
        pdf.drawRightString(535, start_y+95, f"{currency} {document['grand_total']}")


    pdf.setFillColor(fill_colour)
    pdf.setFont('Helvetica-Bold', 10)
    pdf.drawString(70, 740, "Terms & Conditions")
    pdf.setFillColor(colors.black)
    pdf.setFont('Helvetica', 10)
    pdf.drawString(70, 755, document["terms"].title())

            
    return pdf
















def get_report_31(buffer, document, currency, document_type, request):

    now = datetime.now().strftime("%Y-%m-%d %H-%M-%S")

    file_name = f"{document_type.title()} for {request.user.email} - {now}.pdf"

    # create file
    pdf = canvas.Canvas(buffer, bottomup=0)
    pdf.translate(cm, cm)
    pdf.setPageSize((A4[0], A4[1]))

    width = pdf._pagesize[0]
    height = pdf._pagesize[1]
    pdf.setTitle(document_type.title())

    pdf.drawImage("app/pdf/logo_31_body.png", -28, -28, width=width-1, height=height)

    if request.user.logo_path:
        pdf = draw_image(pdf, request.user.logo_path, request.user.email, 510, 120, "logo")


    pdf.setLineWidth(0.5)

    fill_colour = colors.Color(69/255, 100/255, 117/255)
            


    pdf.setFont('Helvetica-Bold', 15)

    pdf.setFillColor(fill_colour)
    pdf.drawString(70, 60, request.user.business_name.title())
    pdf.setFillColor(colors.black)
    
    pdf.setFont('Helvetica', 10)
    pdf.drawString(70, 75, request.user.address.capitalize())
    pdf.drawString(70, 90, request.user.email)
    pdf.drawString(70, 105, request.user.phone_number)

    pdf.setStrokeColor(fill_colour)

    
    pdf.setFont('Helvetica-Bold', 10)
    pdf.setFillColor(fill_colour)
    pdf.drawString(70, 150, "Bill To")
    pdf.drawString(240, 150, "Ship To")
    pdf.setFillColor(colors.black)
    pdf.setFont('Helvetica', 10)
    pdf = draw_wrapped_line(pdf, document["bill_to"], 40, 70, 165, 10)
    pdf = draw_wrapped_line(pdf, document["ship_to"], 40, 240, 165, 10)

    pdf.setFont('Helvetica-Bold', 10)
    pdf.setFillColor(fill_colour)
    pdf.drawRightString(470, 150, f"{document_type.split(' ')[0].title()} #")
    pdf.drawRightString(470, 170, f"{document_type.split(' ')[0].title()} Date")
    pdf.drawRightString(470, 190, "Due Date")
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

    pdf.drawRightString(width - 55, 150, f"{document[doc_number_key]}")
    pdf.drawRightString(width - 55, 170, f"{document[doc_date_key]}")
    pdf.drawRightString(width - 55, 190, f"{document['due_date']}")


    

    pdf.setFont('Helvetica-Bold', 10)
    pdf.setFillColor(fill_colour)
    pdf.rect(70, 220, 470, 25, fill=1)
    pdf.setFillColor(colors.white)

    pdf.drawString(75, 235, "Qty")
    pdf.drawString(150, 235, "Description")
    pdf.drawRightString(420, 235, "Unit Price")
    pdf.drawRightString(width-60, 235, "Amount")


    pdf.setFillColor(colors.black)
    pdf.setFont('Helvetica', 10)

    pdf.drawString(250, 800, f"Page {page_number}")

    item_list = document["item_list"]
    item_len = len(item_list)

    start_y = 270

    if item_len <= 16:
        # it will spill to another page
        for item in item_list:
            pdf.drawString(80, start_y, str(item["quantity"]))
            pdf.drawString(130, start_y, str(item["name"]))
            pdf.drawRightString(420, start_y, str(item["sales_price"]))
            pdf.drawRightString(535, start_y, str(item["amount"]))
                
            start_y += 20

        pdf = total_box(pdf, start_y, currency, document_type, document)

    else:
        i = 0
        for item in item_list:
            if i == 25:
                break


            pdf.drawString(80, start_y, str(item["quantity"]))
            pdf.drawString(130, start_y, str(item["name"]))
            pdf.drawRightString(420, start_y, str(item["sales_price"]))
            pdf.drawRightString(535, start_y, str(item["amount"]))
                
            start_y += 20
            i += 1


        pdf, start_y = add_another_page(pdf, item_list[25:], currency, document, document_type)


    
    pdf.save()


    return file_name