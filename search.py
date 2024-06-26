from transformers import AutoTokenizer, AutoModel, AutoProcessor
import torch
from PIL import Image
from knn import KnnIndex


model = AutoModel.from_pretrained("google/siglip-base-patch16-224")
tokenizer = AutoTokenizer.from_pretrained("google/siglip-base-patch16-224")
processor = AutoProcessor.from_pretrained("google/siglip-base-patch16-224")

print('loaded models!')

index = KnnIndex()
index.load_file('./db.json')
print('loaded index!')

def search(search_query):
    inputs = tokenizer([search_query], padding="max_length", return_tensors="pt")
    with torch.no_grad():
        text_embedding = model.get_text_features(**inputs)[0]

    results = index.knn(text_embedding, 5)
    for e in results:
        image_id = e['embedding']['url']
        similarity_score = e['similarity']
        print(f'image: ./images/images_original/{image_id}.jpg  cosine similarity: {similarity_score}')


while True:
    query = input('what would you like to see? ')
    search(query)