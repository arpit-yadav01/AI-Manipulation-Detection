import torch
import torch.nn.functional as F
from torchvision import models, transforms
from PIL import Image


class AIGeneratedDetector:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Lightweight, safe model
        self.model = models.resnet18(
            weights=models.ResNet18_Weights.DEFAULT
        )
        self.model.fc = torch.nn.Linear(self.model.fc.in_features, 2)
        self.model.to(self.device)
        self.model.eval()

        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])

    def predict(self, image_path: str):
        image = Image.open(image_path).convert("RGB")
        image = self.transform(image).unsqueeze(0).to(self.device)

        with torch.no_grad():
            logits = self.model(image)
            probs = F.softmax(logits, dim=1)

        ai_prob = probs[0][1].item()  # index 1 = AI

        verdict = "AI_GENERATED" if ai_prob > 0.7 else "NOT_AI"

        return {
            "ai_generated_prob": round(ai_prob, 3),
            "ai_verdict": verdict
        }
