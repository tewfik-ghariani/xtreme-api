import os
import json
import html
import base64
from pathlib import Path 
import xml.etree.ElementTree as ET

import requests as req

from xtremeAPI.lib import loadConfig
from xtremeAPI.lib import authenticate
from xtremeAPI.lib import utils
from xtremeAPI.lib.exceptions import XtremeCreateException


API_VERSION           = "2.1"
CASE_AUDIENCES       = ["Public", "Infor Only", "Infor & Staff Partner"]



class XtremeAgent:
    def __init__(self):
        self.params      = loadConfig.get_params()
        self.url         = loadConfig.get_urls()["create"]
        self.logger      = utils.logging_config('log_xtreme_create.log', 'xtremeCreateLogger')
        self.id          = None
        self.link        = None
        self.status      = None
        self.priority    = None
        self.logger.info("------- New Xtreme Ticket ")
        self.logger.info("Environment : " + self.params["xtreme_env"])




    def create_incident(self, jira_subcomponent,
                              summary,
                              description,
                              priority=4,
                              status="Researching",
                              audience="Public"):
        ''' Prepare payload and create the incident

        :param jira_subcomponent: Customer & application using the same syntax as Jira Subcomponent e.g MFP
        :param priority : select the severity of the incident. Default : 4 - Standard
        :param summary: The title of the incident
        :param description: The event note to be written to the incident.
        :param status: Select the status of the incident. Default 'Researching'
        :param audience: Value of CaseAudience. 
            Should be ; "Public", "Infor Only" or "Infor & Staff Partner". Default : 'Public'
        '''

        b64_username         = loadConfig.get_b64_credentials()["username"]
        username             = self.params["username"].decode()
        customer_infos       = utils.fetch_infos(self.logger, jira_subcomponent)
        severity             = str(utils.set_severity(priority))
        self.priority        = priority
        self.status          = status
        self.logger.info("Severity : " + str(self.priority))

        # Structure of the xml file
        incident              = ET.Element('Incident')
        staff_email           = ET.SubElement(incident, 'StaffEmail')
        contact_email         = ET.SubElement(incident, 'ContactEmail')
        alternate_emails      = ET.SubElement(incident, 'AlternateEmail')
        customer              = ET.SubElement(incident, 'Customer')
        product               = ET.SubElement(incident, 'Product')
        incident_summary      = ET.SubElement(incident, 'Summary')
        incident_description  = ET.SubElement(incident, 'Description')
        incident_severity     = ET.SubElement(incident, 'Severity')
        incident_status       = ET.SubElement(incident, 'Status')
        case_audience         = ET.SubElement(incident, 'CaseAudience')
        incident_owner        = ET.SubElement(incident, 'IncidentOwner')
        api_version           = ET.SubElement(incident, 'APIVersion')


        # Value of each sub element
        api_version.text           = API_VERSION
        staff_email.text           = b64_username
        # To Be used when testing against PreProd ( update the contact based on the customerID )
        #contact_email.text         = base64.b64encode("1317135@nothing.local".encode('ascii')).decode()
        contact_email.text         = base64.b64encode(customer_infos["contact_email"].encode('ascii')).decode()
        alternate_emails.text      = base64.b64encode(customer_infos["alternate_emails"].encode('ascii')).decode()
        customer.text              = utils.get_customer_id(self.logger, customer_infos["customer"])
        product.text               = utils.get_product_id(self.logger, customer_infos["product"])
        incident_summary.text      = summary
        incident_description.text  = html.unescape(description)
        incident_severity.text     = severity
        incident_status.text       = utils.get_status_id(self.logger, self.status)
        incident_owner.text        = username

        # Case Audience
        if audience in CASE_AUDIENCES:
            case_audience.text   =  audience
        else:
            case_audience.text   =  "Public"
            self.logger.warn("CaseAudience should be ; Public, Infor Only, Infor & Staff Partner. [Default] Public")
            if audience:
                self.logger.warn("Submitted value : " + audience)

        data = ET.tostring(incident)
        self.logger.info("Payload ready")
        # Submit the request to the API
        self.send_payload(data)
        

    def get_customer(self, customerId):
        url = loadConfig.get_urls()["customer"].format(str(customerId), 'Infor Retail')
        response = authenticate.generate_token()
        if not response["success"]:
            self.logger.error("Exception occurred during login")
            raise XtremeCreateException(response["res"].status_code,
                                        response["res"].reason,
                                        response["res"].text)
        else:
            token = response["token"]
            self.logger.info("Login successful")

        headers = { 'Authorization': 'bearer ' + token,
                    'Content-Type': 'application/octet-stream'}

        res = req.get(url=url, headers=headers)

        if (res.status_code != 200):
            print({"success": False, "res": res})

        print(json.dumps(res.json(), indent=4))


    def send_payload(self, payload):
        ''' Send the Payload to the API

        :param payload: XML object as string
        '''
        response = authenticate.generate_token()
        if not response["success"]:
            self.logger.error("Exception occurred during login")
            raise XtremeCreateException(response["res"].status_code,
                                        response["res"].reason,
                                        response["res"].text)
        else:
            token = response["token"] 
            self.logger.info("Login successful")


        response = authenticate.submit_request(self.url, payload, token)

        if not response["success"]:
            self.logger.error("Exception occurred during incident creation")
            raise XtremeCreateException(response["res"].status_code,
                                        response["res"].reason,
                                        response["res"].text)

        result = ET.fromstring(response["result"])
        
        if result[0][3].text == "OK":
            self.id       = result[0][1].text
            self.link     = result[0][2].text
            self.logger.info("Xtreme incident created successfully!")
            self.logger.info("Incident ID : " + self.id)
            self.logger.info("Link : " + self.link)
        else:
            error_msg = result[0][3].text
            self.logger.error("Request not processed sucessfully")
            self.logger.error(error_msg)
            raise XtremeCreateException(error_msg)


if'__main__'==__name__:
    try:
        xt = XtremeAgent()
        xt.create_incident("Customer X",
                            summary="Quick Maintenance Window",
                            description='''Hello,
                            We are creating this ticket to track the work related to the hotfix release.

                            Further details about deployment testing and release schedule will be shared as soon as these become available. 

                            Thanks,
                            ''',
                            priority=4)

    except XtremeCreateException as ex:
        xt.logger.error("Something went wrong! Please investigate", exc_info=True)



