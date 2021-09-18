DevDiary
Week 8
Communication and Network Security Video Notes

TCP/IP
Transmission Control Protocol
Connectionn-oriented prorocol
Guarentees delivery
Widely used for cruical applications (like email)

3 way handshake
TCP Flags
SYN packets identify flags reuesting new connection
FIN flags requesting closure
ACK flag agnolegis syn of FIN packet

Step 1: System originating the connection sends a SYN FLAG set indicating that it wants to open a connection to the destination system.
Step 2: destination system replys with a ACK flag in response and a coupled SYN flag to ask to open a reciprical connection with the originating connection
Step 3: originating system sends a final ACK flag back to destination system.
After this process is complete the systems can send data back and forth

UDP is more lightweight, and is not connection oriented.
Systems just send off information blindly and and hopes it is recieved. It does not perform accnoligments and is used when not every packet needs to be recieved (like voice or video)

These Models are desctibed by OSI
Networks have seven different layers:

Physical Layer: Wires, radio waves
Data Link Layer: Data transfer between two nodes
Network Layer (IP)
Transport Layer (TCP UDP)
Sessions Layer: Exchanges between systems
Presentation Layer: Data translation, encrypion
Application Layer: User interaction

TCP network Model:
Network Layer interface ->Data Link Layer + Pysical Layer
Network Layer -> Internet Layer
Trasnport Layer -> Transport Layer
Application Layer -> Network Layer + Data Link Layer + Physical Layer

IP Addresses and DHCP
IP = Internet protocol
written as 4 numbers seperated by . each number between 0-255 (8BITS)
IP Addresses must only be used in one location in the world.
Private addresses may exist within a network and translated into an IP Address by a router

IP addresses are divided, first half is the Network Address and the second is the Hots Address
The division does not have to be in the center the address can be divided anywhere
Source identifies the address sending information
Destination identifies the address recieving information
IP Addresses that use dotted quad notation ae part of IPv4 (000.000.000.000)
IPv4 is running out of addresses so is being replaced by IPv6
IPv6 uses hexidecimal notation: e.g. 12af:12af:12af:12af

IP Addresses can be assigned Statically, or by using DHCP, a pool is designated and then automatically assigned.
Servers are normally Static and individual devices are normally DHCP

Domain name system DNS
DNS servers translate names into IP addresses
DNS functions over UDP port 53
When you type in a domain name your computer sends a DNS query to the local DNS server and asks for the IP address.
If the DNS server knows the address then it answers your computer, if it doesn't know it contacts other DNS servers.
DNS is Hierarchical System

Most of the time DNS happens behind the scenes.

Can use he dig command to look up IP addresses
dig www.linkedin.com
Can specify which DNS server to ask with @
dig @8.8.8.8 linkedin.com

Some content filtering tools stop users from accessing undesirable websites. The tools work by providing incorrect answers to DNS queries. If you use this approach you must prevent outbound DNS requests to other webservers. In this case you would need to block all the public webservers. If not, the user can change the DNS server in network settings and avoid filterings.

Hackers may try and insert false DNS records into intermediate, to fool people to accessing fake sits.
DNSSEC protocol adds digital signatures to DNS

Network ports:
IP Address is like an appartment building and network ports are like appartment numbers.
Uses 16 BIT binary numbers.
port numbers range from 0-65,535
0-1,023 = well-known ports reserved for common applications and assigned by internet authorities
1,024-49,151 = registered ports
49,152-65,535 = dynamic ports
FTP uses port 21
SSH uses port 22
RDP use 3389
Windows NetBIOS 137,138,139 email
Port 53 DNS
Port 25 SMTP
Port 110 POP
Port 143 IMAP
Port 80 HTTP
Port 443 HTTPS

ICMP Internet control message protocol
Ping command for network troubleshooting
Ping asks are you there, and the other target system replys
Are you there is ICMP ECHO REQUEST
Yes I am is ICMP ECHO REPLY
In consol can type: ping website.com
Will continue sending pings to website until press cntl+C

