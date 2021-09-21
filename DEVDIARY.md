# Development Diary
This is a *template* for your dev diary in PS2.
Feel free to edit as you see fit e.g., based on your progress updates, hurdles encountered and circumvented.
Make sure to log one comprehensive update per student, per each week of our teaching term.
Please, get in touch with teaching staff for any questions around this or otherwise post on Microsoft Teams.

# Mandatory Student's contributions
Please, specify your individual contributions to the project **as a percentage**. 
Default is a *25% contribution for each student*. However, please modify as necessary, if that is not the case.

# Development Diary Activities
Please, report your key activities in each week this assignment is running.  

**Week 1**
* Muhammad Zain Nauman
    - [x] Read chapter 1 & 2 on textbook
    - [x] Setup VS Code, and Minecraft on my Linux distro
    - [x] Implemented Hello Minecraft!
    - house building methods [link](house_randomisation_testing.py)
* Max Foord
    - [X] Read chapter 1 & 2 on textbook
    - [X] Setup VS Code, and Minecraft on windows 
    - [X] Implemented Hello Minecraft!
* Cal Lamshed
    - [X] Read chapter 1 & 2 on textbook
    - [X] Setup VS Code, and Minecraft on my Windows
    - [X] Implemented Hello Minecraft! [Link](DEVDIARYFILES_CAL_LAMSHED/hellominecraftworld.py)
    - My personal DevDiary can be found in the Folder DEVDIARYFILES_CAL_LAMSHED in the file [DEVDIARY_CAL_LAMSHED.md](DEVDIARYFILES_CAL_LAMSHED/DEVDIARY_CAL_LAMSHED.md)

