# Xtreme API

>Wrapper scripts to leverage the Xtreme updateIncidentAPI and StaffAddIncident API.

## Files 

- updateXtremeAPI.py
- createXtremeAPI.py
- ../requirements.txt
- lib/loadConfig.py
- lib/authenticate.py
- lib/utils.py
- config/configuration.ini
- config/resolution.csv
- config/status.csv
- config/mapping.csv
- config/customers.csv
- config/products.csv

----

## Getting Started

Set up a python3 virtual environment and install the requirements.

```
virtualenv -p python3 ../venv_xtreme
```
```
source ../venv_xtreme/bin/activate
```

```
pip install -r ../requirements.txt
```

## Configuration

1. Update _config/configuration.ini_ file with aps bot creds. ( Find them in the aps instance ;) )

2. Make sure to select the needed environment in the _config/configuration.ini_ file.

*PreProd*

```
[general]
env : Xtreme_preprod
```

*Prod*

```
[general]
env : Xtreme_prod
```


## Logging

The progress is tracked in a log file generated automatically. Every exception is caught and written to the file as well as every step all the way. The log is also redirected to the stdout so no need to tailf anything.


_logs/log\_xtreme\_update.log_

```
[Fri Dec 07 11:48:36 CET 2018] - [INFO] : ------- Xtreme Ticket : 12754174
[Fri Dec 07 11:48:36 CET 2018] - [INFO] : Incident status : solution proposed
[Fri Dec 07 11:48:36 CET 2018] - [INFO] : Resolution Type : knowledge - existing
[Fri Dec 07 11:48:36 CET 2018] - [INFO] : Attachment : image.png
[Fri Dec 07 11:48:36 CET 2018] - [INFO] : File attached
[Fri Dec 07 11:48:36 CET 2018] - [INFO] : Payload ready
[Fri Dec 07 11:48:37 CET 2018] - [INFO] : Login successful
[Fri Dec 07 11:48:39 CET 2018] - [INFO] : Xtreme incident updated successfully!
```

_logs/log\_xtreme\_create.log_

```
[Thu Apr 18 01:29:40 CET 2019] - [INFO] : ------- New Xtreme Ticket
[Thu Apr 18 01:29:40 CET 2019] - [INFO] : Environment : Xtreme_preprod
[Thu Apr 18 01:29:40 CET 2019] - [INFO] : JiraSubComponent : KIABI MFP
[Thu Apr 18 01:29:40 CET 2019] - [INFO] : Contact Email : mfpsupport@kiabi.com
[Thu Apr 18 01:29:40 CET 2019] - [INFO] : Severity : 2
[Thu Apr 18 01:29:40 CET 2019] - [INFO] : Customer : Bunsha
[Thu Apr 18 01:29:40 CET 2019] - [INFO] : Product : Infor Retail Merchandise Financial Planning
[Thu Apr 18 01:29:40 CET 2019] - [INFO] : Incident status : Researching [Default]
[Thu Apr 18 01:29:40 CET 2019] - [WARNING] : Invalid value of caseAudience. Should be ; Public, Infor Only, Infor & Staff Partner.
[Thu Apr 18 01:29:40 CET 2019] - [INFO] : Payload ready
[Thu Apr 18 01:29:41 CET 2019] - [INFO] : Login successful
[Thu Apr 18 01:30:10 CET 2019] - [INFO] : Xtreme incident created successfully!
[Thu Apr 18 01:30:10 CET 2019] - [INFO] : Incident ID : 12917938
[Thu Apr 18 01:30:10 CET 2019] - [INFO] : Link : https://preprod.inforxtreme.com/espublic/EN/AnswerLinkDotNet/SoHo/Cases/SoHoCaseDetails.aspx?CaseID=12917938
```

----

## Usage

### Update Incident

Simple usage instructions ; instantiate an *XtremeAgent* object and use its pre-defined methods.


```
from xtremeAPI import XtremeAgent as UpdateAgent

xt = UpdateAgent(12754174)                               <---------- Xtreme ID

xt.add_attachment(attachment="image.png")                <---------- Optionally add attachment

xt.update_incident(message="Solution proposed via API"    <--------- Update the incident
                   resolution="knowledge - existing",               - message: Mandatory
                   audience="Public",                               - audience: Optional
                   status="solution proposed")                      - status: Optional
                                                                    - resolution: Only required if status is SP
```

### Create Incident

Simple as well

