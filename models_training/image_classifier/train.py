# import os
# import torch
# import torch.nn as nn
# import torch.optim as optim
# from torchvision import datasets, transforms, models
# from torch.utils.data import DataLoader

# print("🔥 STEP 6.5 TRAINING — LARGE SCALE (RESUME ENABLED) 🔥")

# # -------------------------------------------------
# # PATHS
# # -------------------------------------------------
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# DATA_DIR = os.path.join(BASE_DIR, "..", "..", "datasets", "image_ml_split")
# MODEL_DIR = os.path.join(BASE_DIR, "..", "..", "models")
# MODEL_PATH = os.path.join(MODEL_DIR, "image_auth_model.pt")

# print(f"📁 Dataset path: {DATA_DIR}")

# # -------------------------------------------------
# # TRANSFORMS
# # -------------------------------------------------
# train_transform = transforms.Compose([
#     transforms.Resize((256, 256)),
#     transforms.RandomResizedCrop(224),
#     transforms.RandomHorizontalFlip(),
#     transforms.ColorJitter(0.1, 0.1, 0.1, 0.05),
#     transforms.ToTensor(),
#     transforms.Normalize(
#         mean=[0.485, 0.456, 0.406],
#         std=[0.229, 0.224, 0.225]
#     )
# ])

# eval_transform = transforms.Compose([
#     transforms.Resize((224, 224)),
#     transforms.ToTensor(),
#     transforms.Normalize(
#         mean=[0.485, 0.456, 0.406],
#         std=[0.229, 0.224, 0.225]
#     )
# ])

# # -------------------------------------------------
# # DATASETS
# # -------------------------------------------------
# train_ds = datasets.ImageFolder(os.path.join(DATA_DIR, "train"), train_transform)
# val_ds   = datasets.ImageFolder(os.path.join(DATA_DIR, "val"), eval_transform)
# test_ds  = datasets.ImageFolder(os.path.join(DATA_DIR, "test"), eval_transform)

# print("📂 Classes:", train_ds.classes)

# train_loader = DataLoader(train_ds, batch_size=16, shuffle=True)
# val_loader   = DataLoader(val_ds, batch_size=16)
# test_loader  = DataLoader(test_ds, batch_size=16)

# # -------------------------------------------------
# # MODEL — PARTIAL FINE-TUNING
# # -------------------------------------------------
# device = "cuda" if torch.cuda.is_available() else "cpu"

# model = models.resnet18(
#     weights=models.ResNet18_Weights.IMAGENET1K_V1
# )

# # 🔒 Freeze entire backbone
# for param in model.parameters():
#     param.requires_grad = False

# # 🔓 Unfreeze last ResNet block
# for param in model.layer4.parameters():
#     param.requires_grad = True

# # 🔓 Fully connected layer
# model.fc = nn.Linear(model.fc.in_features, 2)
# model.to(device)

# # -------------------------------------------------
# # RESUME TRAINING IF MODEL EXISTS
# # -------------------------------------------------
# os.makedirs(MODEL_DIR, exist_ok=True)

# if os.path.exists(MODEL_PATH):
#     print("🔁 Resuming training from existing model")
#     model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
#     RESUMED = True
# else:
#     print("🆕 Training from ImageNet initialization")
#     RESUMED = False

# # -------------------------------------------------
# # LOSS & OPTIMIZER
# # -------------------------------------------------
# criterion = nn.CrossEntropyLoss()

# optimizer = optim.Adam(
#     filter(lambda p: p.requires_grad, model.parameters()),
#     lr=5e-5 if RESUMED else 1e-4   # lower LR when resuming
# )

# # -------------------------------------------------
# # EVALUATION FUNCTION
# # -------------------------------------------------
# def evaluate(loader):
#     model.eval()
#     correct, total = 0, 0
#     with torch.no_grad():
#         for x, y in loader:
#             x, y = x.to(device), y.to(device)
#             preds = model(x).argmax(dim=1)
#             correct += (preds == y).sum().item()
#             total += y.size(0)
#     return correct / total

# # -------------------------------------------------
# # TRAIN LOOP
# # -------------------------------------------------
# EPOCHS = 3 if RESUMED else 8   # resume = fewer epochs

# for epoch in range(EPOCHS):
#     model.train()
#     loss_sum = 0.0

#     for x, y in train_loader:
#         x, y = x.to(device), y.to(device)

#         optimizer.zero_grad()
#         logits = model(x)
#         loss = criterion(logits, y)
#         loss.backward()
#         optimizer.step()

#         loss_sum += loss.item()

#     val_acc = evaluate(val_loader)

