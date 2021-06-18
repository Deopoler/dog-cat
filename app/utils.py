import torch
import torchvision
from torchvision import transforms
from PIL import Image
import io
import torch.nn.functional as F

model = torch.load("app/model.pt", map_location=torch.device("cpu"))
model.load_state_dict(torch.load("app/model_state_dict.pt",
                      map_location=torch.device("cpu")))


def preprogress(image_bytes):
    transforms_from_img = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    image = Image.open(io.BytesIO(image_bytes))
    return transforms_from_img(image).unsqueeze(0)


def get_predict(image_tensor):
    pred = F.softmax(model(image_tensor))
    return pred.tolist()
