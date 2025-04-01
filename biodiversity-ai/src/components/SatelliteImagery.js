import React, { useState, useEffect } from "react";
import { Satellite } from "lucide-react";

const satelliteVideos = [
  {
    id: 1,
    title: "Deforestation Monitoring",
    description: "High-resolution satellite data tracking illegal logging and deforestation patterns.",
    videoUrl: "/assets/defo.mp4",
    source: "Sentinel-2",
    date: "2024-02-10",
  },
  {
    id: 2,
    title: "Biodiversity Loss & Animal Extinction",
    description: "AI-driven analysis of habitat loss and species extinction due to environmental changes.",
    videoUrl: "/assets/bioloss.mp4",
    source: "NASA MODIS",
    date: "2024-01-25",
  },
  {
    id: 3,
    title: "Water Pollution Detection",
    description: "Real-time monitoring of industrial pollution and contamination in major water bodies.",
    videoUrl: "/assets/waterp.mp4",
    source: "Landsat-9",
    date: "2024-03-05",
  },
];

const SatelliteImagery = () => {
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => setIsLoading(false), 1000);
    return () => clearTimeout(timer);
  }, []);

  return (
    <div style={{ position: "relative", width: "100%", color: "white" }}>
      {/* Background Video */}
      <video
        src="/assets/space.mp4"
        autoPlay
        loop
        muted
        playsInline
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          width: "100%",
          height: "100vh",
          objectFit: "cover",
          zIndex: -1,
          opacity: 1, // Light overlay effect
        }}
      />

      {/* Content */}
      <div style={{ position: "relative", padding: "50px 20px", textAlign: "center" }}>
        <div style={{ display: "flex", alignItems: "center", justifyContent: "center", gap: "10px", marginBottom: "10px" }}>
          <Satellite size={40} style={{ color: "#FFD700" }} />
          <h2 style={{ fontSize: "36px", fontWeight: "bold", color: "#fff" }}>Satellite Environmental Analysis</h2>
        </div>
        <p style={{ fontSize: "18px", color: "#f0f0f0", maxWidth: "800px", margin: "auto", marginBottom: "30px" }}>
          AI-powered insights from real-time satellite monitoring of deforestation, biodiversity loss, and water pollution.
        </p>

        {/* Loading Overlay */}
        {isLoading && (
          <div style={{ display: "flex", justifyContent: "center", alignItems: "center", height: "400px" }}>
            <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
              <div
                style={{
                  width: "30px",
                  height: "30px",
                  border: "4px solid #FFD700",
                  borderTop: "4px solid transparent",
                  borderRadius: "50%",
                  animation: "spin 1s linear infinite",
                }}
              />
              <span>Loading satellite data...</span>
            </div>
          </div>
        )}

        {/* Video Cards */}
        {!isLoading &&
          satelliteVideos.map((video) => (
            <div
              key={video.id}
              style={{
                position: "relative",
                width: "100%",
                height: "500px",
                borderRadius: "10px",
                overflow: "hidden",
                background: "#000",
                marginBottom: "20px",
              }}
            >
              {/* Video */}
              <video
                src={video.videoUrl}
                autoPlay
                loop
                muted
                playsInline
                style={{ width: "100%", height: "100%", objectFit: "cover" }}
              />

              {/* Info Overlay */}
              <div
                style={{
                  position: "absolute",
                  bottom: "0",
                  left: "0",
                  right: "0",
                  padding: "20px",
                  background: "rgba(0, 0, 0, 0.7)",
                  color: "white",
                  borderTopLeftRadius: "10px",
                  borderTopRightRadius: "10px",
                }}
              >
                <h3 style={{ fontSize: "22px", fontWeight: "bold", marginBottom: "10px" }}>{video.title}</h3>
                <p style={{ fontSize: "16px", marginBottom: "10px", color: "#ccc" }}>{video.description}</p>
                <div style={{ display: "flex", justifyContent: "space-between", fontSize: "14px", color: "#bbb" }}>
                  <div>Source: {video.source}</div>
                  <div>Date: {video.date}</div>
                </div>
              </div>
            </div>
          ))}

        {/* Keyframe animation for loader */}
        <style>
          {`
            @keyframes spin {
              from { transform: rotate(0deg); }
              to { transform: rotate(360deg); }
            }
          `}
        </style>
      </div>
    </div>
  );
};

export default SatelliteImagery;
