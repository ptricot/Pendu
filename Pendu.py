# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 08:27:37 2018

@author: Paul
"""

from tkinter import *
import random as rd

largeur_boutons = 25      # Ceci me permet de définir tous les boutons à la même taille

class MonBouton(Button):
    def __init__(self,master,t):
        Button.__init__(self,master,text=' '+t+' ',command=self.clic,activeforeground='white',activebackground='gray35',fg='white',bg='gray35',width=4)
        self.__lettre=t
        self.__actif=True             # Pour activer / désactiver les touches du clavier réel (celui de l'ordinateur)
        
    def clic(self):                   #Gère le clic sur le bouton
        self.config(state=DISABLED)          #Désactive le bouton après clic
        self.config(bg='gray75')             #Change la couleur du bouton après clic
        self.master.master.traitement(self.__lettre)         # Lance le traitement de la lettre
        self.__actif=False
        
    def clic2(self,event):             # Gère les touches du clavier réel, qui implique obligatoirement un argument inutile 'event'.
        if self.__actif:
            self.config(state=DISABLED,bg='gray75')
            self.master.master.traitement(self.__lettre)
            self.__actif=False
            
    def activate(self):
        self.__actif=True
        
class Zonescore(Toplevel):
    def __init__(self,nom ):
        Toplevel.__init__(self,bg='gray75')
        self.__nomJoueur = nom
        #extraction des infos
        with open('scores.txt','r') as f:
            l = f.read().splitlines() #.split('\n')
        self.__tableauScore=[]        #Un tableau à deux dimensions pour les résultats de tous les joueurs
        for ligne in l:
            self.__tableauScore.append(ligne.split('\t'))
        self.__NewPlayer=True          # Sert à créer un nouveau joueur dans le fichier des scores en cas de première partie
        for v in self.__tableauScore:    # On cherche à extraire les scores du joueur, à partir du tableau de scores
            if v[0]==nom:
                self.__NewPlayer=False
                self.__vectScore = v[1:]     #Une liste pour les scores du joueur
                break
        if self.__NewPlayer:
            self.__vectScore = []
            with open('scores.txt','r+') as f:
                f.write('\n'+nom)               # Ajoute un nouveau joueur au fichier score, en cas de première partie
            self.__tableauScore.append([nom])
        self.bind('<Escape>',self.quitter)    #On permet de fermer rapidement la fenetre de score avec echap
      
    def res(self,r):          #méthode d'ajout d'un score
        nom=self.__nomJoueur
        self.__vectScore.append(r)     #On ajoute les nouvelles données dans self.__vectScore
        for i in range(len(self.__tableauScore)):
            if self.__tableauScore[i][0]==nom:
                self.__tableauScore[i].append(r)
                break                 #On ajoute les nouvelles données dans self.__tableauScore
        self.rewrite()
        
    def rewrite(self):
        f = open('scores.txt','r+')
        f.truncate(0)                #On réinitialise le fichier de scores
        for v in self.__tableauScore:
            for i in range(len(v)-1):
                f.write(v[i]+'\t')
            f.write(v[-1]+'\n')      #On réécrit le fichier score à partir de self.__tableauScore qui est à jour
                
    def affiche(self):             #méthode pour afficher le tableau de score du joueur
        nom=self.__nomJoueur
        v=self.__vectScore
        row,column=0,0
        vict,defe=0,0              #Le nombre de victoires et défaites qui serviva à calculer le ratio de victoires
        Label(self,text='Nom du joueur : '+nom,bg='gray75').grid(row=row,column=column)
        row+=1
        for i in range (len(v)):        # Une boulce sur les parties jouées par le joueur (dont les scores sont dans 'v')
            m = v[i].split(' ')         # m représente une partie. m[0] est le mot qui a été joué, et m[1] est '1' pour une victoire, '0' pour une défaite
            Label(self,text=m[0],bg='gray75').grid(row=row,column=column)       # Affiche le mot qui a été joué
            if m[1]=='1':
                Label(self,text=': gagné !',bg='gray75').grid(row=row,column=column+1)
                vict+=1
            else:
                Label(self,text=': perdu !',bg='gray75').grid(row=row,column=column+1)
                defe+=1
            row+=1
            if row>21:
                row=0
                Label(self,text='     ',bg='gray75').grid(row=row,column=column+2)
                column+=3
        if vict+defe>0:
            Label(self,text='Ratio de victoires : '+str(int(100*vict/(vict+defe)))+'%',bg='gray75').grid(row=row,column=column,columnspan=2)
                
    def resetPlayer(self):
        if not self.__NewPlayer:     # Il n'y a rien à faire si le joueur est nouveau
            nom=self.__nomJoueur
            for i in range(len(self.__tableauScore)):
                if self.__tableauScore[i][0]==nom:      #
                    del self.__tableauScore[i]
                    self.__vectScore = []
                    break
            self.rewrite()
            
    def afficheAll(self):            # Pour afficher tous les scores de tous les joueurs
        T = self.__tableauScore
        ligne=1           # retiens la ligne à laquelle afficher
        for v in T:         # Chaque 'v' sera la liste de scores d'un joueur
            if v[0] != '':
                Label(self,text='Nom du joueur : '+v[0],bg='gray75').grid(row=ligne)     # Affiche le nom du joueur sauvegardé dans v[0]
                vict,defe=0,0                # Initialise le nombre de victoires / défaites pour afficher le ratio de victoires
                ligne+=1
                for i in range (1,len(v)):      # Cette partie est la même que dans la méthode 'Affiche' pour seulement le joueur, à l'exception de la prise en compte du paramètre 'ligne', qui dit à quelle ligne écrire
                    m = v[i].split(' ')
                    Label(self,text=m[0],bg='gray75').grid(row=ligne,column=0)
                    if m[1]=='1':
                        Label(self,text=': gagné !',bg='gray75').grid(row=ligne,column=1)
                        vict+=1
                        ligne+=1
                    else:
                        Label(self,text=': perdu !',bg='gray75').grid(row=ligne,column=1)
                        defe+=1
                        ligne+=1
                if vict+defe>0:
                    Label(self,text='Ratio de victoires : '+str(int(100*vict/(vict+defe)))+'%',bg='gray75').grid(row=ligne)
                    ligne+=1
                Label(self,text='------------------------',bg='gray75').grid(row=ligne,column=0,columnspan=2)
                ligne+=1
        Label(self,text='--- esc pour quitter ---',bg='gray75').grid(row=ligne,column=0,columnspan=2)
        
    def quitter(self,event):           # Méthode pour fermer la fenêtre de score
        self.destroy()
        
class ZoneNom(Toplevel):              # Fenêtre affichée pour changer de nom
    def __init__(self,master):
        Toplevel.__init__(self)
        self.__master = master
        self.entry = Entry(self,bg='gray75')            # Une entrée pour écrire son nom
        self.entry.grid(row=0,column=0)
        Button(self,text='valider (entrer)',command=self.validate,fg='white',bg='gray35').grid(row=0,column=1)   # Un bouton pour valider
        self.bind('<Return>',self.validate2)
        
    def validate(self):                # Pour valider avec clic sur le bouton
        self.__master.set_nom(self.entry.get())
        self.destroy()
        
    def validate2(self,event):         #pour valider avec la touche entrer ( il faut gérer l'argument 'event' inutile ici)
        self.validate()

class Fen(Tk):                      # La classe de la fenètre principale
    def __init__(self):
        Tk.__init__(self)
        #donnees
        self.__nom = 'LHAMAP'
        self.__nbManques=0                  # Compteur de vies
        self.__showstat=True                       # L'option d'affichage ou non du score en fin de partie
        #zone d'information joueur
        self.__f2 = Frame(self,bg='gray75')
        self.__nomLab = Label(self.__f2,text='Nom du joueur :'+self.__nom,bg='gray75')
        self.__nomLab.grid(row=0,column=1)
        Button(self.__f2,text='Changer de joueur',command=self.changerJoueur,width=largeur_boutons,fg='white',bg='gray35').grid(row=1,column=0)
        Button(self.__f2,text='Mes scores',command=self.infoJoueur,width=largeur_boutons,fg='white',bg='gray35').grid(row=1,column=1)
        Button(self.__f2,text='Réinitialiser mes scores',command=self.resetScore,width=largeur_boutons,fg='white',bg='gray35').grid(row=1,column=2)
        Button(self.__f2,text='Tous les scores',command=self.infos,width=largeur_boutons,fg='white',bg='gray35').grid(row=2,column=0)
        Button(self.__f2,text='Réinitialiser tous les scores',command=self.resetAllScore,width=largeur_boutons,fg='white',bg='gray35').grid(row=2,column=1)
        self.__f2.grid(row=0,pady=3)
        #zone de contrôle
        self.__f1 = Frame(self,bg='gray75')
        self.__resetBut = Button(self.__f1,text='Nouvelle Partie (F5)',command=self.reset,width=largeur_boutons,fg='white',bg='gray35')
        self.__resetBut.grid(row=0,column=0)
        Button(self.__f1,text='Score en fin de partie :',command=self.setstat,width=largeur_boutons,fg='white',bg='gray35').grid(row=0,column=2)   # Pour activer/désactiver l'affichage des scores en fin de partie
        self.__statLab = Label(self.__f1,text='Actif',bg='gray75')      # Informe le joueur sur si les scores sont affichés en fin de partie
        self.__statLab.grid(row=0,column=3)
        self.__f1.grid(row=1)
        #zone de jeu : pendu
        self.__can = Canvas(self,height=300,width=330,bg='gray75')
        self.__can.grid(row=2)
        #zone de jeu : mot
        self.__mot=''
        self.__motAffiche='*'*len(self.__mot)
        self.__lmot = Label(self,text='mot : '+self.__motAffiche,width=20,font=('Arial',30),bg='gray75')  # Affiche '*****', qui sera lettre par lettre remplacé par le mot à deviner
        self.__lmot.grid(row=3)
        #clavier
        self.__f3 = Frame(self,bg='gray75')
        self.__boutons=[]
        for i in range (26):
            t=chr(ord('A')+i)
            b=MonBouton(self.__f3,t)
            b.grid(row=i-i%13,column=i%13)
            self.__boutons.append(b)
            self.bind('<'+t.lower()+'>',self.__boutons[i].clic2)     #On permet les saisies de lettres au clavier
            self.bind('<F5>',self.F5)                      # On permet de lancer une nouvelle partie avec 'F5'
        self.__f3.grid(row=4)
        
    def reset(self):        # Pour recommencer une partie
        self.chargeMots()          # Changer le mot à trouver
        self.__motAffiche='*'*len(self.__mot)         # Afficher '******' dans la fenetre de jeu
        self.__can.delete(ALL)                        # Retirer les éventuels images d'une partie précédente
        self.__nbManques=0                     # Reinitialiser le compteur de vies
        self.__lmot.config(text='mot : '+self.__motAffiche)
        for b in self.__boutons:
            b.config(state=ACTIVE,activebackground='gray35',activeforeground='white')     # Réactiver le bouton
            b.focus_force()
            b.activate()               # Réactiver le bouton par clic sur le clavier de l'ordinateur
            
    def F5(self,event):        # Sert à gérer l'argument inutile 'event' lors du clic sur 'F5' pour recommencer une partie
        self.reset()
        
    def setstat(self):          # Pour alterner entre afficher le score en fin de partie et ne pas le faire
        if self.__showstat:
            self.__showstat=False
            self.__statLab.config(text='Inactif')
        else:
            self.__showstat=True
            self.__statLab.config(text='Actif')
            
    def loose_life(self):
        n=self.__nbManques       # Le nombre de vies déjà perdues
        if n==0:                        # A chaque perte de vie, on affiche une nouvelle image, un pendu plus proche de la défaite, en fonction de l'état du compteur de vies
            pendu1=PhotoImage(file='pendu1.gif')
            self.__can.create_image(0,0,image=pendu1,anchor=NW)
            self.__can.image = pendu1
        elif n==1:
            pendu2=PhotoImage(file='pendu2.gif')
            self.__can.create_image(0,0,image=pendu2,anchor=NW)
            self.__can.image = pendu2
        elif n==2:
            pendu3=PhotoImage(file='pendu3.gif')
            self.__can.create_image(0,0,image=pendu3,anchor=NW)
            self.__can.image = pendu3
        elif n==3:
            pendu4=PhotoImage(file='pendu4.gif')
            self.__can.create_image(0,0,image=pendu4,anchor=NW)
            self.__can.image = pendu4
        elif n==4:
            pendu5=PhotoImage(file='pendu5.gif')
            self.__can.create_image(0,0,image=pendu5,anchor=NW)
            self.__can.image = pendu5
        elif n==5:
            pendu6=PhotoImage(file='pendu6.gif')
            self.__can.create_image(0,0,image=pendu6,anchor=NW)
            self.__can.image = pendu6
        elif n==6:
            pendu7=PhotoImage(file='pendu7.gif')
            self.__can.create_image(0,0,image=pendu7,anchor=NW)
            self.__can.image = pendu7
        elif n==7:
            pendu8=PhotoImage(file='pendu8.gif')
            self.__can.create_image(0,0,image=pendu8,anchor=NW)
            self.__can.image = pendu8
        elif n==8:
            pendu=PhotoImage(file='pendu.gif')
            self.__can.create_image(0,0,image=pendu,anchor=NW)
            self.__can.image = pendu
            self.fin_de_jeu(False)             # Lancement de la défaite si le compteur de vies atteint 8
        self.__nbManques+=1
        
    def fin_de_jeu(self,b):            # Gère une fin de partie avec b=True pour une victoire et False pour une défaite
        nom=self.__nom
        if b:                         #Cas partie gagnée
            gagne=PhotoImage(file='gagne.gif')
            self.__can.create_image(0,0,image=gagne,anchor=NW)
            self.__can.image = gagne             # afficher l'image de victoire
            r=self.__mot+' 1'                    # le string qui va être ajouté au fichier des scores
        else:                         #Cas partie perdue
            self.__lmot.config(text='mot : '+self.__mot)           # Afficher le mot qu'il fallait trouver
            r=self.__mot+' 0'
        for b in self.__boutons:
            b.config(state=DISABLED)        # Desactiver les boutons en fin de partie
        F = Zonescore(nom)
        F.res(r)
        F.affiche()
        F.focus_force()
        if not self.__showstat:             # Pour ne pas afficher le score en fin de partie si le joueur a activé cette option
            F.destroy()
            
    def traitement(self,lettre):        #Méthode appellée lors du clic sur une lettre
        loose=True          # Représentera si le joueur doit perdre une vie
        for i in range (len(self.__mot)):
            if self.__mot[i] == lettre:      # Si la lettre est présente dans le mot, il n'y a pas perte de vie et on remplace les lettres trouvées dans le mot affiché
                loose=False
                self.__motAffiche=self.__motAffiche[:i]+lettre+self.__motAffiche[(i+1):]
                self.__lmot.config(text='mot : '+self.__motAffiche)
        if loose:
            self.loose_life()                # Si la lettre n'est pas dans le mot, le joueur perd une vie
        if self.__mot == self.__motAffiche and self.__mot != '':
            self.fin_de_jeu(True)            # Lancement de la méthode de victoire si le mot affiché est le mot à trouver
            
    def chargeMots(self):                 # Remplace le mot à trouver à partir du fichier mots.txt lors du lancement d'une nouvelle partie
        with open('mots.txt','r') as f:
            l = f.read().splitlines()
        i=rd.randint(0,len(l)-1)
        self.__mot=l[i]
        
    def changerJoueur(self):        #Méthode appellée lorsque le joueur veut changer de nom, ouvre une fenêtre dédiée
        Z = ZoneNom(self)
        Z.entry.focus_force()
        
    def set_nom(self,nom):         #Méthode appelée lors de la validation dans la fenêtre de changement de nom
        self.__nom = nom
        self.__nomLab.config(text=nom)          # Afficher le nouveau nom en haut de la fenêtre principale
        
    def resetScore(self):                     # Réinitialiser les scores du joueur après appui sur le bouton dédié
        F=Zonescore(self.__nom)
        F.resetPlayer()
        F.affiche()
        F.focus_force()                  # Passe le focus sur la nouvelle fenêtre
        
    def infoJoueur(self):               # Affiche une zone de score pour le joueur
        nom=self.__nom
        F=Zonescore(nom)
        F.affiche()
        F.focus_force()        #Le focus passe sur la fenêtre de score à son affichage pour pouvoir la fermer rapidement avec echap
        
        
    def infos(self):            # Affiche les infos de tous les joueurs
        F=Zonescore(self.__nom)
        F.afficheAll()
        F.focus_force()
        
    def resetAllScore(self):             # Réinitialise tous les scores
        with open('scores.txt','r+') as f:
            f.truncate(0)
            
Fenetre=Fen()
Fenetre["bg"]='gray75'
Fenetre.title("Pendu")
Fenetre.focus_force()
Fenetre.mainloop()