import argparse
from .updateXtremeAPI import XtremeAgent as UpdateAgent
from .createXtremeAPI import XtremeAgent as CreateAgent


def update():
    ## Parsing arguments

    parser = argparse.ArgumentParser(description="Update Xtreme incidents via cli",
                                     prog="Xtreme API",
                                     epilog="Created with love by the Efficiency super team ♥",
                                     usage="xtremeUpdate --id ID --message MESSAGE [options]")

    parser._action_groups.pop()

    # Mandatory Arguments
    required_args = parser.add_argument_group("Required arguments")
    required_args.add_argument("--id", "-i", help="Xtreme incident ID", required=True)
    required_args.add_argument("--message", "-m", help="Message to be added as event note", required=True)

    # Optional Arguments
    optional_args = parser.add_argument_group("Optional arguments")
    optional_args.add_argument("--status", "-t", help="Change incident status , e.g Researching, New..")
    optional_args.add_argument("--audience", "-a", help="Update visibilty : Public/Internal/Restricted")
    optional_args.add_argument("--attachment", "-f",  help="File to be attached")
    optional_args.add_argument("--resolution", "-r", help="Resolution type in case the status is set to 'Solution Proposed'")

    args = vars(parser.parse_args())


    ## Xtreme Update

    xt = UpdateAgent(args["id"])

    xt.add_attachment(attachment=args["attachment"])

    xt.update_incident(message=args["message"],
                       status=args["status"],
                       audience=args["audience"],
                       resolution=args["resolution"])



def create():
    ## Parsing arguments

    parser = argparse.ArgumentParser(description="Create Xtreme incidents via cli",
                                     prog="Xtreme API",
                                     epilog="Created with love by the Efficiency super team ♥",
                                     usage="xtremeCreate --app SUB-COMPONENT --summary TITLE --description MESSAGE --priority [1-4] [options]")

    parser._action_groups.pop()

    # Mandatory Arguments
    required_args = parser.add_argument_group("Required arguments")
    required_args.add_argument("--app", "-j", help="Jira Sub-Component : Customer/App", required=True)
    required_args.add_argument("--summary", "-s", help="Title of the incident", required=True)
    required_args.add_argument("--description", "-d", help="Message to be added as event note", required=True)
    required_args.add_argument("--priority", "-p", help="Severity of the incident [1-4]", required=True)

    # Optional Arguments
    optional_args = parser.add_argument_group("Optional arguments")
    optional_args.add_argument("--status", "-t", help="Set incident status: [Default] Researching")
    optional_args.add_argument("--audience", "-a", help="Select visibilty : 'Public'/'Staff'/'Partner'")

    args = vars(parser.parse_args())


    ## Xtreme Create

    xt = CreateAgent()

    xt.create_incident(args["app"],
                       summary=args["summary"],
                       description=args["description"],
                       priority=args["priority"],
                       status=args["status"],
                       audience=args["audience"])



