import markdown
from lxml import etree

body_markdown = "This is an [inline link](http://google.com). This is a [non inline link][1]\r\n\r\n  [1]: http://yahoo.com"
body_markdown = "body -- [LINE_P201966_104747](https://user-images.githubusercontent.com/19705462/59020178-aa392880-8873-11e9-8b8a-8989cd4bdad3.jpg) By New"
body_markdown = "![repository-open-graph-template](https://user-images.githubusercontent.com/860704/63464035-9a031380-c488-11e9-9fcd-9c01f60ad054.png)\r\n\r\n![repository-open-graph-template](https://user-images.githubusercontent.com/860704/63464042-9e2f3100-c488-11e9-852e-4f39c0368316.png)\r\n\r\n"

body_markdown = body_markdown.replace("![", "[").strip()

m = markdown.markdown(body_markdown)
m = f"<html>{m}</html>"


doc = etree.fromstring(m)
for link in doc.xpath('//a'):
    print(link.text, link.get('href'))
