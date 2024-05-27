from .models import Contact
from django.db import transaction

class ContactService:

    @staticmethod
    @transaction.atomic
    def create_contact(validated_data: dict):
        email = validated_data.get('email')
        phone = validated_data.get('phoneNumber')

        primary_contact = None
        contact_by_email = None
        contact_by_phone = None
        if email:
            contact_by_email = Contact.objects.filter(email = email).first()
            if contact_by_email and not phone:
                return ContactService.get_primary_contact(contact_by_email)
        if phone:
            contact_by_phone = Contact.objects.filter(phoneNumber = phone).first()
            if contact_by_phone and not email:
                return ContactService.get_primary_contact(contact_by_phone)

        if not contact_by_email and not contact_by_phone:
            primary_contact = Contact.objects.create(email = email, phoneNumber = phone)
        elif not contact_by_phone:
            primary_contact_by_email = ContactService.get_primary_contact(contact_by_email)
            Contact.objects.create(email = email, phoneNumber = phone, linkedId = primary_contact_by_email.id, linkPrecedence = Contact.SECONDARY)
            primary_contact = primary_contact_by_email
        elif not contact_by_email:
            primary_contact_by_phone = ContactService.get_primary_contact(contact_by_phone)
            Contact.objects.create(email = email, phoneNumber = phone, linkedId = primary_contact_by_phone.id, linkPrecedence = Contact.SECONDARY)
            primary_contact = primary_contact_by_phone
        else:
            primary_contact_by_email = ContactService.get_primary_contact(contact_by_email)
            primary_contact_by_phone = ContactService.get_primary_contact(contact_by_phone)
            if primary_contact_by_phone != primary_contact_by_email:
                if primary_contact_by_phone.createdAt < primary_contact_by_email.createdAt:
                    primary_contact = ContactService.update_primary_to_secondary(primary_contact_by_phone, primary_contact_by_email)
                elif primary_contact_by_phone.createdAt > primary_contact_by_email.createdAt:
                    primary_contact = ContactService.update_primary_to_secondary(primary_contact_by_email, primary_contact_by_phone)
            else:
                primary_contact = primary_contact_by_email
        return primary_contact
        
    @staticmethod
    def get_primary_contact(curr_contact: Contact):
        if curr_contact.linkPrecedence != Contact.PRIMARY:
            primary_contact = Contact.objects.get(id = curr_contact.linkedId)
        else:
            primary_contact = curr_contact
        return primary_contact
    
    @staticmethod
    def update_primary_to_secondary(primary_contact: Contact, secondary_contact: Contact):
        secondary_contact.linkPrecedence = Contact.SECONDARY
        secondary_contact.linkedId = primary_contact.id
        secondary_contact.save()
        contacts = Contact.objects.filter(linkedId = secondary_contact.id)
        for contact in contacts:
            contact.linkedId = primary_contact.id
            contact.save()
        return primary_contact
    
    @staticmethod
    def get_all_connected_contacts(primary_contact: Contact):
        secondary_contacts = Contact.objects.filter(linkedId = primary_contact.id)
        emails = set()
        if primary_contact.email:
            emails.add(primary_contact.email)
        phones = set()
        if primary_contact.phoneNumber:
            phones.add(primary_contact.phoneNumber)
        secondary_contact_ids = []
        for contact in secondary_contacts:
            if contact.email:
                emails.add(contact.email)
            if contact.phoneNumber:
                phones.add(contact.phoneNumber)
            secondary_contact_ids.append(contact.id)
        output = 	{
		"contact":{
			"primaryContatctId": primary_contact.id,
			"emails": list(emails), 
			"phoneNumbers": list(phones),
			"secondaryContactIds":secondary_contact_ids
		    }
	    }
        return output