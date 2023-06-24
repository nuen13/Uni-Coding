import graphs
import digraphs
import csv


#------- Task 1 ----------# 
def gamesOK1(games):
   E = {(b, a) for (a, b) in games} | games #edges
   V = { u for (u, _) in E } #vertices 

   for p1 in V:
      for p2 in V:
         print(p1, p2)
         distance  = graphs.distance(V, E, p1, p2)
         if distance > 2 or distance == float('inf'):  return False
   return True

# print(gamesOK1({ ('Alice', 'Bob'), ('Bob', 'Charlie') }))



#---------- Task 2 ----------# 
import os
scriptDirectory = os.path.dirname(__file__)

# def potentialReferees(refereecsvfilename, player1, player2):
#    with open(refereecsvfilename, 'r') as csvfile:
#       reader = csv.reader(csvfile)
#       CL = [row for row in reader][1::] #conflict List

#    # print(CL)
#    V = {p for conflictRow in CL for p in conflictRow }
#    ref = {r[0] for r in CL}

#    conflictFile = {tuple(row) for row in CL}

#    E  = {(ref, p) for p in V for conflictSet in conflictFile for ref in conflictSet if p == conflictSet[0]}
#    return ref - graphs.NS(V, E, {player1, player2})

# def potentialReferees(refereecsvfilename, player1, player2):
#    with open(refereecsvfilename, 'r') as csvfile:
#       reader = csv.reader(csvfile)
#       CL = [row for row in reader][1::] #conflict List

#    # turn cl into set that contain tuples 
#    Cset = {tuple(row) for row in CL} #conflict set

#    ref = {r[0] for r in CL}

#    V = {p for conflictRow in Cset for p in conflictRow }
   
#    E  = {(ref, p) for p in V for Crow in Cset for ref in Crow if p == Crow[0]}
#    for a in E:
#       print(a)
#    return ref - graphs.NS(V, E, {player1, player2})
def potentialReferees(refereecsvfilename, player1, player2):
   with open(refereecsvfilename, 'r') as csvfile:
      reader = csv.reader(csvfile)
      Cset = {tuple(row) for row in reader}  #conflict List

   print (Cset)
   # # turn cl into set that contain tuples 

   # Cset = {tuple(row) for row in CL} #conflict set
   # ref = {r[0] for r in CL}

   # V = {p for conflictRow in Cset for p in conflictRow }

   # E  = {(p, r) for r in V for Crow in Cset for p in Crow if r == Crow[0]}

   # return ref - graphs.NS(V, E, {player1, player2})


print(potentialReferees( os.path.join(scriptDirectory, 'referees1.csv'), 'Alice', 'David') )

#---------- Task 3 ----------# 
def gameReferees(gamePotentialReferees):
   poRef = gamePotentialReferees

   refForGames = {(ref,pair) for pair in poRef for ref in poRef[pair]}
   E = {(pair,ref) for (ref,pair) in refForGames}| refForGames
   # for a in E: print("e", a)

   A = {p for p in poRef} # games (2 players)
   B = {r for p in poRef for r in poRef[p]} #refs 

   if len(A) != len(B): return None

   maxMatching = digraphs.maxMatching(A, B, E)
   refForMatch = {match[1]:match[0] for ref in B for match in maxMatching if ref == match[0]}

   return refForMatch 

print(gameReferees({ ('Joy', 'Jobu Tupaki'): { 'Deirdre', 'Gong Gong'},
             ('Waymond', 'Deirdre'): { 'Gong Gong', 'Jobu Tupaki' },
             ('Gong Gong', 'Joy'): { 'Deirdre', 'chad'}
             }
))





#---------- Task 4 ----------# 

def gameSchedule(assignedReferees):

   V = {(p[0], p[1], assignedReferees[p]) for p in assignedReferees} 
 
   #PS: possible Schedule
   PS = {(player1, player2) for player1 in V for player2 in V if player1 != player2}
   
   # edge when game that has same player(s)
   E = {gamesPair for gamesPair in PS for game1 in gamesPair[0] if game1 in gamesPair[1] }
   # for a in E:
   #    print(a)
   # [1] so it does not take the return length of the graph
   minColouring = graphs.minColouring(V,E)[1]

   # return it in the correct format
   gameScheduleNno = {}
   for match, matchNo in minColouring.items():
      gameScheduleNno[matchNo] = [match] if matchNo not in gameScheduleNno.keys() else gameScheduleNno[matchNo] + [match]
   gameSchedule = [set(gameScheduleNno[match]) for match in gameScheduleNno]

   return gameSchedule


# gameSchedule({ 
#       ('Alice', 'Bob'): 'Rene', 
#       ('Elaine', 'Charlie'): 'Dave',
#       ('Rene', 'Elaine'): 'Alice',
#       ('Dave', 'Bob'): 'Charlie',
#       ('Alice', 'Rene'): 'Dave',
#       ('Dave', 'Elaine'): 'Rene'
#    })


#---------- Task 5 ----------# 
def ranking(games):
   V = {player for pair in games for player in pair}
   print(V)
   E = games
   for a in E: print(a)
   return digraphs.topOrdering(V, E)

# print(ranking({ 
#       ('E', 'T'),
#       ('E', 'W'),
#       ('E', 'G'),
#       ('E', 'J'),
#       ('J', 'G'),
#       ('W', 'J'),
#       ('T', 'J'),
#       ('Z', 'L') }))