/**************************************************************************************************
 *
 * Add some helper functions and missing feature to MuPDF
 * 
 *************************************************************************************************/

/**************************************************************************************************/

#ifndef __FITZ_EXTENSION_H__
#define __FITZ_EXTENSION_H__

/**************************************************************************************************/

#include <stdint.h>

#include "mupdf/fitz.h"

/* ********************************************************************************************** *
 *
 * Provide FILE
 *
 */

static inline
FILE *
fz_fopen(const char *filename, const char *mode)
{
  return fopen(filename, mode);
}

static inline
int
fz_fclose(FILE *file)
{
  return fclose(file);
}

/* ********************************************************************************************** *
 *
 * Add missing copy functions
 *   Only fz_copy_matrix is available
 *
 */

static inline
fz_rect *
fz_copy_rect(fz_rect *restrict dst, const fz_rect *restrict src)
{
  *dst = *src;
  return dst;
}

static inline
fz_irect *
fz_copy_irect(fz_irect *restrict dst, const fz_irect *restrict src)
{
  *dst = *src;
  return dst;
}

/* ********************************************************************************************** *
 *
 * Expose Font private API
 *
 */

// still needed?
static inline
const char *
get_font_name(const fz_font *font)
{
  return font->name;
}

int font_is_bold(const fz_font *font);
int font_is_italic(const fz_font *font);

/* ********************************************************************************************** *
 *
 * Provide access to arrays
 *
 */

static inline
fz_text_block *
get_text_block(fz_text_page *page, unsigned int block_index)
{
  return page->blocks[block_index].u.text;
}

static inline
fz_text_line *
get_text_line(fz_text_block *block, unsigned int line_index)
{
  return &block->lines[line_index];
}

static inline
fz_text_char *
get_text_char(fz_text_span *span, unsigned int char_index)
{
  return &span->text[char_index];
}

// needed ?
fz_text_span * get_text_span(fz_text_line *line, unsigned int span_index);

/* ********************************************************************************************** */

// Expose private API / Helper
static inline
char *
fz_buffer_data(fz_buffer *buffer)
{
  // Swig do it
  // char *string = malloc(buffer.len);
  // strcpy(string, buffer.data);
  // return string;
  return buffer->data;
}

/* ********************************************************************************************** */

int meta(fz_document *doc, int key, char *string, char *buffer, int buffer_size);

/* ********************************************************************************************** */

// Missing feature
// Return the Metadata XML stream
fz_buffer * pdf_metadata(fz_document *doc);

/* ********************************************************************************************** */

#endif /* __FITZ_EXTENSION_H__ */

/***************************************************************************************************
 * 
 * End
 * 
 **************************************************************************************************/
