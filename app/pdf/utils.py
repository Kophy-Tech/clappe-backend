from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4
import textwrap


background_color = colors.Color(0.1, 0.1, 1)

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




def add_another_page(pdf, data, initial_total, currency, term):
    new_total= initial_total + 0
    global page_number
    page_number += 1

    # another page
    pdf.showPage()
    pdf.translate(cm, cm)
    pdf.setPageSize((A4[0]+15, A4[1]))
    background_color = colors.Color(0.1, 0.1, 1)

    pdf.setFillColor(background_color)
    pdf.setLineWidth(0.1)
    pdf.setStrokeColor(background_color)
    pdf.setFont('Times-Roman', 10)

    start_y = 10
    box_height = 10

    len_data = len(data)

    for i in range(len_data):
        if i == 50:
            break
        else:
            # quantity
            pdf.drawCentredString(9, start_y+15, str(data[i]['quantity']))
            # description
            pdf.drawString(200, start_y+15, str(data[i]['name']))
            # rate
            pdf.drawCentredString(445, start_y+15, str(data[i]['sales_price']))
            # amount
            pdf.drawCentredString(530, start_y+15, str(data[i]['amount']))

            start_y += 15
            new_total += int(data[i]['amount'])




    if len_data > 0:
        box_height += start_y
        # box for items
        pdf.rect(-15, 10, 585, box_height)
        pdf.line(30, 10, 30, box_height+10)
        pdf.line(400, 10, 400, box_height+10)
        pdf.line(490, 10, 490, box_height+10)

    if len(data) > 49:
        pdf.drawCentredString((A4[0]-15)/2, 805, f"Page {page_number}")
        pdf = add_another_page(pdf, data[50:], new_total, currency, term)
    else:

        # rectangle for amount
        pdf.rect(-15, box_height+20, 585, 50)
        pdf.drawString(-5, box_height+35, "Thank you for your business.")
        pdf = draw_wrapped_line(pdf, term, 95, -5, box_height+45, 10)
        # pdf.drawString(9, box_height+55, data['terms'])
        pdf.line(400, box_height+20, 400, box_height+70)
        pdf.setFont('Times-Roman', 20)
        pdf.drawCentredString(425, box_height+45, "Total")
        pdf.setFont('Times-Roman', 10)
        pdf.drawCentredString(530, box_height+45, f"{currency} {new_total}")
        
        pdf.drawCentredString((A4[0]-15)/2, 805, f"Page {page_number}")

        # box for signature
        pdf.rect(-15, box_height+70, 100, 100)
        pdf.drawString(-15, box_height+80, "Signature")

    return pdf







def add_other_details(pdf, document, start_y, document_type, currency, terms):
    # accept the document object and return the details already added to the pdf

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


    # adding date and document number
    pdf.drawString(445, 60, document[doc_date_key])
    pdf.drawCentredString(530, 60, document[doc_number_key])

    # add customer details
    pdf.drawString(-10, 180, f"{document['customer']['first_name']} {document['customer']['last_name']}")
    pdf.drawString(-10, 192, f"{document['customer']['address']}")
    pdf.drawString(-10, 204, f"{document['customer']['email']}")
    pdf.drawString(-10, 216, f"{document['customer']['phone_number']}")


    # adding the 3 details
    pdf.drawCentredString(420, 225, str(document['po_number']))
    # pdf.drawCentredString(425, 225, "Terms")
    # pdf.drawCentredString(515, 225, "Project")

    total_amount = 0
    item_list = document['item_list']
    item_list_len = len(item_list)
    # item_list_len = 13
    # item_list = [i for i in range(1, item_list_len+1)]



    for i in range(item_list_len):
        if i == 31:
            break
        else:
            # quantity
            pdf.drawCentredString(9, start_y+15, str(item_list[i]['quantity']))
            # description
            pdf.drawString(200, start_y+15, str(item_list[i]['name']))
            # rate
            pdf.drawCentredString(445, start_y+15, str(item_list[i]['sales_price']))
            # amount
            pdf.drawCentredString(530, start_y+15, str(item_list[i]['amount']))

            start_y += 15
            total_amount += int(item_list[i]['amount'])

    

    if item_list_len > 31:
        # call the function to handle the next page
        # global page_number
        # pdf.drawCentredString(350, 820, f"Page {page_number}")
        pdf.drawCentredString((A4[0]-15)/2, 805, "Page 1")
        pdf = add_another_page(pdf, item_list[31: ], total_amount, currency, terms)

    else:
        # global page_number
        # rectangle for amount
        pdf.rect(-15, 740, 585, 50)
        pdf.drawString(-5, 750, "Thank you for your business.")
        draw_wrapped_line(pdf, terms, 95, -5, 760, 10)
        # pdf.drawString(9, 770, data['terms'])
        pdf.line(400, 740, 400, 790)
        pdf.setFont('Times-Roman', 20)
        pdf.drawCentredString(425, 770, "Total")
        pdf.setFont('Times-Roman', 10)
        pdf.drawCentredString(530, 770, f"{currency} {total_amount}")

        pdf.drawCentredString((A4[0]-15)/2, 805, "Page 1")



    

    return pdf