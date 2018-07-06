"""Mapping for command invoke name to logic"""
from .commands import create_contact,search_by_email,create_company,make_deal,create_contact_note,create_deal_note,list_deals


commands_by_invoke_name = {
    "create_contact": create_contact,
    "create_company":create_company,
    "search_by_email":search_by_email,
    "make_deal":make_deal,
    "create_note":create_contact_note,
    "create_deal_note":create_deal_note,
    "list_deals":list_deals
}