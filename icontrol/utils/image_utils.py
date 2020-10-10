from django.utils.html import format_html


class ImagePreview:
    def get_image_thumb_preview(self, obj):
        return format_html(
            "<img src='/media/{}'  width='100px' height='100px' />".format(obj.image)) if obj.image else '-'

    get_image_thumb_preview.allow_tags = True
    get_image_thumb_preview.__name__ = 'Imágen'

    def get_image_preview(self, obj):
        return format_html(
            "<img src='/media/{}'  width='200px' height='200px' />".format(obj.image)) if obj.image else '-'

    get_image_preview.allow_tags = True
    get_image_preview.__name__ = 'Previsualización'
