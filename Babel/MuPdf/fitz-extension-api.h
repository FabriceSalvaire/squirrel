/**************************************************************************************************/

FILE * fz_fopen(const char *filename, const char *mode);
char * fz_buffer_data(fz_buffer *buffer);
const char * get_font_name(const fz_font *font);
fz_buffer * pdf_metadata(fz_document *doc);
fz_irect * fz_copy_irect(fz_irect * dst, const fz_irect * src);
fz_rect * fz_copy_rect(fz_rect * dst, const fz_rect * src);
fz_text_block * get_text_block(fz_text_page *page, unsigned int block_index);
fz_text_char * get_text_char(fz_text_span *span, unsigned int char_index);
fz_text_line * get_text_line(fz_text_block *block, unsigned int line_index);
fz_text_span * get_text_span(fz_text_line *line, unsigned int span_index);
int font_is_bold(const fz_font *font);
int font_is_italic(const fz_font *font);
int fz_fclose(FILE *file);
int meta(fz_document *doc, int key, char * string, char *buffer, int buffer_size);

void init();
void python_throw_exit_callback(char *message);
fz_document * open_document (fz_context * ctx, const char *filename);

/***************************************************************************************************
 * 
 * End
 * 
 **************************************************************************************************/
