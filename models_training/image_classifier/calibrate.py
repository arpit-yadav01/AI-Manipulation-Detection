import os
import torch
import torch.nn as nn
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader

print("🔥 STEP 6.4 — CALIBRATION STARTED 🔥")

# -----------------------
# Paths
# -----------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "..", "datasets", "image_ml_split", "val")
MODEL_PATH = os.path.join(BASE_DIR, "..", "..", "models", "image_auth_model.pt")

print("📁 Validation data:", DATA_DIR)
print("📦 Model path:", MODEL_PATH)

# -----------------------
# Transform (NO AUGMENT)
# -----------------------
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# -----------------------
# Load dataset
# -----------------------
dataset = datasets.ImageFolder(DATA_DIR, transform=transform)
loader = DataLoader(dataset, batch_size=16)

print("📂 Classes:", dataset.classes)

# -----------------------
# Load model
# -----------------------
model = models.resnet18(weights=None)
model.fc = nn.Linear(model.fc.in_features, 2)
model.load_state_dict(torch.load(MODEL_PATH, map_location="cpu"))
model.eval()

# -----------------------
# Collect logits
# -----------------------
logits_list = []
labels_list = []

with torch.no_grad():
    for images, labels in loader:
        outputs = model(images)
        logits_list.append(outputs)
        labels_list.append(labels)

logits = torch.cat(logits_list)
labels = torch.cat(labels_list)

# -----------------------
# Temperature scaling
# -----------------------
temperature = torch.ones(1, requires_grad=True)

optimizer = torch.optim.LBFGS([temperature], lr=0.01, max_iter=50)
criterion = nn.CrossEntropyLoss()

def closure():
    optimizer.zero_grad()
    loss = criterion(logits / temperature, labels)
    loss.backward()
    return loss

optimizer.step(closure)

print(f"🔥 Learned temperature: {temperature.item():.3f}")

# -----------------------
# Save calibration
# -----------------------
torch.save(
    {"temperature": temperature.item()},
    os.path.join(BASE_DIR, "calibration.pt")
)

print("💾 Saved calibration.pt")
print("✅ STEP 6.4.1 COMPLETE")
