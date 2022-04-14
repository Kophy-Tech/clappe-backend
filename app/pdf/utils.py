from reportlab.lib import colors
import textwrap


background_color = colors.Color(0.1875, 0.390625, 0.5625)


def angle_graph(pdf, c, t, x, y, size=100, type='percent'):

    '''
    This function is for drawing the speedometer looking graph using overlapping sector, semi-circle and circle.
    Input:
        pdf - pdf object
        c - current value
        t - target value
        x - value for x-axis
        y - value for y-axis
        size - how big the graph should be, default of 100 (this value worked for most cases)
        type - the type of the text on the graph, it can be percent, money or days, default is percent

    Output: None
    '''

    pdf.setStrokeColor(colors.white)
    pdf.setFillColor(colors.gray)
    # draw the background semi-circle
    pdf.wedge(x, y, x+size, y+size, 180, 180, fill=1)


    # sauce code: 112940

    # calculate the angle for the overlapping sector (converts the current value into angle)
    current_angle = int((c / (c+t))*180)

    pdf.setFillColor(background_color)
    # draw the overlapping sector
    pdf.wedge(x, y, x+size, y+size, 180, current_angle, fill=1)

    pdf.setFillColor(colors.white)
    # draw the top circle that will house the text for the graph
    pdf.circle(x+(size/2),y+(size/2), 30, fill=1)

    pdf.setFillColor(colors.black)
    pdf.setStrokeColor(colors.black)
    
    pdf.setFontSize(8)

    try:
        # this value helps center the text very well
        a = (size-100)/2
    except:
        a = 0

    
    if type == 'percent':
        # calculate the percetanges that will be printed on the circle
        percent_c = int(round((c / (c+t))*100, 2))
        percent_t = int(round((t / (c+t))*100, 2))
        pdf.drawCentredString(x+50+a, y+35, f"{percent_c}%")
        pdf.drawCentredString(x+50+a, y+45, f"C:{percent_c}%")
        pdf.drawCentredString(x+50+a, y+55, f"T:{percent_t}%")

    elif type == 'money':
        # print the text on the graph if the type is money
        pdf.drawCentredString(x+50+a, y+35, "${:.2f}".format(c).strip())
        pdf.drawCentredString(x+50+a, y+45, "C: ${:.2f}".format(c).strip())
        pdf.drawCentredString(x+50+a, y+55, "T: ${:.2f}".format(t).strip())

    else:
        # print the text on the graph if the type is days
        pdf.drawCentredString(x+50+a, y+35, "{:.0f}days".format(c))
        pdf.drawCentredString(x+50+a, y+45, "C:{:.0f}days".format(c))
        pdf.drawCentredString(x+50+a, y+55, "T:{:.0f}days".format(t))
        

# sauce code: 112940


def histogram_graph(pdf, current, epic, hfma, x, y, space=20, type='percent'):
    '''
    This function is for drawing the histogram graph using 3 rectangles.
    Input:
        pdf - pdf object
        current - current value
        epic - epic value
        hfma - hfma value
        x - value for x-axis
        y - value for y-axis
        space - how amount of space that should be between each rectangle, default of 20 (this value worked for most cases)
        type - the type of the text on the graph, it can be percent, money or days, default is percent

    Output: None
    '''

    pdf.setFillColor(background_color)
    pdf.setStrokeColor(colors.white)

    # calculate the percentage of each data passed to the function, using 200 as the max value
    # 200 is used bcause it is the max legth of the rectangle
    current_p = (current / (current+epic+hfma)) * 200
    epic_p = (epic / (current+epic+hfma)) * 200
    hfma_p = (hfma / (current+epic+hfma)) * 200

    # draw the rectangles using percentages calculated above
    pdf.rect(x, y, current_p, 15, fill=1)
    pdf.setFillColor(colors.gray)
    pdf.rect(x, y+space, epic_p, 15, fill=1)
    pdf.setFillColor(colors.lightgrey)
    pdf.rect(x, y+space+space, hfma_p, 15, fill=1)

    pdf.setFillColor(colors.black)
    pdf.setStrokeColor(colors.black)


    if type=='percent':
        # print the text on the graph if the type is percent
        pdf.drawString(x+current_p+10, y+12, "{:.2f}%".format((current_p/200)*100))
        pdf.drawString(x+epic_p+10, y+32, "{:.2f}%".format((epic_p/200)*100))
        pdf.drawString(x+hfma_p+10, y+52, "{:.2f}%".format((hfma_p/200)*100))

    elif type=='money':
        # print the text on the graph if the type is money
        pdf.drawString(x+current_p+10, y+12, "${:.2f}".format(current).strip())
        pdf.drawString(x+epic_p+10, y+32, "${:.2f}".format(epic).strip())
        pdf.drawString(x+hfma_p+10, y+52, "${:.2f}".format(hfma).strip())

    else:
        # print the text on the graph if the type is days
        pdf.drawString(x+current_p+10, y+12, "{:.0f} days".format(current))
        pdf.drawString(x+epic_p+10, y+32, "{:.0f} days".format(epic))
        pdf.drawString(x+hfma_p+10, y+52, "{:.0f} days".format(hfma))



# sauce code: 278832

def draw_wrapped_line(pdf, text, length, x_pos, y_pos, y_offset, w_type):
    '''
    This function is for wrapping text.
    Input:
        pdf - pdf object
        text - the text you want to wrap
        length - the number of characters that should be on eah line.
        x_pos - value for x-axis
        y_pos - value for y-axis
        y_offset - amount of space that should be between each line of text.
        w_type - defines how the text should be displayed, either centered aligned or left aligned, take canter or left as value

    Output: None
    '''

    if len(text) > length:
        wraps = textwrap.wrap(text, length)
        for x in range(len(wraps)):
            if w_type == 'center':
                pdf.drawCentredString(x_pos, y_pos, wraps[x])
            else:
                pdf.drawString(x_pos, y_pos, wraps[x])
            y_pos += y_offset
    else:
        if w_type == 'center':
            pdf.drawCentredString(x_pos, y_pos, text)
        else:
            pdf.drawString(x_pos, y_pos, text)
    
    return y_pos

# sauce code: 210510