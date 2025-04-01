import React, { useState } from "react";
import { motion } from "framer-motion";
import { BarChart2, Download } from "lucide-react";

const API_URL = "http://localhost:5050"; // Backend API URL

const reportTypes = [
  {
    id: "biodiversity",
    title: "Biodiversity Loss Analysis",
    description: "AI-generated assessment of biodiversity impact based on TNFD guidelines.",
  },
  {
    id: "deforestation",
    title: "Deforestation Monitoring",
    description: "Deforestation rates and impact assessment using satellite imagery.",
  },
  {
    id: "water",
    title: "Water Pollution Report",
    description: "Analysis of water body contamination and pollution sources.",
  },
];

const companyList = [
  "amazon_com", "tesla", "apple", "microsoft", "netflix", "pfizer", "meta", "accenture", "goldman_sachs",
  "unitedhealth", "walmart", "pepsico", "ford_motor", "starbucks", "spotify_technology", "coca_cola", "oracle",
  "facebook", "broadcom", "intel_corporation", "nvidia", "adobe", "visa", "mastercard", "twitter", "ebay", "zoom_video",
  "lyft", "airbnb", "square", "wells_fargo", "verizon_communications", "abbott_laboratories", "intuitive_surgical",
  "automatic_data_processing", "uber_technologies", "costco_wholesale", "berkshire_hathaway", "cvs_health", "paypal_holdings"
  // Add more from your list if needed
];

