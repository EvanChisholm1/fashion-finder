from transformers import AutoTokenizer, AutoModel, AutoProcessor
import torch
import csv
from PIL import Image
from knn import KnnIndex

model = AutoModel.from_pretrained("google/siglip-base-patch16-224")
tokenizer = AutoTokenizer.from_pretrained("google/siglip-base-patch16-224")
processor = AutoProcessor.from_pretrained("google/siglip-base-patch16-224")

model = model.to('cuda')

embeddings = None
ids = []

batch_size = 32

with open('./images/images.csv', mode='r') as file:
    csvFile = csv.reader(file)
    count = 0

    batch = []
    id_batch = []

    is_first = True

    for lines in csvFile:
        if is_first:
            is_first = False
            continue

        ids.append(lines[0])

        image = Image.open(f'./images/images_original/{lines[0]}.jpg')
        # make sure the image is in RGB format
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        batch.append(image)


        if len(batch) == batch_size:
            inputs = processor(images=batch, return_tensors="pt")
            inputs.to('cuda')
            with torch.no_grad():
                image_features = model.get_image_features(**inputs)
            
            count += batch_size
            print(count)

            if embeddings is None:
                embeddings = image_features
            else:
                embeddings = torch.cat((embeddings, image_features), dim=0)

            batch = []

    
        # if count > 250:
        #     break
        # if count > 600:
        #     break

inputs = processor(images=batch, return_tensors="pt")
inputs.to('cuda')
with torch.no_grad():
    image_features = model.get_image_features(**inputs)

embeddings = torch.cat((embeddings, image_features), dim=0)

index = KnnIndex()
    
for i, iden in enumerate(ids):
    index.add_item_no_save(iden, embeddings[i])

index.save_file("./db.json")
    