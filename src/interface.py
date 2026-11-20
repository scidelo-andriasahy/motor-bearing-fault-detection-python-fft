import numpy as np
import math
import matplotlib.pyplot as mp
import tkinter as tk
from tkinter import ttk

def get_frequences_harmonique(f0,nb,fr,k):
    frequences=[]  # ligne pour frequence interieur ou exterieur
    coef=0.4
    for i in range(2):
        frequences+=[abs(f0+ ((-1)**i)*coef*nb*fr*k)]
    return frequences
def generer_signal(f0, nb, fr, k, nb_echantillon, Ts,ak, phik, snr_db1, snr_db2):
    # Générer le vecteur de temps
    l=1 #on prend l=1 donc les ak et phik sont de taille 3
    t_list = np.arange(0, nb_echantillon) * Ts
    f_harm=get_frequences_harmonique(f0, nb, fr, k)
    fk=[f_harm[0],f0,f_harm[1]]
    # Générer le signal sain
    signal_sain = np.cos((2 * np.pi * f0 * t_list) + phik[1]) * ak[1]
    
    # Générer le signal clair (défectueux)
    signal_clair = []
    for t in t_list:
        somme = 0
        for k in range((2*l)+1 ):
            somme += ak[k] * math.cos((2 * math.pi * fk[k] * t) + phik[k])
        signal_clair.append(somme)
    
    # Ajouter du bruit aux signaux défectueux
    n = np.random.randn(len(signal_clair))
    snr_lineaire1 = 10 ** (snr_db1 / 10)
    snr_lineaire2 = 10 ** (snr_db2 / 10)
    Es = sum([x**2 for x in signal_clair])
    En = sum([x**2 for x in n])
    alpha1 = math.sqrt(Es / (snr_lineaire1 * En))
    alpha2 = math.sqrt(Es / (snr_lineaire2 * En))
    signal_defectueux1 = signal_clair + alpha1 * n
    signal_defectueux2 = signal_clair + alpha2 * n
    return t_list, signal_sain, signal_defectueux1, signal_defectueux2

def enregistrer_sur_fichier(t_list,signalSain,signalDefectueux1,signalDefectueux2):
    
    with open("signal.txt","w") as fichier:
        for i in range(len(t_list)) :
            fichier.write(f"{t_list[i]};{signalSain[i]};{signalDefectueux1[i]};{signalDefectueux2[i]}\n")
def calculer_FFT(signal1,signal2, fs): 
    n= len(signal1) 
    freq = np.fft.fftfreq(n, d=1/fs) 
    transformee_fourier1 = np.fft.fft(signal1) 
    magnitude1 = np.abs(transformee_fourier1) 
    
    transformee_fourier2 = np.fft.fft(signal2) 
    magnitude2 = np.abs(transformee_fourier2) 
    return freq, magnitude1,magnitude2

def les_courbes(t, signal_sain, signal_def1,signal_def2,f,amp_TFF_def1,amp_TFF_def2): 
    # Créer une figure avec deux sous-graphes côte à côte 
    fig, axs = mp.subplots(2, 2, figsize=(12, 6)) 
    # Premier sous-graphe 
   
    axs[0][0].plot(t,signal_sain, color='blue')
    axs[0][0].set_xlim(0,0.1)
    axs[0][0].set_ylim(-30,30)
    axs[0][0].set_xlabel('temps') 
    axs[0][0].set_ylabel('Val du signal sain') 
    axs[0][0].set_title('Signal sain') 
    axs[0][0].grid(True) 
    # Deuxième sous-graphe 
    axs[0][1].plot(t, signal_def1, label='SNR=0 dB', color='red') 
    axs[0][1].plot(t, signal_def2, label='SNR=50 dB', color='green',linestyle="--") 
    axs[0][1].set_xlim(0,0.1)
    axs[0][1].set_xlabel('temps') 
    axs[0][1].set_ylabel('Val du signal def ') 
    axs[0][1].set_title('Signal defectueux') 
    axs[0][1].legend() 
    axs[0][1].grid(True) 
    
    axs[1][0].plot(f,amp_TFF_def1, color='green')
    axs[1][0].set_xlim(0,400)
    axs[1][0].set_xlabel('frequence') 
    axs[1][0].set_ylabel('Amplitude') 
    axs[1][0].set_title('Signal TFF pour SNR=0 dB') 
    axs[1][0].grid(True) 
    # Deuxième sous-graphe 
    axs[1][1].plot(f,amp_TFF_def2, color='red') 
    axs[1][1].set_xlim(0,400)
    axs[1][1].set_xlabel('frequence') 
    axs[1][1].set_ylabel('Amplitude') 
    axs[1][1].set_title('Signal TFF pour SNR=50 dB') 
    axs[1][1].grid(True) 
    # Ajustement pour une meilleure mise en page 
    mp.tight_layout()  
    mp.show()

def run_simulation():
    f0v = float(f0.get())
    frv = float(fr.get())
    nbv = int(nb.get())
    a0v = float(a0.get())
    a1v = float(ap1.get())
    a_minus1v = float(an1.get())
    ak=[a_minus1v,a0v,a1v]
    Fsv = int(fs.get())
    phikv=[ float(phik.get()) for i in range(3)]
    nv = int(n.get())
    snr1v = float(snr1.get())
    snr2v = float(snr2.get())
    kv=int(k.get())
    t_list, signal_sain, signal_def1, signal_def2=generer_signal(f0v, nbv, frv, kv, nv, 1/Fsv, ak, phikv, snr1v, snr2v)
    enregistrer_sur_fichier( t_list, signal_sain, signal_def1, signal_def2)
    freq, magnitude1,magnitude2=calculer_FFT(signal_def1,signal_def2,Fsv)
    les_courbes(t_list,signal_sain,signal_def1,signal_def2,freq,magnitude1,magnitude2)
    
