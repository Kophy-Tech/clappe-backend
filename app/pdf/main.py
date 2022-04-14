from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A3
from reportlab.lib import colors
from datetime import datetime


from app.pdf.utils import angle_graph, draw_wrapped_line, histogram_graph
from app.pdf.data import get_data

# sauce code: 138235

def get_report(file_name):


    date = datetime.today()


    #get all the needed data
    patient_access, coding, claims, financial = get_data()


    # create file
    pdf = canvas.Canvas(filename=file_name, bottomup=0)
    pdf.translate(cm, cm)
    pdf.setPageSize((A3[0]-50, A3[1]))

    # author info
    pdf.setAuthor("Made by Pyaar")
    pdf.setSubject("Report PDF.")
    pdf.setTitle("Report PDF")

    # setting a custom background color
    background_color = colors.Color(0.1875, 0.390625, 0.5625)

    pdf.setFillColor(background_color)
    pdf.setLineWidth(0.1)
    pdf.setStrokeColor(background_color)

    # the rectangle that covers the whole page
    pdf.rect(5, 10, 725, 865, fill=1)

    pdf.setFillColor(colors.white)
    pdf.setFont('Times-Roman', 10)
    pdf.drawString(10, 25, f"Date: {date.strftime('%d-%m-%Y')}")






# sauce code: 110186




    #################################### PATIENT ACCESS ############################################
    pdf.rect(10, 32, 715, 20, fill=1)
    pdf.setFillColor(colors.red)
    pdf.drawCentredString(362.5, 46, "PATIENT ACCESS")

    pdf.setFillColor(colors.white)
    pdf.drawCentredString(362.5, 66, "HB PATIENT ACCESS -- RATIO OF CURRENT TO TARGET")

    pdf.rect(10, 74, 715, 120, fill=1)
    pdf.setFont('Times-Roman', 8)
    pdf.setFillColor(background_color)

    c = patient_access['Current']['Conversion Rate % of Uninsured Patient to 3rd Party Insurance (Funding Source) ']
    t = patient_access['Target']['Conversion Rate % of Uninsured Patient to 3rd Party Insurance (Funding Source) ']
    angle_graph(pdf, c, t, 20, 80)
    text = "Conversion Rate % of Uninsured Patient to 3rd Party Insurance (Funding Source)"
    draw_wrapped_line(pdf, text, 30, 70, 170, 10, 'center')

    c = patient_access['Current']['Insurance Verification Rate']
    t = patient_access['Target']['Insurance Verification Rate']
    angle_graph(pdf, c, t, 140, 80)
    text = "Insurance Verification Rate"
    draw_wrapped_line(pdf, text, 30, 190, 170, 10, 'center')

    c = patient_access['Current']['Point-of-Service (POS) Cash Collections ']
    t = patient_access['Target']['Point-of-Service (POS) Cash Collections ']
    angle_graph(pdf, c, t, 260, 80, type='money')
    text = "Point-of-Service (POS) Cash Collections"
    draw_wrapped_line(pdf, text, 30, 310, 170, 10, 'center')

    c = patient_access['Current']['Pre-Registration Rate ']
    t = patient_access['Target']['Pre-Registration Rate ']
    angle_graph(pdf, c, t, 380, 80)
    text = "Pre-Registration Rate"
    draw_wrapped_line(pdf, text, 30, 430, 170, 10, 'center')

    c = patient_access['Current']['Service Authorization Rate- Inpatient (IP) & OBS']
    t = patient_access['Target']['Service Authorization Rate- Inpatient (IP) & OBS']
    angle_graph(pdf, c, t, 500, 80)
    text = "Service Authorization Rate-Inpatient (IP) & OBS"
    draw_wrapped_line(pdf, text, 30, 550, 170, 10, 'center')

    c = patient_access['Current']['Service Authorization Rate- Outpatient (OP)']
    t = patient_access['Target']['Service Authorization Rate- Outpatient (OP)']
    angle_graph(pdf, c, t, 620, 80)
    text = "Service Authorization Rate-Outpatient (OP)"
    draw_wrapped_line(pdf, text, 30, 670, 170, 10, 'center')



    pdf.setFillColor(colors.white)
    pdf.setFont('Times-Roman', 10)
    pdf.drawCentredString(362.5, 210, "PB PATIENT ACCESS -- RATIO OF CURRENT TO TARGET")

    pdf.rect(10, 215, 715, 120, stroke=0, fill=1)
    pdf.setFont('Times-Roman', 8)
    pdf.setFillColor(background_color)

    c = patient_access['Current']['Conversion Rate % of Uninsured Patient to 3rd Party Insurance (Funding Source) ']
    t = patient_access['Target']['Conversion Rate % of Uninsured Patient to 3rd Party Insurance (Funding Source) ']
    angle_graph(pdf, c, t, 20, 220)
    text = "Conversion Rate % of Uninsured Patient to 3rd Party Insurance (Funding Source)"
    draw_wrapped_line(pdf, text, 30, 70, 310, 10, 'center')

    c = patient_access['Current']['Insurance Verification Rate']
    t = patient_access['Target']['Insurance Verification Rate']
    angle_graph(pdf, c, t, 140, 220)
    text = "Insurance Verification Rate"
    draw_wrapped_line(pdf, text, 30, 190, 310, 10, 'center')

    c = patient_access['Current']['Point-of-Service (POS) Cash Collections ']
    t = patient_access['Target']['Point-of-Service (POS) Cash Collections ']
    angle_graph(pdf, c, t, 260, 220, type='money')
    text = "Point-of-Service (POS) Cash Collections"
    draw_wrapped_line(pdf, text, 30, 310, 310, 10, 'center')

    c = patient_access['Current']['Pre-Registration Rate ']
    t = patient_access['Target']['Pre-Registration Rate ']
    angle_graph(pdf, c, t, 380, 220)
    text = "Pre-Registration Rate"
    draw_wrapped_line(pdf, text, 30, 430, 310, 10, 'center')

    c = patient_access['Current']['Service Authorization Rate- Inpatient (IP) & OBS']
    t = patient_access['Target']['Service Authorization Rate- Inpatient (IP) & OBS']
    angle_graph(pdf, c, t, 500, 220)
    text = "Service Authorization Rate-Inpatient (IP) & OBS"
    draw_wrapped_line(pdf, text, 30, 550, 310, 10, 'center')

    c = patient_access['Current']['Service Authorization Rate- Outpatient (OP)']
    t = patient_access['Target']['Service Authorization Rate- Outpatient (OP)']
    angle_graph(pdf, c, t, 620, 220)
    text = "Service Authorization Rate-Outpatient (OP)"
    draw_wrapped_line(pdf, text, 30, 670, 310, 10, 'center')



    pdf.setFont('Times-Roman', 10)
    pdf.setFillColor(colors.white)
    pdf.drawCentredString(178, 355, "HB PATIENT ACCESS -- HENNEPIN VS OTHERS")
    pdf.drawCentredString(547, 355, "PB PATIENT ACCESS -- HENNEPIN VS OTHERS")

    pdf.rect(10, 365, 356, 480, stroke=0, fill=1)
    pdf.setFillColor(background_color)
    pdf.setStrokeColor(background_color)

    text = "Conversion Rate % of Uninsured Patient to 3rd Party Insurance (Funding Source)"
    current = patient_access['Current']['Conversion Rate % of Uninsured Patient to 3rd Party Insurance (Funding Source) ']
    epic =  patient_access['EPIC']['Conversion Rate % of Uninsured Patient to 3rd Party Insurance (Funding Source) ']
    hfma =  patient_access['HFMA']['Conversion Rate % of Uninsured Patient to 3rd Party Insurance (Funding Source) ']
    histogram_graph(pdf, current, epic, hfma, 115, 375)
    draw_wrapped_line(pdf, text, 20, 13, 385, 10, 'left')
    pdf.line(10, 445, 367, 445)

    text = "Insurance Verification Rate"
    draw_wrapped_line(pdf, text, 20, 13, 455, 10, 'left')
    current = patient_access['Current']['Insurance Verification Rate']
    epic = patient_access['EPIC']['Insurance Verification Rate']
    hfma = patient_access['HFMA']['Insurance Verification Rate']
    histogram_graph(pdf, current, epic, hfma, 115, 455)
    pdf.line(10, 525, 367, 525)

    text = "Point-of-Service (POS) Cash Collections"
    draw_wrapped_line(pdf, text, 20, 13, 545, 10, 'left')
    current = patient_access['Current']['Point-of-Service (POS) Cash Collections ']
    epic = patient_access['EPIC']['Point-of-Service (POS) Cash Collections ']
    hfma = patient_access['HFMA']['Point-of-Service (POS) Cash Collections ']
    histogram_graph(pdf, current, epic, hfma, 115, 535, type='money')
    pdf.line(10, 605, 367, 605)
    text = "Pre-Registration Rate"
    draw_wrapped_line(pdf, text, 20, 13, 625, 10, 'left')
    current = patient_access['Current']['Pre-Registration Rate ']
    epic = patient_access['EPIC']['Pre-Registration Rate ']
    hfma = patient_access['HFMA']['Pre-Registration Rate ']
    histogram_graph(pdf, current, epic, hfma, 115, 615)
    pdf.line(10, 685, 367, 685)
    text = "Service Authorization Rate-Inpatient (IP) & OBS"
    draw_wrapped_line(pdf, text, 20, 13, 705, 10, 'left')
    current = patient_access['Current']['Service Authorization Rate- Inpatient (IP) & OBS']
    epic = patient_access['EPIC']['Service Authorization Rate- Inpatient (IP) & OBS']
    hfma = patient_access['HFMA']['Service Authorization Rate- Inpatient (IP) & OBS']
    histogram_graph(pdf, current, epic, hfma, 115, 695)
    pdf.line(10, 765, 367, 765)
    text = "Service Authorization Rate-Outpatient (OP)"
    draw_wrapped_line(pdf, text, 20, 13, 785, 10, 'left')
    current = patient_access['Current']['Service Authorization Rate- Outpatient (OP)']
    epic = patient_access['EPIC']['Service Authorization Rate- Outpatient (OP)']
    hfma = patient_access['HFMA']['Service Authorization Rate- Outpatient (OP)']
    histogram_graph(pdf, current, epic, hfma, 115, 775)


    pdf.setFillColor(colors.white)
    pdf.rect(369, 365, 356, 480, stroke=0, fill=1)
    pdf.setFillColor(colors.black)
    pdf.setStrokeColor(colors.black)

    text = "Conversion Rate % of Uninsured Patient to 3rd Party Insurance (Funding Source)"
    current = patient_access['Current']['Conversion Rate % of Uninsured Patient to 3rd Party Insurance (Funding Source) ']
    epic =  patient_access['EPIC']['Conversion Rate % of Uninsured Patient to 3rd Party Insurance (Funding Source) ']
    hfma =  patient_access['HFMA']['Conversion Rate % of Uninsured Patient to 3rd Party Insurance (Funding Source) ']
    histogram_graph(pdf, current, epic, hfma, 470, 375)
    draw_wrapped_line(pdf, text, 20, 372, 385, 10, 'left')
    pdf.line(369, 445, 725, 445)

    text = "Insurance Verification Rate"
    draw_wrapped_line(pdf, text, 20, 372, 455, 10, 'left')
    current = patient_access['Current']['Insurance Verification Rate']
    epic = patient_access['EPIC']['Insurance Verification Rate']
    hfma = patient_access['HFMA']['Insurance Verification Rate']
    histogram_graph(pdf, current, epic, hfma, 470, 455)
    pdf.line(369, 525, 725, 525)

    text = "Point-of-Service (POS) Cash Collections"
    draw_wrapped_line(pdf, text, 20, 372, 545, 10, 'left')
    current = patient_access['Current']['Point-of-Service (POS) Cash Collections ']
    epic = patient_access['EPIC']['Point-of-Service (POS) Cash Collections ']
    hfma = patient_access['HFMA']['Point-of-Service (POS) Cash Collections ']
    histogram_graph(pdf, current, epic, hfma, 470, 535, type='money')
    pdf.line(369, 605, 725, 605)

    text = "Pre-Registration Rate"
    draw_wrapped_line(pdf, text, 20, 372, 625, 10, 'left')
    current = patient_access['Current']['Pre-Registration Rate ']
    epic = patient_access['EPIC']['Pre-Registration Rate ']
    hfma = patient_access['HFMA']['Pre-Registration Rate ']
    histogram_graph(pdf, current, epic, hfma, 470, 615)
    pdf.line(369, 685, 725, 685)

    text = "Service Authorization Rate-Inpatient (IP) & OBS"
    draw_wrapped_line(pdf, text, 20, 372, 705, 10, 'left')
    current = patient_access['Current']['Service Authorization Rate- Inpatient (IP) & OBS']
    epic = patient_access['EPIC']['Service Authorization Rate- Inpatient (IP) & OBS']
    hfma = patient_access['HFMA']['Service Authorization Rate- Inpatient (IP) & OBS']
    histogram_graph(pdf, current, epic, hfma, 470, 695)
    pdf.line(369, 765, 725, 765)

    text = "Service Authorization Rate-Outpatient (OP)"
    draw_wrapped_line(pdf, text, 20, 372, 785, 10, 'left')
    current = patient_access['Current']['Service Authorization Rate- Outpatient (OP)']
    epic = patient_access['EPIC']['Service Authorization Rate- Outpatient (OP)']
    hfma = patient_access['HFMA']['Service Authorization Rate- Outpatient (OP)']
    histogram_graph(pdf, current, epic, hfma, 470, 775)


