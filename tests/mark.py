import markdown
from lxml import etree

body_markdown = "This is an [inline link](http://google.com). This is a [non inline link][1]\r\n\r\n  [1]: http://yahoo.com"
body_markdown = "body -- [LINE_P201966_104747](https://user-images.githubusercontent.com/19705462/59020178-aa392880-8873-11e9-8b8a-8989cd4bdad3.jpg) By New"

doc = etree.fromstring(markdown.markdown(body_markdown))
for link in doc.xpath('//a'):
    print(link.text, link.get('href'))
