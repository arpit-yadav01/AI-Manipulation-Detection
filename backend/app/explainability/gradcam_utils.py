import os
import uuid
from torchvision import transforms
from PIL import Image

from app.explainability.gradcam import GradCAM
from app.explainability.heatmap import overlay_heatmap


def generate_gradcam(image_path: str, model, device) -> str | None:
    try:
        model.train()  # enable gradients

        target_layer = model.layer4[-1]
        cam_generator = GradCAM(model, target_layer)

        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])

        image = Image.open(image_path).convert("RGB")
        input_tensor = transform(image).unsqueeze(0).to(device)

        cam = cam_generator.generate(input_tensor, class_idx=0)

        output_dir = "/app/datasets/uploads/explainability"
        os.makedirs(output_dir, exist_ok=True)

        filename = f"{uuid.uuid4()}_gradcam.jpg"
        output_path = os.path.join(output_dir, filename)

        overlay_heatmap(image_path, cam, output_path)

        model.eval()

        return f"/files/explainability/{filename}"


    except Exception as e:
        print("❌ GradCAM failed:", e)
        return None
