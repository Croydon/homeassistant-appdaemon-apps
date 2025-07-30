
from phonebook_app.parsing import vcard_to_xml
from aiohttp import web

def contacts(instance, username, password, addressbook) -> web.Response:
    return vcard_to_xml(instance, username, password, addressbook) 