# sauce code: 167921



    pdf.setFillColor(colors.white)
    pdf.setFont('Times-Roman', 10)
    pdf.rect(10, 850, 356, 15, stroke=0, fill=1)
    pdf.setFillColor(background_color)
    pdf.setStrokeColor(background_color)
    pdf.rect(12, 852, 10, 10, fill=1)
    pdf.drawString(27, 860, "HB Current")
    pdf.setFillColor(colors.gray)
    pdf.setStrokeColor(colors.gray)
    pdf.rect(100, 852, 10, 10, fill=1)
    pdf.setFillColor(background_color)
    pdf.drawString(115, 860, "HB EPIC")
    pdf.setFillColor(colors.lightgrey)
    pdf.setStrokeColor(colors.lightgrey)
    pdf.rect(190, 852, 10, 10, fill=1)
    pdf.setFillColor(background_color)
    pdf.drawString(205, 860, "HB HFMA")


    pdf.setFillColor(colors.white)
    pdf.rect(369, 850, 356, 15, stroke=0, fill=1)
    pdf.setFillColor(background_color)
    pdf.setStrokeColor(background_color)
    pdf.rect(372, 852, 10, 10, fill=1)
    pdf.drawString(390, 860, "PB Current")
    pdf.setFillColor(colors.gray)
    pdf.setStrokeColor(colors.gray)
    pdf.rect(470, 852, 10, 10, fill=1)
    pdf.setFillColor(background_color)
    pdf.drawString(485, 860, "PB EPIC")
    pdf.setFillColor(colors.lightgrey)
    pdf.setStrokeColor(colors.lightgrey)
    pdf.rect(560, 852, 10, 10, fill=1)
    pdf.setFillColor(background_color)
    pdf.drawString(580, 860, "PB HFMA")


    # footer
    pdf.setFillColor(colors.black)
    pdf.setFont('Times-Roman', 10)
    pdf.drawString(10, 1150, f"Date: {date.strftime('%d-%m-%Y')}")
    pdf.drawCentredString(362.5, 1150, "PATIENT ACCESS")






    ################################################# CODING ###############################################
    pdf.showPage()

    pdf.translate(cm, cm)
    pdf.setPageSize((A3[0]-50, A3[1]))
    pdf.setFillColor(background_color)
    pdf.setLineWidth(0.1)
    pdf.setStrokeColor(background_color)
    pdf.rect(5, 10, 725, 785, stroke=0, fill=1)
    pdf.setFont('Times-Roman', 10)

    pdf.setFillColor(colors.white)
    pdf.rect(10, 20, 715, 20, stroke=0, fill=1)
    pdf.setFillColor(colors.red)
    pdf.drawCentredString(362.5, 36, "CODING")


    pdf.setFillColor(colors.white)
    pdf.drawCentredString(362.5, 60, "HB CODING -- RATIO OF CURRENT TO TARGET")
    pdf.rect(10, 64, 715, 120, stroke=0, fill=1)
    pdf.setFont('Times-Roman', 8)
    pdf.setFillColor(background_color)

    c = coding['Current']['Case Mix Index ']
    t = coding['Target']['Case Mix Index ']
    angle_graph(pdf, c, t, 20, 80)
    text = "Case Mix Index"
    draw_wrapped_line(pdf, text, 30, 70, 170, 10, 'center')

    c = coding['Current']['Days in Final Bill Not Submitted to Payer (FBNS)']
    t = coding['Target']['Days in Final Bill Not Submitted to Payer (FBNS)']
    angle_graph(pdf, c, t, 170, 80, type='days')
    text = "Days in Final Bill Not Submitted to Payer (FBNS)"
    draw_wrapped_line(pdf, text, 30, 220, 170, 10, 'center')

    c = coding['Current']['Days in Total Discharged Not Final Billed (DNFB)']
    t = coding['Target']['Days in Total Discharged Not Final Billed (DNFB)']
    angle_graph(pdf, c, t, 320, 80, type='days')
    text = "Days in Total Discharged Not Final Billed (DNFB)"
    draw_wrapped_line(pdf, text, 30, 370, 170, 10, 'center')

    c = coding['Current']['Days in Total Discharged Not Submitted to Payor (DNSP)']
    t = coding['Target']['Days in Total Discharged Not Submitted to Payor (DNSP)']
    angle_graph(pdf, c, t, 470, 80, type='days')
    text = "Days in Total Discharged Not Submitted to Payor (DNSP)"
    draw_wrapped_line(pdf, text, 30, 520, 170, 10, 'center')

    c = coding['Current']['Total Charge Lag Days ']
    t = coding['Target']['Total Charge Lag Days ']
    angle_graph(pdf, c, t, 620, 80, type='days')
    text = "Total Charge Lag Days"
    draw_wrapped_line(pdf, text, 30, 670, 170, 10, 'center')



    pdf.setFillColor(colors.white)
    pdf.setFont('Times-Roman', 10)
    pdf.drawCentredString(362.5, 200, "PB CODING -- RATIO OF CURRENT TO TARGET")
    pdf.rect(10, 210, 715, 120, stroke=0, fill=1)
    pdf.setFont('Times-Roman', 8)
    pdf.setFillColor(background_color)

    c = coding['Current']['Case Mix Index ']
    t = coding['Target']['Case Mix Index ']
    angle_graph(pdf, c, t, 20, 225)
    text = "Case Mix Index"
    draw_wrapped_line(pdf, text, 30, 70, 315, 10, 'center')

    c = coding['Current']['Days in Final Bill Not Submitted to Payer (FBNS)']
    t = coding['Target']['Days in Final Bill Not Submitted to Payer (FBNS)']
    angle_graph(pdf, c, t, 170, 225, type='days')
    text = "Days in Final Bill Not Submitted to Payer (FBNS)"
    draw_wrapped_line(pdf, text, 30, 220, 315, 10, 'center')

    c = coding['Current']['Days in Total Discharged Not Final Billed (DNFB)']
    t = coding['Target']['Days in Total Discharged Not Final Billed (DNFB)']
    angle_graph(pdf, c, t, 320, 225, type='days')
    text = "Days in Total Discharged Not Final Billed (DNFB)"
    draw_wrapped_line(pdf, text, 30, 370, 315, 10, 'center')

    c = coding['Current']['Days in Total Discharged Not Submitted to Payor (DNSP)']
    t = coding['Target']['Days in Total Discharged Not Submitted to Payor (DNSP)']
    angle_graph(pdf, c, t, 470, 225, type='days')
    text = "Days in Total Discharged Not Submitted to Payor (DNSP)"
    draw_wrapped_line(pdf, text, 30, 520, 315, 10, 'center')

    c = coding['Current']['Total Charge Lag Days ']
    t = coding['Target']['Total Charge Lag Days ']
    angle_graph(pdf, c, t, 620, 225, type='days')
    text = "Total Charge Lag Days"
    draw_wrapped_line(pdf, text, 30, 670, 315, 10, 'center')



    pdf.setFont('Times-Roman', 10)
    pdf.setFillColor(colors.white)
    pdf.drawCentredString(178, 350, "HB CODING -- HENNEPIN VS OTHERS")

    pdf.rect(10, 360, 356, 400, stroke=0, fill=1)
    pdf.setFillColor(colors.black)
    pdf.setStrokeColor(colors.black)
    text = "Case Mix Index"
    draw_wrapped_line(pdf, text, 20, 13, 370, 10, 'left')
    current = coding['Current']['Case Mix Index ']
    epic = coding['EPIC']['Case Mix Index ']
    hfma = coding['HFMA']['Case Mix Index ']
    histogram_graph(pdf, current, epic, hfma, 115, 370)
    pdf.line(10, 440, 367, 440)

    text = "Days in Final Bill Not Submitted to Payer (FBNS)"
    draw_wrapped_line(pdf, text, 20, 13, 450, 10, 'left')
    current = coding['Current']['Days in Final Bill Not Submitted to Payer (FBNS)']
    epic = coding['EPIC']['Days in Final Bill Not Submitted to Payer (FBNS)']
    hfma = coding['HFMA']['Days in Final Bill Not Submitted to Payer (FBNS)']
    histogram_graph(pdf, current, epic, hfma, 115, 450, type='days')
    pdf.line(10, 520, 367, 520)

    text = "Days in Total Discharged Not Final Billed (DNFB)"
    draw_wrapped_line(pdf, text, 20, 13, 530, 10, 'left')
    current = coding['Current']['Days in Total Discharged Not Final Billed (DNFB)']
    epic = coding['EPIC']['Days in Total Discharged Not Final Billed (DNFB)']
    hfma = coding['HFMA']['Days in Total Discharged Not Final Billed (DNFB)']
    histogram_graph(pdf, current, epic, hfma, 115, 530, type='days')
    pdf.line(10, 600, 367, 600)

    text = "Days in Total Discharged Not Submitted to Payor (DNSP)"
    draw_wrapped_line(pdf, text, 20, 13, 610, 10, 'left')
    current = coding['Current']['Days in Total Discharged Not Submitted to Payor (DNSP)']
    epic = coding['EPIC']['Days in Total Discharged Not Submitted to Payor (DNSP)']
    hfma = coding['HFMA']['Days in Total Discharged Not Submitted to Payor (DNSP)']
    histogram_graph(pdf, current, epic, hfma, 115, 610, type='days')
    pdf.line(10, 680, 367, 680)

    text = "Total Charge Lag Days"
    draw_wrapped_line(pdf, text, 20, 13, 690, 10, 'left')
    current = coding['Current']['Total Charge Lag Days ']
    epic = coding['EPIC']['Total Charge Lag Days ']
    hfma = coding['HFMA']['Total Charge Lag Days ']
    histogram_graph(pdf, current, epic, hfma, 115, 690, type='days')


    pdf.setFillColor(colors.white)
    pdf.drawCentredString(547, 350, "PB CODING -- HENNEPIN VS OTHERS")

    pdf.rect(369, 360, 356, 400, stroke=0, fill=1)
    pdf.setFillColor(colors.black)
    pdf.setStrokeColor(colors.black)

    text = "Case Mix Index"
    draw_wrapped_line(pdf, text, 20, 372, 370, 10, 'left')
    current = coding['Current']['Case Mix Index ']
    epic = coding['EPIC']['Case Mix Index ']
    hfma = coding['HFMA']['Case Mix Index ']
    histogram_graph(pdf, current, epic, hfma, 470, 370)
    pdf.line(369, 440, 725, 440)

    text = "Days in Final Bill Not Submitted to Payer (FBNS)"
    draw_wrapped_line(pdf, text, 20, 372, 450, 10, 'left')
    current = coding['Current']['Days in Final Bill Not Submitted to Payer (FBNS)']
    epic = coding['EPIC']['Days in Final Bill Not Submitted to Payer (FBNS)']
    hfma = coding['HFMA']['Days in Final Bill Not Submitted to Payer (FBNS)']
    histogram_graph(pdf, current, epic, hfma, 470, 450, type='days')
    pdf.line(369, 520, 725, 520)

    text = "Days in Total Discharged Not Final Billed (DNFB)"
    draw_wrapped_line(pdf, text, 20, 372, 530, 10, 'left')
    current = coding['Current']['Days in Total Discharged Not Final Billed (DNFB)']
    epic = coding['EPIC']['Days in Total Discharged Not Final Billed (DNFB)']
    hfma = coding['HFMA']['Days in Total Discharged Not Final Billed (DNFB)']
    histogram_graph(pdf, current, epic, hfma, 470, 530, type='days')
    pdf.line(369, 600, 725, 600)

    text = "Days in Total Discharged Not Submitted to Payor (DNSP)"
    draw_wrapped_line(pdf, text, 20, 372, 610, 10, 'left')
    current = coding['Current']['Days in Total Discharged Not Submitted to Payor (DNSP)']
    epic = coding['EPIC']['Days in Total Discharged Not Submitted to Payor (DNSP)']
    hfma = coding['HFMA']['Days in Total Discharged Not Submitted to Payor (DNSP)']
    histogram_graph(pdf, current, epic, hfma, 470, 610, type='days')
    pdf.line(369, 680, 725, 680)

    text = "Total Charge Lag Days"
    draw_wrapped_line(pdf, text, 20, 372, 690, 10, 'left')
    current = coding['Current']['Total Charge Lag Days ']
    epic = coding['EPIC']['Total Charge Lag Days ']
    hfma = coding['HFMA']['Total Charge Lag Days ']
    histogram_graph(pdf, current, epic, hfma, 470, 690, type='days')




    pdf.setFillColor(colors.white)
    pdf.setFont('Times-Roman', 10)
    pdf.rect(10, 770, 356, 15, stroke=0, fill=1)
    pdf.setFillColor(background_color)
    pdf.setStrokeColor(background_color)
    pdf.rect(12, 772, 10, 10, fill=1)
    pdf.drawString(27, 780, "HB Current")
    pdf.setFillColor(colors.gray)
    pdf.setStrokeColor(colors.gray)
    pdf.rect(100, 772, 10, 10, fill=1)
    pdf.setFillColor(background_color)
    pdf.drawString(115, 780, "HB EPIC")
    pdf.setFillColor(colors.lightgrey)
    pdf.setStrokeColor(colors.lightgrey)
    pdf.rect(190, 772, 10, 10, fill=1)
    pdf.setFillColor(background_color)
    pdf.drawString(205, 780, "HB HFMA")


    pdf.setFillColor(colors.white)
    pdf.rect(369, 770, 356, 15, stroke=0, fill=1)
    pdf.setFillColor(background_color)
    pdf.setStrokeColor(background_color)
    pdf.rect(372, 772, 10, 10, fill=1)
    pdf.drawString(390, 780, "PB Current")
    pdf.setFillColor(colors.gray)
    pdf.setStrokeColor(colors.gray)
    pdf.rect(470, 772, 10, 10, fill=1)
    pdf.setFillColor(background_color)
    pdf.drawString(485, 780, "PB EPIC")
    pdf.setFillColor(colors.lightgrey)
    pdf.setStrokeColor(colors.lightgrey)
    pdf.rect(560, 772, 10, 10, fill=1)
    pdf.setFillColor(background_color)
    pdf.drawString(580, 780, "PB HFMA")



    pdf.setFillColor(colors.black)
    pdf.setFont('Times-Roman', 10)
    pdf.drawString(10, 1150, f"Date: {date.strftime('%d-%m-%Y')}")
    pdf.drawCentredString(362.5, 1150, "CODING")





    ############################################# CLAIMS #########################################################
    pdf.showPage()

    pdf.translate(cm, cm)
    pdf.setPageSize((A3[0]-50, A3[1]))
    pdf.setFillColor(background_color)
    pdf.setLineWidth(0.1)
    pdf.setStrokeColor(background_color)
    pdf.rect(5, 10, 725, 615, fill=1)

    pdf.setFillColor(colors.white)
    pdf.rect(10, 20, 715, 20, fill=1)
    pdf.setFillColor(colors.red)
    pdf.drawCentredString(362.5, 36, "CLAIMS")


    pdf.setFont('Times-Roman', 10)
    pdf.setFillColor(colors.white)
    pdf.drawCentredString(362.5, 60, "HB CLAIMS -- RATIO OF CURRENT TO TARGET")
    pdf.rect(10, 64, 715, 120, fill=1)

    pdf.setFillColor(background_color)
    pdf.setStrokeColor(background_color)
    pdf.setFont('Times-Roman', 8)

    c = claims['Current']['Clean Claims Rate ']
    t = claims['Target']['Clean Claims Rate ']
    angle_graph(pdf, c, t, 170, 80)
    text = "Clean Claims Rate"
    draw_wrapped_line(pdf, text, 30, 220, 170, 10, 'center')

    c = claims['Current']['Late charges (as % of Total charges) ']
    t = claims['Target']['Late charges (as % of Total charges) ']
    angle_graph(pdf, c, t, 470, 80, type='money')
    text = "Late charges (as % of Total charges)"
    draw_wrapped_line(pdf, text, 30, 520, 170, 10, 'center')




    pdf.setFont('Times-Roman', 10)
    pdf.setFillColor(colors.white)
    pdf.drawCentredString(362.5, 200, "PB CLAIMS -- RATIO OF CURRENT TO TARGET")
    pdf.rect(10, 210, 715, 120, stroke=0, fill=1)

    pdf.setFillColor(background_color)
    pdf.setStrokeColor(background_color)
    pdf.setFont('Times-Roman', 8)

    c = claims['Current']['Clean Claims Rate ']
    t = claims['Target']['Clean Claims Rate ']
    angle_graph(pdf, c, t, 170, 230)
    text = "Clean Claims Rate"
    draw_wrapped_line(pdf, text, 30, 220, 315, 10, 'center')

    c = claims['Current']['Late charges (as % of Total charges) ']
    t = claims['Target']['Late charges (as % of Total charges) ']
    angle_graph(pdf, c, t, 470, 230, type='money')
    text = "Late charges (as % of Total charges)"
    draw_wrapped_line(pdf, text, 30, 520, 315, 10, 'center')


