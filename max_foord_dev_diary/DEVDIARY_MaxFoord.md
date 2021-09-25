## Week 1:
the initial solution to the foundation generator was taking approx 1 min to generate all the foundations which needed to be improved
	the main issue was coordinates were being generated randomly and then checked  against  the list of created points
	the loop would run until all coordinates were generated, meaning that there was no guarunteed maximum run time (outside of all points being checked)

there were 2 differing ideas one how to solve the problem so the decision was taken to develop both so that if one didn't work we had a back up
* solution1 - set the foundations to a  grid
* solution2 - generate a random sample  of x values with a minimum dist between them,  then match them to random z values to give the village a more random  feel


I was developing solution 2:
	the main problem to solve for this solution was to ensure that any foundation that had close x values,  had differing z values.
	this was acheived by checking every second x value and if they fell within the minimum distance 

	I also created an enum for cardinal direction that makes the calculation and comparisons alot less  cumbersome
	this will assist down the line for determining the start direction of the required paths

	the run time for foundation generation with this solution was reduced from 1min to 6 seconds, allowing for the testing of the paths to be alot quicker


## Week 2:
now impletementing a path from each foundation to at least 1 other foundation

in order to connect the paths to each other 
I think the best way to implement it is to loop through the foundations and find the closest centerpoint with pythagora's theorem.
once the closest foundation is found, the pair are added to each others adjecency lists and the closest foundation is removed from the remaining list

this can be seen in the [groupProximalFoundations](maxsFoundations/village.py) function found in the village class

once the adjacency lists are generated they are run through the path class to generate the paths from one foundation to another

for each pair of foundations a route plan is generated that calulates the required starting side of the foundation using the [getPathPoint](maxsFoundations/foundation.py) function in the foundation class

one problem I had with creating the paths was avoiding creating paths from an adjacency list 
	as for each foundation A and it's neighbour B, there would be 2 paths created

to avoid this, for each path created, 2 tuples  are added to a list with both combinations of the 2 foundation ids
any subsequent path that  is created is checked against this list, and only generated if it does not already exist in the list




after adding code to add stairs the paths no longer work properly - especially the direction that is halved
the staircase code works as expected on its own, so I think the bug lays within the path layer function


to resolve this I am adding a route planner function 
that will use the class Pathpoint to create a list of start and end points and whether stairs are required
this should make it easier to debug, and allows the pathlayer function to only lay the path instead of worrying about the current  position


the start and end points of the path are then fed into a [PathPlan](maxsFoundations/pathPlan.py)
the pathplan splits the initial distance (whether that be the xdistance or the z distance) in half, then traveling the full distance for the other direction
finishing up with the second half of the initial distance. Creating a zigzag 'Z' shape to  reach the foundation

one thing to note is the potential issue for paths to run over the top of other foundations on the  way to it's destination, which may causes issues


## Week 3:
we decided as a group today that we will go with hoonie's approach, as it was simpler and some hurdles for my approach was looking as though it was going to
exceed the time we had left to complete the assignment

	the main issue with my solution was that due to the random nature of the foundation in the x, z dimensions
	having a path that did not overlap any of the other foundations proved harder to implement as noted earlier

	Hoonie's approach creates  foundations on a grid, which guaruntees that the paths will not overlap the foundation and enforces that the foundations will always have the same orientation to each other
	this made implementing the paths a lot quicker as no path finding was required


I'm now intergrating the 2 features of our code together by ensuring that houses are added to the foundations
the main bug was the  foundation wrapper list in the village class was incorrectly labeled as it actually  contained a list of  the row lists of  wrappers

the foudations and the houses have been adapted to work with each other, however there is some remnant code for testing and idividual dev that can be cleaned up, as they are no longer required for function


spent a few hours on a group call debugging the final pieces of code:
paths that didnt have enough distance between them to cover the height change were only drawing half of the path
so I added a check that will not draw the path at all as the foundation should already be connected to other path


Cal and I came up with a way to ensure that the front doors are  not facing the outside of the village grid by passing the corner priority for each of the houses as they  are created