# Créer la fenêtre principale
root = tk.Tk()
root.title("Étude d'un défaut de roulement")
root.geometry("1100x500")
root.configure(bg="lightblue")
root.resizable(False, False)

# Créer les sections dans un cadre principal
main_frame = tk.Frame(root, bg="lightblue")
main_frame.pack(fill="both", expand=True, padx=20, pady=20)

# Créer une section pour les fréquences et phases
freq_phase_frame = tk.LabelFrame(main_frame, text="Fréquences et Phases", bg="lightblue", font=("Arial", 14))
freq_phase_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# Ajouter les widgets dans la section des fréquences et phases
tk.Label(freq_phase_frame, text="Entrez la fréquence d'alimentation électrique fo :", bg="lightblue", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5, sticky="w")
f0 = tk.Entry(freq_phase_frame)
f0.grid(row=0, column=1, padx=10, pady=5)

tk.Label(freq_phase_frame, text="Entrez la fréquence du rotor fr :", bg="lightblue", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5, sticky="w")
fr = tk.Entry(freq_phase_frame)
fr.grid(row=1, column=1, padx=10, pady=5)

tk.Label(freq_phase_frame, text="Entrez la valeur de la phase phiK :", bg="lightblue", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5, sticky="w")
phik = tk.Entry(freq_phase_frame)
phik.grid(row=2, column=1, padx=10, pady=5)

tk.Label(freq_phase_frame, text="Entrez le nombre entier K :", bg="lightblue", font=("Arial", 12)).grid(row=3, column=0, padx=10, pady=5, sticky="w")
k = tk.Entry(freq_phase_frame)
k.grid(row=3, column=1, padx=10, pady=5)

# Créer une section pour les fréquences électriques
elec_freq_frame = tk.LabelFrame(main_frame, text="Fréquences Électriques", bg="lightblue", font=("Arial", 14))
elec_freq_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

# Ajouter les widgets dans la section des fréquences électriques
tk.Label(elec_freq_frame, text="Entrez la fréquence d'échantillonnage fs :", bg="lightblue", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5, sticky="w")
fs = tk.Entry(elec_freq_frame)
fs.grid(row=0, column=1, padx=10, pady=5)

# Créer une section pour les paramètres de roulement
bearing_frame = tk.LabelFrame(main_frame, text="Paramètres de Roulement", bg="lightblue", font=("Arial", 14))
bearing_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

# Ajouter les widgets dans la section des paramètres de roulement
tk.Label(bearing_frame, text="Entrez le nombre d'échantillon n :", bg="lightblue", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5, sticky="w")
n = tk.Entry(bearing_frame)
n.grid(row=0, column=1, padx=10, pady=5)

tk.Label(bearing_frame, text="Entrez le nombre de billes du roulement nb :", bg="lightblue", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5, sticky="w")
nb = tk.Entry(bearing_frame)
nb.grid(row=1, column=1, padx=10, pady=5)

# Créer une section pour les amplitudes et SNR
amp_snr_frame = tk.LabelFrame(main_frame, text="Amplitudes et SNR", bg="lightblue", font=("Arial", 14))
amp_snr_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

# Ajouter les widgets dans la section des amplitudes et SNR
tk.Label(amp_snr_frame, text="Entrez la valeur de l'amplitude a-1 :", bg="lightblue", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5, sticky="w")
an1 = tk.Entry(amp_snr_frame)
an1.grid(row=0, column=1, padx=10, pady=5)

tk.Label(amp_snr_frame, text="Entrez la valeur de l'amplitude a0 :", bg="lightblue", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5, sticky="w")
a0 = tk.Entry(amp_snr_frame)
a0.grid(row=1, column=1, padx=10, pady=5)

tk.Label(amp_snr_frame, text="Entrez la valeur de l'amplitude a1 :", bg="lightblue", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5, sticky="w")
ap1 = tk.Entry(amp_snr_frame)
ap1.grid(row=2, column=1, padx=10, pady=5)

tk.Label(amp_snr_frame, text="Entrez la valeur du premier SNR :", bg="lightblue", font=("Arial", 12)).grid(row=3, column=0, padx=10, pady=5, sticky="w")
snr1 = tk.Entry(amp_snr_frame)
snr1.grid(row=3, column=1, padx=10, pady=5)

tk.Label(amp_snr_frame, text="Entrez la valeur du deuxième SNR :", bg="lightblue", font=("Arial", 12)).grid(row=4, column=0, padx=10, pady=5, sticky="w")
snr2 = tk.Entry(amp_snr_frame)
snr2.grid(row=4, column=1, padx=10, pady=5)

# Ajouter un bouton de validation avec un style moderne
style = ttk.Style()
style.configure("TButton", font=("Arial", 14), foreground="black")

bouton = ttk.Button(main_frame, text="VALIDER", style="TButton", command=run_simulation)
bouton.grid(row=2, column=0, columnspan=2, pady=20)

# Démarrer la boucle principale
root.mainloop()
