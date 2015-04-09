/**************************************************************************************************
 *
 * Constants
 *
 */

enum {
  FZ_STORE_UNLIMITED = 0,
  // FZ_STORE_DEFAULT = 256 << 20,
};

/**************************************************************************************************/

/* Structures */

typedef struct _IO_FILE FILE;

typedef struct fz_alloc_context_s fz_alloc_context;
typedef struct fz_buffer_s fz_buffer;
typedef struct fz_colorspace_s fz_colorspace;
typedef struct fz_context_s fz_context;
typedef struct fz_cookie_s fz_cookie;
typedef struct fz_device_s fz_device;
typedef struct fz_document_s fz_document;
typedef struct fz_font_s fz_font;
typedef struct fz_image_block_s fz_image_block;
typedef struct fz_image_s fz_image;
typedef struct fz_irect_s fz_irect;
typedef struct fz_locks_context_s fz_locks_context;
typedef struct fz_matrix_s fz_matrix;
typedef struct fz_output_s fz_output;
typedef struct fz_page_block_s fz_page_block;
typedef struct fz_page_s fz_page;
typedef struct fz_pixmap_s fz_pixmap;
typedef struct fz_point_s fz_point;
typedef struct fz_rect_s fz_rect;
typedef struct fz_scale_cache_s fz_scale_cache;
typedef struct fz_stream_s fz_stream;
typedef struct fz_text_block_s fz_text_block;
typedef struct fz_text_char_s fz_text_char;
typedef struct fz_text_item_s fz_text_item;
typedef struct fz_text_line_s fz_text_line;
typedef struct fz_text_page_s fz_text_page;
typedef struct fz_text_sheet_s fz_text_sheet;
typedef struct fz_text_span_s fz_text_span;
typedef struct fz_text_style_s fz_text_style;

/**************************************************************************************************/

/* Structures Details */

/*
struct fz_colorspace_s
{
  // fz_storable storable;
  unsigned int size;
  char name[16];
  int n;
  void (*to_rgb)(fz_context *ctx, fz_colorspace *, float *src, float *rgb);
  void (*from_rgb)(fz_context *ctx, fz_colorspace *, float *rgb, float *dst);
  void (*free_data)(fz_context *Ctx, fz_colorspace *);
  void *data;
};
*/

/*
struct fz_image_block_s
{
  fz_rect bbox;
  fz_matrix mat;
  fz_image *image;
  fz_colorspace *cspace;
  float colors[FZ_MAX_COLORS];
};
*/

struct fz_irect_s
{
  int x0, y0;
  int x1, y1;
};

/*
struct fz_document_s
{
  void (*close)(fz_document *);
  int (*needs_password)(fz_document *doc);
  int (*authenticate_password)(fz_document *doc, char *password);
  // fz_outline *(*load_outline)(fz_document *doc);
  int (*count_pages)(fz_document *doc);
  fz_page *(*load_page)(fz_document *doc, int number);
  // fz_link *(*load_links)(fz_document *doc, fz_page *page);
  fz_rect *(*bound_page)(fz_document *doc, fz_page *page, fz_rect *);
  void (*run_page_contents)(fz_document *doc, fz_page *page, fz_device *dev, const fz_matrix *transform, fz_cookie *cookie);
  // void (*run_annot)(fz_document *doc, fz_page *page, fz_annot *annot, fz_device *dev, const fz_matrix *transform, fz_cookie *cookie);
  void (*free_page)(fz_document *doc, fz_page *page);
  int (*meta)(fz_document *doc, int key, void *ptr, int size);
  // fz_transition *(*page_presentation)(fz_document *doc, fz_page *page, float *duration);
  // fz_annot *(*first_annot)(fz_document *doc, fz_page *page);
  // fz_annot *(*next_annot)(fz_document *doc, fz_annot *annot);
  // fz_rect *(*bound_annot)(fz_document *doc, fz_annot *annot, fz_rect *rect);
  // void (*write)(fz_document *doc, char *filename, fz_write_options *opts);
};
*/

struct fz_matrix_s
{
  float a, b, c, d, e, f;
};

struct fz_point_s
{
  float x, y;
};

struct fz_rect_s
{
  float x0, y0;
  float x1, y1;
};

struct fz_text_s
{
  fz_font *font;
  fz_matrix trm;
  int wmode;
  int len, cap;
  fz_text_item *items;
};

struct fz_text_page_s
{
  fz_rect mediabox;
  int len, cap;
  fz_page_block *blocks;
  fz_text_page *next;
};

struct fz_page_block_s
{
  int type;
  union
  {
    fz_text_block *text;
    fz_image_block *image;
  } u;
};

struct fz_text_block_s
{
  fz_rect bbox;
  int len, cap;
  fz_text_line *lines;
};

struct fz_text_char_s
{
  fz_point p;
  int c;
  fz_text_style *style;
};

struct fz_text_line_s
{
  fz_text_span *first_span, *last_span;
  float distance;
  fz_rect bbox;
  void *region;
};

struct fz_text_sheet_s
{
  int maxid;
  fz_text_style *style;
};

