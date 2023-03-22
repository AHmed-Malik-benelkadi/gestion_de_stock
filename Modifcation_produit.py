import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from main import *

class ModifierProduitDialogue(tk.Toplevel):
    def __init__(self, parent, id_produit):
        super().__init__(parent)
        self.title("Modifier produit")
        self.geometry("400x300")
        self.parent = parent
        self.id_produit = id_produit
        self.creer_widgets()

    def creer_widgets(self):
        produit = [p for p in recuperer_produits() if p[0] == self.id_produit][0]
        categories = recuperer_categories()

        self.lbl_nom = ttk.Label(self, text="Nom")
        self.lbl_description = ttk.Label(self, text="Description")
        self.lbl_prix = ttk.Label(self, text="Prix")
        self.lbl_quantite = ttk.Label(self, text="Quantité")
        self.lbl_categorie = ttk.Label(self, text="Catégorie")

        self.entry_nom = ttk.Entry(self)
        self.entry_nom.insert(0, produit[1])
        self.entry_description = ttk.Entry(self)
        self.entry_description.insert(0, produit[2])
        self.entry_prix = ttk.Entry(self)
        self.entry_prix.insert(0, produit[3])
        self.entry_quantite = ttk.Entry(self)
        self.entry_quantite.insert(0, produit[4])
        self.combo_categorie = ttk.Combobox(self, values=[c[1] for c in categories], state="readonly")
        self.combo_categorie.set(categories[produit[5] - 1][1])

        self.lbl_nom.grid(row=0, column=0, padx=10, pady=10)
        self.lbl_description.grid(row=1, column=0, padx=10, pady=10)
        self.lbl_prix.grid(row=2, column=0, padx=10, pady=10)
        self.lbl_quantite.grid(row=3, column=0, padx=10, pady=10)
        self.lbl_categorie.grid(row=4, column=0, padx=10, pady=10)

        self.entry_nom.grid(row=0, column=1, padx=10, pady=10)
        self.entry_description.grid(row=1, column=1, padx=10, pady=10)
        self.entry_prix.grid(row=2, column=1, padx=10, pady=10)
        self.entry_quantite.grid(row=3, column=1, padx=10, pady=10)

        self.entry_quantite.grid(row=3, column=1, padx=10, pady=10)
        self.combo_categorie.grid(row=4, column=1, padx=10, pady=10)

        self.btn_enregistrer = ttk.Button(self, text="Enregistrer modifications",
                                          command=self.enregistrer_modifications)
        self.btn_annuler = ttk.Button(self, text="Annuler", command=self.destroy)

        self.btn_enregistrer.grid(row=5, column=0, padx=10, pady=20)
        self.btn_annuler.grid(row=5, column=1, padx=10, pady=20)

    def enregistrer_modifications(self):
        nom = self.entry_nom.get()
        description = self.entry_description.get()
        prix = self.entry_prix.get()
        quantite = self.entry_quantite.get()
        id_categorie = recuperer_categories()[self.combo_categorie.current()][0]

        if nom and description and prix and quantite and id_categorie:
            try:
                modifier_produit(self.id_produit, nom, description, float(prix), int(quantite), id_categorie)
                self.parent.charger_produits()
                self.destroy()
                messagebox.showinfo("Succès", "Le produit a été modifié avec succès")
            except ValueError:
                messagebox.showerror("Erreur", "Veuillez entrer des valeurs valides pour le prix et la quantité")
        else:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs")