import requests
from requests.auth import HTTPBasicAuth
from phonebook_app.models import *
from phonebook_app.xml_generation import build_xml
from aiohttp import web
import re


def fetch_vcard(instance, username, password, address_book):
    url = f"https://{instance.rstrip('/')}/remote.php/dav/addressbooks/users/{username}/{address_book}?export"
    request = requests.get(url, auth=HTTPBasicAuth(username, password))
    return request.content.decode(), request.status_code


def isolate_cards(vcard: str):
    vcard = vcard.replace("\r\n", "\n").replace("\r\n", "\n")
    vcard = vcard.removeprefix("BEGIN:VCARD\n")
    vcard = vcard.removesuffix("END:VCARD\n")
    cards = vcard.split("\nEND:VCARD\nBEGIN:VCARD\n")
    return cards


def parse_cards(cards: list[str]):
    contacts = []
    for card in cards:
        name = re.search(r"(?<=FN:)(.*?)(?=\n)", card)
        name = name.group(0) if name else None

        # original: phone_match = re.findall(r"(?<=TEL;TYPE=)\"?([a-z,]+)\"?:(.*?)(?=\n)", card, re.IGNORECASE)
        phone_match = re.findall(r"TEL;TYPE=([^\n:]+):([^\n]+)", card, re.IGNORECASE)
        phones = []
        for phone in phone_match:
            if phone[1]:
                types = [t for t in re.split(r"[;,]", phone[0]) if not t.upper().startswith("PREF=")]
                phones.append(Phone(types, phone[1]))

        print(name, phones)
        if phones:
            contacts.append(Contact(name, phones))
    return contacts


def vcard_to_xml(instance, username, password, address_book) -> web.Response:
    doc, status_code = fetch_vcard(instance, username, password, address_book)

    if status_code != 200:
        error_message = "The address book could not be called. Please check if the parameters are correct."
        print(error_message)
        return web.Response(
            text=error_message,
            content_type="text/plain",
            status=status_code
        )

    cards = isolate_cards(doc)
    contacts = parse_cards(cards)

    tree = build_xml(contacts)

    xml_byte_string = ET.tostring(tree.getroot(), encoding="utf-8", xml_declaration=True)

    return web.Response(
        text=xml_byte_string.decode("utf-8"),
        content_type="application/xml",
        status=200
    )