ICMP Traceroute shows path between systems
I flag means use ICMP
consol: traceroute -I website.com
Can be used to troubleshoot slow connections by telling you where the problem is

Other ICMP Functions:
Destination unreachable
Redirects
Time exceeded
Addresses mask requests and replies

Multilayer protocols:
DNP3
Provides network connectivity for SCADA system (Supervisery control and data aquisition)
Purpose is to collect data from remote substations
Communcation links then connected to
SCADA Master station/control center Which collects the data and sends back commands
DNP3 covers the entire OSI Model

------------------------------------------------------------------------------------

Public and Private addressing
Public IP Addresses:
Assigned by a central authority and are routabe over the internet
Private IP Addresses:
Avaliable for anyone's use but not routabe through the internet.

ICANN breaks up addresses into blocks and gives them to regions in the world.
IP Addresses are scarce, and must be purchased to assigned.
IPv4 has only 4.3 billion possible addresses, but there are 7.4 billion mobile devices only.

The solution is private IP Addresses Ranges:
10.0.0.1 - 10.255.255.255
172.16.0.1-172.31.255.255
192.168.0.1-192.168.255.255

Typially organisations normally use a combination.
The issue is that users within a network with private IP addresses can't access the internet

The solution is NAT (network address translation)
routers and firewalls provide nat translations
the router records he outgoing request from a private IP the NAT system lends an IP address temporarily. It records the public and private IP address translation and when a reply comes in to routes the packet.
Issues
NAT Hides internal addresses from interne systems.
Limits direct access to systems.
Makes it difficul to identiy the true origin of the traffic

NAT requires a public IP Address for each device that communicates, as a organisation may only have a limited number of address no new systems can communicate on the system.

PAT solves this (Port Address Translation)
Allows multiple systems to share the same public address
Assigns unique ports to each communiation

Subnetting
Brings a large network address space into smaller pieces
TO do this we need to use subnet masks
192.168.1.100
Draw line between 192.168. | 1.100
255.255.255.0 is the subnet mask

Secruity zones
Network boarder firewall
Networks may create different security zones.
Zero Trust approach
System gains no trust based solely upon network location
Extranet is special intranet sets that are accessable from outside
Honeynets are decoy networks
Ad Hoc Networks are normally temporary and may present a secruity risk
East-West traffic
Network traffic between systems in a data center
North-South traffic is traffic between systems on the internet
Noth East-West and North-South may be effected by the firewall

VLANs
Can be used to connect different parts of the network
They extend the boardcast domain,

Security Device Placement
Firewalls should be placed wherever you want to inforce a network security boundry
Many security systems collect information such as
Intrusion detection and prevention sensors
Network traps
Port mirrors
Where you locate sensors allows monitoring of different traffic
Security Information and Event management
Gather information using collectors
Analyze information with a centrailsed aggregation and correlation engine
Multiple collectors and a single coorlation engine performs aggregation.
Place collectors in networklocations that minimizes the path distance between the collectors and the devices sending information.
Proxy servers and content filters typically belong in the DMZ
VPN concentators commonly go on their own vlan. And then limit access
DDoS Mitigation Tools
Belong as close to the internet connection as possible to stop it entering deeper into the network.

SDN
Treats network functionality and implementation seperately

Network Security Devices
Routers switches and bridges:
switches connect devices to the network
some switches connect wireless (WAPs)
Switches are limited to creating local networks and work at layer 2 of the OSI model
some swtiches may work at layer 3 of the OSI model
ROuters provide a higher level role. ROuter is the airtraffic controler of the network. Routers also provide some security roles.
Bridges are like switches (level 2) but only connect two networks together.
Firewalls are the securityguards of the network. They decided if things should be allowed or denied.
They can see all inbound and outbound connections.
Firewalls often connect the internal network / internet and / DMZ together

Older firewalls used stateless inspection. Inspects all requests
Modern firewalls used statefull inspection. which tracks open connections, and only checks new requests.
Firewall rule contents
Source system address
Desitnation system address
Destination port and protocol
Action (allow/deny)

