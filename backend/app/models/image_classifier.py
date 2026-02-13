import torch
import torch.nn.functional as F
from torchvision import models, transforms
from PIL import Image
from pathlib import Path

# 🔑 NEW: registry-based model resolution
from app.models.image.registry import get_active_image_model_dir


class ImageAuthenticityModel:
    def __init__(self, model_path: str | None = None):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # -------------------------------------------------
        # 🔑 Resolve model directory from registry
        # -------------------------------------------------
        if model_path is None:
            model_dir: Path = get_active_image_model_dir()
            model_path = model_dir / "image_auth_model.pt"
            calib_path = model_dir / "calibration.pt"
        else:
            model_path = Path(model_path)
            calib_path = model_path.with_name("calibration.pt")

        # -----------------------
        # Load model
        # -----------------------
        self.model = models.resnet18(weights=None)
        self.model.fc = torch.nn.Linear(self.model.fc.in_features, 2)
        self.model.load_state_dict(
            torch.load(model_path, map_location=self.device)
        )
        self.model.to(self.device)
        self.model.eval()

        # -----------------------
        # Load calibration
        # -----------------------
        if calib_path.exists():
            data = torch.load(calib_path, map_location="cpu")
            self.temperature = torch.tensor(data["temperature"])
        else:
            print("⚠️ calibration.pt not found — using temperature=1.0")
            self.temperature = torch.tensor(1.0)

        # -----------------------
        # Preprocessing
        # -----------------------
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])

    def predict(self, image_path: str) -> float:
        image = Image.open(image_path).convert("RGB")
        image = self.transform(image).unsqueeze(0).to(self.device)

        with torch.no_grad():
            logits = self.model(image)
            calibrated_logits = logits / self.temperature
            probs = F.softmax(calibrated_logits, dim=1)

        # ✅ index 0 = FAKE, index 1 = REAL
        return probs[0][0].item()

    # ✅ REQUIRED FOR GRAD-CAM
    def get_raw_model(self):
        return self.model
