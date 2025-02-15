import json

# Step 1: Read the contacts from contacts.json
def contactsort():
    with open('data/contacts.json', 'r') as file:
        contacts = json.load(file)

    # Step 2: Sort the contacts by last_name, then first_name
    sorted_contacts = sorted(contacts, key=lambda contact: (contact['last_name'], contact['first_name']))

    # Step 3: Write the sorted contacts to contacts-sorted.json
    with open('data/contacts-sorted.json', 'w') as file:
        json.dump(sorted_contacts, file, indent=4)

print("Contacts sorted and written to contacts-sorted.json")