# sauce code: 230119


    pdf.setFont('Times-Roman', 10)
    pdf.setFillColor(colors.white)
    pdf.drawCentredString(178, 350, "HB CLAIMS -- HENNEPIN VS OTHERS (%)")
    pdf.rect(10, 360, 356, 100, stroke=0, fill=1)
    pdf.setFillColor(colors.black)
    pdf.setStrokeColor(colors.black)

    text = "Clean Claims Rate"
    draw_wrapped_line(pdf, text, 30, 13, 380, 10, 'left')
    current = claims['Current']['Clean Claims Rate ']
    epic = claims['EPIC']['Clean Claims Rate ']
    hfma = claims['HFMA']['Clean Claims Rate ']
    histogram_graph(pdf, current, epic, hfma, 100, 380)


    pdf.setFont('Times-Roman', 10)
    pdf.setFillColor(colors.white)
    pdf.drawCentredString(547, 350, "HB CLAIMS -- HENNEPIN VS OTHERS ($)")
    pdf.rect(369, 360, 356, 100, stroke=0, fill=1)
    pdf.setFillColor(colors.black)
    pdf.setStrokeColor(colors.black)

    text = "Late charges (as % of Total charges)"
    draw_wrapped_line(pdf, text, 20, 372, 380, 10, 'left')
    current = claims['Current']['Late charges (as % of Total charges) ']
    epic = claims['EPIC']['Late charges (as % of Total charges) ']
    hfma = claims['HFMA']['Late charges (as % of Total charges) ']
    histogram_graph(pdf, current, epic, hfma, 460, 380, type='money')






    pdf.setFont('Times-Roman', 10)
    pdf.setFillColor(colors.white)
    pdf.drawCentredString(178, 480, "PB CLAIMS -- HENNEPIN VS OTHERS (%)")
    pdf.rect(10, 490, 356, 100, stroke=0, fill=1)
    pdf.setFillColor(colors.black)
    pdf.setStrokeColor(colors.black)

    text = "Clean Claims Rate"
    draw_wrapped_line(pdf, text, 30, 13, 500, 10, 'left')
    current = claims['Current']['Clean Claims Rate ']
    epic = claims['EPIC']['Clean Claims Rate ']
    hfma = claims['HFMA']['Clean Claims Rate ']
    histogram_graph(pdf, current, epic, hfma, 100, 500)


    pdf.setFont('Times-Roman', 10)
    pdf.setFillColor(colors.white)
    pdf.drawCentredString(547, 480, "PB CLAIMS -- HENNEPIN VS OTHERS ($)")
    pdf.rect(369, 490, 356, 100, stroke=0, fill=1)
    pdf.setFillColor(colors.black)
    pdf.setStrokeColor(colors.black)

    text = "Late charges (as % of Total charges)"
    draw_wrapped_line(pdf, text, 20, 372, 500, 10, 'left')
    current = claims['Current']['Late charges (as % of Total charges) ']
    epic = claims['EPIC']['Late charges (as % of Total charges) ']
    hfma = claims['HFMA']['Late charges (as % of Total charges) ']
    histogram_graph(pdf, current, epic, hfma, 460, 500, type='money')









    pdf.setFillColor(colors.white)
    pdf.setFont('Times-Roman', 10)
    pdf.rect(10, 600, 356, 15, stroke=0, fill=1)
    pdf.setFillColor(background_color)
    pdf.setStrokeColor(background_color)
    pdf.rect(12, 602, 10, 10, fill=1)
    pdf.drawString(27, 610, "HB Current")
    pdf.setFillColor(colors.gray)
    pdf.setStrokeColor(colors.gray)
    pdf.rect(100, 602, 10, 10, fill=1)
    pdf.setFillColor(background_color)
    pdf.drawString(115, 610, "HB EPIC")
    pdf.setFillColor(colors.lightgrey)
    pdf.setStrokeColor(colors.lightgrey)
    pdf.rect(190, 602, 10, 10, fill=1)
    pdf.setFillColor(background_color)
    pdf.drawString(205, 610, "HB HFMA")


    pdf.setFillColor(colors.white)
    pdf.rect(369, 600, 356, 15, stroke=0, fill=1)
    pdf.setFillColor(background_color)
    pdf.setStrokeColor(background_color)
    pdf.rect(372, 602, 10, 10, fill=1)
    pdf.drawString(390, 610, "PB Current")
    pdf.setFillColor(colors.gray)
    pdf.setStrokeColor(colors.gray)
    pdf.rect(470, 602, 10, 10, fill=1)
    pdf.setFillColor(background_color)
    pdf.drawString(485, 610, "PB EPIC")
    pdf.setFillColor(colors.lightgrey)
    pdf.setStrokeColor(colors.lightgrey)
    pdf.rect(560, 602, 10, 10, fill=1)
    pdf.setFillColor(background_color)
    pdf.drawString(580, 610, "PB HFMA")


    pdf.setFillColor(colors.black)
    pdf.setFont('Times-Roman', 10)
    pdf.drawString(10, 1150, f"Date: {date.strftime('%d-%m-%Y')}")
    pdf.drawCentredString(362.5, 1150, "CLAIMS")


