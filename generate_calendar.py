#!/usr/bin/env python
# encoding: utf-8
"""
generate_calendar.py

Created by Maximillian Dornseif on 2010-07-13.
Copyright (c) 2010 HUDORA. All rights reserved.
"""

import sys
import os
import math
import cairo
import calendar
import datetime

LENGTHFACTOR = 1
WIDTH, HEIGHT = 4800, 3250 * LENGTHFACTOR

MONTHFONTSIZE = 36
DAYFONTSIZE = 6
DAYTEXTOFFSET = 12
DAYNUMFONTSIZE = 42
DAYTOPOFFSET = 200
DAYHEIGHT = 80 * LENGTHFACTOR
MONTHWIDTH = 350

def print_centered(ctx, text, x, y):
    x_bearing, y_bearing, width, height = ctx.text_extents(text)[:4]
    ctx.move_to(x - width / 2 - x_bearing, y)
    ctx.show_text(text)

monthnames = u"dummy Januar Februar März April Mai Juni Juli August September Oktober November Dezember".split()
daynames = u"Montag Dienstag Mittwoch Donnerstag Freitag Samstag Sonntag".split()


def main(year):
    surface = cairo.PSSurface("%s.eps" % year, WIDTH, HEIGHT)
    surface.set_eps(True)
    ctx = cairo.Context(surface)
    ctx.set_source_rgb(1, 1, 1)
    ctx.rectangle(0, 0, WIDTH, HEIGHT)
    ctx.fill()

    # ctx.scale (WIDTH/1.0, HEIGHT/1.0) # Normalizing the canvas
    #ctx.scale (72/25.4, 72/25.4);

    # pat = cairo.LinearGradient (0.0, 0.0, 0.0, 1.0)
    # pat.add_color_stop_rgba (1, 0.7, 0, 0, 0.5) # First stop, 50% opacity
    # pat.add_color_stop_rgba (0, 0.9, 0.7, 0.2, 1) # Last stop, 100% opacity
    # #
    # ctx.rectangle (0, 0, 1, 1) # Rectangle(x0, y0, x1, y1)
    # ctx.set_source (pat)
    # ctx.fill ()

    ctx.translate (0.1, 0.1) # Changing the current transformation matrix

    ctx.move_to (0, 0)
    ctx.arc (0.2, 0.1, 0.1, -math.pi/2, 0) # Arc(cx, cy, radius, start_angle, stop_angle)
    ctx.line_to (0.5, 0.1) # Line to (x,y)
    ctx.curve_to (0.5, 0.2, 0.5, 0.4, 0.2, 0.8) # Curve(x1, y1, x2, y2, x3, y3)
    ctx.close_path ()

    ctx.set_source_rgb (0.3, 0.2, 0.5) # Solid color
    ctx.set_line_width(0.01)
    ctx.stroke()

    ctx.set_source_rgb(0.0, 0.0, 0.0)
    ctx.select_font_face("Helvetica", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(DAYFONTSIZE)


    # Drucke eine Spalte mit Wochentagsnamen
    # for i in range(0, 40):
    #     ctx.move_to(10, (DAYHEIGHT * (i+1))+DAYTOPOFFSET + DAYTEXTOFFSET)
    #     ctx.show_text(daynames[i%7])

    for month in range(1, 13):
        # Monatsnamen
        ctx.set_font_size(MONTHFONTSIZE)
        print_centered(ctx, monthnames[month], MONTHWIDTH * (month + 0.5), DAYTOPOFFSET-10)

        day1, ndays = calendar.monthrange(year, month)
        # draw day rectangle background
        for i in range(day1, ndays+day1):
            daynum = i - day1 + 1
            monthposx, monthposy = MONTHWIDTH*month, (DAYHEIGHT * (i + 1) + DAYTOPOFFSET)

            week = int(datetime.date(year, month, daynum).strftime('%V'))  # works on sane C libraries
            if week % 2 == 0 or (week==53 and month==1):
                ctx.set_source_rgb(0.9, 0.95, 1)
                ctx.rectangle(monthposx, monthposy, MONTHWIDTH, DAYHEIGHT)
                ctx.fill()


        # draw week numbers
        ctx.set_font_size(140)
        lastweek = 0
        for i in range(day1, ndays+day1):
            daynum = i - day1 + 1
            monthposx, monthposy = MONTHWIDTH*month, (DAYHEIGHT * (i + 1) + DAYTOPOFFSET)

            week = int(datetime.date(year, month, daynum).strftime('%V'))  # works on sane C libraries
            if week != lastweek:
                lastweek = week
                if week % 2 == 0 or (week==53 and month==1):
                    ctx.set_source_rgb(1, 1, 1)
                else:
                    ctx.set_source_rgb(0.9, 0.95, 1)
                if i > 5:
                    print_centered(ctx, str(week), MONTHWIDTH*month+(MONTHWIDTH*0.6), (DAYHEIGHT * (i + 5) + DAYTOPOFFSET))
                else:
                    print_centered(ctx, str(week), MONTHWIDTH*month+(MONTHWIDTH*0.6), (DAYHEIGHT * (i+(7-i)) + DAYTOPOFFSET))

        # draw day rectangle
        for i in range(day1, ndays+day1):
            daynum = i - day1 + 1
            monthposx, monthposy = MONTHWIDTH*month, (DAYHEIGHT * (i + 1) + DAYTOPOFFSET)

            week = int(datetime.date(year, month, daynum).strftime('%V'))  # works on sane C libraries
            ctx.set_line_width(0.002)
            ctx.set_source_rgb(0, 0, 0)
            ctx.rectangle(monthposx, monthposy, MONTHWIDTH, DAYHEIGHT)
            ctx.stroke()

        # draw days
        for i in range(day1, ndays+day1):
            ctx.set_source_rgb(0, 0, 0)
            daynum = i - day1 + 1
            monthposx, monthposy = MONTHWIDTH*month, (DAYHEIGHT * (i + 1) + DAYTOPOFFSET)

            ctx.set_font_size(DAYNUMFONTSIZE)
            ctx.move_to((MONTHWIDTH*month)+5, (DAYHEIGHT * (i + 1)) + DAYTOPOFFSET + (3*DAYTEXTOFFSET))
            ctx.show_text(str(daynum))

            ctx.set_font_size(DAYFONTSIZE)
            ctx.move_to((MONTHWIDTH*month)+60, (DAYHEIGHT * (i + 1)) + DAYTOPOFFSET + DAYTEXTOFFSET)
            ctx.show_text(daynames[i%7])

    surface.write_to_png("%s.png" % year) # Output to PNG

if __name__ == '__main__':
    main(2013)
    main(2014)
    main(2015)
    main(2016)
    main(2017)
    main(2018)