* Myeonghoon Sun
    ## Week 1
    - [x] Read chapter 1 & 2 on textbook 📖 
    - [x] Setup VS Code, and Minecraft on my Mac 🆚
    - [x] Implemented Hello Minecraft! [Hello Minecraft](Myeonghoon%20Sun's%20PAs/hello_world.py)
    - [x] I've finished writing my version of a foundation generator which randomly chooses from a limited range of values to pad a foundation with buffers. Buffers ensure against another buffer piling up on pre-existing ones. This process gets repeated until the maximum number of foundations is generated in all rows. It also adds to the element of randomness by spacing out these grids. The result of this algorithm is metropolitan grids where buildings are never far away from each other, but never predictably placed to take the fun away from a potential wanderer. You could find more about it through this link: [link](foundation_generator/foundation_grid.py)

    On a side note, my code will never see the light of day in the implementation of our code, as another teammate has taken it upon himself to build his own version to accomodate his roads. 

    * PAs
      - Convert the binary number 10101 to decimal: 21
      - Convert the hexadecimal number 3E to decimal: 62
      - Convert the binary number 1101001010111111 to hexadecimal: d2bf
      - Convert the decimal number 39 to binary: 100111
      - Convert the decimal number 63 to hexadecimal: 3f
      - [Stairway](Myeonghoon%20Sun's%20PAs/staircase.py)    

    ---

    ## Week 2
    
    ### Integration of teammate's works
    
    Cal's house class needs to be integrated into Max's foundation class. Cal's house_property class equals Max's foundaion class. As Max's Village class contains a list for foundations, we can build a method inside it to generate houses on each foundation. 

    Cal's foundation class:
    - Arguments 
        1. location
        2. width
        3. depth (which is the same thing as width at the moment)
    - Attributes
        1. xstart (based on the player's position.x + 1)
        2. base (based on the player's position.y - 1)
        3. zstart (based on the player's position.z + 1)
        4. xend (based on the player's position.x + width + 1)
        5. zend (based on the player's position.z + depth + 1)
        6. width ( == foundationSize found in Max's class)
        7. depth ( == foundationSize found in Max's class)

    Max's foudnation class:
    - Arguments
        1. centerPoint
        2. size
        3. fId
    - Attributes
        1. id
        2. boundingBox (contains 4 vectors and the center vector)
        3. neightbours (not a necessary component for integration)

    How does Cal build his house?
    1. `prop = buildHouse.house_property(p,30,30)` first assigns location, width, and depth
    2.  `myHouse = buildHouse.house(prop,floorHeight,roomSize)` then generates a house instance with foundation passed as an argument
    3.  `myHouse.createFloor()` creates a floor
    4. 
    ```python
       myHouse.floors[0].addRoom(mc)
       myHouse.floors[0].addRoom(mc)
       myHouse.floors[0].addRoom(mc)
       myHouse.floors[0].addRoom(mc)
       myHouse.floors[0].addRoom(mc)
       myHouse.floors[0].addDoors(mc)
       myHouse.floors[0].addFrontDoor(mc)
       print('---------')
       myHouse.createFloor()
       myHouse.floors[1].addRoom(mc)
       myHouse.floors[1].addRoom(mc)
       myHouse.floors[1].addRoom(mc)
       myHouse.floors[1].addDoors(mc)
       
       myHouse.createFloor()
       myHouse.floors[2].addRoom(mc)
       myHouse.floors[2].addRoom(mc)
       myHouse.floors[2].addDoors(mc)
       
       myHouse.addAllStairs(mc)
    ``` 
    creates rooms, another floor, more rooms, and stairs.

    Cal's y-axis doesn't match up with Max's. Where is Cal's pointing to? player.pos.y - 1 Where is Max's pointing to? centerPoint.y. Cal's house doesn't populate with varying y-axes. His houses are all position at the same y-axis whereas Max's foundations vary in heights. 

    Cal's
    self.base refers to centerPoint.y. createEmptyFloor uses it to build a floor. Max's centerPoint.y axis gets set to the proper value not at the initialisation, but along the way. 

    Foundation() class picks a random x, z coordinate and assign it with centerPoint 

    The integration is now complete.

    ## Save and Load Blocks to build a dictionary of furniture

    Inspired by some students from our cohort, I've created scripts to write to a csv file information about the composition of any gob of blocks, in this case furniture. [save_blocks.py](foundation_generator/save_blocks.py) As a way to find out whether I can translate this information with Minecraft blocks, I have also written a script to place furniture saved in the form of rows in a csv file. You could try this script: [load_blocks.py](foundation_generator/load_blocks.py). My next job is to generate a random piece of furniture in a randomly selected room. 

    * PAs
      1. Identify threat sources
        * Cyber attack
	  2. Identify threat sources
	    * Power outage due to cyber attacks
	  3. Identify vulnerabilities and the conditions needed to exploit them
	    * No back up infrastructure in the case of power outage; lack of staff members to deal with the issue efficiently
	  4. Identify the likelihood such attacks would succeed
	    * Probably the assessed likelihood by the organisation is lower than it actually is in reality, and then only it falls victim to the attack, it realises the likelihood was a lot higher. How would you accurately access the likelihood in the case of a cyber attack?
	  5. Identify the potential impact
	    * The besmirched reputation of the organisation, and client dissatisfaction
	  6. Determine the risk posed
	    * Discontinuation of service
        
      7. My public IP address:
      8. What is the IP address of www.rmit.edu.au?
         54.79.75.6131.170.77.128
         
    ## Week 3

    ### Generate Furniture

    This is the last week before we need to submit our project. There are a few things we need to concentrate on to achieve the most ideal outcome.

    1. Connect the roads to foundations 
    2. Make a fenced-off swimming pool  
    3. Make sure a house's main door is visible from the road it is connected to
    4. Add some furniture in each room 

    I'm currently working on the number 4 task. We should be able to put some furniture in some of the rooms by early this week. 

    Change of a plan. I'm building roads

    Find a center point between foundations and extend roads to the point from each foundation so that its roads can meet at half point. Each instance of road class should have this center point as an attribute as well as its original start point. w



.....
.....
.....
