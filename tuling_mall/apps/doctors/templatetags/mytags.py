from html import unescape

from django import template

register = template.Library()
@register.simple_tag
def show_article(value, n):
    # 解码 HTML 实体编码
    decoded_value = unescape(value)
    # 如果解码后的字符串长度大于指定长度，则只显示指定长度的内容并添加省略号
    if len(decoded_value) > n:
        return f'{decoded_value[:n]}...'
    else:
        return decoded_value