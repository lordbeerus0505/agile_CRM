"""Code which actually takes care of application API calls or other business logic"""


from yellowant.messageformat import MessageClass , MessageAttachmentsClass, AttachmentFieldsClass
from ..yellowant_message_builder.messages import items_message, item_message
import requests
import json
from ..yellowant_command_center.unix_epoch_time import convert_to_epoch
from urllib.parse import urljoin
from ..yellowant_command_center import command_center
from ..yellowant_api.models import Agile_Credentials,UserIntegration
from ..yellowant_api import views



#agc=Agile_Credentials()
#ui=UserIntegration.objects.get()

#
# APIKEY = "br2gfaog120d0u1tuti1ouk76u"   # Your API KEY
# EMAIL = "ankur@yellowant.com"  # Your API EMAIL
# DOMAIN = "yellowant"  # Your DOMAIN

#API reqests made to https://{domain}.agilecrm.com/dev/ domain=yellowant
# URL='https://{}.agilecrm.com/dev/api'.format(DOMAIN)
# print(URL)
#
# BASE_URL = "https://" + DOMAIN + ".agilecrm.com/dev/api/"

contenttype='application/json'



#-----------------------------------------------------------CREATE CONTACT--------------------------------------------

def create_contact(args,user_integration):
    print(str(user_integration.id)+"userid")
    agc=Agile_Credentials.objects.get(user_integration_id=user_integration.id)
    APIKEY=agc.AGILE_API_KEY
    EMAIL=agc.AGILE_EMAIL_ID
    DOMAIN=agc.AGILE_DOMAIN_NAME
    BASE_URL = "https://" + DOMAIN + ".agilecrm.com/dev/api/"

    company_name=""
    email=""
    address=""
    phone=""
    full_name=args['Full-Name']
    print ("here")
    if args.get('Company-Name',None) is not None:
        company_name = args['Company-Name']
    if args.get('Email',None) is not None:
        email=args['Email']
    if args.get('Address',None) is not None:
        address=args['Address']
    if args.get('Phone-No',None) is not None:
        phone=args['Phone-No']
    name=full_name.split(" ")
    first_name = name[0]
    last_name = name[1]
    print (first_name)
    print (last_name)

    url = BASE_URL + "contacts"
    method="POST"
    headers = {
        'Accept': 'application/json',
        'content-type': contenttype,
    }
    starvalue="5"

    #open json file
    contact_data = {
        "star_value": starvalue,
        "lead_score": "92",
        "tags": [
            "Lead",
            "Likely Buyer"
        ],
        "properties": [
            {
                "type": "SYSTEM",
                "name": "first_name",
                "value": first_name
            },
            {
                "type": "SYSTEM",
                "name": "last_name",
                "value": last_name
            },
            {
                "type": "SYSTEM",
                "name": "company",
                "value": company_name
            },
            {
                "type": "SYSTEM",
                "name": "title",
                "value": "Mr/Ms."
            },
            {
                "type": "SYSTEM",
                "name": "email",
                "subtype": "work",
                "value": email
            },
            {
                "type": "SYSTEM",
                "name": "address",
                "value": address
            },

            {
                "type": "SYSTEM",
                "name": "phone",
                "value": phone
            }
        ]
    }

    print("data recieved\n\n")
    if (method == "POST"):
        response = requests.post(
            url,
            data=json.dumps(contact_data),
            headers=headers,
            auth=(EMAIL, APIKEY)
        )
        print("Full Name:"+full_name+"\nEmailID:"+email +"\nPhone No:"+phone)
        m = MessageClass()
        m.message_text = "Full Name:"+full_name+"\nEmailID:"+email +"\nPhone No:"+phone
        return m



    return "Wrong method provided"


#def create_contact(first_name,last_name,title,company_name,email,phone,tags):
#print(create_contact("Abhiram","N","Programmer","YellowAnt","abhiram.natarajan@gmail.com","address","9886051850"))


