import tkinter as tk
import pyttsx3
import pickle

import numpy as np
import pandas as pd

df=pickle.load(open('model.pkl','rb'))
similarity=pickle.load(open('similarity.pkl','rb'))

def find_index(text):  # to find the index of the
    text=text.lower()
    t_list=text.split(' ')
    c=0
    for i in df['Description']:
        for element in t_list:
            if element not in i:
                c=c+1
                break
            else:
                return c+1
    return []

def recommend(med):
    id=find_index(med)
    dis=similarity[id]
    med_list=sorted(list(enumerate(dis)),reverse=True,key=lambda x:x[1])[1:6]
    c=1
    recommended_medis=[]
    for i in med_list:
        recommended_medis.append(df.iloc[i[0]].Drug_Name)
    return recommended_medis

class RecommendationApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Medicine Recommender")
        self.master.iconbitmap('icon_med.ico')

        self.label=tk.Label(self.master, text="Enter your Symptoms:",font=('Arial', 12))
        self.label.pack(side=tk.TOP, padx=10, pady=10)

        self.frame = tk.Frame(self.master)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Create label for showing camera footage
        self.entry = tk.Entry(self.frame,font=('Cambria', 20))
        self.entry.pack(side=tk.TOP, padx=10, pady=10)


        # Create button to capture and save image
        self.submit_button = tk.Button(self.frame, text="Submit",command=self.show_list)
        self.submit_button.pack(side=tk.TOP, padx=10, pady=10)


        # Create frame for text output canvas and speak button
        self.text_frame = tk.Frame(self.frame)
        self.text_frame.pack(side=tk.TOP, padx=10, pady=10)

        self.label2 = tk.Label(self.text_frame, text="Recommended Medicines:",font=('Arial', 12),anchor="w")
        self.label2.pack(side=tk.TOP, padx=10, pady=10)
        # Create canvas for text output
        self.text_label = tk.Label(self.text_frame, text="Thinking..", width=40, height=12,bd = 2,bg='white'
                                   ,highlightthickness  = 1, highlightbackground = 'white'
                                   ,font=('Times New Roman', 10))
        self.text_label.pack(side=tk.TOP,padx=10, pady=10)

        # Create button to speak text
        self.speak_button = tk.Button(self.text_frame, text="Speak", command=self.speak_text)
        self.speak_button.pack(side=tk.TOP,padx=10, pady=10)

    def show_list(self):
        # Get the text from the entry widget
        text = self.entry.get()
        med_list=recommend(text)
        ans=""
        c=1
        for i in med_list:
            ans=ans+str(c) +". "+str(i)+'\n'+'\n'
            c=c+1
        self.text_label.configure(text=ans,anchor="w")


    # Define function to speak text
    def speak_text(self):
        # Get the text from the canvas
        text = self.text_label.cget("text")
        # Initialize a text-to-speech engine
        #text="Hala Madrid"
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        # Speak the text
        engine.say(text)
        engine.runAndWait()

if __name__ == "__main__":
    root = tk.Tk()
    app = RecommendationApp(root)
    root.mainloop()
