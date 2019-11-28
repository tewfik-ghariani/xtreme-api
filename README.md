# Xtreme CLI


> XtremeCLI using the wrapper script that leverages the Xtreme updateIncidentAPI & createIncidentAPI.

## Files 

- xtremeAPI/__main__.py
- setup.py
- install.sh
- requirements.txt

----

## Initial Setup

Set up a python3 virtual environment and install the requirements.

```
virtualenv -p python3 venv_xtreme
```

```
source venv_xtreme/bin/activate
```

```
pip3 install -r requirements.txt
```

```
bash install.sh
```

## Configuration

1. Update _xtremeAPI/config/configuration.ini_ file with aps bot creds. ( Find them in the aps instance ;) )

2. Make sure to select the needed environment in the _xtremeAPI/config/configuration.ini_ file.

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


_xtremeAPI/logs/log\_xtreme\_update.log_

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

_xtremeAPI/logs/log\_xtreme\_create.log_

```
[Thu Apr 18 01:29:40 CET 2019] - [INFO] : ------- New Xtreme Ticket
[Thu Apr 18 01:29:40 CET 2019] - [INFO] : Environment : Xtreme_preprod
[Thu Apr 18 01:29:40 CET 2019] - [INFO] : JiraSubComponent : MFP
[Thu Apr 18 01:29:40 CET 2019] - [INFO] : Contact Email : support@customer3.com
[Thu Apr 18 01:29:40 CET 2019] - [INFO] : Severity : 2
[Thu Apr 18 01:29:40 CET 2019] - [INFO] : Customer : customer3
[Thu Apr 18 01:29:40 CET 2019] - [INFO] : Product : Merchandise Financial Planning
[Thu Apr 18 01:29:40 CET 2019] - [INFO] : Incident status : Researching [Default]
[Thu Apr 18 01:29:40 CET 2019] - [WARNING] : Invalid value of caseAudience. Should be ; Public, Staff, Partner.
[Thu Apr 18 01:29:40 CET 2019] - [INFO] : Payload ready
[Thu Apr 18 01:29:41 CET 2019] - [INFO] : Login successful
[Thu Apr 18 01:30:10 CET 2019] - [INFO] : Xtreme incident created successfully!
[Thu Apr 18 01:30:10 CET 2019] - [INFO] : Incident ID : 12917938
[Thu Apr 18 01:30:10 CET 2019] - [INFO] : Link : https://preprod.xtreme.com/espublic/EN/AnswerLinkDotNet/SoHo/Cases/SoHoCaseDetails.aspx?CaseID=12917938
```

----


## Usage

Pretty straightforward 

### Update Incident

```
xtremeUpdate --id 0000001337 --message "Hello world"
```

_Example_

```
xtremeUpdate --id 12754174 --status Researching --audience Internal --message "Hello Xtreme Team, 
>
>  Thank you so much for the collaboration
>
> Regards,"

```

_Help_

```
$ xtremeUpdate -h
usage: xtremeUpdate --id ID --message MESSAGE [options]

Update Xtreme incidents via cli

Required arguments:
  --id ID, -i ID        Xtreme incident ID
  --message MESSAGE, -m MESSAGE
                        Message to be added as event note

Optional arguments:
  --status STATUS, -s STATUS
                        Change incident status , e.g Researching, New..
  --audience AUDIENCE, -a AUDIENCE
                        Update visibilty : Public/Internal/Restricted
  --attachment ATTACHMENT, -f ATTACHMENT
                        File to be attached
  --resolution RESOLUTION, -r RESOLUTION
                        Resolution type in case the status is set to 'Solution
                        Proposed'

Created with love by the Efficiency super team ♥
```

### Create Incident

```
xtremeCreate --app "JIRA-SUB-COMPONENT" --summary "HELLO WORLD" --priority X --description MESSAGE
```

_Example_

```
$ xtremeCreate --app  "MFP" --summary "Creating via CLI" --priority 2 --description "Hey
> This is really cool
>
> Bye"

```

_Help_

```
$ xtremeCreate  -h
usage: xtremeCreate --app SUB-COMPONENT --summary TITLE --description MESSAGE --priority [1-4] [options]

Create Xtreme incidents via cli

Required arguments:
  --app APP, -j APP     Jira Sub-Component : Customer/App
  --summary SUMMARY, -s SUMMARY
                        Title of the incident
  --description DESCRIPTION, -d DESCRIPTION
                        Message to be added as event note
  --priority PRIORITY, -p PRIORITY
                        Severity of the incident [1-4]

Optional arguments:
  --status STATUS, -t STATUS
                        Set incident status: [Default] New
  --audience AUDIENCE, -a AUDIENCE
                        Select visibilty : 'Public'/'Staff'/'Partner'

Created with love by the Efficiency super team ♥

```

## Updating CLI

Once you make some changes to the cli, you just have to re-install it

```
bash install.sh
```

---

Author : Tewfik Ghariani

Date : 05 Jan 2019