# sauce code: 139033

    ############################################### Financial ######################################################
    pdf.showPage()

    pdf.translate(cm, cm)
    pdf.setPageSize((A3[0]-50, A3[1]))
    pdf.setFillColor(background_color)
    pdf.setLineWidth(0.1)
    pdf.setStrokeColor(background_color)
    pdf.rect(5, 10, 725, 1050, stroke=0, fill=1)

    pdf.setFont('Times-Roman', 10)
    pdf.setFillColor(colors.white)
    pdf.rect(10, 20, 715, 20, stroke=0, fill=1)
    pdf.setFillColor(colors.red)
    pdf.drawCentredString(362.5, 36, "PATIENT FINANCIAL INFORMATION")


    pdf.setFillColor(colors.white)
    pdf.drawCentredString(362.5, 60, "HB PATIENT FINANCIAL SERVICES -- RATIO OF CURRENT TO TARGET ($)")
    pdf.rect(10, 64, 715, 120, stroke=0, fill=1)

    pdf.setFont('Times-Roman', 8)
    c = financial['Current']['Bad Debt']
    t = financial['Target']['Bad Debt']
    angle_graph(pdf, c, t, 15, 80, type='money')
    text = "Bad Debt"
    draw_wrapped_line(pdf, text, 70, 65, 170, 10, 'center')

    c = financial['Current']['Charity Care']
    t = financial['Target']['Charity Care']
    angle_graph(pdf, c, t, 165, 80, type='money')
    text = "Charity Care"
    draw_wrapped_line(pdf, text, 70, 215, 170, 10, 'center')

    c = financial['Current']['cost to Collect ']
    t = financial['Target']['cost to Collect ']
    angle_graph(pdf, c, t, 315, 80, type='money')
    text = "Cost to Collect"
    draw_wrapped_line(pdf, text, 70, 360, 170, 10, 'center')

    c = financial['Current']['Denial Write-offs as a % of NPSR']
    t = financial['Target']['Denial Write-offs as a % of NPSR']
    angle_graph(pdf, c, t, 465, 80, type='money')
    text = "Denial Write-offs as a % of NPSR"
    draw_wrapped_line(pdf, text, 30, 520, 170, 10, 'center')

    c = financial['Current']['Point-of-Service (POS) Cash Collections ']
    t = financial['Target']['Point-of-Service (POS) Cash Collections ']
    angle_graph(pdf, c, t, 615, 80, type='money')
    text = "Point-of-Service (POS) Cash Collections"
    draw_wrapped_line(pdf, text, 30, 670, 170, 10, 'center')


    pdf.setFillColor(colors.white)
    pdf.setFont('Times-Roman', 10)
    pdf.drawCentredString(362.5, 200, "HB PATIENT FINANCIAL SERVICES -- RATIO OF CURRENT TO TARGET (% and DAYS)")
    pdf.rect(10, 204, 715, 120, stroke=0, fill=1)
    pdf.setFont('Times-Roman', 8)
    pdf.setFillColor(background_color)

    c = financial['Current']['Aged AR as a % of Total AR ']
    t = financial['Target']['Aged AR as a % of Total AR ']
    angle_graph(pdf, c, t, 15, 220, 90)
    text = "Aged AR as a % of Total AR"
    draw_wrapped_line(pdf, text, 20, 60, 310, 10, 'center')

    c = financial['Current']['Aged AR as a % of Total Billed AR']
    t = financial['Target']['Aged AR as a % of Total Billed AR']
    angle_graph(pdf, c, t, 115, 220, 90)
    text = "Aged AR as a % of Total Billed AR"
    draw_wrapped_line(pdf, text, 20, 165, 310, 10, 'center')
    c = financial['Current']['Cash Collections as % of NPSR']
    t = financial['Target']['Cash Collections as % of NPSR']
    angle_graph(pdf, c, t, 215, 220, 90)
    text = "Cash Collections as % of NPSR"
    draw_wrapped_line(pdf, text, 20, 265, 310, 10, 'center')

    c = financial['Current']['Net Days In AR']
    t = financial['Target']['Net Days In AR']
    angle_graph(pdf, c, t, 315, 220, 90, type='days')
    text = "Net Days In AR"
    draw_wrapped_line(pdf, text, 20, 355, 310, 10, 'center')

    c = financial['Current']['Net Days in Credit Balance']
    t = financial['Target']['Net Days in Credit Balance']
    angle_graph(pdf, c, t, 415, 220, 90, type='days')
    text = "Net Days in Credit Balance"
    draw_wrapped_line(pdf, text, 20, 460, 310, 10, 'center')

    c = financial['Current']['Remittance Denials Rate ']
    t = financial['Target']['Remittance Denials Rate ']
    angle_graph(pdf, c, t, 515, 220, 90)
    text = "Remittance Denials Rate"
    draw_wrapped_line(pdf, text, 20, 560, 310, 10, 'center')

    c = financial['Current']['Uncompensated Care ']
    t = financial['Target']['Uncompensated Care ']
    angle_graph(pdf, c, t, 615, 220, 90)
    text = "Uncompensated Care"
    draw_wrapped_line(pdf, text, 20, 660, 310, 10, 'center')





    pdf.setFont('Times-Roman', 10)

    pdf.setFillColor(colors.white)
    pdf.drawCentredString(362.5, 338, "PB PATIENT FINANCIAL SERVICES -- RATIO OF CURRENT TO TARGET ($)")
    pdf.rect(10, 345, 715, 120, stroke=0, fill=1)

    pdf.setFont('Times-Roman', 8)
    c = financial['Current']['Bad Debt']
    t = financial['Target']['Bad Debt']
    angle_graph(pdf, c, t, 15, 360, type='money')
    text = "Bad Debt"
    draw_wrapped_line(pdf, text, 70, 65, 450, 10, 'center')

    c = financial['Current']['Charity Care']
    t = financial['Target']['Charity Care']
    angle_graph(pdf, c, t, 165, 360, type='money')
    text = "Charity Care"
    draw_wrapped_line(pdf, text, 70, 215, 450, 10, 'center')

    c = financial['Current']['cost to Collect ']
    t = financial['Target']['cost to Collect ']
    angle_graph(pdf, c, t, 315, 360, type='money')
    text = "Cost to Collect"
    draw_wrapped_line(pdf, text, 70, 360, 450, 10, 'center')

    c = financial['Current']['Denial Write-offs as a % of NPSR']
    t = financial['Target']['Denial Write-offs as a % of NPSR']
    angle_graph(pdf, c, t, 465, 360, type='money')
    text = "Denial Write-offs as a % of NPSR"
    draw_wrapped_line(pdf, text, 30, 520, 450, 10, 'center')

    c = financial['Current']['Point-of-Service (POS) Cash Collections ']
    t = financial['Target']['Point-of-Service (POS) Cash Collections ']
    angle_graph(pdf, c, t, 615, 360, type='money')
    text = "Point-of-Service (POS) Cash Collections"
    draw_wrapped_line(pdf, text, 30, 670, 450, 10, 'center')


    pdf.setFillColor(colors.white)
    pdf.setFont('Times-Roman', 10)
    pdf.drawCentredString(362.5, 483, "PB PATIENT FINANCIAL SERVICES -- RATIO OF CURRENT TO TARGET (% and DAYS)")
    pdf.rect(10, 490, 715, 120, fill=1)
    pdf.setFont('Times-Roman', 8)
    pdf.setFillColor(background_color)

    c = financial['Current']['Aged AR as a % of Total AR ']
    t = financial['Target']['Aged AR as a % of Total AR ']
    angle_graph(pdf, c, t, 15, 500, 90)
    text = "Aged AR as a % of Total AR"
    draw_wrapped_line(pdf, text, 20, 60, 590, 10, 'center')

    c = financial['Current']['Aged AR as a % of Total Billed AR']
    t = financial['Target']['Aged AR as a % of Total Billed AR']
    angle_graph(pdf, c, t, 115, 500, 90)
    text = "Aged AR as a % of Total Billed AR"
    draw_wrapped_line(pdf, text, 20, 165, 590, 10, 'center')
    c = financial['Current']['Cash Collections as % of NPSR']
    t = financial['Target']['Cash Collections as % of NPSR']
    angle_graph(pdf, c, t, 215, 500, 90)
    text = "Cash Collections as % of NPSR"
    draw_wrapped_line(pdf, text, 20, 265, 590, 10, 'center')

    c = financial['Current']['Net Days In AR']
    t = financial['Target']['Net Days In AR']
    angle_graph(pdf, c, t, 315, 500, 90, type='days')
    text = "Net Days In AR"
    draw_wrapped_line(pdf, text, 20, 355, 590, 10, 'center')

    c = financial['Current']['Net Days in Credit Balance']
    t = financial['Target']['Net Days in Credit Balance']
    angle_graph(pdf, c, t, 415, 500, 90, type='days')
    text = "Net Days in Credit Balance"
    draw_wrapped_line(pdf, text, 20, 460, 590, 10, 'center')

    c = financial['Current']['Remittance Denials Rate ']
    t = financial['Target']['Remittance Denials Rate ']
    angle_graph(pdf, c, t, 515, 500, 90)
    text = "Remittance Denials Rate"
    draw_wrapped_line(pdf, text, 20, 560, 590, 10, 'center')

    c = financial['Current']['Uncompensated Care ']
    t = financial['Target']['Uncompensated Care ']
    angle_graph(pdf, c, t, 615, 500, 90)
    text = "Uncompensated Care"
    draw_wrapped_line(pdf, text, 20, 660, 590, 10, 'center')



