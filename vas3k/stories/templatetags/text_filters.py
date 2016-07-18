import re
from django import template

register = template.Library()


@register.filter(is_safe=True)
def escape(text):
    if text is not None:
        return text.replace(r'"', r'\"').replace(r"'", r"\'")
    else:
        return ""


@register.filter(is_safe=True)
def nl2br(text):
    if not text:
        return ""
    text = text.replace("\n\n", "</p><p>")
    text = text.replace("\r\n\r\n", "</p><p>")
    # text = text.replace("\n", "<br />")
    return text


@register.filter(is_safe=True)
def nl2br2(text):
    if not text:
        return ""
    text = text.replace("\n", "<br />")
    return text


@register.filter(is_safe=True)
def htmlspecialchars(text):
    if text is not None:
        return text.replace(r"<", r"&lt;").replace(r">", r"&gt;")
    else:
        return ""


@register.filter(is_safe=True)
def quoting(text):
    text = text.replace(r"<", r"&lt;").replace(r">", r"&gt;")

    newtext = u""
    for line in text.split("\n"):
        if line.strip().startswith("&gt;"):
            newtext += '<span class="comment__quote">%s</span><br />' % line
        else:
            newtext += "%s<br />" % line
    text = newtext
    text = re.sub(r"&lt;[B|b]&gt;(.*?)&lt;/[B|b]&gt;", r"<strong>\1</strong>", text)
    text = re.sub(r"&lt;[I|i]&gt;(.*?)&lt;/[I|i]&gt;", r"<i>\1</i>", text)
    text = re.sub(r"&lt;[S|s]&gt;(.*?)&lt;/[S|s]&gt;", r"<strike>\1</strike>", text)
    text = re.sub(r"&lt;[U|u]&gt;(.*?)&lt;/[U|u]&gt;", r"<u>\1</u>", text)
    text = re.sub(r"&lt;pre&gt;(.*?)&lt;/pre&gt;", r"<pre>\1</pre>", text)
    text = re.sub(r"&lt;code&gt;(.*?)&lt;/code&gt;", r"<code>\1</code>", text)
    text = re.sub(r"&lt;[hr|HR].*?/&gt;", r"<hr />", text)
    text = re.sub(u'(\(?https?://[-A-Za-zА-Яа-я0-9+&@#/%?=~_()|!:,.;]*[-A-Za-zА-Яа-я0-9+&@#/%=~_()|])(\">|</a>)?',
                  r'<a href="\1">\1</a>', text)
    text = re.sub(r'&lt;[a|A] href=["|\']<a href="(.*?)">.*?</a>["|\']&gt;(.*?)&lt;/[A|a]&gt;', r'<a href="\1">\2</a>',
                  text)
    # text = nl2br2(text)
    return text


@register.filter
def rupluralize(value, arg="дурак,дурака,дураков"):
    args = arg.split(",")
    number = abs(int(value))
    a = number % 10
    b = number % 100

    if (a == 1) and (b != 11):
        return args[0]
    elif (a >= 2) and (a <= 4) and ((b < 10) or (b >= 20)):
        return args[1]
    else:
        return args[2]


@register.filter
def flip_coordinates(value):
    a, b = value.split(",", 1)
    return "%s,%s" % (b, a)


@register.filter
def resized_image(value, arg="full"):
    if not value or not arg or not value.startswith("http://i.vas3k.ru/"):
        return value
    if value.startswith("http://i.vas3k.ru/full/"):
        return value.replace("http://i.vas3k.ru/full/", "http://i.vas3k.ru/{}/".format(arg))
    else:
        return value.replace("http://i.vas3k.ru/", "http://i.vas3k.ru/{}/".format(arg))
