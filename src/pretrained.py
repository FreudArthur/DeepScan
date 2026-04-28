from facenet_pytorch import MTCNN, InceptionResnetV1

# Détection de visage
MTCNN_MODEL = MTCNN(image_size=160 , margin=20)

# Modèle FaceNet pré-entraîné
EMBED_MODEL = InceptionResnetV1(pretrained='vggface2').eval()