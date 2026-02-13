import torch
from torchvision import models, transforms
from PIL import Image

# Label contract:
# 0 -> FAKE
# 1 -> REAL

device = "cpu"

model = models.resnet18(weights=None)
model.fc = torch.nn.Linear(model.fc.in_features, 2)

model.load_state_dict(
    torch.load("/models/image_auth_model.pt", map_location=device)
)

model.to(device)
model.eval()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

def predict_image(image_path: str) -> dict:
    img = Image.open(image_path).convert("RGB")
    x = transform(img).unsqueeze(0).to(device)

    with torch.no_grad():
        outputs = model(x)
        probs = torch.softmax(outputs, dim=1)[0]

    return {
        "fake_probability": round(probs[0].item(), 3),
        "real_probability": round(probs[1].item(), 3)
    }

if __name__ == "__main__":
    print(predict_image("datasets/image_ml/real/any_real_image.jpg"))