```
from xtremeAPI import XtremeAgent as CreateAgent

xt = CreateAgent()                                       <---------- Object Instantiation

xt.create_incident("KIABI FR",                           <--------- - Jira Sub-Component : Mandatory
                   summary="Hotfix release 2.2",                    - summary: Mandatory
                   description="This is the event note",            - description : Mandatory
                   priority=3,                                      - priority : Mandatory
                   status="awaiting customer",                      - status: Optional
                   audience="Public")                               - audience: Optional

```

---

## Options in details

### Incident Status

If not defined, the status is set by default to “Researching”.

In case the status is incorrect, a warning would be displayed in the logs and the default value would be used.

Please be advised that the status is case insensitive. 

_Examples_
‌
```
xt.update_incident(message="Default status via API")
```

```
 xt.update_incident(message="Changing incident status via API", status="awaiting Infor")
```

```
xt.update_incident(message="Solution proposed via API",
                   status="task pending scheduling")
```

```
xt.update_incident(message="Changing status via API", status="Solution proposed")
```
Note : Resolution type is required if the status is set to "Solution Proposed".



Please refer to _config/status.csv_ for the full list.



### Resolution Type

There is no default value for the resolution. It is required in case the status is set to "Solution Proposed".

```
xt.update_incident(message="Solution proposed via API",
                   resolution="knowledge - existing",
                   status="solution proposed")
```


The script will raise an exception in case the resolution is not specified or incorrect while the status is "Solution Proposed"


```
[Fri Dec 07 11:31:59 CET 2018] - [INFO] : ------- Xtreme Ticket : 12754174
[Fri Dec 07 11:31:59 CET 2018] - [INFO] : Incident status : Solution proposed
[Fri Dec 07 11:31:59 CET 2018] - [ERROR] : Resolution type not specified.
[Fri Dec 07 11:31:59 CET 2018] - [ERROR] : Something went wrong! Please investigate
Traceback (most recent call last):
  File "update.py", line 324, in <module>
    status="Solution proposed")
  File "update.py", line 273, in update_incident
    resolution_type_id.text   = self.get_resolution_type_id(resolution, status_id.text)
  File "update.py", line 122, in get_resolution_type_id
    raise Exception("Resolution type is required if status is 'Solution Proposed'.")
Exception: Resolution type is required if status is 'Solution Proposed'.
```

Please refer to _config/resolution.csv_ for the exhaustive list of resolution types.

### Attachments

You may optionally attach one file while updating an incident. To achieve that, it is possible to either specify the relative path or absolute path of a file.

```
xt.add_attachment(attachment="image.png")
```

```
xt.add_attachment("/home/tawfikghariani/Downloads/wbs_cv.png")
```
You may optionally specify the file name of the attachment. If not specified, it would be detected automatically from the file itself.

```
xt.add_attachment(attachment="files/image.png", filename="results.png")
```


Additionally, it is possible to view the list of attachments referenced by the currently instantiated object

```
xt.list_attachments()
```
It is also possible to flush the attachment attribute of the object

```
xt.remove_attachment()
```

### Audience

Voluntarily alter the value of eventAudience. It should be one of these options ; Public, Internal, Restricted.

```
xt.update_incident(message="Jira Ticket as Internal contribution", audience="Public")  
```
Default audience : "Public"

### Event Action Type

The event action type is by default set to "Update" except for the case where the status is "Solution proposed".
In that case, it’s set to Solution Proposed as well. This attribute is not up for modification.


### Priority

Set the severity of the incident while creating it. Simply choose the priority number of the corresponding severity as shown below

1 : "ProductionOutageCriticalApplicationhalted"

2 : "Majorimpact"

3 : "Highimpact"

4 : "Standard"


_Example_

```
xt.create_incident("KIABI MFP",summary="Data surgery",description="This is a Sev1 incident",priority=1)
```

---

Author : Tewfik Ghariani

Date : 07 Dec 2018

Hello APS : [Aps Tools -- Xtreme API](https://hello-aps.predictix.com/courses/course-v1:Infor+Infor_Retail005+infor_2017/courseware/dfa16f943e0649f791016fb39e848333/ecc1c1db86c448b1903412d061e84bd9/)

Details ;
UpdateAPI : [AET-186](https://logicblox-jira.atlassian.net/browse/AET-186)
CreateAPI : [AET-207](https://logicblox-jira.atlassian.net/browse/AET-207)


