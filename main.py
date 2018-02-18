from kivy.app import App
from kivy.core.window import Window
from kivy.core.window import WindowBase
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.graphics import Rectangle
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.core.audio import SoundLoader
#Nombres aleatoires:
import random

#On declare deux ecrans 'Menu' et 'Game'
class MenuScreen(Screen):
    def build(self):
        self.name='Menu'#On donne un nom a l'ecran
        #Une image de fond:
        self.add_widget(Image(source='bggames.png',allow_stretch=True,keep_ratio=False))
        #On definie un layout pour cet ecran:
        Menu_Layout = BoxLayout(padding=100,spacing=10,orientation='vertical')
        #On cree un bouton pour lancer le jeu:
        self.Bouton_Jeu=Button(text='Attraper des dollars!')
        self.Bouton_Jeu.font_size=Window.size[0]*0.05
        self.Bouton_Jeu.background_color=[0,0,0,0.2]
        self.Bouton_Jeu.bind(on_press=self.Vers_Game)
        #On ajoute le bouton dans l'affichage:
        Menu_Layout.add_widget(self.Bouton_Jeu)
        #On ajoute ce layout dans l'ecran:
        self.add_widget(Menu_Layout)

    def Vers_Game(self,instance):#Fonction de transition vers 'Game'
        Game=GameScreen()
        Game.build()#On construit l'ecran 'Game'
        sm.add_widget(Game)#On ajoute l'ecran dans le screen manager
        sm.current='Game'#On definit 'Menu' comme ecran courant

class GameScreen(Screen):
    def build(self):
        self.name='Game'#On donne un nom a l'ecran
        Game_Layout=Jeu()#Creation du jeu
        Game_Layout.debut()#Initialisation du jeu
        self.add_widget(Game_Layout)#On l'ajoute dans l'ecran


class Dollars(Widget):
    def __init__(self,canvas):
        self.dy=-10
        self.canvas=canvas
        #Taille et position aleatoire:
        self.size=(Window.size[0]*0.05,Window.size[1]*0.1)
        self.x = random.randint(0,int(Window.size[0]-self.size[0]))
        self.y=Window.size[1]-100
        #Ajout de l'image du dollar:
        with self.canvas:
            self.dessin = Rectangle(source='dollars.png',size=self.size, pos=self.pos)
        #Detection des mouvements:
        self.bind(pos=self.update_canvas)

    def update_canvas(self, *args):#Mise a jour des positions de l'image:
        self.dessin.pos = self.pos

    def move(self):
        #On recalcule les positions:
        self.y=self.y+self.dy
        #On teste la fin de la chute:
        if self.y<=0-self.size[1]:
            #Repositionnement aleatoire en haut:
            self.y=Window.size[1]
            self.x=random.randint(0,int(Window.size[0]-self.size[0]))

    def prise(self):#Changement d'image pour le succes:
        self.dy=0#On stoppe la chute
        #Position au dessus du wallet pour stopper la collision:
        self.y=Window.size[1]*0.2
        self.dessin.source='+1.png'#Nouvelle image
        #On lance le nouveau dollars dans 0.5 seconde:
        Clock.schedule_once(self.prise_fin, 0.5)

    def prise_fin(self,dt):#Retour a l'image de dollar et en haut:
        self.y=0-self.size[1]#On le place en dessous pour qu'il remonte
        self.dessin.source='dollars.png'   #On change l'image
        self.dy=-10    #On relance la chute

class Wallet(Widget):
    def __init__(self,canvas):
        self.canvas=canvas
        #Taille et position:
        self.size=(Window.size[0]*0.1,Window.size[1]*0.1)
        self.pos=(0,Window.size[1]*0.02)
        #Ajout de l'image (add_wiget fonctionne aussi):
        with self.canvas:
            self.dessin = Rectangle(source='wallet.png',size=self.size, pos=self.pos)
        #On associe le mouvement du wallet et son image:
        self.bind(pos=self.update_canvas)

    def update_canvas(self, *args):#Mise a jour des positions de l'image:
        self.dessin.pos = self.pos


class Jeu(FloatLayout):
    def debut(self):
        #On recupere la taille de l'ecran:
        self.size=Window.size
        #Une image de fond:
        self.add_widget(Image(source='bggames.png',allow_stretch=True,keep_ratio=False))

        #Un label pour le score:
        self.score=0#Creation de la variable score
        self.label=Label(text='Score : '+str(self.score),markup=True)
        #Taille de la police en fonction de l'ecran:
        self.label.font_size=self.size[0]*0.05
        #Le label ne doit pas ecraser tout l'ecran:
        self.label.size_hint=(None,None)
        #Position du label vers le centre de l'ecran:
        self.label.pos=(Window.size[0]*0.05,Window.size[1]*0.85)
        self.label.color=[0,0,0,1]
        #On ajoute le label dans l'ecran du jeu:
        self.add_widget(self.label)

        #Creation du wallet:
        self.wallet=Wallet(self.canvas)
        #Creation des dollars:
        self.dollars=[]
        for i in range(0,5):#On ajoute les dollars
            self.dollars.append(Dollars(self.canvas))

        #Depart de l'horloge du jeu:
        Clock.schedule_interval(self.update_chute, 4.0/100.0)

    def update_chute(self,dt):#Chute des dollars et tests de collisions
        for dollar in self.dollars:
            dollar.move()
            if dollar.collide_widget(self.wallet):
                    dollar.prise()#Animation de la capture
                    self.score+=1
                    self.label.text='Score : '+str(self.score)

    def on_touch_move(self,touch):#Deplacement du wallet
        if touch.y<self.size[1]/3:
            self.wallet.center_x=touch.x


# Creation du screen manager
sm = ScreenManager()

class DollarsApp(App):
    def build(self):
        Menu=MenuScreen()#Creation de l'ecran 'Menu'
        Menu.build()#Construction de l'ecran 'Menu'
        #On ajoute l'ecran dans le screen manager
        sm.add_widget(Menu)
        sm.current='Menu'#On definit 'Menu' comme ecran courant
        return sm #On envoie le screen manager pour affichage

if __name__ == '__main__':
    DollarsApp().run()
