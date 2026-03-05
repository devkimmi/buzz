const API_BASE = "http://localhost:8000";

export async function transformScore(
  file: File,
  difficulty: "easier" | "harder"
): Promise<string> {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("difficulty", difficulty);

  const res = await fetch(`${API_BASE}/api/transform`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) {
    throw new Error(`변환 실패: ${res.status}`);
  }

  const data = await res.json();
  return data.musicxml;
}
