import { useEffect, useRef, useState } from "react";
import { OpenSheetMusicDisplay } from "osmd-audio-player/node_modules/opensheetmusicdisplay";
import PlaybackEngine from "osmd-audio-player";
import { transformScore } from "./api";

type Difficulty = "easier" | "harder";

function ScorePanel({
  title,
  xml,
  onDownload,
}: {
  title: string;
  xml: string;
  onDownload?: () => void;
}) {
  const scoreRef = useRef<HTMLDivElement>(null);
  const playerRef = useRef<PlaybackEngine | null>(null);
  const [playing, setPlaying] = useState(false);
  const [ready, setReady] = useState(false);

  useEffect(() => {
    if (!scoreRef.current) return;
    const div = scoreRef.current;
    div.innerHTML = "";
    setPlaying(false);
    setReady(false);
    playerRef.current = null;

    const osmd = new OpenSheetMusicDisplay(div);
    osmd.load(xml).then(async () => {
      osmd.render();
      const player = new PlaybackEngine();
      await player.loadScore(osmd);
      playerRef.current = player;
      setReady(true);
    }).catch((e) => console.error("OSMD error:", e));
  }, [xml]);

  async function handlePlay() {
    const player = playerRef.current;
    if (!player) return;
    if (playing) {
      player.stop();
      setPlaying(false);
    } else {
      setPlaying(true);
      await player.play();
      setPlaying(false);
    }
  }

  return (
    <div style={{ width: "100%" }}>
      <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 8 }}>
        <strong>{title}</strong>
        <button
          onClick={handlePlay}
          disabled={!ready}
          style={{ padding: "4px 12px", cursor: ready ? "pointer" : "not-allowed", opacity: ready ? 1 : 0.4 }}
        >
          {playing ? "■ 정지" : "▶ 재생"}
        </button>
        {onDownload && (
          <button onClick={onDownload} style={{ padding: "4px 12px", cursor: "pointer" }}>
            다운로드
          </button>
        )}
      </div>
      <div
        ref={scoreRef}
        style={{
          border: "1px solid #ddd",
          borderRadius: 4,
          padding: 12,
          minHeight: 200,
          background: "#fff",
          color: "#000",
          overflowX: "auto",
        }}
      />
    </div>
  );
}

export default function App() {
  const [file, setFile] = useState<File | null>(null);
  const [difficulty, setDifficulty] = useState<Difficulty>("easier");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [originalXml, setOriginalXml] = useState<string | null>(null);
  const [resultXml, setResultXml] = useState<string | null>(null);

  function handleFileChange(e: React.ChangeEvent<HTMLInputElement>) {
    const f = e.target.files?.[0] ?? null;
    setFile(f);
    setOriginalXml(null);
    setResultXml(null);

    if (f) {
      const reader = new FileReader();
      reader.onload = (ev) => setOriginalXml(ev.target?.result as string);
      reader.readAsText(f);
    }
  }

  async function handleTransform() {
    if (!file) return;
    setLoading(true);
    setError(null);
    setResultXml(null);

    try {
      const xml = await transformScore(file, difficulty);
      setResultXml(xml);
    } catch (e) {
      setError(e instanceof Error ? e.message : "알 수 없는 오류");
    } finally {
      setLoading(false);
    }
  }

  function handleDownload() {
    if (!resultXml) return;
    const blob = new Blob([resultXml], { type: "application/xml" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "transformed.xml";
    a.click();
    URL.revokeObjectURL(url);
  }

  return (
    <div style={{ maxWidth: 1200, margin: "40px auto", padding: "0 20px", fontFamily: "sans-serif" }}>
      <h1>Sheet Music Transformer</h1>

      <div style={{ display: "flex", alignItems: "center", gap: 16, marginBottom: 24, flexWrap: "wrap" }}>
        <input type="file" accept=".xml,.musicxml" onChange={handleFileChange} />

        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
          <span>난이도:</span>
          {(["easier", "harder"] as Difficulty[]).map((d) => (
            <button
              key={d}
              onClick={() => setDifficulty(d)}
              style={{
                padding: "6px 20px",
                background: difficulty === d ? "#1a73e8" : "#eee",
                color: difficulty === d ? "#fff" : "#555",
                border: difficulty === d ? "2px solid #1a73e8" : "2px solid #ccc",
                borderRadius: 4,
                cursor: "pointer",
                fontWeight: difficulty === d ? "bold" : "normal",
              }}
            >
              {d === "easier" ? "쉽게" : "어렵게"}
            </button>
          ))}
          <span style={{ color: "#666", fontSize: 13 }}>
            선택됨: <strong>{difficulty === "easier" ? "쉽게" : "어렵게"}</strong>
          </span>
        </div>

        <button
          onClick={handleTransform}
          disabled={!file || loading}
          style={{
            padding: "10px 24px",
            background: "#1a73e8",
            color: "#fff",
            border: "none",
            borderRadius: 4,
            cursor: file && !loading ? "pointer" : "not-allowed",
            opacity: file && !loading ? 1 : 0.5,
          }}
        >
          {loading ? "변환 중..." : "변환하기"}
        </button>
      </div>

      {error && <p style={{ color: "red", marginBottom: 16 }}>{error}</p>}

      <div style={{ display: "flex", flexDirection: "column", gap: 40 }}>
        {originalXml && (
          <ScorePanel title={`원본 (음표 수: ${(originalXml.match(/<note>/g) || []).length})`} xml={originalXml} />
        )}
        {resultXml && (
          <ScorePanel title={`변환 결과 (음표 수: ${(resultXml.match(/<note>/g) || []).length})`} xml={resultXml} onDownload={handleDownload} />
        )}
      </div>
    </div>
  );
}