const AIReportSection = () => {
  const [activeTab, setActiveTab] = useState("biodiversity");
  const [selectedCompany, setSelectedCompany] = useState("amazon_com");
  const [isGenerating, setIsGenerating] = useState(false);
  const [isReportGenerated, setIsReportGenerated] = useState(false);

  const generateReport = async () => {
    setIsGenerating(true);
    setIsReportGenerated(false);
    try {
      const res = await fetch(`${API_URL}/generate-report/${activeTab}`);
      if (!res.ok) throw new Error(`Server returned ${res.status}`);
      const result = await res.json();
      console.log("✅ Report Generated:", result);
      setIsReportGenerated(true);
    } catch (error) {
      console.error("❌ Error generating report:", error.message);
      alert("Failed to generate report. See console for details.");
    }
    setIsGenerating(false);
  };

  const downloadReport = async () => {
    try {
      const response = await fetch(`${API_URL}/download-report/${selectedCompany}`);
      if (!response.ok) throw new Error("Failed to download PDF.");
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `${selectedCompany}_report.pdf`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error(" Error downloading report:", error);
      alert("Could not download the report. See console for details.");
    }
  };

  return (
    <motion.div
      id="ai-reports"
      initial={{ opacity: 0, y: 50 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 1 }}
      style={{
        position: "relative",
        width: "100%",
        minHeight: "100vh",
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        textAlign: "center",
        color: "white",
        padding: "40px 20px",
      }}
    >
      <div
        style={{
          position: "absolute",
          inset: 0,
          background: "linear-gradient(to bottom, rgba(10, 61, 98, 0.8), rgba(50, 10, 80, 0.3))",
          zIndex: 0,
        }}
      />
      <div style={{ maxWidth: "900px", zIndex: 1 }}>
        <div style={{ display: "flex", alignItems: "center", justifyContent: "center", gap: "10px", marginBottom: "10px" }}>
          <BarChart2 size={40} style={{ color: "#8A2BE2" }} />
          <h2 style={{ fontSize: "36px", fontWeight: "bold", color: "#fff" }}>AI-Generated ESG Reports</h2>
        </div>
        <p style={{ fontSize: "18px", color: "#f0f0f0", marginBottom: "30px" }}>
          Generate comprehensive environmental impact reports powered by artificial intelligence and satellite data.
        </p>

        {/* Tabs */}
        <div style={{ display: "flex", justifyContent: "center", gap: "15px", marginBottom: "20px" }}>
          {reportTypes.map((report) => (
            <button
              key={report.id}
              onClick={() => {
                setActiveTab(report.id);
                setIsReportGenerated(false);
              }}
              style={{
                padding: "12px 18px",
                borderRadius: "5px",
                fontSize: "16px",
                fontWeight: "bold",
                background: activeTab === report.id ? "#8A2BE2" : "transparent",
                color: activeTab === report.id ? "white" : "#ccc",
                border: activeTab === report.id ? "none" : "1px solid #ccc",
                cursor: "pointer",
                transition: "background 0.3s",
              }}
            >
              {report.title.split(" ")[0]}
            </button>
          ))}
        </div>

        {/* Select Company */}
        <div style={{ marginTop: "20px" }}>
          <label style={{ color: "#fff", marginRight: "10px" }}>Select Company:</label>
          <select
            value={selectedCompany}
            onChange={(e) => setSelectedCompany(e.target.value)}
            style={{
              padding: "8px 12px",
              borderRadius: "5px",
              fontSize: "14px",
              outline: "none",
            }}
          >
            {companyList.map((name) => (
              <option key={name} value={name}>
                {name.replace(/_/g, " ")}
              </option>
            ))}
          </select>
        </div>

        {/* Report Generation Section */}
        {!isReportGenerated ? (
          <div style={{ textAlign: "center", padding: "30px" }}>
            <BarChart2 size={48} style={{ color: "#8A2BE2", marginBottom: "10px" }} />
            <h3 style={{ fontSize: "22px", marginBottom: "10px" }}>Generate AI-Powered ESG Report</h3>
            <p style={{ fontSize: "16px", color: "#ddd", marginBottom: "20px" }}>
              Our AI synthesizes satellite data, environmental metrics, and TNFD guidelines to create comprehensive ESG reports.
            </p>
            <button
              onClick={generateReport}
              disabled={isGenerating}
              style={{
                padding: "14px 28px",
                background: "#8A2BE2",
                color: "white",
                fontSize: "18px",
                fontWeight: "bold",
                borderRadius: "5px",
                border: "none",
                cursor: isGenerating ? "not-allowed" : "pointer",
                transition: "background 0.3s",
              }}
            >
              {isGenerating ? "Generating Report..." : "Generate Report"}
            </button>
          </div>
        ) : (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 1 }}>
            <div style={{ padding: "20px", background: "rgba(0, 0, 0, 0.5)", borderRadius: "10px", marginBottom: "20px" }}>
              <h4 style={{ fontSize: "20px", fontWeight: "bold", marginBottom: "10px" }}>Executive Summary</h4>
              <p style={{ fontSize: "16px", color: "#ddd" }}>
                {reportTypes.find((r) => r.id === activeTab)?.description}
              </p>
            </div>

            <div style={{ display: "flex", justifyContent: "center", gap: "20px", marginTop: "20px" }}>
              <button
                onClick={() => setIsReportGenerated(false)}
                style={{
                  padding: "12px 24px",
                  background: "transparent",
                  color: "white",
                  fontSize: "16px",
                  fontWeight: "bold",
                  borderRadius: "5px",
                  border: "2px solid #8A2BE2",
                  cursor: "pointer",
                  transition: "background 0.3s",
                }}
              >
                Generate New Report
              </button>
              <button
                onClick={downloadReport}
                style={{
                  padding: "12px 24px",
                  background: "#1E90FF",
                  color: "white",
                  fontSize: "16px",
                  fontWeight: "bold",
                  borderRadius: "5px",
                  border: "none",
                  cursor: "pointer",
                  transition: "background 0.3s",
                  display: "flex",
                  alignItems: "center",
                  gap: "8px",
                }}
              >
                <Download size={18} />
                Download Report
              </button>
            </div>
          </motion.div>
        )}
      </div>
    </motion.div>
  );
};

export default AIReportSection;
