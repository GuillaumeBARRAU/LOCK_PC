import cv2
import time
import threading
import os  # Pour exécuter la commande de verrouillage
from pynput import mouse, keyboard

# Variable pour garder trace de la dernière activité
last_activity_time = time.time()
running = True  # Pour contrôler l'exécution des threads

# Fonction pour prendre une photo
def take_photo():
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    if ret:
        filename = f"photo_{int(time.time())}.jpg"
        cv2.imwrite(filename, frame)
        print(f"Photo taken and saved as {filename}")
    cam.release()

# Fonction qui surveille l'inactivité
def monitor_inactivity():
    global last_activity_time, running
    while running:
        current_time = time.time()
        if current_time - last_activity_time >= 10:  # Inactif pendant 10 secondes
            print("No activity detected for 10 seconds. Waiting for interaction...")
            while running:
                # Attendre l'interaction
                current_time = time.time()
                if current_time - last_activity_time < 10:  # Une activité a été détectée
                    print("Activity detected, taking photo...")
                    take_photo()
                    break  # Quitte la boucle après avoir pris la photo

            # Après avoir pris la photo, verrouille le PC
            os.system("rundll32.exe user32.dll,LockWorkStation")  # Verrouille le PC
            time.sleep(5)  # Petite pause avant de reprendre la surveillance
        time.sleep(1)

# Fonction pour réinitialiser le timer d'inactivité lors de l'activité de la souris
def on_move(x, y):
    global last_activity_time
    last_activity_time = time.time()

def on_click(x, y, button, pressed):
    global last_activity_time
    last_activity_time = time.time()

def on_scroll(x, y, dx, dy):
    global last_activity_time
    last_activity_time = time.time()

# Fonction pour réinitialiser le timer d'inactivité lors de l'activité du clavier
def on_press(key):
    global last_activity_time, running
    last_activity_time = time.time()
    if key == keyboard.Key.esc:  # Appuyer sur 'esc' pour quitter le programme
        print("Escape key pressed. Exiting program...")
        running = False
        return False  # Stopper l'écoute du clavier

# Configurer les écouteurs pour la souris et le clavier
mouse_listener = mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)
keyboard_listener = keyboard.Listener(on_press=on_press)

# Démarrer les écouteurs dans des threads séparés
mouse_listener.start()
keyboard_listener.start()

# Lancer le moniteur d'inactivité
monitor_thread = threading.Thread(target=monitor_inactivity)
monitor_thread.start()

# Garder les écouteurs actifs
mouse_listener.join()
keyboard_listener.join()

# Attendre que le thread se termine
monitor_thread.join()

print("Programme terminé.")
