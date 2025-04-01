import React, { useEffect } from "react";
import { BrowserRouter as Router, Route, Routes, useLocation } from "react-router-dom";
import NavBar from "./components/NavBar";
import HeroSection from "./components/HeroSection";
import SatelliteImagery from "./components/SatelliteImagery";
import AIReportSection from "./components/AlReportSection";
import DashboardLink from "./components/DashboardLink";

const ScrollToTop = () => {
  const { pathname, hash } = useLocation();

  useEffect(() => {
    if (hash) {
      const element = document.getElementById(hash.substring(1));
      if (element) {
        element.scrollIntoView({ behavior: "smooth" });
      }
    } else {
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
  }, [pathname, hash]);

  return null;
};

const App = () => {
  return (
    <Router>
      <NavBar />
      <ScrollToTop />
      
      <Routes>
        <Route
          path="/"
          element={
            <>
              <HeroSection />
              <SatelliteImagery />
              <AIReportSection />
            </>
          }
        />
        <Route path="/reports" element={<AIReportSection />} />
        <Route path="/dashboards" element={<DashboardLink />} />
      </Routes>
    </Router>
  );
};

export default App;
