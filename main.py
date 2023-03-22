import mysql.connector
from mysql.connector import Error
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from Modifcation_produit import *
import csv

def create_connexion():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Kiko2002=",
            database="boutique"
        )
        return conn
    except Error as e:
        print(f"Erreur: {e}")
        return None

def ajouter_produit(nom, description, prix, quantite, id_categorie):
    conn = create_connexion()
    cursor = conn.cursor()
    query = "INSERT INTO produit (nom, description, prix, quantite, id_categorie) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (nom, description, prix, quantite, id_categorie))
    conn.commit()
    cursor.close()
    conn.close()

def supprimer_produit(id):
    conn = create_connexion()
    cursor = conn.cursor()
    query = "DELETE FROM produit WHERE id=%s"
    cursor.execute(query, (id,))
    conn.commit()
    cursor.close()
    conn.close()

def modifier_produit(id, nom, description, prix, quantite, id_categorie):
    conn = create_connexion()
    cursor = conn.cursor()
    query = "UPDATE produit SET nom=%s, description=%s, prix=%s, quantite=%s, id_categorie=%s WHERE id=%s"
    cursor.execute(query, (nom, description, prix, quantite, id_categorie, id))
    conn.commit()
    cursor.close()
    conn.close()

def recuperer_produits():
    conn = create_connexion()
    cursor = conn.cursor()
    query = "SELECT * FROM produit"
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def recuperer_categories():
    conn = create_connexion()
    cursor = conn.cursor()
    query = "SELECT * FROM categorie"
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

class GestionStockApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestion de stock")
        self.geometry("800x600")
        self.creer_widgets()

    def creer_widgets(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(pady=10)

        self.frame_produits = ttk.Frame(self.notebook)
        self.frame_ajout = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_produits, text='Produits')
        self.notebook.add(self.frame_ajout, text='Ajouter un produit')

        # Frame Produits
        self.tree = ttk.Treeview(self.frame_produits, columns=("ID", "Nom", "Description", "Prix", "Quantité", "ID Catégorie"))
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nom", text="Nom")
        self.tree.heading("Description", text="Description")
        self.tree.heading("Prix", text="Prix")
        self.tree.heading("Quantité", text="Quantité")
        self.tree.heading("ID Catégorie", text="ID Catégorie")
        self.tree['show'] = 'headings'
        self.tree.column("ID", width=50)
        self.tree.column("Nom", width=200)
        self.tree.column("Description", width=300)
        self.tree.column("Prix", width=100)
        self.tree.column("Quantité", width=100)
        self.tree.column("ID Catégorie", width=100)
        self.tree.pack(pady=20)

        self.charger_produits()

        self.btn_supprimer = ttk.Button(self.frame_produits, text="Supprimer produit", command=self.supprimer_produit)
        self.btn_supprimer.pack(pady=10)

        self.btn_modifier = ttk.Button(self.frame_produits, text="Modifier produit",
                                       command=self.ouvrir_modifier_produit)
        self.btn_modifier.pack(pady=10)

        self.frame_categories = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_categories, text='Catégories')

        # Frame Produits
        # ...
        self.tree.pack(pady=10)

        self.frame_controls = ttk.Frame(self.frame_produits)
        self.frame_controls.pack(pady=10)

        self.combo_filtrer = ttk.Combobox(self.frame_controls,
                                          values=["Toutes"] + [c[1] for c in recuperer_categories()], state="readonly")
        self.combo_filtrer.set("Toutes")
        self.combo_filtrer.bind("<<ComboboxSelected>>", self.filtrer_produits)
        self.combo_filtrer.pack(side="left", padx=10)

        self.btn_exporter_csv = ttk.Button(self.frame_controls, text="Exporter CSV", command=self.exporter_csv)
        self.btn_exporter_csv.pack(side="right", padx=10)

        # Frame Ajout
        self.lbl_nom = ttk.Label(self.frame_ajout, text="Nom")
        self.lbl_description = ttk.Label(self.frame_ajout, text="Description")
        self.lbl_prix = ttk.Label(self.frame_ajout, text="Prix")
        self.lbl_quantite = ttk.Label(self.frame_ajout, text="Quantité")
        self.lbl_categorie = ttk.Label(self.frame_ajout, text="Catégorie")

        self.entry_nom = ttk.Entry(self.frame_ajout)
        self.entry_description = ttk.Entry(self.frame_ajout)
        self.entry_prix = ttk.Entry(self.frame_ajout)
        self.entry_quantite = ttk.Entry(self.frame_ajout)
        self.combo_categorie = ttk.Combobox(self.frame_ajout, values=[c[1] for c in recuperer_categories()], state="readonly")

        self.lbl_nom.grid(row=0, column=0, padx=10, pady=10)
        self.lbl_description.grid(row=1, column=0, padx=10, pady=10)
        self.lbl_prix.grid(row=2, column=0, padx=10, pady=10)
        self.lbl_quantite.grid(row=3, column=0, padx=10, pady=10)
        self.lbl_categorie.grid(row=4, column=0, padx=10, pady=10)

        self.entry_nom.grid(row=0, column=1, padx=10, pady=10)
        self.entry_description.grid(row=1, column=1, padx=10, pady=10)
        self.entry_prix.grid(row=2, column=1, padx=10, pady=10)
        self.entry_quantite.grid(row=3, column=1, padx=10, pady=10)
        self.combo_categorie.grid(row=4, column=1, padx=10, pady=10)

        self.btn_ajouter = ttk.Button(self.frame_ajout, text="Ajouter produit", command=self.ajouter_nouveau_produit)
        self.btn_ajouter.grid(row=5, column=0, columnspan=2, pady=20)

        # Frame Catégories
        self.lbl_categorie_nom = ttk.Label(self.frame_categories, text="Nom de la catégorie")
        self.entry_categorie_nom = ttk.Entry(self.frame_categories)
        self.btn_ajouter_categorie = ttk.Button(self.frame_categories, text="Ajouter catégorie",
                                                command=self.ajouter_nouvelle_categorie)

        self.lbl_categorie_nom.pack(pady=10)
        self.entry_categorie_nom.pack(pady=10)
        self.btn_ajouter_categorie.pack(pady=10)

    def charger_produits_par_categorie(self, id_categorie):
        for i in self.tree.get_children():
            self.tree.delete(i)

        produits = self.recuperer_produits_par_categorie(id_categorie)  # Utilisez 'self.' ici
        for p in produits:
            self.tree.insert('', 'end', values=p)

    def filtrer_produits(self, event):
        selected_categorie = self.combo_filtrer.get()
        if selected_categorie == "Toutes":
            self.charger_produits()
        else:
            id_categorie = [c[0] for c in recuperer_categories() if c[1] == selected_categorie][0]
            self.charger_produits_par_categorie(id_categorie)  # Utilisez 'self.' ici

    def recuperer_produits_par_categorie(self, id_categorie):  # Gardez cette méthode à l'intérieur de la classe
        conn = create_connexion()
        cursor = conn.cursor()
        query = "SELECT * FROM produit WHERE id_categorie = %s"
        cursor.execute(query, (id_categorie,))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

    def ajouter_nouveau_produit(self):
        nom = self.entry_nom.get()
        description = self.entry_description.get()
        prix = self.entry_prix.get()
        quantite = self.entry_quantite.get()
        id_categorie = recuperer_categories()[self.combo_categorie.current()][0]

        if nom and description and prix and quantite and id_categorie:
            try:
                ajouter_produit(nom, description, float(prix), int(quantite), id_categorie)
                self.charger_produits()
                self.entry_nom.delete(0, 'end')
                self.entry_description.delete(0, 'end')
                self.entry_prix.delete(0, 'end')
                self.entry_quantite.delete(0, 'end')
                self.combo_categorie.set('')
            except ValueError:
                messagebox.showerror("Erreur", "Veuillez entrer des valeurs valides pour le prix et la quantité")
        else:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs")

    def ouvrir_modifier_produit(self):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item)
            id_produit = item["values"][0]
            self.modifier_produit_dialogue = ModifierProduitDialogue(self, id_produit)
        else:
            messagebox.showerror("Erreur", "Veuillez sélectionner un produit à modifier")

    def ajouter_categorie(self,nom):
        conn = create_connexion()
        cursor = conn.cursor()
        query = "INSERT INTO categorie (nom) VALUES (%s)"
        cursor.execute(query, (nom,))
        conn.commit()
        cursor.close()
        conn.close()

    def ajouter_nouvelle_categorie(self):
        nom = self.entry_categorie_nom.get()
        if nom:
            self.ajouter_categorie(nom)  # Change this line
            self.entry_categorie_nom.delete(0, 'end')
            self.combo_categorie["values"] = [c[1] for c in recuperer_categories()]
            self.combo_filtrer["values"] = ["Toutes"] + [c[1] for c in recuperer_categories()]
        else:
            messagebox.showerror("Erreur", "Veuillez entrer un nom de catégorie")

    def charger_produits(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        produits = recuperer_produits()
        for p in produits:
            self.tree.insert('', 'end', values=p)

    def supprimer_produit(self):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item)
            supprimer_produit(item["values"][0])
            self.charger_produits()
        else:
            messagebox.showerror("Erreur", "Veuillez sélectionner un produit à supprimer")

    def exporter_csv(self):
        produits = recuperer_produits()
        with open("produits.csv", mode="w", newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(["ID", "Nom", "Description", "Prix", "Quantité", "ID Catégorie"])
            for p in produits:
                csv_writer.writerow([p[0], p[1], p[2], f"{p[3]:.2f}", p[4], p[5]])

        messagebox.showinfo("Succès", "Les produits ont été exportés avec succès dans le fichier produits.csv")





if __name__ == "__main__":
    app = GestionStockApp()
    app.mainloop()