#---------------------------------------------------------UPDATE CONTACT------------------------------------------------

# #assuming youre not updating any information to NULL
# def update_contact(id,first_name,last_name,title,company_name,email,address,phone):
#     url=BASE_URL+"contacts/edit-properties"
#     method="PUT"
#     update_contact_data = {
#         "id": id,
#         "properties": [
#             {
#                 "type": "SYSTEM",
#                 "name": "last_name",
#                 "value": "Chan"
#             },
#             {
#                 "type": "CUSTOM",
#                 "name": "My Custom Field",
#                 "value": "Custom value chane"
#             }
#         ]
#     }


#-----------------------------------------------GET CONTACT BY EMAIL----------------------------------------------------

def search_by_email(args,user_integration):
    agc = Agile_Credentials.objects.get(user_integration_id=user_integration.id)
    APIKEY = agc.AGILE_API_KEY
    EMAIL = agc.AGILE_EMAIL_ID
    DOMAIN = agc.AGILE_DOMAIN_NAME
    BASE_URL = "https://" + DOMAIN + ".agilecrm.com/dev/api/"
    email=args['EmailID']
    url = BASE_URL + "contacts/search/email/" + email
    headers = {
        'Accept': 'application/json',
        'content-type': contenttype,
    }



    response = requests.get(url,headers=headers,auth=(EMAIL, APIKEY))
    m = MessageClass()
    m.message_text = str(response.text)
    #print (str(response.text) + "test")
    a=json.loads(response.text)

    print("\n\nFULL NAME:" + a['properties'][0]['value'] +" "+ a['properties'][1]['value']+"\nEMAIL:"+a['properties'][4]['value']+"\nPHONE:"+a['properties'][5]['value'])
    m.message_text="\n\nFULL NAME:" + a['properties'][0]['value'] +" "+ a['properties'][1]['value']+"\nEMAIL:"+a['properties'][4]['value']+"\nPHONE:"+a['properties'][5]['value']
    return m



#print(search_by_email("abhiram.natarajan@gmail.com"))

#----------------------------------------------------CREATE COMPANY----------------------------------------------------

def create_company(args,user_integration):
    agc = Agile_Credentials.objects.get(user_integration_id=user_integration.id)
    APIKEY = agc.AGILE_API_KEY
    EMAIL = agc.AGILE_EMAIL_ID
    DOMAIN = agc.AGILE_DOMAIN_NAME
    BASE_URL = "https://" + DOMAIN + ".agilecrm.com/dev/api/"


    company_type="MNC"
    company_url=""
    company_phone=""
    company_email=""
    company_address=""
    company_name=args['Company-Name']

    print("here")
    if args.get('Company-URL', None) is not None:
        company_url = args['Company-URL']
    if args.get('Company-Email', None) is not None:
        company_email = args['Company-Email']
    if args.get('Company-Address', None) is not None:
        company_address = args['Company-Address']
    if args.get('Company-Phone', None) is not None:
        company_phone = args['Company-Phone']

    url = BASE_URL + "contacts"
    method = "POST"
    headers = {
        'Accept': 'application/json',
        'content-type': contenttype,
    }

    company_data = {
        "type": "COMPANY",
        "star_value": 4,
        "lead_score": 120,
        "tags": [

        ],
        "properties": [
            {
                "name": "Company Type",
                "type": "CUSTOM",
                "value": company_type
            },
            {
                "type": "SYSTEM",
                "name": "name",
                "value": company_name
            },
            {
                "type": "SYSTEM",
                "name": "url",
                "value": company_url
            },
            {
                "name": "email",
                "value": company_email,
                "subtype": ""
            },
            {
                "name": "phone",
                "value": company_phone,
                "subtype": ""
            },
            {
                "name": "website",
                "value": "",
                "subtype": "LINKEDIN"
            },
            {
                "name": "address",
                "value": company_address,
                "subtype": "office"
            }
        ]
    }

    if (method == "POST"):
        response = requests.post(
            url,
            data=json.dumps(company_data),
            headers=headers,
            auth=(EMAIL, APIKEY)
        )
        print("Company Name:" + company_name + "\nCompany Phone No:" + company_phone)
        m = MessageClass()
        m.message_text = "Company Name:" + company_name + "\nCompany Phone No:" + company_phone
        return m
    return "Invalid inputs"

#create_company(company_name,company_type,company_url,company_email,company_phone,company_address):

#print(create_company("MSR","MNC","msr.com","support@msr.com","9346191429284","gbsgjsdbgsbgkje adddressss"))

#------------------------------------------------------MAKE DEAL--------------------------------------------------

def make_deal(args,user_integration):
    agc = Agile_Credentials.objects.get(user_integration_id=user_integration.id)
    APIKEY = agc.AGILE_API_KEY
    EMAIL = agc.AGILE_EMAIL_ID
    DOMAIN = agc.AGILE_DOMAIN_NAME
    BASE_URL = "https://" + DOMAIN + ".agilecrm.com/dev/api/"


    deal_name=args['Deal-Name']
    print("Here inside make_deal")
    deal_value=args['Deal-Value']
    deal_probability=args['Deal-Probability']
    deal_close_date=""
    deal_milestone=args['Deal-Milestone']

    headers = {
        'Accept': 'application/json',
        'content-type': contenttype,
    }
    method="POST"

    url = BASE_URL + "opportunity"
    if args.get('Deal-Close-Date', None) is not None:
        deal_close_date = args['Deal-Close-Date']
        deal_close_date=convert_to_epoch(deal_close_date)
        print(deal_close_date)



    deal_data = {
        "name": deal_name,
        "expected_value": deal_value,
        "probability": deal_probability,
        "close_date": deal_close_date,
        "milestone": deal_milestone,
        "contact_ids": [
            "5661679325020160"
        ],
        "custom_data": [
            {
                "name": "Group Size",
                "value": "10"
            }
        ]
    }

    if (method == "POST"):
        response = requests.post(
            url,
            data=json.dumps(deal_data),
            headers=headers,
            auth=(EMAIL, APIKEY)
        )
        print("Deal Name:" + deal_name + "\nProbability:" + deal_probability)
        m = MessageClass()
        m.message_text = "Deal Name:" + deal_name + "\nProbability:" + deal_probability
        return m
    return "Invalid inputs"

#-------------------------------------------------------CREATE CONTACT NOTE-------------------------------------------------


def create_contact_note(args,user_integration):
    agc = Agile_Credentials.objects.get(user_integration_id=user_integration.id)
    APIKEY = agc.AGILE_API_KEY
    EMAIL = agc.AGILE_EMAIL_ID
    DOMAIN = agc.AGILE_DOMAIN_NAME
    BASE_URL = "https://" + DOMAIN + ".agilecrm.com/dev/api/"


    subject=args['Subject']
    description=""
    if args.get('Description', None) is not None:
        description=args['Description']
    email=args['EmailID']

    #making call to search by email and generate the ID
    url = BASE_URL + "contacts/search/email/" + email
    headers = {
        'Accept': 'application/json',
        'content-type': contenttype,
    }

    response = requests.get(url, headers=headers, auth=(EMAIL, APIKEY))
    m = MessageClass()
    m.message_text = str(response.text)
    # print (str(response.text) + "test")
    a = json.loads(response.text)

    id=a['id']
    print(str(id)+"is the converted ID")


    note_data = {
        "subject": subject,
        "description": description,
        "contact_ids": [
            str(id)
        ]
    }
    url=BASE_URL+'notes'
    print(url)

    response = requests.post(
        url,
        data=json.dumps(note_data),
        headers=headers,
        auth=(EMAIL, APIKEY)
    )
    print("Subject:"+subject+"\nDescription: "+description+"\nID: "+str(id))
    m = MessageClass()
    m.message_text = "Subject:"+subject+"\nDescription:"+description+"\nID:"+str(id)
    return m


