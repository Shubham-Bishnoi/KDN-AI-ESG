import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import {
  Menu,
  X,
  Satellite,
  BarChart2,
  TreeDeciduous,
  Droplet,
  Home,
} from "lucide-react";

const NavBar = () => {
  const [isScrolled, setIsScrolled] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 10);
    };
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  const toggleMobileMenu = () => {
    setMobileMenuOpen(!mobileMenuOpen);
  };

  const scrollToSection = (id) => {
    const element = document.getElementById(id);
    if (element) {
      element.scrollIntoView({ behavior: "smooth" });
    } else if (id === "home") {
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
    setMobileMenuOpen(false);
  };

  const navButtonStyle = {
    background: "none",
    color: "white",
    fontSize: "16px",
    border: "1px solid white",
    padding: "10px 15px",
    borderRadius: "5px",
    cursor: "pointer",
    transition: "all 0.3s",
  };

  const navButtonHover = {
    backgroundColor: "rgba(255, 255, 255, 0.2)",
    color: "#00e5ff",
    borderColor: "#00e5ff",
  };

  return (
    <nav
      style={{
        position: "fixed",
        top: 0,
        left: 0,
        right: 0,
        zIndex: 1000,
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        padding: "15px 30px",
        background: isScrolled ? "rgba(0, 0, 0, 0.7)" : "rgba(0, 0, 0, 0.4)",
        backdropFilter: "blur(5px)",
        transition: "all 0.3s ease-in-out",
      }}
    >
      {/* Background Video */}
      <video
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
        }}
      >
        <source src="/assets/earth.mp4" type="video/mp4" />
      </video>

      {/* Logo with Satellite + KPMG */}
      <div style={{ display: "flex", alignItems: "center", zIndex: 1 }}>
        <Satellite style={{ width: 30, height: 30, color: "white" }} />
        <span
          style={{
            fontSize: "20px",
            fontWeight: "bold",
            color: "white",
            marginLeft: "10px",
            marginRight: "8px",
          }}
        >
          Eco-Sentinel
        </span>
        <img
          src="/assets/k.png"
          alt="KPMG Logo"
          style={{
            height: "30px",
            marginLeft: "8px",
            objectFit: "contain",
          }}
        />
      </div>

      {/* Desktop Menu */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: "15px",
          zIndex: 1,
        }}
      >
        {[
          { label: "Home", icon: <Home size={18} />, id: "home" },
          { label: "Deforestation", icon: <TreeDeciduous size={18} />, id: "deforestation" },
          { label: "Biodiversity", icon: <TreeDeciduous size={18} />, id: "biodiversity" },
          { label: "Water Pollution", icon: <Droplet size={18} />, id: "water-pollution" },
          { label: "AI Reports", icon: <BarChart2 size={18} />, id: "ai-reports" },
        ].map((item, i) => (
          <button
            key={i}
            onClick={() => scrollToSection(item.id)}
            style={navButtonStyle}
            onMouseEnter={(e) => Object.assign(e.target.style, navButtonHover)}
            onMouseLeave={(e) => Object.assign(e.target.style, navButtonStyle)}
          >
            {item.icon}
            <span style={{ marginLeft: "5px" }}>{item.label}</span>
          </button>
        ))}

        <Link
          to="/dashboards"
          style={{
            padding: "10px 20px",
            background: "#6c5ce7",
            color: "white",
            borderRadius: "5px",
            textDecoration: "none",
            fontSize: "16px",
            transition: "background 0.3s",
          }}
          onMouseEnter={(e) => (e.target.style.background = "#8e44ad")}
          onMouseLeave={(e) => (e.target.style.background = "#6c5ce7")}
        >
          Dashboards
        </Link>
      </div>

      {/* Mobile Toggle */}
      <button
        className="md:hidden"
        onClick={toggleMobileMenu}
        style={{
          background: "none",
          border: "none",
          cursor: "pointer",
          zIndex: 1,
        }}
      >
        {mobileMenuOpen ? (
          <X style={{ width: 30, height: 30, color: "white" }} />
        ) : (
          <Menu style={{ width: 30, height: 30, color: "white" }} />
        )}
      </button>

      {/* Mobile Menu */}
      {mobileMenuOpen && (
        <div
          style={{
            position: "absolute",
            top: "60px",
            right: "0",
            background: "rgba(0, 0, 0, 0.85)",
            width: "200px",
            borderRadius: "5px",
            display: "flex",
            flexDirection: "column",
            gap: "10px",
            padding: "15px",
          }}
        >
          {["home", "deforestation", "biodiversity", "water-pollution", "ai-reports"].map((id) => (
            <button
              key={id}
              onClick={() => scrollToSection(id)}
              style={{
                background: "none",
                color: "white",
                border: "none",
                fontSize: "15px",
                textAlign: "left",
                padding: "8px 5px",
                cursor: "pointer",
              }}
            >
              {id.replace("-", " ").replace(/^\w/, (c) => c.toUpperCase())}
            </button>
          ))}
          <Link to="/dashboards" style={{ color: "white", padding: "8px 5px", textDecoration: "none" }}>
            Dashboards
          </Link>
        </div>
      )}
    </nav>
  );
};

export default NavBar;
