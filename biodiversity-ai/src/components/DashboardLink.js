import React from "react";
import { ExternalLink, BarChart2, Globe } from "lucide-react";

const dashboards = [
  {
    title: "ESG AI Dashboard",
    description: "AI-driven ESG scoring, greenwashing detection, and sustainability insights.",
    details: "Automate ESG analysis using AI & real-time news sentiment scoring.",
    icon: <BarChart2 size={50} />,
    url: "http://localhost:8501",
    color: "#1E90FF",
  },
  {
    title: "Geospatial Analysis",
    description:
      "Streamlit Geospatial Hub – Explore U.S. Housing 🏠, Split Map 🪟, Ordnance Survey 🧱, and Timelapse 🌍. Create your own satellite timelapse anywhere on Earth.",
    details:
      "A multi-page web app demonstrating mapping tools built with streamlit + open-source libraries like leafmap, geemap, pydeck, and kepler.gl. Click on the left sidebar to access different modules.",
    icon: <Globe size={50} />,
    url: "http://localhost:8502",
    color: "#32CD32",
  },
];

const DashboardLink = () => {
  return (
    <div style={{ width: "100%", minHeight: "100vh", position: "relative", color: "white", textAlign: "center" }}>
      {/* Background Video */}
      <video
        autoPlay
        loop
        muted
        playsInline
        style={{
          position: "fixed",
          top: 0,
          left: 0,
          width: "100%",
          height: "100%",
          objectFit: "cover",
          zIndex: -1,
          filter: "brightness(0.3)",
        }}
      >
        <source src="/assets/dash.mp4" type="video/mp4" />
      </video>

      {/* Header */}
      <div style={{ marginBottom: "30px", padding: "50px 20px" }}>
        <h2 style={{ fontSize: "44px", fontWeight: "bold" }}>AI-Powered ESG Dashboards</h2>
        <p style={{ fontSize: "20px", color: "#ddd", maxWidth: "700px", margin: "10px auto" }}>
          Explore AI-driven insights into ESG analysis and geospatial environmental intelligence.
        </p>
      </div>

      {/* Cards */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(350px, 1fr))",
          gap: "30px",
          maxWidth: "1100px",
          margin: "auto",
          paddingBottom: "80px",
          position: "relative",
          zIndex: 1,
        }}
      >
        {dashboards.map((dashboard, index) => (
          <a
            key={index}
            href={dashboard.url}
            target="_blank"
            rel="noopener noreferrer"
            style={{
              display: "block",
              textDecoration: "none",
              transition: "transform 0.3s ease, box-shadow 0.3s ease",
            }}
            onMouseEnter={(e) => (e.currentTarget.style.transform = "scale(1.07)")}
            onMouseLeave={(e) => (e.currentTarget.style.transform = "scale(1)")}
          >
            <div
              style={{
                background: "rgba(20, 20, 20, 0.9)",
                borderLeft: `6px solid ${dashboard.color}`,
                padding: "30px",
                borderRadius: "14px",
                color: "white",
                display: "flex",
                flexDirection: "column",
                justifyContent: "space-between",
                transition: "box-shadow 0.3s ease",
                boxShadow: "0px 0px 15px rgba(255, 255, 255, 0.1)",
              }}
            >
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <div style={{ color: dashboard.color }}>{dashboard.icon}</div>
                <ExternalLink size={22} style={{ color: "#ccc" }} />
              </div>

              <h3 style={{ fontSize: "24px", marginTop: "14px", fontWeight: "bold" }}>{dashboard.title}</h3>
              <p style={{ fontSize: "16px", color: "#ccc", marginBottom: "12px" }}>{dashboard.description}</p>
              <p style={{ fontSize: "14px", color: "#bbb" }}>{dashboard.details}</p>
              <p style={{ fontSize: "13px", color: "#aaa", marginTop: "15px" }}>Powered by Streamlit</p>
            </div>
          </a>
        ))}
      </div>
    </div>
  );
};

export default DashboardLink;
