####################################################################################################
#
# Babel - An Electronic Document Management System
# Copyright (C) 2014 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
####################################################################################################

####################################################################################################

import textwrap

####################################################################################################

def remove_enclosing_new_line(text):
    return text[1:-1]

####################################################################################################

class Filet:

    ##############################################

    def __init__(self,
                 horizontal, vertical,
                 top_left, top_right, bottom_left, bottom_right):

        self.horizontal, self.vertical = horizontal, vertical
        self.top_left, self.top_right = top_left, top_right
        self.bottom_left, self.bottom_right = bottom_left, bottom_right

####################################################################################################

empty_filet = Filet('', '', '', '', '', '')

solid_thin_filet = Filet(chr(9472), chr(9474),
                         chr(9484), chr(9488),
                         chr(9492), chr(9496))

solid_wide_filet = Filet(chr(9473), chr(9475),
                         chr(9487), chr(9491),
                         chr(9495), chr(9499))

dash_thin_filet = Filet(chr(9476), chr(9478),
                        chr(9484), chr(9488),
                        chr(9492), chr(9496))

dash_wide_filet = Filet(chr(9477), chr(9479),
                        chr(9487), chr(9491),
                        chr(9495), chr(9499))

solid_thin_doublefilet = Filet(chr(9552), chr(9553),
                               chr(9556), chr(9559),
                               chr(9562), chr(9565))

####################################################################################################

def format_frame(text,
                 filet=solid_thin_filet,
                 centered=False,
                 margin=False,
                 console_width=100,
                 minimum_width=100,
):

    console_width_margin = 2
    lines = []
    for line in text.splitlines():
        sub_lines = textwrap.wrap(line, width=(console_width-console_width_margin))
        if sub_lines:
            lines += [sub_lines[0]] + [' '*console_width_margin + sub_line for sub_line in sub_lines[1:]]
        else:
            lines += ['']
    width = max(max([len(line) for line in lines]), minimum_width)
    if margin:
        width += 2
    rule = filet.horizontal*width
    empty_line = filet.vertical + ' '*width + filet.vertical + '\n'

    output_text = filet.top_left + rule + filet.top_right + '\n'
    if margin:
        output_text += empty_line
    for line in lines:
        if margin:
            line = ' ' + line + ' '
        if centered:
            line = line.center(width)
        else:
            line = line + ' '*(width - len(line))
        output_text += filet.vertical + line + filet.vertical + '\n'
    if margin:
        output_text += empty_line
    output_text += filet.bottom_left + rule + filet.bottom_right + '\n'

    return output_text

####################################################################################################

def format_message_header(text,
                          width=80,
                          centered=False,
                          margin=False,
                          filet=solid_wide_filet,
                          border=False,
                          bottom_rule=True,
                          newline=False):

    if not border:
        filet = empty_filet

    rule = filet.horizontal*width
    empty_line = filet.vertical + ' '*width + filet.vertical + '\n'

    output_text = ''
    if newline:
        output_text += '\n'
    output_text += filet.top_left + rule + filet.top_right + '\n'
    if margin:
        output_text += empty_line
        width_text = width - 2
    else:
        width_text = width
    for line in text.splitlines():
        if margin:
            line = ' ' + line + ' '
        if centered:
            line = line.center(width)
        else:
            line = line + ' '*(width - len(line))
        output_text += filet.vertical + line
        if bottom_rule:
            output_text += filet.vertical
        output_text += '\n'
    if margin:
        output_text += empty_line
    if bottom_rule:
        output_text += filet.bottom_left + rule + filet.bottom_right + '\n'

    return output_text
