from transformers import AutoTokenizer, AutoModel, AutoProcessor
import torch
from flask import Flask, request, Response, send_file
from flask_cors import CORS, cross_origin
import json
from knn import KnnIndex

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

model = AutoModel.from_pretrained("google/siglip-base-patch16-224")
tokenizer = AutoTokenizer.from_pretrained("google/siglip-base-patch16-224")
processor = AutoProcessor.from_pretrained("google/siglip-base-patch16-224")

print('loaded models!')

index = KnnIndex()
index.load_file('./db.json')
print('loaded index!')

@app.get("/images/<image_id>")
def get_image(image_id):
    return send_file(f'./images/images_original/{image_id}.jpg')

@app.get("/search")
@cross_origin()
def search():
    q = request.args.get('q')

    print("searched for:", q)

    inputs = tokenizer([q], padding="max_length", return_tensors="pt")
    with torch.no_grad():
        text_embedding = model.get_text_features(**inputs)[0]


    most_similar = index.knn(text_embedding, 10)

    # format of API is rather weird but is like that to support my pre-existing frontend for WTFDIST
    out = [{
        'id': e['embedding']['url'],
        'link': e['embedding']['url'],
        'similarity': e['similarity'] if e['similarity'] > -10 else -10
    } for e in most_similar if not e['embedding'] == None]

    
    return Response(json.dumps(out), content_type='Application/json')

if __name__ == "__main__":
    app.run(port=5000)