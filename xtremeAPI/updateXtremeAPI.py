import os
import base64
import json
import html
from pathlib import Path 
import xml.etree.ElementTree as ET

import requests as req

from xtremeAPI.lib import loadConfig
from xtremeAPI.lib import authenticate
from xtremeAPI.lib import utils
from xtremeAPI.lib.exceptions import XtremeUpdateException


API_VERSION           = "2.1"
EVENT_AUDIENCES       = ["Public", "Internal", "Restricted"]



class XtremeAgent:
    def __init__(self, xtreme_id):
        # Incident ID
        self.xtreme_id   = str(xtreme_id)
        self.attachment  = None
        self.file_name   = None
        self.params      = loadConfig.get_params()
        self.url         = loadConfig.get_urls()["update"]
        self.logger      = utils.logging_config('log_xtreme_update.log', 'xtremeUpdateLogger')
        self.logger.info("------- Xtreme Ticket : " + self.xtreme_id)
        self.logger.info("Environment : " + self.params["xtreme_env"])



    def add_attachment(self, attachment, filename=None):
        ''' Add any sort of attachments

        :param attachment: The absolute or relative path of the file.
        :param filename: the label of the attachment.
        '''

        if not attachment:
            self.logger.warn("No attachment specified, ignoring..")
            return

        if not os.path.isfile(attachment):
            self.logger.error("The attachment cannot be found : " + attachment)
            raise XtremeUpdateException("Please verify the path of the attachment file.")

        # Detect automatically the file name
        if not filename:
            self.filename = Path(attachment).name

        with open(attachment, "rb") as _file:
            self.attachment = base64.b64encode(_file.read()).decode()


    def list_attachment(self):
        ''' List the attachment's filename that has been added to the current object.
        '''
        if self.attachment:
            self.logger.info("Attachment : " + self.filename)
            return self.filename
        else:
            self.logger.warn('No attachment has been added so far.')
            return None


    def remove_attachment(self):
        ''' Flush the attachment associated to the object
        '''
        if self.attachment:
            self.attachment  = None
            self.filename    = None
            self.logger.info('No more attachment.')
            return True
        else:
            self.logger.warn('There was actually no attachment.')
            return False

        
    def update_incident(self, message,
                              audience="Public",
                              status=None,
                              resolution=None):
        ''' Prepare payload and update the incident

        :param message: The event note to be written to the ticket.
        :param audience: Value of eventAudience. 
            Should be ; Public, Internal or Restricted. Default : 'Public'
        :param status: Change the status of the incident (Optional)
        :param resolution: Resolution Type (Required only of status is SP)
        '''

        b64_username         = loadConfig.get_b64_credentials()["username"]
        username             = self.params["username"].decode()


        # Structure of the xml file
        incident             = ET.Element('Incident')
        email_id             = ET.SubElement(incident, 'EmailID')
        staff_email          = ET.SubElement(incident, 'StaffEmail')
        incident_id          = ET.SubElement(incident, 'IncidentID')
        event_note           = ET.SubElement(incident, 'EventNote')
        event_audience       = ET.SubElement(incident, 'EventAudience')
        status_id            = ET.SubElement(incident, 'IncidentStatusID')
        action_owner_email   = ET.SubElement(incident, 'ActionOwnerEmail')
        case_owner_email     = ET.SubElement(incident, 'CaseOwnerEmail')
        action_owner_group   = ET.SubElement(incident, 'ActionOwnerGroup')
        case_owner_group     = ET.SubElement(incident, 'CaseOwnerGroup')
        service_restored     = ET.SubElement(incident, 'ServiceRestored')
        solution_proposed    = ET.SubElement(incident, 'SolutionProposed')
        resolution_type_id   = ET.SubElement(incident, 'ResolutionTypeID')
        event_action_type_id = ET.SubElement(incident, 'EventActionTypeID')
        filename             = ET.SubElement(incident, 'Filename')
        attachment           = ET.SubElement(incident, 'Attachment')
        api_version          = ET.SubElement(incident, 'APIVersion')

        # Value of each sub element
        api_version.text          = API_VERSION
        email_id.text             = b64_username
        staff_email.text          = username
        incident_id.text          = self.xtreme_id
        event_note.text           = html.unescape(message)
        # Event Audience
        if audience in EVENT_AUDIENCES:
            event_audience.text   =  audience
        else:
            event_audience.text   =  "Public"
            self.logger.warn("CaseAudience should be ; Public, Infor Only, Infor & Staff Partner. [Default] Public")
            if audience:
                self.logger.warn("Submitted value : " + audience)

        status_id.text            = utils.get_status_id(self.logger, status)
        action_owner_email.text   = None
        case_owner_email.text     = None
        action_owner_group.text   = None
        case_owner_group.text     = None
        service_restored.text     = None
        solution_proposed.text    = None
        resolution_type_id.text   = utils.get_resolution_type_id(self.logger, resolution, status_id.text)
        event_action_type_id.text = utils.get_event_action_type_id(status_id.text)
        # Attachment
        if self.attachment and self.filename:
            self.list_attachment()
            filename.text         = self.filename
            attachment.text       = self.attachment
            self.logger.info("File attached")
        else:
            filename.text         = None
            attachment.text       = None

        data = ET.tostring(incident)
        self.logger.info("Payload ready")
        # Submit the request to the API
        self.send_payload(data)
        

    def send_payload(self, payload):
        ''' Send the Payload to the API

        :param payload: XML object as string
        '''
        response = authenticate.generate_token()
        if not response["success"]:
            self.logger.error("Exception occurred during login")
            raise XtremeUpdateException(response["res"].status_code,
                                        response["res"].reason,
                                        response["res"].text)
        else:
            token = response["token"] 
            self.logger.info("Login successful")


        response = authenticate.submit_request(self.url, payload, token)

        if not response["success"]:
            self.logger.error("Exception occurred during incident update")
            raise XtremeUpdateException(response["res"].status_code,
                                        response["res"].reason,
                                        response["res"].text)

        result = ET.fromstring(response["result"])[0][1].text

        if result == "OK":
            self.logger.info("Xtreme incident updated successfully!")
        else:
            self.logger.error("Request not processed sucessfully")
            self.logger.error(result)
            raise XtremeUpdateException(result)


if'__main__'==__name__:
    try:
        xt = XtremeAgent(12754174)
        #xt.add_attachment(attachment="image.png")
        xt.update_incident(message="Solution proposed via API",
                           resolution="knowledge - existing",
                           status="solution proposed")

    except XtremeUpdateException as ex:
        xt.logger.error("Something went wrong! Please investigate", exc_info=True)


