# -*-coding:Latin-1 -*  #permet d'accepter les accent pour les commentaires

import random     #permet de g�n�rer un taquin al�atoire
import itertools   #permet d'utiliser itertools.product()
import collections   #permet d'utiliser deque() pour faciliter les ajouts et sorties � chaque extremit�
import time   #permet de r�cup�rer le temps d'ex�cution

class Node:
    """
    Classe d'un noeud
    - taquin est un instance de taquin s'il y en � un
    - parent est le noeud pr�c�dent celui g�n�r� par la classe solver s'il y en � un
    - action est l'action permettant de cr�er le nouveau taquin si'l y en avait d�j� un
    """
    def __init__(self, taquin, parent=None, action=None):
        self.taquin = taquin
        self.parent = parent
        self.action = action
        #incr�mente de 1 le num�ro du noeud
        if (self.parent != None):
            self.g = parent.g + 1
        #initialise le premier noeud � 0
        else:
            self.g = 0

    #d�finit le score
    # g = le num�ro du noeud qui commence � 0 pour le taquin g�n�r�
    # h = distance de manhattan qui est la distance entre la mauvaise place d'un chiffre et sa bonne place
    @property
    def score(self):
        return self.g + self.h

    @property
    def state(self):
        """
        return une representation string de self
        """
        return str(self)

    @property
    def chemin(self):
        """
        recr�er le chemin depuis le chemin root 'parent'
        """
        node, p = self, []
        while node:
            p.append(node)
            node = node.parent
        yield from reversed(p)

    @property
    def resolu(self):
        """ permet de v�rifier si le taquin est r�solu ou non """
        return self.taquin.resolu

    @property
    def actions(self):
        """ donne les action possibles pour l'�tat donn� """
        return self.taquin.actions

    @property
    def h(self):
        """"h repr�sente la distance de manhattan"""
        return self.taquin.manhattan

    @property
    def f(self):
        """"repr�sente le score vue pr�c�demment, distance manhattan + num�ro du noeud"""
        return self.h + self.g

    def __str__(self):
        return str(self.taquin)

#-------------------------------------Classe pour r�soudre---------------------------------------


class Solver:
    """
    classe permettant de r�soudre le taquin
    - 'start' est une  instance de taquin
    """
    def __init__(self, start):
        self.start = start

    def resoudre(self):
        """
        utilse le parcours en largeur et retourne le chemin
        vers la solution si il existe.
        """
        #cr�e la root du noeud
        #collections.deque est un conteneur comme une liste qui permet
        # des ajouts et des retraits rapides � chaque extremit�
        queue = collections.deque([Node(self.start)])
        #vu repr�sente les noeuds d�j� crois�s
        vu = set()
        vu.add(queue[0].state)
        while queue:
            #le noeud qui ressort d�pend du score (h+g vu pr�c�demment),
            queue = collections.deque(sorted(list(queue), key=lambda node: node.f))
            # on prend le score le plus faible pour se rapprocher du but avec un score de 0
            node = queue.popleft()
            #on v�rifie s'il est �gal � l'�tat du but c'est � dire le taquin = [1,2,3,4,5,6,7,8,0]
            if node.resolu:
                return node.chemin

            #si ce n'est pas l'�tat du but on regarde les diff�rents noeuds enfants possibles
            # en faisant toutes les directions ( haut, bas, gauche, droite)
            for deplacement, action in node.actions:
                child = Node(deplacement(), node, action)

                if child.state not in vu:
                    #on ajoute le noeud enfant � la queue
                    queue.appendleft(child)
                    vu.add(child.state)

#-------------------------------------Classe pour cr�er le taquin---------------------------------------