One of core actions of firewall is that of implicity deny. Which denys anything that is not specifically allowed.
NGFW incorperates a lot more functionality into the firewall (Next generation firewall)
NAT Gateway
Firewalls provide content filtering.
Web application firewalls understand how the HTTP protocol works and checks for web application attacks

Network firewalls and software firewalls can be used together.

Proxy
Gives anonymity.
Gives cached copys and reduces network bandwidth
Can do content filtering.
Transparent Proxies work without the knowledge of both client and servers knowledge
Proxies and handle web traffic and other network protocols

Load balancers
connect multiple webservers to manage traffic
the load balancer has the DNS entry that is published to the world
As the demand increases the administrator can simply add new servers / or this can be done automatically.
load balancers can also create a single point of failure. to compensate can use multiple load balancers, so if one fails the other can take over

VPN
Provide secure protection to connect remote offices to eachother
Remote access VPNS allow remote workers to connect with the organisaitons network.
VPNS are like tunnels.
VPNS require endpoints, these can be routers, firewalls, servers, and VPN concentrators.
VPN traffic requires a lot of resources can can cause performance issues.
IPsec works at the network level of OSI model
These can be difficult to configure, so is less used by remote users.
SSL / TLS VPNS work at the application layer.
HTML5 VPNS work entirly in the web server using it as a proxy.


----------------------------------------------------------------------------------------------------------------------------


WEEK 8 PROJECT WORK:

Implemented Door construction.
Each room remembers what rooms are on its bot/top/left/and right posistions. Doors are then constructed along these axis.
The doors are built by looking at an array which remembers the order that rooms are added to the house_property. Doors are then drawn between each room in order. This results in houses that may have the same final floorplan but will still have a different doors internally.
The Front door is a base case, as in the case of the front door the room that it is built off does not exist. To solve this problem in a simple way the
system will seach for the first room that appears and add a door in the left position of this room. This results in a predictable front door location. However this system could be improved at a later date if time permits.

