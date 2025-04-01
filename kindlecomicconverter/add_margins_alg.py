from PIL import ImageOps
import math


def addMargins(img, left, top, right, bottom, fill):
    horizontal_margin = left + right
    vertical_margin = top + bottom
    aspect_ratio = img.size[0] / img.size[1]
    natural_horizontal_margin = int((aspect_ratio) * vertical_margin)
    natural_vertical_margin = int((1/aspect_ratio) * horizontal_margin)
    
    primary_axis = 'vertical' if (horizontal_margin - natural_horizontal_margin < vertical_margin - natural_vertical_margin) else 'horizontal'

    if primary_axis == 'vertical':
        ssize = (int((img.size[1] - vertical_margin) * aspect_ratio), img.size[1] - (vertical_margin))
    else:
        ssize =  (img.size[0] - horizontal_margin, int((img.size[0] - horizontal_margin) * (1/aspect_ratio)))

    print('ssize', ssize)
    result = ImageOps.contain(img, ssize)
    
    if primary_axis == 'vertical':
        if horizontal_margin != 0:
            diff_ratio = natural_horizontal_margin / horizontal_margin
            adjusted_left = math.ceil(left * diff_ratio)
        else:
            adjusted_left = math.ceil(natural_horizontal_margin / 2)
        adjusted_right = img.size[0] - result.size[0] - adjusted_left
        adjusted_bottom = img.size[1] - result.size[1] - top # for floating-point inaccuracies

        result = ImageOps.expand(result, (adjusted_left, top, adjusted_right, adjusted_bottom), fill=fill)
    else:
        if vertical_margin != 0:
            diff_ratio = natural_vertical_margin / vertical_margin
            adjusted_top = math.ceil(top * diff_ratio)
        else:
            adjusted_top = math.ceil(natural_vertical_margin / 2)
        adjusted_bottom = img.size[1] - result.size[1] - adjusted_top
        adjusted_right = img.size[0] - result.size[0] - left # for floating-point inaccuracies
        result = ImageOps.expand(result, (left, adjusted_top, adjusted_right, adjusted_bottom), fill=fill)

    assert result.size == img.size
    return result