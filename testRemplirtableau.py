#laisser l'utilisateur rentrer son taquin :
plateauI = []
plateauJ = []
plateauL = []
plateauTotal = []
elemList = []
def remplir_taquin_user():
    while len(elemList) < 9:
        a = input("Tapez un num que vous voulez (jamais rentré) : ")
        # On convertit l'entrée
        try:
            b = int(a)
        except ValueError or a in elemList :
            print("Vous n'avez pas saisi de nombre ou le nombre à déjà été saisi")
            continue
        if len(elemList) < 3:
            if b not in elemList:
                plateauI.append(b)
                elemList.append(b)
        elif len(elemList) ==  3 or len(elemList) < 6 :
            if b not in elemList:
                plateauJ.append(b)
                elemList.append(b)
        elif len(elemList) ==  6 or len(elemList) < 9 :
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
        print(plateauTotal)


remplir_taquin_user()