
from phonebook_app.parsing import vcard_to_xml
from aiohttp import web
import xml.etree.ElementTree as ET

def contacts(username, password, addressbook):
    tree = vcard_to_xml(username, password, addressbook)
    xml_byte_string = ET.tostring(tree.getroot(), encoding="utf-8", xml_declaration=True)

    return web.Response(
        text=xml_byte_string.decode("utf-8"),
        content_type="application/xml",
        status=200
    )
