from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
import cv2
import numpy as np
import time




class VideoProcessor(VideoProcessorBase):
    
    
    def __init__(self, recognice_face ,  interval=0.5):
        self.interval = interval
        self.last_time = 0
        self.recognice_face = recognice_face
        self.results = None
        
        
    def recv(self, frame):
        
        
        img = frame.to_ndarray(format="bgr24")
        current_time = time.time()
        
        
        if current_time - self.last_time > self.interval:
            print("Frame reçue")
            self.last_time = current_time
            
            img = frame.to_ndarray(format="bgr24")


            rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)	
            
            try:
                print("Envoi au modèle...")
                self.results = self.recognice_face(rgb)
                print("Résultat obtenu :", self.results)

            except Exception as e:
                print("Erreur modèle :", e)
        else:
            print("⏭️ Frame ignorée (throttle)")

        return img