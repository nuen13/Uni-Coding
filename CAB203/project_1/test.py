import graphs
import digraphs
import csv

# V -> Vertices
# E -> Edges 
# A, B -> Vertice "A", Vertice "B"

def gamesOK(games):
   V = {player for pair in games for player in pair}
   fullCasePlayer = {players[::-1] for players in games} | games
   for player in games: 
      for p in V: 
         x = graphs.distance(V, fullCasePlayer, player[0], p)
         if x > 2 or x == float('inf'): 
            return False
   return True

import os
scriptDirectory = os.path.dirname(__file__)


def potentialReferees(refereecsvfilename, player1, player2):
   with open(refereecsvfilename, 'r') as csvfile:
      reader = csv.reader(csvfile)
      players = [row for row in reader][1::]

   V = {r[0] for r in players}
   A = set()
   for row in players: 
      row = tuple(row)
      A.add(row)

   E  = {(row, v) for v in V for players in A for row in players if v == players[0]}
   S = {player1, player2}
   return V - graphs.NS(V, E, S)

potentialReferees( os.path.join(scriptDirectory, 'referees1.csv'), 'Ashley', 'Douglas')




def gameReferees(gamePotentialReferees):
   poRef = gamePotentialReferees

   refForEach ={(ref,pair) for pair in poRef for ref in poRef[pair]}
   refFull = {p[::-1] for p in refForEach} | refForEach

   
 
   pair = {p for p in poRef}
   refs = {r for p in poRef for r in poRef[p]}

   y = digraphs.maxMatching(pair, refs, refFull)

   refForMatch = {match[1]:match[0] for ref in refs for match in y if ref == match[0]}

   if len(refForMatch) != len(poRef): return None
   for player in refForMatch: 
      if refForMatch[player] == set(): return None
   return refForMatch


gameReferees({ ('Joy', 'Jobu Tupaki'): { 'Deirdre', 'Gong Gong' },
             ('Waymond', 'Deirdre'): { 'Gong Gong', 'Jobu Tupaki' },
             ('Gong Gong', 'Joy'): { 'Deirdre' }
             })

def gameSchedule(assignedReferees):

   V = {(pair[0], pair[1], assignedReferees[pair]) for pair in assignedReferees}
   possiblePair = {(player1, player2) for player1 in V for player2 in V if player1 != player2}
   E = {players for players in possiblePair for player1 in players[0] if player1 in players[1] }


   matchingMatch = graphs.minColouring(V,E)[1]
   gameScheduleNno = {}
   for match, matchNo in matchingMatch.items():
      gameScheduleNno[matchNo] = [match] if matchNo not in gameScheduleNno.keys() else gameScheduleNno[matchNo] + [match]

   gameSchedule = [set(gameScheduleNno[match]) for match in gameScheduleNno]

   return gameSchedule

def ranking(games):
   return digraphs.topOrdering({player for pair in games for player in pair}, games)