#-------------------------------------------------------MAKE DEAL NOTE--------------------------------------------------------


def create_deal_note(args,user_integration):
    agc = Agile_Credentials.objects.get(user_integration_id=user_integration.id)
    APIKEY = agc.AGILE_API_KEY
    EMAIL = agc.AGILE_EMAIL_ID
    DOMAIN = agc.AGILE_DOMAIN_NAME
    BASE_URL = "https://" + DOMAIN + ".agilecrm.com/dev/api/"


    subject=args['Subject']
    description=""
    headers = {
        'Accept': 'application/json',
        'content-type': contenttype,
    }


    if args.get('Description', None) is not None:
        description = args['Description']
    #Get ID value using email ID

    id = args['Deal-ID']
    print(str(id) + "is the converted ID")


    note_deal_data = {
        "subject": subject,
        "description": description,
        "deal_ids": [
            str(id)
        ]
    }


    url = BASE_URL + 'opportunity/deals/notes'
    print(url)

    response = requests.post(
        url,
        data=json.dumps(note_deal_data),
        headers=headers,
        auth=(EMAIL, APIKEY)
    )
    print("Subject:" + subject + "\nDescription: " + description + "\nID: " + str(id))
    m = MessageClass()
    m.message_text = "Subject:" + subject + "\nDescription:" + description + "\nID:" + str(id)
    return m


#---------------------------------------------------------LIST ALL DEALS-------------------------------------------------------------

def list_deals(args,user_integration):
    agc = Agile_Credentials.objects.get(user_integration_id=user_integration.id)
    APIKEY = agc.AGILE_API_KEY
    EMAIL = agc.AGILE_EMAIL_ID
    DOMAIN = agc.AGILE_DOMAIN_NAME
    BASE_URL = "https://" + DOMAIN + ".agilecrm.com/dev/api/"

    headers={
        'Accept':'application/json',
    }
    response = requests.get('https://'+DOMAIN+
                            '.agilecrm.com/dev/api/opportunity',headers=headers, auth=(EMAIL, APIKEY))


    a = json.loads(response.text)
    print(type(a))

    s=''
    #8 occurances of id in the json file
    count=0
    m=MessageClass()
    data = {'list': []}
    print("\n\n\n\n")
    name=''
    val=''
    attachment = MessageAttachmentsClass()
    for c in a:
        field = AttachmentFieldsClass()
        for k,v in c.items():

            if k=="name":
                field.title=str(v)
                name=str(v)

            if k=="id":
                field.value=str(v)
                val=str(v)
                print(val)
        data['list'].append({"Name":name, "ID": val})
        print(name)
        attachment.attach_field(field)
    m.attach(attachment)

        # if 'colorName' in c:
        #     count=count+1
    #print("number of deals="+str(count))
    #x=''
    m.data=data





    # data = {'list': []}
    # m=MessageClass()
    # for i in range(count):
    #     print(str(a[i]['id'])+" "+str(a[i]['name']))
    #     #x=x+"Name: "+str(a[i]['name'])+"\n ID: "+str(a[i]['id'])+"\n\n"
    #     attachment = MessageAttachmentsClass()
    #     field = AttachmentFieldsClass()
    #     field.title ="Name: "+str(a[i]['name'])
    #     field.value="ID: "+str(a[i]['id'])
    #     attachment.attach_field(field)
    #     m.attach(attachment)
    #     data['list'].append({"Name": str(a[i]['name']), "ID": str(a[i]['id'])})
    #
    #
    #
    #
    #
    #
    #
    # m.data=data
    #print(a[0]['id'])
   # m=MessageClass()
    m.message_text="Testing..."
    return m