class Taquin:
    """
    classe repr�sentant le taquin.
    - 'plateau' est une liste � deux dimensions
    """
    def __init__(self, plateau):
        self.width = len(plateau[0])
        self.plateau = plateau

    @property
    def resolu(self):
        """
        Le taquin est resolu si les chiffres sont dans l'ordre croissant et si
        le 0 est � la fin du plateau
        """
        N = self.width * self.width
        return str(self) == ''.join(map(str, range(1,N))) + '0'

    @property
    def actions(self):
        """
        return une liste de deplacements et actions . 'deplacement' can be called
        to return a new taquin that results in sliding the '0' tile in
        the direction of 'action'.
        """
        def create_move(de, vers):
            return lambda: self._move(de, vers)

        deplacements = []
        #itertools.product = boucle for imbriqu� avec en parametre a,b
        # ici la longueur et la largeur du tableau
        for i, j in itertools.product(range(self.width),
                                      range(self.width)):
            #D : droite , G : gauche , B : bas , H : haut.
            directions = {'La gauche':(i, j-1),
                          'La droite':(i, j+1),
                          'Le haut':(i-1, j),
                          'Le bas':(i+1, j)}

            for action, (r, c) in directions.items():
                if r >= 0 and c >= 0 and r < self.width and c < self.width and \
                   self.plateau[r][c] == 0:
                    deplacement = create_move((i,j), (r,c)), action
                    deplacements.append(deplacement)
        return deplacements

    @property
    def manhattan(self):
        """
        Calcul des distances de manhattan
        """
        distance = 0
        for i in range(3):
            for j in range(3):
                if self.plateau[i][j] != 0:
                    x, y = divmod(self.plateau[i][j]-1, 3)
                    distance += abs(x - i) + abs(y - j)
        return distance

    def shuffle(self):
        """
        Return un taquin m�lang� avec 1000 d�placements al�atoires dans la liste
        """
        taquin = self
        for _ in range(1000):
            taquin = random.choice(taquin.actions)[0]()
        return taquin

    def copy(self):
        """
        return un taquin avec le meme plateau que dans le self
        """
        plateau = []
        for row in self.plateau:
            plateau.append([x for x in row])
        return Taquin(plateau)

    def _move(self, at, to):
        """
        Return un nouveau taquin ou 'at' et 'to' tiles ont �t� �chang�s.
        tous les deplacements sont des actions
        """
        copy = self.copy()
        #position actuelle
        i, j = at
        #position apr�s �change
        r, c = to
        copy.plateau[i][j], copy.plateau[r][c] = copy.plateau[r][c], copy.plateau[i][j]
        return copy

    def afficher(self):
        for row in self.plateau:
            print(row)
        print()

    def __str__(self):
        return ''.join(map(str, self))

    def __iter__(self):
        for row in self.plateau:
            yield from row


#-------------------Test du jeu-----------------------------

#laisser l'utilisateur rentrer son taquin :
plateauI = []
plateauJ = []
plateauL = []
plateauTotal = []
elemList = []


def remplir_taquin_user():
    """ - Permet � l'utilisateur de rentrer le taquin qu'il souhaite."""
    """ - Si le taquin rentr� � un niveau de m�lange impair il sera impossible � r�soudre."""
    """ - La case X doit �tre remplac�e par 0. """

    print("Rentrez les chiffres de 0 � 8 dans l'odre que vous souhaitez.")
    while len(elemList) < 9:
        a = input("Tapez le chiffre que vous voulez (un que vous n'avez jamais rentr�) : ")
        # On convertit l'entr�e
        try:
            b = int(a)
            if b < 0:
                print("Vous ne pouvez pas rentrer de valeur n�gative")
                continue
            elif b in elemList:
                print("Le nombre � d�j� �t� saisi")
                continue
            elif b > 8:
                print("Votre valeur doit �tre comprise entre 0 et 8 compris")
                continue
        except ValueError:
            print("Ce n'est pas un chiffre")
            continue

        if len(elemList) < 3:
            if b not in elemList:
                plateauI.append(b)
                elemList.append(b)
        elif len(elemList) == 3 or len(elemList) < 6:
            if b not in elemList:
                plateauJ.append(b)
                elemList.append(b)
        elif len(elemList) == 6 or len(elemList) < 9:
            if b not in elemList:
                plateauL.append(b)
                elemList.append(b)
        if len(elemList) == 9:
            plateauTotal.append(plateauI)
            plateauTotal.append(plateauJ)
            plateauTotal.append(plateauL)
        print(plateauI)
        print(plateauJ)
        print(plateauL)


automatique = True
print("Bienvenue dans le jeu du taquin !")
repUser = input("Souhaitez-vous cr�er votre taquin (o/n) ? ")
if repUser == "o" or repUser == "O":
    print("A vous de cr�er votre taquin !")
    automatique = False
    remplir_taquin_user()
    # on cr�er un objet taquin auquel on donne le plateau cr��
    taquin = Taquin(plateauTotal)

elif repUser == "n" or repUser == "N" or repUser == "":
    print("Pas de probl�me, on en cr�er un automatiquement pour vous !")
    #on initialise un plateau al�atoire � deux dimensions
    plateau = [[0,1,2],[3,4,5],[6,7,8]]
    # on cr�er un objet taquin auquel on donne le plateau cr��
    taquin = Taquin(plateau)
    # on appelle la methode shuffle de la classe taquin pour le melanger si on le souhaite
    taquin = taquin.shuffle()


#on cr�� un objet solver � qui on donne le taquin qui va r�soudre celui-ci
s = Solver(taquin)
#variable qui r�cup�re le temps au lancement
time1 = time.perf_counter()
#on r�soud le taquin
p = s.resoudre()
#variable qui r�cup�re le temps apr�s la r�solution
time2 = time.perf_counter()
#compte le nombre d'�tapes
etapes = 0

#on incr�mente le nombre d'�tape � chaque noeud
premierDeplacement = True
for node in p:
    if premierDeplacement:
        print("Aucun d�placement � l'initialisation.")
        node.taquin.afficher()
        etapes += 1
        premierDeplacement = False
    else:
        print(" Deplacement vers : ", node.action)
        node.taquin.afficher()
        etapes += 1

#on affiche le nombre d'�tapes et le temps de recherche
print("Nombre d'�tape(s) : " + str(etapes))
print("Temps de recherche : " + str(time2 - time1) + " second(s)")