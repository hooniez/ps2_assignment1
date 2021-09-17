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
    - [x] Read chapter 1 & 2 on textbook 📖
    - [x] Setup VS Code, and Minecraft on my Mac 🆚
    - [x] Implemented Hello Minecraft! 🎮
    - [ ] <!-- Built a foundation generator -->
    
    * PAs
      - Convert the binary number 10101 to decimal: 21
      - Convert the hexadecimal number 3E to decimal: 62
      - Convert the binary number 1101001010111111 to hexadecimal: d2bf
      - Convert the decimal number 39 to binary: 100111
      - Convert the decimal number 63 to hexadecimal: 3f
      - [Stairway](Myeonghoon%20Sun's%20PAs/staircase.py)    


**Week 2**

* Myeonghoon Sun
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
    ```
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
    ``` creates rooms, another floor, more rooms, and stairs.

    Cal's y-axis doesn't match up with Max's. Where is Cal's pointing to? player.pos.y - 1 Where is Max's pointing to? centerPoint.y. Cal's house doesn't populate with varying y-axes. His houses are all position at the same y-axis whereas Max's foundations vary in heights. 

    Cal's
    self.base refers to centerPoint.y. createEmptyFloor uses it to build a floor. Max's centerPoint.y axis gets set to the proper value not at the initialisation, but along the way. 

    Foundation() class picks a random x, z coordinate and assign it with centerPoint 
    
       




.....
.....

**Week 3**

.....
.....
.....
