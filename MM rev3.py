# Created by chinchill (discord) please do not reupload, copy, change, modify without my consent, thanks :)
import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter import *
from ttkthemes import ThemedStyle
import threading
from tqdm import tqdm
import time

app = tk.Tk()
app.title("GTA V Mod Mover")
app.resizable(False, False)


MODS_TO_EXCLUDE = set([
    "x64a.rpf", "x64b.rpf", "x64c.rpf", "x64d.rpf", "x64e.rpf", "x64f.rpf", "x64g.rpf", "x64h.rpf",
    "x64i.rpf", "x64j.rpf", "x64k.rpf", "x64l.rpf", "x64m.rpf", "x64n.rpf", "x64o.rpf", "x64p.rpf",
    "x64q.rpf", "x64r.rpf", "x64s.rpf", "x64t.rpf", "x64u.rpf", "x64v.rpf", "x64w.rpf", "x64x.rpf",
    "x64y.rpf", "x64z.rpf", "common.rpf", "GTA5.exe", "GTAVLanguageSelect.exe", "GTAVLauncher.exe",
    "bink2w64.dll", "d3dcompiler.dll", "d3dcsx.dll", "GFSDK_ShadowLib.win64.dll", "GFSDK_TXAA.win64.dll",
    "GFSDK_TXAA_AlphaResolve.win64.dll", "GPUPerfAPIDX11-x64.dll", "NvPmApi.Core.win64.dll", "version.txt",
    "index.bin", "d3dcompiler_46.dll", "d3dcsx_46.dll", "PlayGTAV.exe", "uninstall.exe",
])

FOLDERS_TO_EXCLUDE = set(["ReadMe", "Redistributables", "update", "x64"])

# Translations
translations = {
    "en": {
        "title": "GTA V Mod Mover",
        "source_folder": "Game Folder (or folder with mods):",
        "destination_folder": "Destination Folder:",
        "move_button": "Move Mods",
        "author": "Author: chinchill (Discord) please do not reupload, thank you",
        "success_message": "Mods have been moved.",
        "select_game_folder": "Select Game Folder",
        "select_destination_folder": "Select Destination Folder",
        "success": "Success!",
    
    },
    "pl": {
        "title": "Przenośnik módów GTA V",
        "source_folder": "Folder gry (lub folder z modami):",
        "destination_folder": "Folder do którego będą przenoszone mody:",
        "move_button": "Przenieś mody",
        "author": "      Autor: chinchill (Discord) nie reuploadować, dziękuję",
        "success_message": "Mody zostały przeniesione.",
        "select_game_folder": "Wybierz folder z GTA V",
        "select_destination_folder": "Wybierz folder docelowy",
        "success": "Sukces!",
    
    },
}
current_language = "en"  # Default language


def select_gta_v_directory():
    gta_v_directory = filedialog.askdirectory(title=translations[current_language]["select_game_folder"])
    if gta_v_directory:
        gta_v_entry.delete(0, tk.END)
        gta_v_entry.insert(0, gta_v_directory)

def select_destination_directory():
    destination_directory = filedialog.askdirectory(title=translations[current_language]["select_destination_folder"])
    if destination_directory:
        destination_entry.delete(0, tk.END)
        destination_entry.insert(0, destination_directory)

def move_mod(mod, src_directory, dst_directory, pbar):
    src_path = os.path.join(src_directory, mod)
    dst_path = os.path.join(dst_directory, mod)

    try:
        shutil.move(src_path, dst_path)
    except PermissionError:
        messagebox.showerror("Error", f"Cannot move mod '{mod}'. Permission denied. Set correct folder permissions.")
        return False
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while moving mod '{mod}': {str(e)}")
        return False

    return True

def move_mods(mods, src_directory, dst_directory, pbar):
    for mod in mods:
        if not move_mod(mod, src_directory, dst_directory, pbar):
            return False

        time.sleep(0.05)  # Introduce a 50ms delay between each move operation
        pbar.set(pbar.get() + 1)  # Update the progress bar

    return True

def move_mods_async_handler():
    gta_v_directory = gta_v_entry.get()
    destination_directory = destination_entry.get()

    if not os.path.isdir(destination_directory):
        messagebox.showerror("Error", translations[current_language]["select_destination_folder"])
        return

    mods = os.listdir(gta_v_directory)
    mods_to_move = [mod for mod in mods if mod not in MODS_TO_EXCLUDE and mod not in FOLDERS_TO_EXCLUDE]

    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(app, mode="determinate", variable=progress_var, maximum=len(mods_to_move))
    progress_bar.place(x=20, y=146, width=270, height=8)

    move_thread = threading.Thread(target=move_mods, args=(mods_to_move, gta_v_directory, destination_directory, progress_var))
    move_thread.start()

    # Display the success message and stop the progress bar after moving is complete
    def show_success_message():
        move_thread.join()

        if progress_var.get() == progress_bar['maximum']:
            messagebox.showinfo(translations[current_language]["success"], translations[current_language]["success_message"])

        progress_bar.stop()

    success_thread = threading.Thread(target=show_success_message)
    success_thread.start()

def switch_to_english():
    global current_language
    current_language = "en"
    update_language()

def switch_to_polish():
    global current_language
    current_language = "pl"
    update_language()

def update_language():
    app.title(translations[current_language]["title"])
    source_folder_label.config(text=translations[current_language]["source_folder"])
    destination_folder_label.config(text=translations[current_language]["destination_folder"])
    move_mods_button.config(text=translations[current_language]["move_button"])
    author_label.config(text=translations[current_language]["author"])

app.configure(bg="#2b2b2b")
style = ThemedStyle(app)
style.set_theme("equilux")

app.geometry("310x200")

# The create_transparent_label function
def create_transparent_label(parent, x, y, text):
    label = tk.Label(parent, text=text, bg="#2b2b2b", fg="white")
    label.place(x=x, y=y)
    return label

# English Button
english_button = ttk.Button(app, text="EN", command=switch_to_english, width=3)
english_button.place(x=275, y=158)

# Polish Button
polish_button = ttk.Button(app, text="PL", command=switch_to_polish, width=3)
polish_button.place(x=5, y=158)

source_folder_label = create_transparent_label(app, 20, 5, translations[current_language]["source_folder"])
destination_folder_label = create_transparent_label(app, 20, 60, translations[current_language]["destination_folder"])

gta_v_entry = tk.Entry(app, width=40)
gta_v_entry.place(x=20, y=25)
select_gta_v_button = ttk.Button(app, text="...", command=select_gta_v_directory, width=1.5)
select_gta_v_button.place(x=270, y=24)

destination_entry = tk.Entry(app, width=40)
destination_entry.place(x=20, y=80)
select_destination_button = ttk.Button(app, text="...", command=select_destination_directory, width=1.5)
select_destination_button.place(x=270, y=79.4)

move_mods_button = ttk.Button(app, text=translations[current_language]["move_button"], command=move_mods_async_handler)
move_mods_button.place(x=100, y=110)

select_gta_v_button["padding"] = (3, -1)
select_destination_button["padding"] = (3, -1)
move_mods_button["padding"] = (20, 5)
polish_button["padding"] = (1, -1)
english_button["padding"] = (1, -1)

author_label = tk.Label(app, text=translations[current_language]["author"], bg="#2b2b2b", fg="white", font=("Helvetica", 8))
author_label.place(x=5, y=180) #162

app.mainloop()
