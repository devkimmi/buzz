const API_BASE = "http://localhost:8000";

export type ProgressEvent = { type: "progress"; step: number; message: string };
export type DoneEvent = { type: "done"; musicxml: string };
export type TransformEvent = ProgressEvent | DoneEvent;

export async function transformScore(
  file: File,
  difficulty: "easier" | "harder",
  onProgress: (event: TransformEvent) => void
): Promise<string> {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("difficulty", difficulty);

  const res = await fetch(`${API_BASE}/api/transform`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) throw new Error(`변환 실패: ${res.status}`);

  const reader = res.body!.getReader();
  const decoder = new TextDecoder();
  let buffer = "";

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split("\n\n");
    buffer = lines.pop() ?? "";

    for (const line of lines) {
      if (!line.startsWith("data: ")) continue;
      const event: TransformEvent = JSON.parse(line.slice(6));
      onProgress(event);
      if (event.type === "done") return event.musicxml;
    }
  }

  throw new Error("스트림이 완료되지 않았습니다");
}
