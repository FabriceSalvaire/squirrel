/**************************************************************************************************/

#include "fitz-extension.h"

/**************************************************************************************************/

#include "mupdf/pdf.h"

#include <ft2build.h>
#include FT_FREETYPE_H
#include FT_ADVANCES_H

/* ********************************************************************************************** */

int
font_is_bold(const fz_font *font)
{
  FT_Face face = font->ft_face;
  if (face && (face->style_flags & FT_STYLE_FLAG_BOLD))
    return 1;
  if (strstr(font->name, "Bold"))
    return 1;
  return 0;
}

int
font_is_italic(const fz_font *font)
{
  FT_Face face = font->ft_face;
  if (face && (face->style_flags & FT_STYLE_FLAG_ITALIC))
    return 1;
  if (strstr(font->name, "Italic") || strstr(font->name, "Oblique"))
    return 1;
  return 0;
}

/* ********************************************************************************************** */

fz_text_span *
get_text_span(fz_text_line *line, unsigned int span_index)
{
  fz_text_span * span = line->first_span;
  size_t i = 0;
  while (i < span_index)
    {
      if (span)
	span = span->next;
      else
	return NULL;
      i += 1;
    }

  return span;
}

/* ********************************************************************************************** */

// Helper for
//  int fz_meta(fz_document *doc, int key, void *ptr, int size);
int
meta(fz_document *doc, int key, char *string, char *buffer, int buffer_size)
{
  *(char **)buffer = string;
  return fz_meta(doc, key, buffer, buffer_size);
}

/* ********************************************************************************************** */

// Fixme: missing feature in mupdf/pdf.h
fz_buffer *
pdf_metadata(fz_document *_doc)
{
  if (_doc) // Fixme: check document is a pdf!
    {
      pdf_document *doc = (pdf_document *)_doc;
      pdf_obj *catalog = pdf_dict_gets(pdf_trailer(doc), "Root");
      pdf_obj *metadata = pdf_dict_gets(catalog, "Metadata");
      if (metadata)
	{
	  fz_stream *stm = pdf_open_stream(doc, pdf_to_num(metadata), pdf_to_gen(metadata));
	  fz_buffer *buffer = fz_read_all(stm, 10240); // Fixme:
	  fz_close(stm);
	  return buffer;
	}
    }
  return NULL;
}

/* ********************************************************************************************** */

#include <setjmp.h>
jmp_buf exception_buffer;
char *exception_message = NULL;

void
python_throw_exit_callback(char *message)
{
  exception_message = message;
  fz_longjmp(exception_buffer, 1);
}

void
init () {
  fz_set_throw_exit_callback(python_throw_exit_callback);
}

fz_document *
open_document (fz_context * ctx, const char *filename) {
  if (! fz_setjmp(exception_buffer))
  {
    return fz_open_document(ctx, filename);
  }
  else // an exception raised
  {
    // PyErr_SetString(PyExc_NameError, exception_message);
    return NULL;
  }
}

/***************************************************************************************************
 * 
 * End
 * 
 **************************************************************************************************/