struct fz_text_span_s
{
  int len, cap;
  fz_text_char *text;
  fz_point min;
  fz_point max;
  int wmode;
  fz_matrix transform;
  float ascender_max;
  float descender_min;
  fz_rect bbox;
  float base_offset;
  float spacing;
  int column;
  float column_width;
  int align;
  float indent;
  fz_text_span *next;
};

struct fz_text_style_s
{
  fz_text_style *next;
  int id;
  fz_font *font;
  float size;
  int wmode;
  int script;
  float ascender;
  float descender;
};

/**************************************************************************************************/

/* Functions */

fz_colorspace * fz_device_rgb (fz_context * ctx);
fz_context * fz_new_context (fz_alloc_context * alloc, fz_locks_context * locks, unsigned int max_store);
fz_device * fz_new_draw_device (fz_context * ctx, fz_pixmap * dest);
fz_device * fz_new_draw_device_type3 (fz_context * ctx, fz_pixmap * dest);
fz_device * fz_new_draw_device_with_bbox (fz_context * ctx, fz_pixmap * dest, const fz_irect * clip);
fz_device * fz_new_text_device (fz_context * ctx, fz_text_sheet * sheet, fz_text_page * page);
fz_document * fz_open_document (fz_context * ctx, const char *filename);
fz_document * fz_open_document_with_stream (fz_context * ctx, const char *magic, fz_stream * stream);
fz_irect * fz_round_rect (fz_irect * bbox, const fz_rect * rect);
fz_matrix * fz_concat (fz_matrix * result, const fz_matrix * left, const fz_matrix * right);
fz_matrix * fz_pre_scale (fz_matrix * m, float sx, float sy);
fz_matrix * fz_rotate (fz_matrix * m, float degrees);
fz_matrix * fz_scale (fz_matrix * m, float sx, float sy);
fz_output * fz_new_output_with_file (fz_context * ctx, FILE *);
fz_pixmap * fz_new_pixmap_with_bbox (fz_context * ctx, fz_colorspace * colorspace, const fz_irect * bbox);
fz_pixmap * fz_new_pixmap_with_bbox_and_data (fz_context * ctx, fz_colorspace * colorspace, const fz_irect * rect, unsigned char *samples);
fz_pixmap * fz_scale_pixmap (fz_context * ctx, fz_pixmap * src, float x, float y, float w, float h, fz_irect * clip);
fz_pixmap * fz_scale_pixmap_cached (fz_context * ctx, fz_pixmap * src, float x, float y, float w, float h, const fz_irect * clip, fz_scale_cache * cache_x, fz_scale_cache * cache_y);
fz_rect * fz_bound_page (fz_document * doc, fz_page * page, fz_rect * rect);
fz_rect * fz_transform_rect (fz_rect * rect, const fz_matrix * transform);
fz_scale_cache * fz_new_scale_cache (fz_context * ctx);
fz_text_page * fz_new_text_page (fz_context * ctx);
fz_text_sheet * fz_new_text_sheet (fz_context * ctx);
int fz_count_pages (fz_document * doc);
int fz_meta(fz_document *doc, int key, void *ptr, int size);
void fz_clear_pixmap_with_value (fz_context * ctx, fz_pixmap * pix, int value);
void fz_close_document (fz_document * doc);
void fz_close_output (fz_output *);
void fz_concat_push (fz_stream * concat, fz_stream * chain);
void fz_drop_buffer (fz_context * ctx, fz_buffer * buf);
void fz_drop_pixmap (fz_context * ctx, fz_pixmap * pix);
void fz_free_context (fz_context * ctx);
void fz_free_device (fz_device * dev);
void fz_free_page (fz_document * doc, fz_page * page);
void fz_free_scale_cache (fz_context * ctx, fz_scale_cache * cache);
void fz_free_text_page (fz_context * ctx, fz_text_page * page);
void fz_free_text_sheet (fz_context * ctx, fz_text_sheet * sheet);
void fz_pixmap_set_resolution (fz_pixmap * pix, int res);
void fz_print_text_page (fz_context * ctx, fz_output * out, fz_text_page * page);
void fz_print_text_page_html (fz_context * ctx, fz_output * out, fz_text_page * page);
void fz_print_text_page_xml (fz_context * ctx, fz_output * out, fz_text_page * page);
void fz_print_text_sheet (fz_context * ctx, fz_output * out, fz_text_sheet * sheet);
void fz_run_page (fz_document * doc, fz_page * page, fz_device * dev, const fz_matrix * transform, fz_cookie * cookie);
void fz_run_page_contents (fz_document * doc, fz_page * page, fz_device * dev, const fz_matrix * transform, fz_cookie * cookie);
void fz_set_aa_level (fz_context * ctx, int bits);
void fz_write_png (fz_context * ctx, fz_pixmap * pixmap, char *filename, int savealpha);

void fz_set_throw_exit_callback(void (*throw_exit_callback) (char * message));

/**************************************************************************************************/

/* pdf.h */
fz_page * fz_load_page (fz_document * doc, int number);

/***************************************************************************************************
 * 
 * End
 * 
 **************************************************************************************************/
