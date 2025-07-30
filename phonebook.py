import appdaemon.plugins.hass.hassapi as hass
from phonebook_app.main import contacts

class Phonebook(hass.Hass):
    def initialize(self):
        self.register_route(self.contacts_endpoint, "phonebook.xml")

    async def contacts_endpoint(self, request, *args, **kwargs):
        instance = request.query.get("instance")
        username = request.query.get("username")
        password = request.query.get("password")
        address_book = request.query.get("addressbook")

        return contacts(instance, username, password, address_book)
