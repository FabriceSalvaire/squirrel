/* Constants */

enum {
  FZ_STORE_UNLIMITED = 0,
  // FZ_STORE_DEFAULT = 256 << 20,
};

/* Structures */

typedef struct fz_alloc_context_s fz_alloc_context;
typedef struct fz_buffer_s fz_buffer;
typedef struct fz_colorspace_s fz_colorspace;
typedef struct fz_context_s fz_context;
typedef struct fz_cookie_s fz_cookie;
typedef struct fz_device_s fz_device;
typedef struct fz_irect_s fz_irect;
typedef struct fz_locks_context_s fz_locks_context ;
typedef struct fz_matrix_s fz_matrix;
typedef struct fz_page_s fz_page;
typedef struct fz_pixmap_s fz_pixmap;
typedef struct fz_rect_s fz_rect;
typedef struct fz_scale_cache_s fz_scale_cache;
typedef struct fz_stream_s fz_stream;
typedef struct fz_text_page_s fz_text_page;
typedef struct fz_text_sheet_s fz_text_sheet;
typedef struct fz_document_s fz_document;

/* Structures Details */

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

struct fz_irect_s
{
  int x0, y0;
  int x1, y1;
};

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

struct fz_matrix_s
{
  float a, b, c, d, e, f;
};

struct fz_rect_s
{
  float x0, y0;
  float x1, y1;
};

struct fz_text_page_s
{
  fz_rect mediabox;
  int len, cap;
  // fz_page_block *blocks;
  fz_text_page *next;
};

/* Functions */

fz_colorspace *fz_device_rgb (fz_context * ctx);
fz_device *fz_new_draw_device (fz_context * ctx, fz_pixmap * dest);
fz_device *fz_new_draw_device_type3 (fz_context * ctx, fz_pixmap * dest);
fz_device *fz_new_draw_device_with_bbox (fz_context * ctx, fz_pixmap * dest, const fz_irect * clip);
fz_device *fz_new_text_device (fz_context * ctx, fz_text_sheet * sheet, fz_text_page * page);
fz_document *fz_open_document (fz_context * ctx, const char *filename);
fz_document *fz_open_document_with_stream (fz_context * ctx, const char *magic, fz_stream * stream);
fz_irect *fz_round_rect (fz_irect * bbox, const fz_rect * rect);
fz_matrix *fz_concat (fz_matrix * result, const fz_matrix * left, const fz_matrix * right);
fz_matrix *fz_pre_scale (fz_matrix * m, float sx, float sy);
fz_matrix *fz_rotate (fz_matrix * m, float degrees);
fz_matrix *fz_scale (fz_matrix * m, float sx, float sy);
fz_pixmap *fz_new_pixmap_with_bbox (fz_context * ctx, fz_colorspace * colorspace, const fz_irect * bbox);
fz_pixmap *fz_new_pixmap_with_bbox_and_data (fz_context * ctx, fz_colorspace * colorspace, const fz_irect * rect, unsigned char *samples);
fz_pixmap *fz_scale_pixmap (fz_context * ctx, fz_pixmap * src, float x, float y, float w, float h, fz_irect * clip);
fz_pixmap *fz_scale_pixmap_cached (fz_context * ctx, fz_pixmap * src, float x, float y, float w, float h, const fz_irect * clip, fz_scale_cache * cache_x, fz_scale_cache * cache_y);
fz_rect *fz_bound_page (fz_document * doc, fz_page * page, fz_rect * rect);
fz_rect *fz_transform_rect (fz_rect * rect, const fz_matrix * transform);
fz_scale_cache *fz_new_scale_cache (fz_context * ctx);
fz_text_page *fz_new_text_page (fz_context * ctx);
fz_text_sheet *fz_new_text_sheet (fz_context * ctx);
int fz_count_pages (fz_document * doc);
void fz_clear_pixmap_with_value (fz_context * ctx, fz_pixmap * pix, int value);
void fz_close_document (fz_document * doc);
void fz_concat_push (fz_stream * concat, fz_stream * chain);
void fz_drop_buffer (fz_context * ctx, fz_buffer * buf);
void fz_drop_pixmap (fz_context * ctx, fz_pixmap * pix);
void fz_free_context (fz_context * ctx);
void fz_free_device (fz_device * dev);
void fz_free_page (fz_document * doc, fz_page * page);
void fz_free_scale_cache (fz_context * ctx, fz_scale_cache * cache);
void fz_free_text_page (fz_context * ctx, fz_text_page * page);
void fz_free_text_sheet (fz_context * ctx, fz_text_sheet * sheet);
void fz_new_context (fz_alloc_context * alloc, fz_locks_context * locks, unsigned int max_store);
void fz_pixmap_set_resolution (fz_pixmap * pix, int res);
void fz_run_page (fz_document * doc, fz_page * page, fz_device * dev, const fz_matrix * transform, fz_cookie * cookie);
void fz_run_page_contents (fz_document * doc, fz_page * page, fz_device * dev, const fz_matrix * transform, fz_cookie * cookie);
void fz_set_aa_level (fz_context * ctx, int bits);
void fz_write_png (fz_context * ctx, fz_pixmap * pixmap, char *filename, int savealpha);

/***************************************************************************************************
 * 
 * End
 * 
 **************************************************************************************************/
