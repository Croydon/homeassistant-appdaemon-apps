# HomeAssistant AppDaemon Apps

IMPORTANT: This assumes, that you do NOT expose your Home Assistant instance to the web. This might be dangerous.



## Nextcloud Grandstream Contacts

Synchronise Grandstream VOIP phonebooks with Nextcloud Contacts, via an [XML file](https://www.grandstream.com/hubfs/Product_Documentation/GXP_XML_phonebook_guide.pdf).

This will create a HTTP endpoint that Grandstream phones can access to receive an up-to-date copy of your Nextcloud contacts.


## Requirements

- Python 3.10 or higher (due to type annotations)
- An account on a Nextcloud instance that has the [Contacts app](https://apps.nextcloud.com/apps/contacts) installed


## Setup

1. Add `requests` to the list of installed packages in your AppDaemon settings
2. Copy all files into your `addon_configs/<appdaemon folder>/apps` directory
3. Add to your `apps.yaml` file:
```
nextcloud_contacts_to_phonebook_xml:
  module: phonebook
  class: Phonebook
```

The URL structure to access the generated Phonebook XML is like that:

> http://homeassistant.local/app/phonebook.xml?instance=cloud.example.com&username=NextcloudUser&addressbook=myadresssbook&password=my-generated-nextcloud-app-password


## License

GNU GPL 3
