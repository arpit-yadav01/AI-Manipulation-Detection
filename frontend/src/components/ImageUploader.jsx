import { useState } from "react";
import { uploadImage } from "../api/client";

function ImageUploader({ onJobCreated }) {
  const [file, setFile] = useState(null);

  const upload = async () => {
    if (!file) {
      alert("Select an image first");
      return;
    }

    const data = await uploadImage(file);
    onJobCreated(data.job_id);
  };

  return (
    <div style={{ marginBottom: 20 }}>
      <input
        type="file"
        accept="image/*"
        onChange={(e) => setFile(e.target.files[0])}
      />
      <br /><br />
      <button onClick={upload}>Analyze Image</button>
    </div>
  );
}

export default ImageUploader;
