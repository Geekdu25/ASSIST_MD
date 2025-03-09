from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
from lxml import etree
import platform, os, random, pygame, shutil

class Personnage:
    def __init__(self, nom="Torinn Delmirev", race="Drakéide", classe="Moine", niveau=1, ca=10, pv=10, init=2):
        self.nom = nom
        self.race = race
        self.classe = classe
        self.niveau = niveau
        self.ca = ca
        self.pv = pv
        self.initiative = init

class Application(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.cwd = os.getcwd()
        self.title("L'assistant du MD")
        self.iconphoto(False, PhotoImage(file='../pictures/plus.png'))
        self.minsize(1550, 850)
        if not os.path.exists(self.get_path()):
            showinfo("Fichiers non existants", "Aucun fichier de sauvegarde du logiciel n'a été trouvé sur votre ordinateur.\nDe nouveaux fichiers de sauvegardes vont être crées.")
            os.mkdir(self.get_path())
            os.mkdir(self.get_path() +"/personnages")
            os.mkdir(self.get_path() +"/campagnes")
        self.campagnes = []
        self.menubar = Menu(self)
        self.menu1 = Menu(self.menubar, tearoff=0)
        self.menu1.add_command(label="Nouvelle campagne", command=self.nouvelle_campagne)
        self.menu1.add_command(label="Nouveau personnage", command=self.new_character)
        self.menu1.add_separator()
        self.menu1.add_command(label="Ouvrir un fichier...", command=self.open_file)
        self.menu1.add_separator()
        self.menu1.add_command(label="Revenir à l'écran d'accueil", command=self.home)
        self.menu1.add_separator()
        self.menu1.add_command(label="Quitter", command=self.quitter)
        self.menubar.add_cascade(label="Fichier", menu=self.menu1)
        self.menu3 = Menu(self.menubar, tearoff=0)
        self.menu3.add_command(label="Gestionnaire de musique", command=self.audio_manager)
        self.menu3.add_separator()
        self.menu3.add_command(label="Réinitialiser les fichiers de sauvegarde", command=self.reset)
        self.menubar.add_cascade(label="Outils", menu=self.menu3)
        self.menu2 = Menu(self.menubar, tearoff=0)
        self.menu2.add_command(label="A propos", command=self.apropos)
        self.menubar.add_cascade(label="Aide", menu=self.menu2)
        self.config(menu=self.menubar)
        self.protocol("WM_DELETE_WINDOW", self.quitter)
        pygame.mixer.init()
        self.fichiers_nom = {}
        for file in os.scandir(self.get_path()+"/personnages"):
            if file.name.endswith(".xml"):
                self.fichiers_nom[file.name] = etree.parse(self.get_path()+"/personnages/"+file.name).xpath("/builder/character/name")[0].text     
        self.status = None
        self.apropos_open = False
        self.home()

    def open_file(self):
        path = askopenfilename(filetypes=[("Fichiers eXtensible Markup Language (XML)", "*.xml")])
        if path != "":
            a = True
            new_path = self.get_path()+"/personnages/"+path.split("/")[len(path.split("/"))-1]
            if os.path.exists(new_path):
                a = askyesno("Fichier déjà existant", "Un fichier possédant le même nom que le fichier que vous êtes en train d'enregistrer se trouve déjà dans le dossier des personnages. Désirez-vous tout de même l'écraser ?")
            if a:    
              try:
                shutil.copy2(path, new_path)
                self.fichiers_nom = {}
                for file in os.scandir(self.get_path()+"/personnages"):
                  if file.name.endswith(".xml"):
                    self.fichiers_nom[file.name] = etree.parse(self.get_path()+"/personnages/"+file.name).xpath("/builder/character/name")[0].text  
                showinfo("Enregistrement", "Le fichier a été enregistré !")
                if self.status == "new":
                    self.liste_total.insert("end", path.split("/")[len(path.split("/"))-1] +" -> "+self.fichiers_nom[path.split("/")[len(path.split("/"))-1]])
              except:
                  showinfo("Echec", "Suite à une erreur, votre fichier n'a pas pu être enregistré.")

    def reset(self):
        if hasattr(self, "aide"):
            self.aide.destroy()
        if askyesno("Réinitialisation", "Désirez-vous réinitialiser toutes les données de sauvegarde du logiciel présentes sur votre ordinateur ?"):
            if askyesno("Réinitialisation", "En êtes-vous sûr ? (Les données effacées ne peuvent pas être récupérées)"):
                try:
                  if platform.system() == "Windows":  
                    os.chdir(f"C://users/{os.getlogin()}/AppData/Roaming")  
                    shutil.rmtree("ASSIST_MD")
                  elif platform.system() == "Linux":  
                    os.chdir(f"/home/{os.getlogin()}")  
                    shutil.rmtree(".ASSIST_MD")  
                  os.chdir(self.cwd)  
                except:
                    showwarning("Echec", "La réinitialisation a échoué. (Il est probable que cela soit du a une protection des données.)")
                    showinfo("Information", f"Pour effacer les données manuellement, veuillez supprimer le dossier : {self.get_path()}")
                else:
                  showinfo("Réintialisation effectuée", "La réinitialisation a été effectuée avec succès ! (L'application va désormais s'arrêter)")
                  pygame.mixer.quit()
                  self.destroy()
            else:
                self.apropos_open = False
        else:
            self.apropos_open = False

    def audio_manager(self):
        self.delete_frames()
        self.status = "audio"
        self.main_frame = Frame(self)
        self.main_frame.pack()

    def apropos(self):
        if not self.apropos_open:
          self.apropos_open = True  
          self.aide = Tk()
          self.aide.title("A propos")
          self.aide.minsize(600, 450)
          if platform.system() == "Windows":
            self.aide.ico = PhotoImage(file='../pictures/plus.png')
            self.aide.iconphoto(False, self.aide.ico)
          self.aide.protocol("WM_DELETE_WINDOW", self.quit_apropos)
          text_intro = Label(self.aide, text="L'assistant du MD.", font=("Arial", 25))
          text_intro.pack()
          text_intro2 = Label(self.aide, text="Une application créée dans le but d'aider les maîtres du donjon \nde Donjons et dragons dans la lourde tâche\n qu'est la gestion d'une partie.\nCette application a été crée par le fabuleux Geekdu25.", font=("Arial", 15))
          text_intro2.pack(pady=10)
          text_intro2 = Label(self.aide, text="Ce logiciel et son code source sont disponibles en ligne à l'adresse : https://www.github.com/Geekdu25/ASSIST_MD", font=("Arial", 15))
          text_intro2.pack(pady=15)
          self.aide.mainloop()

    def quit_apropos(self):
        self.apropos_open = False
        self.aide.destroy()
        del self.aide

    def get_path(self):
        path = ""
        if platform.system() == "Windows":
            path = f"C://users/{os.getlogin()}/AppData/Roaming/ASSIST_MD"
        elif platform.system() == "Linux":
            path = f"/home/{os.getlogin()}/.ASSIST_MD"
        return path

    def delete_frames(self):
        if hasattr(self, "main_frame"):
          self.main_frame.destroy()
          del self.main_frame

    def home(self):
        ok_status = [None, "load", "home", "audio"]
        if (self.status == "new_ch" and askyesno("Abandonner le personnage", "Désirez-vous réellement abandonner le personnage en cours de création ?")) or (self.status == "new" and askyesno("Abandonner la campagne", "Désirez-vous réellement abandonner la campagne en cours de création ?")) or self.status in ok_status:
          self.status = "home"  
          self.delete_frames()
          self.main_frame = Frame(self)
          self.main_frame.pack()
          text_intro = Label(self.main_frame, text="Bienvenue sur l'écran d'accueil de l'assistant du MD.", font=("Arial", 25))
          text_intro.pack()
          self.liste_campagnes = Listbox(self.main_frame)
          self.campagnes = []
          for fichier in os.scandir(self.get_path()+"/campagnes"):
              if fichier.is_dir():
                self.campagnes.append(fichier.name)
          self.campagnes.sort()
          for campagne in self.campagnes:
              self.liste_campagnes.insert("end", campagne)
          self.liste_campagnes.pack(fill=BOTH, expand=True, pady=20)
          self.buttons_frame = Frame(self.main_frame)
          self.buttons_frame.pack()
          self.button_delete = Button(self.buttons_frame, text="Supprimer la campagne", command=self.delete_campagne)
          self.button_delete.grid(row=0, column=0, columnspan=2)
          self.button_charger = Button(self.buttons_frame, text="Charger la campagne", command=self.load_campagne)
          self.button_charger.grid(row=0, column=2, columnspan=2)
          

    def delete_campagne(self):
        if len(self.liste_campagnes.curselection()) > 0:
          if askyesno("Suppression de la campagne.", "Êtes-vous vraiment sûr de vouloir supprimer cette campagne ?"):
            os.chdir(self.get_path()+"/campagnes")
            shutil.rmtree(self.liste_campagnes.get(self.liste_campagnes.curselection()))
            os.chdir(self.cwd)
            self.liste_campagnes.delete(self.liste_campagnes.curselection())
            

    def nouvelle_campagne(self):
        self.status = "new"
        self.delete_frames()
        self.main_frame = Frame(self)
        self.main_frame.pack()
        text_intro = Label(self.main_frame, text="Création d'une nouvelle campagne.", font=("Arial", 25))
        text_intro.pack()
        text_intro2 = Label(self.main_frame, text="Commencez par donner un nom à votre campagne :", font=("Arial", 13))
        text_intro2.pack(pady=15)
        value = StringVar()
        value.set("Ma campagne")
        self.nom = Entry(self.main_frame, textvariable=value, width=30)
        self.nom.pack(pady=7)
        text_intro3 = Label(self.main_frame, text="Ensuite, veuillez ajouter des joueurs à votre groupe.", font=("Arial", 15))
        text_intro3.pack(pady=15)
        text_intro4 = Label(self.main_frame, text="Ajoutez à votre campagne des personnages que vous avez déjà crées avec l'éditeur de personnages.\nSi ce n'est pas déjà fait, commencez par en créer au moins un avec l'éditeur de personnages.", font=("Arial", 8))
        text_intro4.pack(pady=1)
        frame = Frame(self.main_frame)
        frame.pack()
        self.liste_total = Listbox(frame)
        self.liste_total.grid(row=0, column=0, columnspan=2)
        bouton_add = Button(frame, text="->", compound=LEFT, command=self.deplace_new_campagne)
        bouton_add.grid(row=0, column=3, sticky=N, columnspan=1)
        self.liste_final = Listbox(frame)
        self.liste_final.grid(row=0, columnspan=3, column=4)
        for fichier in os.scandir(self.get_path()+"/personnages"):
            if fichier.name.endswith(".xml"):
                self.liste_total.insert("end", fichier.name+" -> "+self.fichiers_nom[fichier.name])
        bouton_delete = Button(frame, text="Supprimer le dernier personnage", command=self.delete_last)        
        bouton_delete.grid(row=0, column=8, sticky=S)        
        bouton_record = Button(self.main_frame, text="Enregistrer la campagne", command=self.record_campagne)
        bouton_record.pack(pady=15)

    def deplace_new_campagne(self):
        if self.liste_final.size() == 5:
            showinfo("Attention", "Attention ! Votre nombre de joueurs va maintenant passer à 6.\nPlus on est de fous plus on rit, mais la gestion d'une partie comprenant autant de joueurs risque d'être compliquée.\n Vous voilà prévenu.")
        self.liste_final.insert("end", self.liste_total.get(self.liste_total.curselection()))

    def delete_last(self):
        self.liste_final.delete("end")

    def record_campagne(self):
        path = self.get_path()+"/campagnes/"+self.nom.get()
        if len(self.nom.get()) < 1:
            showwarning("Attention", "Vous ne pouvez pas enregistrer une campagne sans nom.")
        elif os.path.exists(path):
            showwarning("Attention", "Une campagne comprenant ce nom existe déjà.\n Veuillez supprimer la campagne avant d'en créer une nouvelle avec le même nom.")
        elif  self.liste_final.size() < 1:
            showwarning("Attention", "Vous ne pouvez pas enregistrer une campagne sans joueurs.")
        else:
          del self.nom
          os.mkdir(path)
          self.status = "home"
          self.home()

    def new_character(self):
        self.status = "new_ch"
        self.infos = []
        self.delete_frames()
        self.main_frame = Frame(self)
        self.main_frame.pack()
        texte_intro = Label(self.main_frame, text="Entrez les informations les plus importantes de votre personnage.", font=("Courrier", 20))
        texte_intro.pack()
        frame_champs = Frame(self.main_frame)
        frame_champs.pack()
        #--------------------Nom---------------------------------------------------
        frame_nom = LabelFrame(frame_champs, text="Nom : ")
        value = StringVar()
        value.set("Nom")
        nom = Entry(frame_nom, textvariable=value, width=30)
        self.infos.append(nom)
        nom.pack()
        frame_nom.grid(row=0, column=1, columnspan=1)
        #-----------------------------Race-------------------------
        frame_r = LabelFrame(frame_champs, text="Race : ")
        value = StringVar()
        value.set("Race")
        r = Entry(frame_r, textvariable=value, width=20)
        self.infos.append(r)
        r.pack()
        frame_r.grid(row=1, column=0, columnspan=1)
        #---------------------------Classe------------------------------------
        frame_c = LabelFrame(frame_champs, text="Classe : ")
        value = StringVar()
        value.set("Classe")
        c = Entry(frame_c, textvariable=value, width=20)
        self.infos.append(c)
        c.pack()
        frame_c.grid(row=1, column=1, columnspan=1)
        #------------------Niveau---------------------------------------------
        frame_niveau = LabelFrame(frame_champs, text="Niveau : ")
        frame_niveau.grid(row=1, column=2, columnspan=1)
        niveau = Spinbox(frame_niveau, from_=1, to=20)
        self.infos.append(niveau)
        niveau.pack()
        #-------------------Classe d'armure----------------------------------------
        info_ca = LabelFrame(frame_champs, text="Classe d'armure : ")
        info_ca.grid(row=2, column=0, columnspan=1)
        value = StringVar()
        value.set("10")
        ca = Entry(info_ca, textvariable=value, width=20)
        self.infos.append(ca)
        ca.pack()
        #---------------------Points de vie------------------------------------------
        info_pv = LabelFrame(frame_champs, text="Points de vie : ")
        info_pv.grid(row=2, column=1, columnspan=1)
        value = StringVar()
        value.set("10")
        pv = Entry(info_pv, textvariable=value, width=20)
        self.infos.append(pv)
        pv.pack()
        #------------------------Initiative--------------------------------------------
        info_init = LabelFrame(frame_champs, text="Initiative : ")
        info_init.grid(row=2, column=2, columnspan=1)
        value = StringVar()
        value.set("0")
        init = Entry(info_init, textvariable=value, width=20)
        self.infos.append(init)
        init.pack()
        #------------------------------------Bouton de sauvegarde----------------------------------------------
        save_button = Button(self.main_frame, text="Enregistrer le personnage", command=self.save_new_character)
        save_button.pack(padx=30, pady=20)
        
    def save_new_character(self):
        informations = []
        for info in self.infos:
            informations.append(info.get())
        if len(informations[0]) < 1:
            showinfo("Champ incomplet", "Attention ! Le nom de votre personnage n'est pas rempli !")
        if len(informations[1]) < 1:
            showinfo("Champ incomplet", "Attention ! La race de votre personnage n'est pas remplie !")
        if len(informations[2]) < 1:
            showinfo("Champ incomplet", "Attention ! La classe de votre personnage n'est pas remplie !") 
        else:
          del self.infos
          new_personnage = Personnage(nom=informations[0], race=informations[1], classe=informations[2], niveau=informations[3], ca=informations[4], pv=informations[5], init=informations[6])
          showinfo("Réussite", "L'enregistrement de votre personnage a été effectué avec succès !")
        
        
    def load_campagne(self):
        campagne = self.liste_campagnes.curselection()
        if len(campagne) < 1:
            showwarning("Erreur", "Veuillez sélectionner une de vos campagnes.")
        else:
            self.status = "load"
            self.delete_frames()
            self.main_frame = Frame(self)
            self.main_frame.pack()

    def quitter(self):
        if askyesno("Quitter le logiciel", "Voulez-vous vraiment quitter le logiciel ? \n (Les éventuelles données non sauvegardées ne seront pas conservées.)"):
          self.destroy()
          pygame.mixer.quit()

app = Application()
app.mainloop()
