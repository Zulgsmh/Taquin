# -*-coding:Latin-1 -*  #permet d'accepter les accent pour les commentaires

import random     #permet de générer un taquin aléatoire
import itertools   #permet d'utiliser itertools.product()
import collections   #permet d'utiliser deque() pour faciliter les ajouts et sorties à chaque extremité
import time   #permet de récupérer le temps d'exécution

"""
Ensembles des variables globales utilisées pour les statistiques.
"""
nb_iterations = 0
liste_h1 = []
liste_h2 = []
liste_h3 = []
liste_h4 = []
liste_h5 = []
liste_h6 = []

class Node:
    """
    Classe d'un noeud
    - taquin est un instance de taquin s'il y en à un
    - parent est le noeud précédent celui généré par la classe solver s'il y en à un
    - action est l'action permettant de créer le nouveau taquin si'l y en avait déjà un
    """
    def __init__(self, taquin, parent=None, action=None):
        self.taquin = taquin
        self.parent = parent
        self.action = action
        #incrémente de 1 le numéro du noeud
        if (self.parent != None):
            self.g = parent.g + 1
        #initialise le premier noeud à 0
        else:
            self.g = 0

    #définit le score
    # g = le numéro du noeud qui commence à 0 pour le taquin généré
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
        recréer le chemin depuis le chemin root 'parent'
        """
        node, p = self, []
        while node:
            p.append(node)
            node = node.parent
        yield from reversed(p)

    @property
    def resolu(self):
        """ permet de vérifier si le taquin est résolu ou non """
        return self.taquin.resolu

    @property
    def actions(self):
        """ donne les action possibles pour l'état donné """
        return self.taquin.actions

    @property
    def h(self):
        """"h représente la distance de manhattan"""
        return self.taquin.heuristiques

    @property
    def f(self):
        """"représente le score vue précédemment, distance manhattan + numéro du noeud"""
        return self.h + self.g

    def __str__(self):
        return str(self.taquin)

#-------------------------------------Classe pour résoudre---------------------------------------


class Solver:
    """
    classe permettant de résoudre le taquin
    - 'start' est une  instance de taquin
    """
    def __init__(self, start):
        self.start = start

    def resoudre(self):
        """
        utilse le parcours en largeur et retourne le chemin
        vers la solution si il existe.
        """
        #crée la root du noeud
        #collections.deque est un conteneur comme une liste qui permet
        # des ajouts et des retraits rapides à chaque extremité
        queue = collections.deque([Node(self.start)])
        #vu représente les noeuds déjà croisés
        vu = set()
        vu.add(queue[0].state)
        while queue:
            #le noeud qui ressort dépend du score (h+g vu précédemment),
            queue = collections.deque(sorted(list(queue), key=lambda node: node.f))
            # on prend le score le plus faible pour se rapprocher du but avec un score de 0
            node = queue.popleft()
            #on vérifie s'il est égal à l'état du but c'est à dire le taquin = [1,2,3,4,5,6,7,8,0]
            if node.resolu:
                return node.chemin

            #si ce n'est pas l'état du but on regarde les différents noeuds enfants possibles
            # en faisant toutes les directions ( haut, bas, gauche, droite)
            for deplacement, action in node.actions:
                child = Node(deplacement(), node, action)

                if child.state not in vu:
                    #on ajoute le noeud enfant à la queue
                    queue.appendleft(child)
                    vu.add(child.state)

#-------------------------------------Classe pour créer le taquin---------------------------------------


