import csv
import os
import logging


SOLUTION_PROPOSED_ID  = "4700"

directoryPath  = os.path.dirname(os.path.realpath(__file__)) + "/"
confFile       = directoryPath + "../config/configuration.ini"
status_csv     = directoryPath + "../config/status.csv"
resolution_csv = directoryPath + "../config/resolution.csv"
mapping_csv    = directoryPath + "../config/mapping.csv"
product_csv    = directoryPath + "../config/products.csv"
customer_csv   = directoryPath + "../config/customers.csv"


def fetch_id(file_csv, label_field, id_field, value ):
    '''Generic method to fetch an ID from a csv file

    :param file_csv: csv file under config dir
    :param label_field : Label of name of the entity
    :param id_field : label of entity ID
    '''

    with open(file_csv, "r") as _file:
        rows = csv.DictReader(_file, delimiter='|', quotechar='"')
        for row in rows:
            if row[label_field].lower() == value.lower():
                return str(row[id_field])
    return None


def get_status_id(logger, status_label):
    ''' Return the ID of the incident status according to status_label 
                 from status.csv config file. ( Case insensitive )
    Default status : "Researching"

    :param status_label: Status submitted by the user.
    '''
    # Default: Researching
    status_id        = "1300"

    if not status_label:
        logger.info("Incident status : Researching [Default]")
        return status_id
    
    status_id = fetch_id(file_csv=status_csv,
                         label_field="StatusName",
                         id_field="StatusID",
                         value=status_label)
    if not status_id:
        logger.warn("Status not recognized : " + status_label)
        logger.warn("Using default : Researching")

    logger.info("Incident status : " + status_label)
    return status_id


def get_customer_id(logger, customer):
    ''' Return the Customer ID according to customer label
                 from customers.csv config file. ( Case insensitive )

    :param customer: Customer Label fetched from mapping.csv
    '''
    if not customer:
        logger.error("Customer label not specified")
        raise Exception("Customer missing from mapping.csv")

    customer_id = fetch_id(file_csv=customer_csv,
                           label_field="Customer",
                           id_field="CustomerID",
                           value=customer)
    if not customer_id:
        logger.error("Customer not recognized : " + customer)
        raise Exception("Customer missing from customers.csv")
    logger.info("Customer : " + customer)
    return customer_id


def get_product_id(logger, product_name):
    ''' Return the ID of the Xtreme product according to product name
                 from products.csv config file. ( Case insensitive )

    :param product_name: Product Label fetched from mapping.csv
    '''
    if not product_name:
        logger.error("Product name not specified")
        raise Exception("Product missing from mapping.csv")

    product_id = fetch_id(file_csv=product_csv,
                          label_field="ProductLabel",
                          id_field="ProductID",
                          value=product_name)
    if not product_id:
        logger.error("Product not recognized : " + product_name)
        raise Exception("Product missing from products.csv")
    logger.info("Product : " + product_name)
    return product_id


def get_resolution_type_id(logger, resolution_label, status_id):
    ''' Return the ID of the incident resolution type according to resolution label 
                 from resolution.csv config file. ( Case insensitive )
    No default value. Required if status is "Solution proposed"

    :param resolution_label: Resolution type submitted by the user.
    :param status_id : ID of the status to compare with the ID of SP.
    '''
    # Specify the resolution type only if status is Solution Proposed
    if status_id != SOLUTION_PROPOSED_ID:
        return None

    if not resolution_label:
        logger.error("Resolution type not specified.")
        raise Exception("Resolution type is required if status is 'Solution Proposed'.")


    resolution_id = fetch_id(file_csv=resolution_csv,
                             label_field="ResolutionName",
                             id_field="ResolutionTypeID",
                             value=resolution_label)
    if not resolution_id:
        logger.error("Resolution not recognized : " + resolution_label)
        raise Exception("Please submit the correct resolution name.")
    logger.info("Resolution Type : " + resolution_label)
    return resolution_id


def get_event_action_type_id(status_id):
    ''' Return the ID of the event action type according to the status 
    Either "Update" or "Solution Proposed"
    Set to SP only if the status is Solution Proposed.

    :param status_id : ID of the status to compare with the ID of SP.
    '''
    if status_id != SOLUTION_PROPOSED_ID:
        # Event action type : Update
        return "7"
    else:
        # Event action type : Solution Proposed
        return "2"


def fetch_infos(logger, jira_subcomponent):
    ''' Retrieves information such as customer, productLine, email addresses etc
    about a specific client by the mean of a mapping.csv file
    This method uses the Jira Subcomponent as input ; e.g WFM GPM

    :param logger: the logger object 
    :param jira_subcomponent: the customer/application value
    '''
    
    with open(mapping_csv, "r") as mapping_file:
        all_mappings = csv.DictReader(mapping_file, delimiter='|', quotechar='"')
        for mapping in all_mappings:
            if mapping["JiraSubcomponent"].lower() == jira_subcomponent.lower():
                logger.info("JiraSubComponent : " + jira_subcomponent)
                
                customer         = mapping["Customer"]
                product          = mapping["Product"]
                contact_email    = mapping["ContactEmail"]
                alternate_emails = mapping["AlternateEmails"]  
                logger.info("Contact Email : " + contact_email)
                if alternate_emails:
                    logger.info("Alternate Emails : " + alternate_emails)

                return {"customer"         : customer,
                        "product"          : product,
                        "contact_email"    : contact_email,
                        "alternate_emails" : alternate_emails}

    logger.error("Could not find this JiraSubComponent in mapping.csv")
    logger.error(jira_subcomponent)
    raise Exception("Please submit the correct Jira Sub-Component.")


def set_severity(priority):
    if priority == 1:
        return 4 #"ProductionOutageCriticalApplicationhalted"
    if priority == 2:
        return 3 #"Majorimpact"
    if priority == 3:
        return 2 #"Highimpact"
    return 1 #"Standard"


# Logging config
def logging_config(file, name):

    directoryPath = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/"
    log_dir = directoryPath + "logs/"
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
    logfile = log_dir + file
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - [%(levelname)s] : %(message)s",
                        datefmt="[%a %b %d %H:%M:%S %Z %Y]",
                        handlers=[
                             logging.FileHandler(logfile),
                             logging.StreamHandler()
                        ])

    logger = logging.getLogger(name)
    return logger


