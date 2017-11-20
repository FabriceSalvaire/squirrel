#! /usr/bin/env python
# -*- Python -*-

####################################################################################################

import argparse

import numpy as np

import Babel.MuPdf as mupdf

####################################################################################################

def show_metadata(ctx, doc):

    for key in (
        'Title',
        'Subject',
        'Author',
        'Creator',
        'Producer',
        'CreationDate',
        'ModDate',
        ):
        print(mupdf.decode_utf8(mupdf.get_meta_info(ctx, doc, key, 1024)))

    fz_buffer = mupdf.pdf_metadata(doc)
    print(mupdf.decode_utf8(mupdf.buffer_data(fz_buffer)))
    mupdf.drop_buffer(ctx, fz_buffer)

####################################################################################################

argument_parser = argparse.ArgumentParser(description='Example.')

argument_parser.add_argument('filename', metavar='FILENAME',
                             help='PDF file')

argument_parser.add_argument('--page', dest='page_number',
                             type=int,
                             default=1,
                             help='Page number')

argument_parser.add_argument('--zoom', dest='zoom',
                             type=int,
                             default=100,
                             help='Zoom factor in %%')

argument_parser.add_argument('--rotation', dest='rotation',
                             type=int,
                             default=0,
                             help='Rotation')

args = argument_parser.parse_args()

####################################################################################################

# Create a context to hold the exception stack and various caches.
ctx = mupdf.new_context()
mupdf.register_document_handlers(ctx)

####################################################################################################

# Open the PDF, XPS or CBZ document.
doc = mupdf.open_document(ctx, args.filename.encode('utf-8'))

# Fixme:
# show_metadata(ctx, doc)

####################################################################################################

# Retrieve the number of pages (not used in this example).
page_count = mupdf.count_pages(ctx, doc)

# Load the page we want. Page numbering starts from zero.
page = mupdf.load_page(ctx, doc, args.page_number -1)

####################################################################################################

# Calculate a transform to use when rendering. This transform contains the scale and
# rotation. Convert zoom percentage to a scaling factor. Without scaling the resolution is 72 dpi.
transform = mupdf.Matrix()
mupdf.rotate(transform, args.rotation)
mupdf.pre_scale(transform, args.zoom / 100.0, args.zoom / 100.0)

# Take the page bounds and transform them by the same matrix that we will use to render the page.
bounds = mupdf.Rect()
mupdf.bound_page(ctx, page, bounds)
mupdf.transform_rect(bounds, transform)

####################################################################################################

# A page consists of a series of objects (text, line art, images, gradients). These objects are
# passed to a device when the interpreter runs the page. There are several devices, used for
# different purposes:
#
#	draw device -- renders objects to a target pixmap.
#
#	text device -- extracts the text in reading order with styling
#	information. This text can be used to provide text search.
#
#	list device -- records the graphic objects in a list that can
#	be played back through another device. This is useful if you
#	need to run the same page through multiple devices, without
#	the overhead of parsing the page each time.

####################################################################################################

# Create a blank pixmap to hold the result of rendering. The pixmap bounds used here are the same as
# the transformed page bounds, so it will contain the entire page. The page coordinate space has the
# origin at the top left corner and the x axis extends to the right and the y axis extends down.
bbox = mupdf.IRect()
mupdf.round_rect(bbox, bounds)
width, height = bbox.x1 - bbox.x0, bbox.y1 - bbox.y0
np_array = np.zeros((height, width, 4), dtype=np.uint8)
# pixmap = mupdf.new_pixmap_with_bbox(ctx, mupdf.get_fz_device_rgb(), bbox)
pixmap = mupdf.new_pixmap_with_bbox_and_data(ctx, mupdf.device_rgb(ctx), bbox,
                                                 mupdf.np_array_uint8_ptr(np_array))
mupdf.clear_pixmap_with_value(ctx, pixmap, 0xff)

# Create a draw device with the pixmap as its target.
# Run the page with the transform.
device = mupdf.new_draw_device(ctx, pixmap)
mupdf.set_aa_level(ctx, 8)
mupdf.run_page(ctx, page, device, transform, mupdf.NULL)
mupdf.drop_device(ctx, device)

# Save the pixmap to a file.
# mupdf.write_png(ctx, pixmap, 'out.png'.encode('utf-8'), 0)
from PIL import Image
image = Image.fromarray(np_array, mode='RGBA')
image.save('out.png')

####################################################################################################

# Clean up.
mupdf.drop_pixmap(ctx, pixmap)
mupdf.drop_page(ctx, page)
mupdf.drop_document(ctx, doc)
mupdf.drop_context(ctx)