The add door class is shown below as an example:

    def addDoors(self, mc):
        print('room order is',self.roomOrder)
        for index in range(len(self.roomOrder)): #the position of the first room in rooms list
            print('this rooms location is:',self.roomOrder[index][0]) #first element in the roomOrder tuple
            print('this rooms creator is:',self.roomOrder[index][1]) #first element in the roomOrder tuple
            if(self.roomOrder[index][1]!=None): #if its not the first room
                self.rooms[self.roomOrder[index][0]].createDoor(mc,self.rooms[self.roomOrder[index][1]]) #create a door between this room
            else: #its the first room, send in None
                self.rooms[self.roomOrder[index][0]].createDoor(mc,None)

    def createDoor(self,mc,prevRoom,doortype='single'):
        if(prevRoom is None): #Do nothing
            pass
        else: #Previous room exists, 
            currentLocation = self.connectedRooms.index(prevRoom.roomPos) #find index of prevRoom room in the prevRoom room connectedRooms array
            self.doors[currentLocation] = currentLocation
            doorLocationPrev = prevRoom.connectedRooms.index(self.roomPos) #find index of current room in the prevRoom room connectedRooms array
            prevRoom.doors[doorLocationPrev] = doorLocationPrev
            print('self.doors:',self.doors)
            self.drawDoor(mc,currentLocation, doortype)
    
    def drawDoor(self,mc,doordirection,doortype):
        doorWidth = 1 #these are hard coded but could be changed to be given as inputs to the function at a later date
        doorDepth = 1
        doorHeight = 3
        roomWidth = abs(self.xstart-self.xend)
        roomDepth = abs(self.zstart-self.zend)
        if(doordirection == 0): #door is on bot
            mc.setBlocks(self.xstart-doorDepth,self.ystart+1,self.zstart+roomDepth//2,self.xstart+doorDepth,self.ystart+doorHeight,self.zstart+roomDepth//2+doorWidth,0) #Acacia Wood Plank
        if(doordirection == 1): #door is on top
            mc.setBlocks(self.xend+doorWidth,self.ystart+1,self.zstart+roomDepth//2,self.xend-doorWidth,self.ystart+doorHeight,self.zstart+roomDepth//2+doorWidth,0) #Coarse Dirt
        if(doordirection == 2): #door is on left
            mc.setBlocks(self.xstart+roomDepth//2,self.ystart+1,self.zstart-doorWidth,self.xstart+roomDepth//2+doorWidth,self.ystart+doorHeight,self.zstart+doorWidth,0) #Granite
        if(doordirection == 3): #door is on right
            mc.setBlocks(self.xstart+roomDepth//2,self.ystart+1,self.zend-doorWidth,self.xstart+roomDepth//2+doorWidth,self.ystart+doorHeight,self.zend+doorWidth,0) #Polished Diorite

Now implementation will move onto adding a second story to the house.
Currently I am looking at two positiblities 
    1) Adding a Above/Below position to the room class to keep track of what is above or below them.
    2) Adding a level to the house class which will then build depending on what is below it (but not remember exactly which room is below)

After working at implementation decided to use option two, the reason is that due to each level having an equal amount of divisions (same room size)
it is trivial to work out the room which is below the current room

17-09-2021: 4:30
    Working on implemetning windows.
    Strategy is to add windows to all floors after the house is constructed
    Will look at room adjacencies and determin which rooms outwards facing, then add a window to each avaliable outwards faceing wall

17-09-2021 5:40pm
    Working on implementing windows.
    Strategy it working however having irregular bug in window positions, searching for the cause.
    Found the cause to be a problem in the way I was calculating the which locations were potential window allocations. My loop was checking for rooms with edges facing outside the property boundy but not those which faced empty rooms.
    After finding the issue i was able to solve the problem. Solution code snippit included below.

    def addWindows(self,mc):
        for currentRoom in self.rooms: #Search through all the rooms
            if currentRoom.full == True: #The room is filled
                print(f'{currentRoom.roomPos=}')
                print(f'{currentRoom.roomPos} has empty wall space at {currentRoom.walls}')
                for index, conRoom in enumerate(currentRoom.connectedRooms): #look at the connected rooms:
                    if conRoom != None: #If there is no room there potential window Location
                        if self.rooms[conRoom].full == False:
                            if(currentRoom.walls[index] == None):
                                currentRoom.createWindow(mc,index)
                    else:
                        if(currentRoom.walls[index] == None):
                            currentRoom.createWindow(mc,index)

    An error still exists in this code when the room is of type pool. This will need to be a base case, another potential issue is that windows are not build on the upper level of a staircase, while this is potentially optional the space exists to include the window at this location so changes can be made depending on time permitting.

18-09-2021: 8:40am
    After Hoonie connected the house class to maxs property system some the window code was not included (he was working to connected an older version).
    Working to reimplement the windowsclass in the new house.py file
    Reimplementation of windows trivial. Also notices some bug fixes that had no made it across also fixed.

18-09-2021: 8:55am
    Started implentation of room coupling (wide door)
    Wide rooms created without problem, simply added a new door type of 'fullwidth' which draws a door that takes the entire width of the room.
    Very happy with implementation and simplicity of building double walls, will put a random chance generater in the wall building function to move between this type of door and regular doors.
    Random selection functionality created, uses an array which holds a list of possible door types and selects each with equal probability
18-09-2021: 10:22am
    Started testing with larger block sizing. Added color property to a room, set at houseCreation, staircases will take color of floor above them to help navigation
    No issues yet found with larger block sizes.
    Discovered and fixed a bug related to the adding more rooms to a level than can be be fitted in the space,

18-09-2021: 12:06am
    Fixed bugs related to the location of the staircase, now all stairs share a similar directional pattern, making them fit together.
    Started working on implementing the building roof, added a property to floor which points to the floor above it.
