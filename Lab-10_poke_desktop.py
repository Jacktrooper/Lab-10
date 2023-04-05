import poke_api
import image_lib
from tkinter import *
from tkinter import ttk
import os
import ctypes


# Get the path of the script and its parent directory
script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)
image_cache_dir = os.path.join(script_dir, 'images')

# Make the image cache foled if it does not alrady exist
if not os.path.isdir(image_cache_dir):
    os.makedirs(image_cache_dir)

## Create the main window
root = Tk()
root.title("Shiny Pokemon Image Viewer") 
root.minsize(500, 600)


ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('COMP593.PokeImageViewer')
icon_path = os.path.join(script_dir, 'Master-Ball.ico')
root.iconbitmap(icon_path)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)


# create the frame
frame = ttk.Frame(root)
frame.grid(row=0, column=0, padx=10, pady=10, sticky=NSEW)
frame.columnconfigure(0, weight=1)
frame.rowconfigure(0, weight=1)


# add the image to the frame
img_poke = PhotoImage(file=os.path.join(script_dir, 'MasterBall.png'))
lbl_poke_image = ttk.Label(frame, image=img_poke)
lbl_poke_image.grid(row=0, column=0)


# Add the Pokemon names pull-down list 
pokemon_name_list = sorted(poke_api.get_pokemon_names())
cbox_poke_names = ttk.Combobox(frame, values=pokemon_name_list, state='readonly')
cbox_poke_names.set("Select a Pokemon")
cbox_poke_names.grid(row=1, column=0, padx=10, pady=10)


def handle_pokemon_sel(event):
    
    # get the name of the selected Pokemon
    pokemon_name = cbox_poke_names.get()
    
    # download and save the artwork for the pokemon
    global imgae_path
    imgae_path = poke_api.download_pokemon_artwork(pokemon_name, image_cache_dir)
    
    # display the pokeon artwork
    if imgae_path is not None:
        img_poke['file'] = imgae_path
    btn_set_desktop.state(['!disabled'])

cbox_poke_names.bind('<<ComboboxSelected>>', handle_pokemon_sel)


def btn_Set_Desktop():
    backround_image = image_lib.set_desktop_background_image(imgae_path)


# Button that sets the desktop as the seceled pokemon
btn_set_desktop = ttk.Button(frame, text='Set as Desktop Image', command=btn_Set_Desktop, state=DISABLED)
btn_set_desktop.grid(row=2, column=0, padx=10, pady=10)



root.mainloop()
