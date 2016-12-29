#Let us assume that there are five houses of different colors next to each other on the same road. 
#In each house lives a man of a different nationality. 
# Every man has his favorite drink, his favorite brand of cigarettes, and keeps pets of a particular kind.
    #The Englishman lives in the red house.
    #The Swede keeps dogs.
    #The Dane drinks tea.
    #The green house is just to the left of the white one.
    #The owner of the green house drinks coffee.
    #The Pall Mall smoker keeps birds.
    #The owner of the yellow house smokes Dunhills.
    #The man in the center house drinks milk.
    #The Norwegian lives in the first house.
    #The Blend smoker has a neighbor who keeps cats.
    #The man who smokes Blue Masters drinks beer.
    #The man who keeps horses lives next to the Dunhill smoker.
    #The German smokes Prince.
    #The Norwegian lives next to the blue house.
    #The Blend smoker has a neighbor who drinks water.

#The question to be answered is: Who keeps fish?

from CSPmain import *

P = Graph()

# The problem is modelled with 25 variables storing the house number of a property
domain = {1,2,3,4,5}
P.new_node("english",domain)
P.new_node("swede",domain)
P.new_node("dane",domain)
P.new_node("norwegian",domain)
P.new_node("german",domain)

P.new_node("red",domain)
P.new_node("white",domain)
P.new_node("blue",domain)
P.new_node("yellow",domain)
P.new_node("green",domain)

P.new_node("fish",domain)
P.new_node("cats",domain)
P.new_node("birds",domain)
P.new_node("dog",domain)
P.new_node("horses",domain)

P.new_node("tea",domain)
P.new_node("coffee",domain)
P.new_node("milk",domain)
P.new_node("beer",domain)
P.new_node("water",domain)

P.new_node("pall",domain)
P.new_node("dunhill",domain)
P.new_node("blend",domain)
P.new_node("master",domain)
P.new_node("prince",domain)

# "every one has a different .... "
def diff(x,y) : return x != y
P.new_constraint(diff,["english","german","dane","swede","norwegian"],"mutual")
P.new_constraint(diff,["green","yellow","white","blue","red"],"mutual")
P.new_constraint(diff,["water","beer","tea","coffee","milk"],"mutual")
P.new_constraint(diff,["pall","dunhill","blend","master","prince"],"mutual")
P.new_constraint(diff,["fish","cats","birds","dog","horses"],"mutual")

def idd(x,y) : return x==y
P.new_constraint(idd, ["english", "red"],"mutual")
P.new_constraint(idd, ["swede", "dog"],"mutual")
P.new_constraint(idd, ["dane", "tea"],"mutual")
P.new_constraint(idd, ["german", "prince"],"mutual")
P.new_constraint(idd, ["green", "coffee"],"mutual")
P.new_constraint(idd, ["master", "beer"],"mutual")
P.new_constraint(idd, ["yellow", "dunhill"],"mutual")
P.new_constraint(idd, ["pall", "birds"],"mutual")

def left_of(x,y) : return x == y-1
P.new_constraint(left_of, ["green", "white"])

# directly given constraints
P.set_value("milk",3)
P.set_value("norwegian",1)

def neighbour(x,y) : return abs(x-y)==1
P.new_constraint(neighbour, ["cats", "blend"],"mutual")
P.new_constraint(neighbour, ["horses", "dunhill"],"mutual")
P.new_constraint(neighbour, ["norwegian", "blue"],"mutual")
P.new_constraint(neighbour, ["blend", "water"],"mutual")

# initialize solver
X = Solver(P)
X.search_solution()
X.display_solution()