# sauce code: 15194

    pdf.setFont('Times-Roman', 10)
    pdf.setFillColor(colors.white)
    pdf.drawCentredString(178, 623, "HB PATIENT FINANCIAL ACCESS -- HENNEPIN VS OTHERS ($)")

    pdf.rect(10, 630, 356, 400, fill=1)
    pdf.setFillColor(colors.black)
    pdf.setStrokeColor(colors.black)

    text = "Bad Debt"
    draw_wrapped_line(pdf, text, 13, 13, 640, 10, 'left')
    current = financial['Current']['Bad Debt']
    epic = financial['EPIC']['Bad Debt']
    hfma = financial['HFMA']['Bad Debt']
    histogram_graph(pdf, current, epic, hfma, 80, 640, type='money')
    pdf.line(10, 710, 367, 710)

    text = "Charity Care"
    draw_wrapped_line(pdf, text, 13, 13, 720, 10, 'left')
    current = financial['Current']['Charity Care']
    epic = financial['EPIC']['Charity Care']
    hfma = financial['HFMA']['Charity Care']
    histogram_graph(pdf, current, epic, hfma, 80, 720, type='money')
    pdf.line(10, 790, 367, 790)

    text = "Cost to Collect"
    draw_wrapped_line(pdf, text, 13, 13, 800, 10, 'left')
    current = financial['Current']['cost to Collect ']
    epic = financial['EPIC']['cost to Collect ']
    hfma = financial['HFMA']['cost to Collect ']
    histogram_graph(pdf, current, epic, hfma, 80, 800, type='money')
    pdf.line(10, 870, 367, 870)

    text = "Denial Write-offs as a % of NPSR"
    draw_wrapped_line(pdf, text, 13, 13, 880, 10, 'left')
    current = financial['Current']['Denial Write-offs as a % of NPSR']
    epic = financial['EPIC']['Denial Write-offs as a % of NPSR']
    hfma = financial['HFMA']['Denial Write-offs as a % of NPSR']
    histogram_graph(pdf, current, epic, hfma, 80, 880, type='money')
    pdf.line(10, 950, 367, 950)

    text = "Point-of-Service (POS) Cash Collections"
    draw_wrapped_line(pdf, text, 13, 13, 960, 10, 'left')
    current = financial['Current']['Point-of-Service (POS) Cash Collections ']
    epic = financial['EPIC']['Point-of-Service (POS) Cash Collections ']
    hfma = financial['HFMA']['Point-of-Service (POS) Cash Collections ']
    histogram_graph(pdf, current, epic, hfma, 80, 960, type='money')



    pdf.setFont('Times-Roman', 10)
    pdf.setFillColor(colors.white)
    pdf.drawCentredString(547, 623, "PB PATIENT FINANCIAL ACCESS -- HENNEPIN VS OTHERS ($)")

    pdf.rect(369, 630, 356, 400, fill=1)
    pdf.setFillColor(colors.black)
    pdf.setStrokeColor(colors.black)

    text = "Bad Debt"
    draw_wrapped_line(pdf, text, 13, 372, 640, 10, 'left')
    current = financial['Current']['Bad Debt']
    epic = financial['EPIC']['Bad Debt']
    hfma = financial['HFMA']['Bad Debt']
    histogram_graph(pdf, current, epic, hfma, 450, 640, type='money')
    pdf.line(369, 710, 725, 710)

    text = "Charity Care"
    draw_wrapped_line(pdf, text, 13, 372, 720, 10, 'left')
    current = financial['Current']['Charity Care']
    epic = financial['EPIC']['Charity Care']
    hfma = financial['HFMA']['Charity Care']
    histogram_graph(pdf, current, epic, hfma, 450, 720, type='money')
    pdf.line(369, 790, 725, 790)

    text = "Cost to Collect"
    draw_wrapped_line(pdf, text, 13, 372, 800, 10, 'left')
    current = financial['Current']['cost to Collect ']
    epic = financial['EPIC']['cost to Collect ']
    hfma = financial['HFMA']['cost to Collect ']
    histogram_graph(pdf, current, epic, hfma, 450, 800, type='money')
    pdf.line(369, 870, 725, 870)

    text = "Denial Write-offs as a % of NPSR"
    draw_wrapped_line(pdf, text, 13, 372, 880, 10, 'left')
    current = financial['Current']['Denial Write-offs as a % of NPSR']
    epic = financial['EPIC']['Denial Write-offs as a % of NPSR']
    hfma = financial['HFMA']['Denial Write-offs as a % of NPSR']
    histogram_graph(pdf, current, epic, hfma, 450, 880, type='money')
    pdf.line(369, 950, 725, 950)

    text = "Point-of-Service (POS) Cash Collections"
    draw_wrapped_line(pdf, text, 13, 372, 960, 10, 'left')
    current = financial['Current']['Point-of-Service (POS) Cash Collections ']
    epic = financial['EPIC']['Point-of-Service (POS) Cash Collections ']
    hfma = financial['HFMA']['Point-of-Service (POS) Cash Collections ']
    histogram_graph(pdf, current, epic, hfma, 450, 960, type='money')





    pdf.setFillColor(colors.white)
    pdf.setFont('Times-Roman', 10)
    pdf.rect(10, 1040, 356, 15, stroke=0, fill=1)
    pdf.setFillColor(background_color)
    pdf.setStrokeColor(background_color)
    pdf.rect(12, 1042, 10, 10, fill=1)
    pdf.drawString(27, 1050, "HB Current")
    pdf.setFillColor(colors.gray)
    pdf.setStrokeColor(colors.gray)
    pdf.rect(100, 1042, 10, 10, fill=1)
    pdf.setFillColor(background_color)
    pdf.drawString(115, 1050, "HB EPIC")
    pdf.setFillColor(colors.lightgrey)
    pdf.setStrokeColor(colors.lightgrey)
    pdf.rect(190, 1042, 10, 10, fill=1)
    pdf.setFillColor(background_color)
    pdf.drawString(205, 1050, "HB HFMA")


    pdf.setFillColor(colors.white)
    pdf.rect(369, 1040, 356, 15, stroke=0, fill=1)
    pdf.setFillColor(background_color)
    pdf.setStrokeColor(background_color)
    pdf.rect(372, 1042, 10, 10, fill=1)
    pdf.drawString(390, 1050, "PB Current")
    pdf.setFillColor(colors.gray)
    pdf.setStrokeColor(colors.gray)
    pdf.rect(470, 1042, 10, 10, fill=1)
    pdf.setFillColor(background_color)
    pdf.drawString(485, 1050, "PB EPIC")
    pdf.setFillColor(colors.lightgrey)
    pdf.setStrokeColor(colors.lightgrey)
    pdf.rect(560, 1042, 10, 10, fill=1)
    pdf.setFillColor(background_color)
    pdf.drawString(580, 1050, "PB HFMA")



    pdf.setFillColor(colors.black)
    pdf.setFont('Times-Roman', 10)
    pdf.drawString(10, 1150, f"Date: {date.strftime('%d-%m-%Y')}")
    pdf.drawCentredString(362.5, 1150, "PATIENT FINANCIAL INFORMATION - Page 1")





    # page 2
    pdf.showPage()
    pdf.translate(cm, cm)
    pdf.setPageSize((A3[0]-50, A3[1]))
    pdf.setFillColor(background_color)
    pdf.setLineWidth(0.1)
    pdf.setStrokeColor(background_color)
    pdf.rect(5, 10, 725, 605, stroke=0, fill=1)



    pdf.setFont('Times-Roman', 10)
    pdf.setFillColor(colors.white)
    pdf.drawCentredString(178, 20, "HB PATIENT FINANCIAL ACCESS -- HENNEPIN VS OTHERS ($)")


    pdf.setFillColor(colors.white)
    pdf.rect(10, 25, 356, 560, fill=1)
    pdf.setFillColor(colors.black)
    pdf.setStrokeColor(colors.black)

    text = "Aged AR as a % of Total AR"
    draw_wrapped_line(pdf, text, 70, 13, 35, 10, 'left')
    current = financial['Current']['Aged AR as a % of Total AR ']
    epic = financial['EPIC']['Aged AR as a % of Total AR ']
    hfma = financial['HFMA']['Aged AR as a % of Total AR ']
    histogram_graph(pdf, current, epic, hfma, 100, 40)
    pdf.line(10, 105, 725, 105)

    text = "Aged AR as a % of Total Billed AR"
    draw_wrapped_line(pdf, text, 30, 13, 115, 10, 'left')
    current = financial['Current']['Aged AR as a % of Total Billed AR']
    epic = financial['EPIC']['Aged AR as a % of Total Billed AR']
    hfma = financial['HFMA']['Aged AR as a % of Total Billed AR']
    histogram_graph(pdf, current, epic, hfma, 100, 120)
    pdf.line(10, 185, 725, 185)

    text = "Cash Collections as % of NPSR"
    draw_wrapped_line(pdf, text, 70, 13, 195, 10, 'left')
    current = financial['Current']['Cash Collections as % of NPSR']
    epic = financial['EPIC']['Cash Collections as % of NPSR']
    hfma = financial['HFMA']['Cash Collections as % of NPSR']
    histogram_graph(pdf, current, epic, hfma, 100, 200)
    pdf.line(10, 265, 725, 265)

    text = "Net Days In AR"
    draw_wrapped_line(pdf, text, 70, 13, 275, 10, 'left')
    current = financial['Current']['Net Days In AR']
    epic = financial['EPIC']['Net Days In AR']
    hfma = financial['HFMA']['Net Days In AR']
    histogram_graph(pdf, current, epic, hfma, 100, 280, type='money')
    pdf.line(10, 345, 725, 345)

    text = "Net Days in Credit Balance"
    draw_wrapped_line(pdf, text, 70, 13, 355, 10, 'left')
    current = financial['Current']['Net Days in Credit Balance']
    epic = financial['EPIC']['Net Days in Credit Balance']
    hfma = financial['HFMA']['Net Days in Credit Balance']
    histogram_graph(pdf, current, epic, hfma, 100, 360, type='money')
    pdf.line(10, 425, 725, 425)

    text = "Remittance Denials Rate"
    draw_wrapped_line(pdf, text, 70, 13, 435, 10, 'left')
    current = financial['Current']['Remittance Denials Rate ']
    epic = financial['EPIC']['Remittance Denials Rate ']
    hfma = financial['HFMA']['Remittance Denials Rate ']
    histogram_graph(pdf, current, epic, hfma, 100, 440)
    pdf.line(10, 505, 725, 505)

    text = "Uncompensated Care"
    draw_wrapped_line(pdf, text, 70, 13, 515, 10, 'left')
    current = financial['Current']['Uncompensated Care ']
    epic = financial['EPIC']['Uncompensated Care ']
    hfma = financial['HFMA']['Uncompensated Care ']
    histogram_graph(pdf, current, epic, hfma, 100, 520)



