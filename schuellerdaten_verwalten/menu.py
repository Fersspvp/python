import tkinter
from tkinter import font, scrolledtext, messagebox, ttk, Menu







#make window
root = tkinter.Tk()

scrolltext_widget = None
#refresh the screen so it doesnt bug out dont delete
def clear_screen():
    for widget in root.winfo_children():
        if not isinstance(widget, tkinter.Menu):
            widget.destroy()






#admin login
def adminlogin():
    get_admin_passwords_and_usernames()
    clear_screen()
    global admin_password_entry
    global admin_entry
    username_label = tkinter.Label(root, text="username:")
    username_label.pack()
    admin_entry = tkinter.Entry(root)
    admin_entry.pack()
    admin_password_label = tkinter.Label(root, text="password")
    admin_password_label.pack()
    admin_password_entry = tkinter.Entry(root, show="*")
    admin_password_entry.pack()
    submit_button = tkinter.Button(root, text="Submit", command=submitt_for_admin)
    submit_button.pack()




def get_admin_passwords_and_usernames():
    global usernames_and_passwords_from_admin_file
    with open("admin_usernames_and_passwords.txt", "r") as f:
        usernames_and_passwords_from_admin_file = f.read()
        print(usernames_and_passwords_from_admin_file)


def submitt_for_admin():
    global admin_username_menu
    admin_username_menu = admin_entry.get()
    password = admin_password_entry.get()
    print(admin_username_menu,password)
    if usernames_and_passwords_from_admin_file == "ferdinand ferdinand123" and password:
        succesfull_login_admin()



def succesfull_login_admin():
    clear_screen() 
    if not root.cget("menu"): 
        menubar = Menu(root)
        root.config(menu=menubar)
        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(label="schliessen", command=root.destroy)
        menubar.add_cascade(label="Suche", menu=file_menu)
        sub_menu = Menu(file_menu, tearoff=0)
        sub_menu.add_command(label="jahrgang suchen", command=ganzer_jahrgang)
        sub_menu.add_command(label="SuS suchen", command=SuSsuchen)
        sub_menu.add_command(label="SuS daten bearbeiten", command=SuS_daten_bearbeiten)
        file_menu.add_cascade(label="Suchen", menu=sub_menu)
    root.geometry("500x500")
    welcome_label = tkinter.Label(root, text=f"Willkommen, {admin_username_menu}!",font=("Arial", 16, "bold"))
    welcome_label.pack(pady=50)














#jahrgangs daten

def ganzer_jahrgang():
    clear_screen()
    global jahrgang_eingabe
    ssl = tkinter.Label(root, text="Name des Schülers/der Schülerin:")
    ssl.pack()
    jahrgang_eingabe = tkinter.Entry(root)
    jahrgang_eingabe.pack()
    submitt_button_for_jahrgans_suche = tkinter.Button(root, text="Suchen", command=jahrgang_suchen)
    submitt_button_for_jahrgans_suche.pack()

def jahrgang_suchen():
    global jahrgang
    jahrgang = jahrgang_eingabe.get()
    with open(f"SCHUELERDATEN_PROJEKT_NEU/JAHRGANG_{jahrgang}/schueller_des_jahrgangs.txt", "r") as f:
        schueller_des_jahrgangs_daten = f.read()
        clean_schueller_des_jahrgangs = schueller_des_jahrgangs_daten.strip()
    global scrolltext_widget
    if scrolltext_widget:
        scrolltext_widget.destroy()
    scrolltext_widget = scrolledtext.ScrolledText(root, wrap=tkinter.WORD, width=50, height=15,font=('Consolas', 10), padx=10, pady=10)
    scrolltext_widget.pack(padx=10, pady=10, fill=tkinter.BOTH, expand=True)
    scrolltext_widget.delete('1.0', tkinter.END) 
    scrolltext_widget.insert(tkinter.END,  clean_schueller_des_jahrgangs) 
    scrolltext_widget.config(state='disabled')
        









#SuS daten

def SuS_daten_bearbeiten():
    print("idk cuh do it yourself or smth tbh")



def SuSsuchen():
    clear_screen()
    global schueller_suchen_eingabe
    global schueller_suchen_jahrgang_eingabe
    global schueller_suchen_klasse_eingabe
    ssl = tkinter.Label(root, text="Name des Schülers*in:")
    ssl.pack()
    schueller_suchen_eingabe = tkinter.Entry(root)
    schueller_suchen_eingabe.pack()
    ssl2 = tkinter.Label(root, text="Jahrgang von 5 bis 11:")
    ssl2.pack()
    schueller_suchen_jahrgang_eingabe = tkinter.Entry(root)
    schueller_suchen_jahrgang_eingabe.pack()
    ssl3 = tkinter.Label(root, text="Klasse a, b, c, d:")
    ssl3.pack()
    schueller_suchen_klasse_eingabe = tkinter.Entry(root)
    schueller_suchen_klasse_eingabe.pack()
    submit_button = tkinter.Button(root, text="Suchen", command=SuS_daten_suchen)
    submit_button.pack(pady=10)



def SuS_daten_suchen():
    global bereinigter_text
    global jahrgang_des_schuellers
    global name_des_schuellers
    global klasse_des_schuellers
    jahrgang_des_schuellers = schueller_suchen_jahrgang_eingabe.get()
    name_des_schuellers = schueller_suchen_eingabe.get()
    klasse_des_schuellers = schueller_suchen_klasse_eingabe.get()
    file_path = f"Schuelerdaten_Projekt_Neu/Jahrgang_{jahrgang_des_schuellers}/Klasse_{klasse_des_schuellers.upper()}/{name_des_schuellers.upper()}.txt"
    with open(file_path, "r", encoding="utf-8") as f:
        daten_SuS_from_file = f.read()
        bereinigter_text = daten_SuS_from_file.replace("{", "").replace("}", "").replace("#", "").strip()
        SuS_daten_anzeigen_admin()





def SuS_daten_anzeigen_admin():
    global scrolltext_widget
    if scrolltext_widget:
        scrolltext_widget.destroy()
    scrolltext_widget = scrolledtext.ScrolledText(root, wrap=tkinter.WORD, width=50, height=15,font=('Consolas', 10), padx=10, pady=10)
    scrolltext_widget.pack(padx=10, pady=10, fill=tkinter.BOTH, expand=True)
    scrolltext_widget.delete('1.0', tkinter.END) 
    scrolltext_widget.insert(tkinter.END, bereinigter_text) 
    scrolltext_widget.config(state='disabled')


adminlogin()


root.mainloop()
