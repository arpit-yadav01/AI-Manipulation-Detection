const BASE = "http://localhost:8000/api";

export async function uploadImage(file) {
  const fd = new FormData();
  fd.append("file", file);

  const res = await fetch(`${BASE}/image/analyze`, {
    method: "POST",
    body: fd,
  });

  return res.json();
}

export async function uploadVideo(file) {
  const fd = new FormData();
  fd.append("file", file);

  const res = await fetch(`${BASE}/video/analyze`, {
    method: "POST",
    body: fd,
  });

  return res.json();
}

export async function getResult(jobId) {
  const res = await fetch(`${BASE}/result/${jobId}`);
  return res.json();
}