class Taquin:
    """
    classe représentant le taquin.
    - 'plateau' est une liste à deux dimensions
    """
    def __init__(self, plateau):
        self.width = len(plateau[0])
        self.plateau = plateau

    @property
    def resolu(self):
        """
        Le taquin est resolu si les chiffres sont dans l'ordre croissant et si
        le 0 est à la fin du plateau
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
        #itertools.product = boucle for imbriqué avec en parametre a,b
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

    @property
    def heuristiques(self):
        """
        Calcul des heuristiques.
        """
        global nb_iterations
        global liste_h1
        global liste_h2
        global liste_h3
        global liste_h4
        global liste_h5
        global liste_h6

        # détection des tuiles du taquin.
        for ligne in range(3):
            for colonne in range(3):
                if self.plateau[ligne][colonne] == 1:
                    x_a, y_a = divmod(self.plateau[ligne][colonne] - 1, 3)
                    dist_a = abs(x_a - ligne) + abs(y_a - colonne)
                elif self.plateau[ligne][colonne] == 2:
                    x_b, y_b = divmod(self.plateau[ligne][colonne] - 1, 3)
                    dist_b = abs(x_b - ligne) + abs(y_b - colonne)
                elif self.plateau[ligne][colonne] == 3:
                    x_c, y_c = divmod(self.plateau[ligne][colonne] - 1, 3)
                    dist_c = abs(x_c - ligne) + abs(y_c - colonne)
                elif self.plateau[ligne][colonne] == 4:
                    x_d, y_d = divmod(self.plateau[ligne][colonne] - 1, 3)
                    dist_d = abs(x_d - ligne) + abs(y_d - colonne)
                elif self.plateau[ligne][colonne] == 5:
                    x_e, y_e = divmod(self.plateau[ligne][colonne] - 1, 3)
                    dist_e = abs(x_e - ligne) + abs(y_e - colonne)
                elif self.plateau[ligne][colonne] == 6:
                    x_f, y_f = divmod(self.plateau[ligne][colonne] - 1, 3)
                    dist_f = abs(x_f - ligne) + abs(y_f - colonne)
                elif self.plateau[ligne][colonne] == 7:
                    x_g, y_g = divmod(self.plateau[ligne][colonne] - 1, 3)
                    dist_g = abs(x_g - ligne) + abs(y_g - colonne)
                elif self.plateau[ligne][colonne] == 8:
                    x_i, y_i = divmod(self.plateau[ligne][colonne] - 1, 3)
                    dist_i = abs(x_i - ligne) + abs(y_i - colonne)

        # calcul de h1.
        h1 = abs(((dist_a * 36) + (dist_b * 12) + (dist_c * 12) + (dist_d * 4) + (dist_e * 1) + (dist_f * 1) +
                  (dist_g * 4) + (dist_i * 1)) / 4)
        liste_h1.append(h1)
        h_efficace = h1

        # calcul de h2.
        h2 = abs((dist_a * 8) + (dist_b * 7) + (dist_c * 6) + (dist_d * 5) + (dist_e * 4) + (dist_f * 3) +
                 (dist_g * 2) + (dist_i * 1))
        liste_h2.append(h2)
        if h_efficace > h2:
            h_efficace = h2

        # calcul de h3.
        h3 = abs(((dist_a * 8) + (dist_b * 7) + (dist_c * 6) + (dist_d * 5) + (dist_e * 4) + (dist_f * 3) +
                  (dist_g * 2) + (dist_i * 1)) / 4)
        liste_h3.append(h3)
        if h_efficace > h3:
            h_efficace = h3

        # calcul de h4.
        h4 = abs((dist_a * 8) + (dist_b * 7) + (dist_c * 6) + (dist_d * 5) + (dist_e * 3) + (dist_f * 2) +
                 (dist_g * 4) + (dist_i * 1))
        liste_h4.append(h4)
        if h_efficace > h4:
            h_efficace = h4

        # calcul de h5.
        h5 = abs(((dist_a * 8) + (dist_b * 7) + (dist_c * 6) + (dist_d * 5) + (dist_e * 3) + (dist_f * 2) +
                  (dist_g * 4) + (dist_i * 1)) / 4)
        liste_h5.append(h5)
        if h_efficace > h5:
            h_efficace = h5

        # calcul de h6.
        h6 = self.manhattan
        liste_h6.append(h6)
        if h_efficace > h6:
            h_efficace = h6

        nb_iterations += 1
        return h_efficace



    def shuffle(self):
        """
        Return un taquin mélangé avec 1000 déplacements aléatoires dans la liste
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
        Return un nouveau taquin ou 'at' et 'to' tiles ont été échangés.
        tous les deplacements sont des actions
        """
        copy = self.copy()
        #position actuelle
        i, j = at
        #position après échange
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
    """ - Permet à l'utilisateur de rentrer le taquin qu'il souhaite."""
    """ - Si le taquin rentré à un niveau de mélange impair il sera impossible à résoudre."""
    """ - La case X doit être remplacée par 0. """

    print("Rentrez les chiffres de 0 à 8 dans l'odre que vous souhaitez.")
    while len(elemList) < 9:
        a = input("Tapez le chiffre que vous voulez (un que vous n'avez jamais rentré) : ")
        # On convertit l'entrée
        try:
            b = int(a)
            if b < 0:
                print("Vous ne pouvez pas rentrer de valeur négative")
                continue
            elif b in elemList:
                print("Le nombre à déjà été saisi")
                continue
            elif b > 8:
                print("Votre valeur doit être comprise entre 0 et 8 compris")
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
print("Ici, le '0' représente le trou !")
repUser = input("Souhaitez-vous créer votre taquin (o/n) ? ")
#repUser = "n"
if repUser == "o" or repUser == "O":
    print("A vous de créer votre taquin !")
    automatique = False
    remplir_taquin_user()
    # on créer un objet taquin auquel on donne le plateau créé
    taquin = Taquin(plateauTotal)

elif repUser == "n" or repUser == "N" or repUser == "":
    print("Pas de problème, on en créer un automatiquement pour vous !")
    #on initialise un plateau aléatoire à deux dimensions
    plateau = [[0,1,2],[3,4,5],[6,7,8]]
    # on créer un objet taquin auquel on donne le plateau créé
    taquin = Taquin(plateau)
    # on appelle la methode shuffle de la classe taquin pour le melanger si on le souhaite
    taquin = taquin.shuffle()


#on créé un objet solver à qui on donne le taquin qui va résoudre celui-ci
s = Solver(taquin)
#variable qui récupère le temps au lancement
time1 = time.perf_counter()
#on résoud le taquin
p = s.resoudre()
#variable qui récupère le temps après la résolution
time2 = time.perf_counter()
#compte le nombre d'étapes (à -1 pour éviter de compter l'état initial)
etapes = -1

#on incrémente le nombre d'étape à chaque noeud
premierDeplacement = True
for node in p:
    if premierDeplacement:
        print("Aucun déplacement à l'initialisation.")
        node.taquin.afficher()
        etapes += 1
        premierDeplacement = False
    else:
        print(" Deplacement vers : ", node.action)
        node.taquin.afficher()
        etapes += 1

#on affiche le nombre d'étapes et le temps de recherche
print("Nombre d'étape(s) : " + str(etapes))
print("Nombre d'itérations: "+ str(nb_iterations))
print("Temps de recherche : " + str(time2 - time1) + " second(s)")


"""
print("Liste des heuristiques calculées:")
print("h1: ", liste_h1)
print("h2: ", liste_h2)
print("h3: ", liste_h3)
print("h4: ", liste_h4)
print("h5: ", liste_h5)
print("h6: ", liste_h6)
"""