def Coredraw(scale_method, *waarden):
    "0 voor gelijk houden; null; 1; 2; 3; 1,2; 1,3; 2,3'"
    #translatie (.5 ; .5), dus middelpunt gelijkzijdige driehoek
    if scale_method == 0:
        scale = 300 / waarden[7]
    else:
        scale = scale_method

    import tkinter as tk
    root = tk.Tk()
    width_ = waarden[7] * 3**.5 * scale + 5
    height_ = 1.5 * waarden[7] * scale + 5
    w = tk.Canvas(root, width = width_, height = height_)
    w.pack()
    ez = (0, -scale)
    ey = (.5 * scale * 3**.5, .5 * scale)
    ex = (-.5 * scale * 3**.5, .5 * scale)

    def drawline(coords1, coords2, **kwargs):
        w.create_line(.5 * width_ + coords1[0] * ex[0] + coords1[1] * ey[0] + coords1[2] * ez[0],
                     2/3 * height_ + coords1[0] * ex[1] + coords1[1] * ey[1] + coords1[2] * ez[1],
                     .5 * width_ + coords2[0] * ex[0] + coords2[1] * ey[0] + coords2[2] * ez[0],
                     2/3 * height_ + coords2[0] * ex[1] + coords2[1] * ey[1] + coords2[2] * ez[1],
                     **kwargs)
    drawline( (0,0,waarden[7]), (0,waarden[7],0) )
    drawline( (waarden[1],0,waarden[7] - waarden[1]), (waarden[1], waarden[7] - waarden[1], 0) )
    drawline( (waarden[7] - waarden[6], 0, waarden[6]), (waarden[7] - waarden[6], waarden[6], 0), dash=(12,6), fill='red' )

    drawline( (0,0,waarden[7]), (waarden[7],0,0) )
    drawline( (0, waarden[2], waarden[7] - waarden[2]), (waarden[7] - waarden[2], waarden[2], 0) )
    drawline( (0,waarden[7] - waarden[5], waarden[5]), (waarden[5], waarden[7] - waarden[5], 0), dash=(12,6), fill='red' )

    drawline( (waarden[7],0,0), (0,waarden[7],0) )
    drawline( (waarden[7] - waarden[3],0,waarden[3]), (0,waarden[7] - waarden[3],waarden[3]) )
    drawline( (waarden[4], 0, waarden[7] - waarden[4]), (0, waarden[4], waarden[7] - waarden[4]), dash=(12,6), fill='red' )
    def drawcircle(coords1, **kwargs):
        x = .5 * width_ + coords1[0] * ex[0] + coords1[1] * ey[0] + coords1[2] * ez[0]
        y = 2/3 * height_ + coords1[0] * ex[1] + coords1[1] * ey[1] + coords1[2] * ez[1]
        w.create_oval(x-1, y-1, x+1, y+1, **kwargs)
    drawcircle(tuple(Shapley(3,*waarden)),outline='red')
    drawcircle(nucleolus(3,*waarden)[1:4],outline='green')
    
    tk.mainloop()
    
#Coredraw(20,0,1,3,4,4,5,8,10)

def Shapley(N, *waarden):
    from itertools import combinations
    from math import factorial
    coalities = [list(x) for i in range(N+1) for x in combinations(range(1,N+1),i)]
    teller = [factorial(len(x)) * factorial(N - len(x) - 1) for x in coalities if not 1 in x]
    noemer = factorial(N)
    sommatie = [[x for x in coalities if i not in x] for i in range(1,N+1)]
    result = []
    for i in range(1,N + 1):
        shapley = 0
        for j in range(len(teller)):
            shapley += (teller[j] * ( waarden[coalities.index(sorted(sommatie[i-1][j] + [i] ))] - waarden[coalities.index(sommatie[i-1][j])] ))
        result.append(round(shapley/noemer, 3))
    return result

def nucleolus(N, *waarden):
    waarden = list(waarden)
    from itertools import combinations
    from math import factorial
    spelers = list(range(1,N+1))
    coalities = [list(x) for i in range(N+1) for x in combinations(spelers,i)]
    a = waarden[-1] - sum([waarden[i] for i in spelers])
    while a > 0:
##        print(a)
        speling = []
        for i in spelers:
            list_substract = coalities[2**N - i - 1]
            speling.append( (waarden[-1] - waarden[coalities.index(list_substract)]) - (waarden[i]) )
        spelers = [spelers[x] for x in range(len(spelers)) if speling[x] != 0]
        speling = [x for x in speling if x != 0]
        translatie = min(a / len(spelers), .5 * min(speling) )
##        print(speling, a / len(spelers))
##        print(translatie)
##        print(spelers)
        for i in spelers:
            waarden[i] += translatie
            waarden[2**N - i - 1] += translatie
##        print(waarden)
        a = waarden[-1] - sum([waarden[i] for i in range(1,N+1)])
    #return [round(x,3) for x in waarden[1:N+1]]
    return waarden

def preferentie_huwerlijksprobleem(wensen_mannen, wensen_vrouwen):
    "VB: {'a':'cd', 'b':'c'}, {'c':'a'}"
    actief = list(wensen_mannen.keys())
    passief = list(wensen_vrouwen.keys())
    koppels = {}
    for man in actief:
        p = 0
        vrouw = wensen_mannen[man][p]
        if vrouw in koppels.values():
            for a in wensen_vrouwen[vrouw]:
                if koppels[a] == vrouw:
                    p += 1
                    continue #welke?
                elif a == man:
                    'verliezer = a'
        else:
            koppel[man] = (wensen_mannen[man][0])

def preferentie_huwerlijksprobleem(wensen_mannen, wensen_vrouwen):
    "Geordende lijst zonder weigeren passieve vrouwen\nVB: {'a':'cd', 'b':'dc'}, {'c':'b','d':'a'}"
    koppels = {}
    preferentie = {}
    for man in wensen_mannen:
        preferentie[man] = 0
    for man in wensen_mannen.keys():
        if not man in koppels.keys():
            while True:
                try:
                    aangevraagde = wensen_mannen[man][preferentie[man]]
                except IndexError:
                    del koppels['b']
                    break
##                print('ask ', man, aangevraagde)
                if not aangevraagde in koppels.values():
                    koppels[man] = aangevraagde
##                    print('init ', man, aangevraagde)
                    break
                else:
                    bruiloft = False
                    for prefer_vrouw in wensen_vrouwen[aangevraagde]:
                        if prefer_vrouw == man:
                            koppels[man] = aangevraagde
                            bruiloft = True
                            continue
                        elif not prefer_vrouw in koppels.keys():
                            continue
                        elif koppels[prefer_vrouw] == aangevraagde:
                            if bruiloft == False:
##                                print('verloren van ',prefer_vrouw)
                                pass
                            else:
##                                print('gewonnen van ',prefer_vrouw)
                                man = prefer_vrouw
                            preferentie[man] += 1
                            break
    return koppels
'''preferentie_huwerlijksprobleem({\
'a':'fkgl',
'b':'gkfl',
'c':'lgfk',
'd':'lfgk',
'e':'kglf'},
{'f':'cbaed',
'g':'dabec',
'k':'ecadb',
'l':'eabcd'})
'''
