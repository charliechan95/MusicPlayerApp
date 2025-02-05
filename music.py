from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog
import pygame
import os 
from pygame import mixer
import tkinter.messagebox
mixer.init()
import glob
import time


class musicplayer:
    def __init__(self, Tk):
        pygame.mixer.init() 
        self.root=Tk
        self.root.title('Music_Player')
        self.root.geometry('700x400')
        self.background_image = Image.open('sunrise.jpg')
        self.background_image = self.background_image.resize((700, 400), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.background_image)
        self.bg_label = Label(self.root, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.label=Label(text='Charlie Music', bg='black', fg='white', font=40).place(x=40, y=350)
        self.label1=Label(self.root, text='Music is Playing', bg='black', fg='white')
        self.label1.pack(side=BOTTOM, fill=X)
        
        self.music_folder = None
        self.loop_enabled = False
                 # Variable to manage loop state
        self.is_paused = False
        self.current_song_index = 0
        self.music_folder = None
        self.songs_loaded_from_folder = False


        
       

   

                                                             


        original_image = Image.open('handpan.jpg')
        resized_image = original_image.resize((300, 300))  # Resize to 200x200 pixels
        self.photo = ImageTk.PhotoImage(resized_image)

        #add img
        
        photo_label = Label(self.root, image=self.photo)
        photo_label.place(x=10, y=20)

        
  


     


        #add play button
        self.button_image = Image.open('play.png')
        self.button_image = self.button_image.resize((60, 60), Image.LANCZOS)
        self.button = ImageTk.PhotoImage(self.button_image)
        self.play_button = Button(self.root, image=self.button, bd=0, bg='white', command=self.play_music)
        self.play_button.place(x=330, y=280) 

        #add pause button
        self.button_image1 = Image.open('Pause.png')
        self.button_image1 = self.button_image1.resize((60, 60), Image.LANCZOS)
        self.button1 = ImageTk.PhotoImage(self.button_image1)
        self.pause_button = Button(self.root, image=self.button1, bd=0, bg='white', command=self.pausemusic)
        self.pause_button.place(x=400, y=280)

        #add stop_button
        self.button_image2 = Image.open('stop.png')
        self.button_image2 = self.button_image2.resize((60, 60), Image.LANCZOS)
        self.button2 = ImageTk.PhotoImage(self.button_image2)
        self.stop_button = Button(self.root, image=self.button2, bd=0, bg='white', command=self.stop_music)
        self.stop_button.place(x=470, y=280)
        def About():
            tkinter.messagebox.showinfo('About', 'music player created by Charlie')


        #loop button

        self.loop_button = Button(self.root, text='Loop', bg='white', command=self.toggle_loop)
        self.loop_button.place(x=540, y=280)


        #Menu

        self.menubar=Menu(self.root)
        self.root.configure(menu=self.menubar)
        self.submenu=Menu(self.menubar)
        self.menubar.add_cascade(label='File', menu=self.submenu)
        self.submenu.add_command(label='Open', command=self.open_file)
        self.submenu.add_command(label='Exit', command=self.root.destroy)

        self.submenu2=Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='help', menu=self.submenu2)
        self.submenu2.add_command(label='About', command=About)
        self.filename=None 

        #Playlist listbox
        self.playlist = Listbox(self.root, bg='pink', fg='black', width=30, height=10)
        self.playlist.place(x=350, y=60)
        self.playlist.bind('<<ListboxSelect>>', self.on_playlist_select)

        #create playlist button
        self.folder_button = Button(self.root, text='Select Music Folder', command=self.select_folder, bg='white')
        self.folder_button.place(x=400, y=10)

        #progress bar
        self.progress_bar = Scale(self.root, from_=0, to=100, orient=HORIZONTAL, length=350, bg='black', fg='white', sliderlength=20, command=self.seek_music)
        self.progress_bar.place(x=340, y=235)
        self.root.after(100, self.check_music_end)

    def select_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.music_folder = folder_path
            self.load_songs(folder_path)

    def load_songs(self, folder_path):
        # Clear the current playlist
        self.stop_music()
        self.playlist.delete(0, END)
        self.music_folder = folder_path
        self.songs_loaded_from_folder = True

        # Load all audio files from the selected folder
        for file in glob.glob(os.path.join(folder_path, '*.mp3')) + glob.glob(os.path.join(folder_path, '*.wav')):
            self.playlist.insert(END, os.path.basename(file))
        if self.playlist.size() > 0:
            self.playlist.select_set(0) 
            self.current_song_index = 0
            
            

    def on_playlist_select(self, event):
        if self.music_folder and self.playlist.size() > 0:
            self.play_music()
        else:
            self.label1['text'] = 'Song is selected.' 
             # Only play music if song is selected




    def open_file(self):
            
        self.filename = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav")])
        if self.filename:
            if os.path.isfile(self.filename):  # Check if a file was selected
                self.label1['text'] = f'Selected: {os.path.basename(self.filename)}'
                self.playlist.delete(0, END)
                self.playlist.insert(END, os.path.basename(self.filename))
                self.music_folder = None  # Reset music folder if necessary
                self.songs_loaded_from_folder = False  #
            else:
                tkinter.messagebox.showerror("Error", "Selected file does not exist.")

    def update_progress_bar(self):
        if pygame.mixer.music.get_busy() and not self.is_paused:
        # Get the current position in seconds
            current_pos = pygame.mixer.music.get_pos() / 1000
        # Get the total length of the song in seconds
            total_length = pygame.mixer.Sound(self.filename).get_length() if self.filename else 0
        
        # Update the progress bar
            if total_length > 0:
                self.progress_bar.set((current_pos / total_length) * 100)

        # Call this function again after 1 second
        self.root.after(1000, self.update_progress_bar)

    def seek_music(self, value):

    # Seek to the position in the song indicated by the progress bar
        try:
            if self.filename:  # Ensure a file is loaded
               total_length = pygame.mixer.Sound(self.filename).get_length()
               seek_position = (int(value) / 100) * total_length
               pygame.mixer.music.play(start=seek_position)  # Seek to the new position
        except Exception as e:
            print(f"Error seeking music: {e}")


        
       

    def play_music(self):

        # Define the action when the play button is clicked
        print("Play music")
        selected_song_index = self.playlist.curselection() 

        
        


        if not selected_song_index:
                
                selected_song_index = (self.current_song_index,)  # Ensure it's a tuple

                
                self.label1['text'] = 'No song selected to play.'
                return 
        self.current_song_index = selected_song_index[0]


        
        
    

    
    
        
        if self.playlist.size() == 0:
            self.label1['text'] = 'No songs in the playlist.'
            return
        
    

      
  
      
            
        



        
  
        

        


        if self.music_folder:
            song_name = self.playlist.get(selected_song_index)
            full_path = os.path.join(self.music_folder, song_name)
            self.label1['text'] = 'Song is playing.'
            
        else: 
            self.filename
            full_path = self.filename
            

            
      
            
            
            

    
            
        

        try:
            pygame.mixer.music.load(full_path) 
            pygame.mixer.music.stop() # Load the selected song
            pygame.mixer.music.play()
              # Play the song
            self.label1['text'] = f'Playing: {os.path.basename(full_path)}'
            
            self.is_paused = False
            


            
      
               
 
                
        except pygame.error as e:
            self.label1['text'] = f'Error playing song: {e}'
        else:
            self.label1['text'] = 'Please select a song from the playlist.'




        if self.filename:
     


            pygame.mixer.music.load(self.filename) 
            pygame.mixer.music.play() 
            self.label1['text']='Music is Playing'
        else:
            self.label1['text'] = 'Please select a music file first.'
            
        
    def pausemusic(self):
        pygame.mixer.music.pause()
        self.label1['text']='music is paused'
        self.is_paused = True
        
        
    def stop_music(self):
        pygame.mixer.music.stop()
        self.label1['text']='music stopped'
        self.is_paused = False 
        self.playlist.delete(0, END)


    def toggle_loop(self):
        self.loop_enabled = not self.loop_enabled  # Toggle the loop state
        if self.loop_enabled:
            self.label1['text'] += ' | Looping Enabled'
        else:
            self.label1['text'] = self.label1['text'].replace(' | Looping Enabled', '')

    def check_music_end(self):
        if not pygame.mixer.music.get_busy() and self.loop_enabled:
            self.play_music()


       # Restart the music if looping is enabled
        self.root.after(100, self.check_music_end) 





root=Tk()
obj=musicplayer(root)

root.mainloop()