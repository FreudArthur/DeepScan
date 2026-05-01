from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
import cv2
import numpy as np
import time
import streamlit as st



class VideoProcessor(VideoProcessorBase):
    
    
    def __init__(self, recognice_face, interval=1.5):
        self.interval = interval
        self.last_time = 0
        self.recognice_face = recognice_face
        self.results = None
        self.frame_count = 0
        
        
    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        current_time = time.time()
        
        if current_time - self.last_time > self.interval:
            self.last_time = current_time
            
            rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            try:
                print(f"[Frame {self.frame_count}] Envoi au modèle...")
                start = time.time()
                self.results = self.recognice_face(rgb)
                print(f"Voir Résultats : {self.results}")
                elapsed = time.time() - start
                
                best = self.results.get("best_match") if self.results else None
                if best:
                    
                    print(f"✅ Match: {best['name']} ({best['probability']:.2%}) - {elapsed:.2f}s")
                else:
                    print(f"⊘ Aucun match trouvé - {elapsed:.2f}s")

            except Exception as e:
                print(f"❌ Erreur: {e}")
                self.results = None
        else:
            pass

        return frame