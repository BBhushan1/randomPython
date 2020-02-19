import requests, urllib3
from xml.etree import ElementTree

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def PullTickets(xmlfile):
    ticketlist = []
    root = ElementTree.fromstring(xmlfile)
    for child in root:
        if str(child.tag) == '{http://www.w3.org/2005/Atom}entry':
            ticketlist.append(child)
    return ticketlist


def ReturnTicketInfo(ticketid, rsession):
    ticketinfo = {}
    r = rsession.get("https://ticket-api.amazon.com/tickets/" + ticketid)
    root = ElementTree.fromstring(r.text)
    for child in root:
        tagname = child.tag.split("}")[1][0:]
        if tagname == 'correspondence' or tagname == 'work_log':
            ticketinfo[tagname] = child
        else:
            ticketinfo[tagname] = child.text
    return ticketinfo


def TicketSearch(url, apiquery, message='', flxauth: tuple = ('NOAUTH', 'NOAUTH')):
    session = requests.Session()
    session.auth = flxauth
    session.verify = False
    r = session.get(apiquery)
    messeages = []
    ticketlist = PullTickets(r.text)
    if ticketlist:
        with open("oldhighsev.txt", 'a+') as f:
            headers = {"Content-Type": "application/json"}
            emoji = ":bell:"
            for tickets in ticketlist:
                if tickets[0].text not in alloldticket:
                    print(tickets[0].text)
                    tinfo = ReturnTicketInfo(tickets[0].text, session)
                    #severity = 'SEV' + tinfo['impact']
                    create_date = tinfo['create_date']
                    assigned_individual = tinfo['assigned_individual']
                    # chimetext = "{emoji} [{impact}] Ticket Link: https://tt.amazon.com/{id} : {sdesc}".format(
                    #     emoji=emoji, impact=severity, id=tickets[0].text, sdesc=tickets[6].text)
                    chimetext = "{assigned_individual} - {emoji} - Ticket Link: https://tt.amazon.com/{id} - {create_date}".format(emoji=emoji, id=tickets[0].text, assigned_individual=assigned_individual, create_date=create_date)
                    messeages.append((chimetext[:150] + '..') if len(chimetext) > 150 else chimetext)
                    f.write(tickets[0].text + '\n')
            if messeages:
                r = session.post(url, headers=headers, json={"Content": message.format(tickets='\n'.join(messeages))})
    else:
        return 1


alloldticket = []
try:
    with open("oldhighsev.txt", 'r') as f:
        for line in f:
            alloldticket.append(line.rstrip("\n"))
except FileNotFoundError:
    open("oldhighsev.txt", 'a+').close()

groups = ["IT-Support-APAC","Helpdesk"]  # Replace with groups you want to monitor
buildings = ('BOM14')  # Replace with city or cities
assigned_users = ('bhbhu','pkgiri','anandlad')
impacts = ('1', '2', '3', '4', '5')  # Severity Levels
whurl = "https://hooks.chime.aws/incomingwebhooks/a5afc579-7027-4c07-9a96-a286d09c67fc?token=a2twREI5Zk18MXxva2xEZXVQTWdNV1FVbDR6cDJ6X19sSV9OR0xNbFl2Mlg4QVRsbXdmY1VV"
chimeMessage = "Hi, Please check the following Ticket:\n {tickets}"  # Please note that you must have '{tickets}' some where in the string. I would recommend trying in a test room to see how the message will look.

apiSearchQuery = "https://ticket-api.amazon.com/tickets/?status=Assigned,Pending&assigned_group={groups}&impact={impact}&assigned_individual={assigned_users}".format(
    groups=';'.join(groups), impact=';'.join(impacts), assigned_users=';'.join(assigned_users))
print(apiSearchQuery)
TicketSearch(whurl, apiSearchQuery, chimeMessage, ("flx-itsupport-bom", "NJI(9ol."))
#, city=';'.join(cities)
#&city={city}
# + "&building_id=BOM14"