# sauce code: 292090


    pdf.setFont('Times-Roman', 10)
    pdf.setFillColor(colors.white)
    pdf.drawCentredString(547, 20, "PB PATIENT FINANCIAL ACCESS -- HENNEPIN VS OTHERS ($)")

    pdf.setFillColor(colors.white)
    pdf.rect(369, 25, 356, 560, fill=1)
    pdf.setFillColor(colors.black)
    pdf.setStrokeColor(colors.black)

    text = "Aged AR as a % of Total AR"
    draw_wrapped_line(pdf, text, 70, 372, 35, 10, 'left')
    current = financial['Current']['Aged AR as a % of Total AR ']
    epic = financial['EPIC']['Aged AR as a % of Total AR ']
    hfma = financial['HFMA']['Aged AR as a % of Total AR ']
    histogram_graph(pdf, current, epic, hfma, 450, 40)
    pdf.line(369, 105, 725, 105)

    text = "Aged AR as a % of Total Billed AR"
    draw_wrapped_line(pdf, text, 30, 372, 115, 10, 'left')
    current = financial['Current']['Aged AR as a % of Total Billed AR']
    epic = financial['EPIC']['Aged AR as a % of Total Billed AR']
    hfma = financial['HFMA']['Aged AR as a % of Total Billed AR']
    histogram_graph(pdf, current, epic, hfma, 450, 120)
    pdf.line(369, 185, 725, 185)

    text = "Cash Collections as % of NPSR"
    draw_wrapped_line(pdf, text, 70, 372, 195, 10, 'left')
    current = financial['Current']['Cash Collections as % of NPSR']
    epic = financial['EPIC']['Cash Collections as % of NPSR']
    hfma = financial['HFMA']['Cash Collections as % of NPSR']
    histogram_graph(pdf, current, epic, hfma, 450, 200)
    pdf.line(369, 265, 725, 265)

    text = "Net Days In AR"
    draw_wrapped_line(pdf, text, 70, 372, 275, 10, 'left')
    current = financial['Current']['Net Days In AR']
    epic = financial['EPIC']['Net Days In AR']
    hfma = financial['HFMA']['Net Days In AR']
    histogram_graph(pdf, current, epic, hfma, 450, 280, type='money')
    pdf.line(369, 345, 725, 345)

    text = "Net Days in Credit Balance"
    draw_wrapped_line(pdf, text, 70, 372, 355, 10, 'left')
    current = financial['Current']['Net Days in Credit Balance']
    epic = financial['EPIC']['Net Days in Credit Balance']
    hfma = financial['HFMA']['Net Days in Credit Balance']
    histogram_graph(pdf, current, epic, hfma, 450, 360, type='money')
    pdf.line(369, 425, 725, 425)

    text = "Remittance Denials Rate"
    draw_wrapped_line(pdf, text, 70, 372, 435, 10, 'left')
    current = financial['Current']['Remittance Denials Rate ']
    epic = financial['EPIC']['Remittance Denials Rate ']
    hfma = financial['HFMA']['Remittance Denials Rate ']
    histogram_graph(pdf, current, epic, hfma, 450, 440)
    pdf.line(369, 505, 725, 505)

    text = "Uncompensated Care"
    draw_wrapped_line(pdf, text, 70, 372, 515, 10, 'left')
    current = financial['Current']['Uncompensated Care ']
    epic = financial['EPIC']['Uncompensated Care ']
    hfma = financial['HFMA']['Uncompensated Care ']
    histogram_graph(pdf, current, epic, hfma, 450, 520)









    pdf.setFillColor(colors.white)
    pdf.setFont('Times-Roman', 10)
    pdf.rect(10, 590, 356, 15, stroke=0, fill=1)
    pdf.setFillColor(background_color)
    pdf.setStrokeColor(background_color)
    pdf.rect(12, 592, 10, 10, fill=1)
    pdf.drawString(27, 600, "HB Current")
    pdf.setFillColor(colors.gray)
    pdf.setStrokeColor(colors.gray)
    pdf.rect(100, 592, 10, 10, fill=1)
    pdf.setFillColor(background_color)
    pdf.drawString(115, 600, "HB EPIC")
    pdf.setFillColor(colors.lightgrey)
    pdf.setStrokeColor(colors.lightgrey)
    pdf.rect(190, 592, 10, 10, fill=1)
    pdf.setFillColor(background_color)
    pdf.drawString(205, 600, "HB HFMA")


    pdf.setFillColor(colors.white)
    pdf.rect(369, 590, 356, 15, stroke=0, fill=1)
    pdf.setFillColor(background_color)
    pdf.setStrokeColor(background_color)
    pdf.rect(372, 592, 10, 10, fill=1)
    pdf.drawString(390, 600, "PB Current")
    pdf.setFillColor(colors.gray)
    pdf.setStrokeColor(colors.gray)
    pdf.rect(470, 592, 10, 10, fill=1)
    pdf.setFillColor(background_color)
    pdf.drawString(485, 600, "PB EPIC")
    pdf.setFillColor(colors.lightgrey)
    pdf.setStrokeColor(colors.lightgrey)
    pdf.rect(560, 592, 10, 10, fill=1)
    pdf.setFillColor(background_color)
    pdf.drawString(580, 600, "PB HFMA")



# sauce code: 281826



    pdf.setFillColor(colors.black)
    pdf.setFont('Times-Roman', 10)
    pdf.drawString(10, 1150, f"Date: {date.strftime('%d-%m-%Y')}")
    pdf.drawCentredString(362.5, 1150, "PATIENT FINANCIAL INFORMATION - Page 2")





    # save
    pdf.save()