#     print(
#         f"Epoch [{epoch + 1}/{EPOCHS}] "
#         f"Train Loss: {loss_sum:.4f} "
#         f"Val Acc: {val_acc:.3f}"
#     )

# # -------------------------------------------------
# # TEST
# # -------------------------------------------------
# test_acc = evaluate(test_loader)
# print(f"\n✅ FINAL TEST ACCURACY: {test_acc:.3f}")

# # -------------------------------------------------
# # SAVE MODEL
# # -------------------------------------------------
# torch.save(model.state_dict(), MODEL_PATH)
# print(f"💾 Model saved to {MODEL_PATH}")



import os
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader

print("🔥 STEP 6.5 — LARGE SCALE IMAGE TRAINING (WINDOWS SAFE) 🔥")

# -------------------------------------------------
# PATHS
# -------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "..", "datasets", "image_ml_split")
MODEL_DIR = os.path.join(BASE_DIR, "..", "..", "models")
MODEL_PATH = os.path.join(MODEL_DIR, "image_auth_model.pt")

print(f"📁 Dataset path: {DATA_DIR}")
print(f"📦 Model path: {MODEL_PATH}")

# -------------------------------------------------
# TRANSFORMS
# -------------------------------------------------
train_transform = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.RandomResizedCrop(224),
    transforms.RandomHorizontalFlip(),
    transforms.ColorJitter(0.1, 0.1, 0.1, 0.05),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

eval_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# -------------------------------------------------
# DATASETS
# -------------------------------------------------
train_ds = datasets.ImageFolder(os.path.join(DATA_DIR, "train"), train_transform)
val_ds   = datasets.ImageFolder(os.path.join(DATA_DIR, "val"), eval_transform)
test_ds  = datasets.ImageFolder(os.path.join(DATA_DIR, "test"), eval_transform)

print("📂 Classes:", train_ds.classes)

# ⚠️ IMPORTANT FIX FOR WINDOWS
train_loader = DataLoader(train_ds, batch_size=16, shuffle=True, num_workers=0)
val_loader   = DataLoader(val_ds, batch_size=16, num_workers=0)
test_loader  = DataLoader(test_ds, batch_size=16, num_workers=0)

# -------------------------------------------------
# MODEL
# -------------------------------------------------
device = "cuda" if torch.cuda.is_available() else "cpu"
print("🖥 Device:", device)

model = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)

# Freeze backbone
for param in model.parameters():
    param.requires_grad = False

# Unfreeze last block
for param in model.layer4.parameters():
    param.requires_grad = True

# FC layer
model.fc = nn.Linear(model.fc.in_features, 2)
model.to(device)

# -------------------------------------------------
# RESUME TRAINING
# -------------------------------------------------
os.makedirs(MODEL_DIR, exist_ok=True)

if os.path.exists(MODEL_PATH):
    print("🔁 Resuming from existing model")
    model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
    RESUMED = True
else:
    print("🆕 Training from ImageNet weights")
    RESUMED = False

# -------------------------------------------------
# OPTIMIZER & LOSS
# -------------------------------------------------
criterion = nn.CrossEntropyLoss()

optimizer = optim.Adam(
    filter(lambda p: p.requires_grad, model.parameters()),
    lr=5e-5 if RESUMED else 1e-4
)

# -------------------------------------------------
# EVAL FUNCTION
# -------------------------------------------------
def evaluate(loader):
    model.eval()
    correct, total = 0, 0
    with torch.no_grad():
        for x, y in loader:
            x, y = x.to(device), y.to(device)
            preds = model(x).argmax(dim=1)
            correct += (preds == y).sum().item()
            total += y.size(0)
    return correct / total

# -------------------------------------------------
# TRAINING LOOP
# -------------------------------------------------
EPOCHS = 3 if RESUMED else 8

for epoch in range(EPOCHS):
    model.train()
    loss_sum = 0.0

    for x, y in train_loader:
        x, y = x.to(device), y.to(device)

        optimizer.zero_grad()
        logits = model(x)
        loss = criterion(logits, y)
        loss.backward()
        optimizer.step()

        loss_sum += loss.item()

    val_acc = evaluate(val_loader)

    print(
        f"Epoch [{epoch + 1}/{EPOCHS}] "
        f"Train Loss: {loss_sum:.2f} "
        f"Val Acc: {val_acc:.4f}"
    )

# -------------------------------------------------
# TEST
# -------------------------------------------------
test_acc = evaluate(test_loader)
print(f"\n✅ FINAL TEST ACCURACY: {test_acc:.4f}")

# -------------------------------------------------
# SAVE MODEL
# -------------------------------------------------
torch.save(model.state_dict(), MODEL_PATH)
print(f"💾 Model saved to {MODEL_PATH}")
