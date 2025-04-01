import React, { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { ArrowDown } from "lucide-react";
import EarthVisualization from "./EarthVisualization"; // Earth animation component

const HeroSection = () => {
  const fullTitle = "Environmental Intelligence Platform";
  const fullSubtitle = "Real-time ESG insights powered by satellite data and AI";

  const [title, setTitle] = useState("");
  const [subtitle, setSubtitle] = useState("");

  useEffect(() => {
    let i = 0;
    let j = 0;

    const typeEffect = () => {
      if (i < fullTitle.length) {
        setTitle(fullTitle.substring(0, i + 1));
        i++;
      } else if (j < fullSubtitle.length) {
        setSubtitle(fullSubtitle.substring(0, j + 1));
        j++;
      } else {
        return;
      }
      setTimeout(typeEffect, 50); // Adjust typing speed
    };

    typeEffect(); // Start typing effect

    return () => clearTimeout(typeEffect); // Cleanup
  }, []);

  const scrollToContent = () => {
    const contentElement = document.getElementById("ai-reports"); // ✅ Make sure this exists in AIReportSection.js
    if (contentElement) {
      contentElement.scrollIntoView({ behavior: "smooth" });
    } else {
      console.error("Element with ID 'ai-reports' not found!"); // Debugging
    }
  };
  

  return (
    <section
      style={{
        position: "relative",
        height: "100vh",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        overflow: "hidden",
        textAlign: "center",
        color: "white",
        padding: "20px",
      }}
    >
       {/* Background Video */}
       <video
        src="/assets/blurai.mp4"
        autoPlay
        loop
        muted
        playsInline
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          width: "100%",
          height: "100%",
          objectFit: "cover",
          zIndex: -1,
          opacity: 1,
        }}
      />

      {/* Earth Animation */}
      <div style={{ position: "absolute", inset: 0, zIndex: 0, opacity: 0.5 }}>
        <EarthVisualization />
      </div>

      {/* Content */}
      <motion.div
        initial={{ opacity: 0, y: -50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 1 }}
        style={{
          position: "relative",
          zIndex: 1,
          maxWidth: "800px",
          padding: "20px",
        }}
      >
        <h1
          style={{
            fontSize: "48px",
            fontWeight: "bold",
            marginBottom: "15px",
            textTransform: "capitalize",
            whiteSpace: "nowrap",
          }}
        >
          {title}
          <span style={{ animation: "blink 1s infinite" }}>|</span>
        </h1>

        <p
          style={{
            fontSize: "20px",
            marginBottom: "30px",
            color: "#ddd",
            textAlign: "center",
          }}
        >
          {subtitle}
        </p>

        {/* Buttons */}
        <div style={{ display: "flex", justifyContent: "center", gap: "20px" }}>
          <button
            onClick={scrollToContent}
            style={{
              padding: "12px 24px",
              background: "#1E90FF",
              color: "white",
              borderRadius: "5px",
              fontSize: "16px",
              border: "none",
              cursor: "pointer",
              transition: "background 0.3s",
            }}
          >
            Explore Reports
          </button>

          <button
            onClick={() => document.getElementById("ai-reports")?.scrollIntoView({ behavior: "smooth" })}
            style={{
              padding: "12px 24px",
              background: "transparent",
              color: "#8A2BE2",
              border: "2px solid #8A2BE2",
              borderRadius: "5px",
              fontSize: "16px",
              cursor: "pointer",
              transition: "background 0.3s",
            }}
          >
            AI-Generated Insights
          </button>
        </div>
      </motion.div>

      {/* Scroll Indicator */}
      <div
        style={{
          position: "absolute",
          bottom: "20px",
          left: "50%",
          transform: "translateX(-50%)",
          zIndex: 1,
          cursor: "pointer",
          animation: "bounce 2s infinite",
        }}
        onClick={scrollToContent}
      >
        <ArrowDown size={32} color="white" />
      </div>
    </section>
  );
};

export default HeroSection;
