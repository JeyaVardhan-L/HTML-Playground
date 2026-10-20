import React, { useState } from "react";
import StateCounter from "./components/StateCounter";
import ClassStudent from "./components/ClassStudent";
import StudentProps from "./components/StudentProps";
import HooksDemo from "./components/HooksDemo";
import FunctionStudent from "./components/FunctionStudent";

/**
 * Main Application Component for React Practicals
 * Houses Practicals 2 through 6 in an intuitive, tabbed layout.
 */
function App() {
  const [activeTab, setActiveTab] = useState("all");

  return (
    <div className="app-container">
      {/* Top Header */}
      <header className="site-header">
        <span className="site-badge">Assignment 4 — React Practicals (WAF Lab)</span>
        <h1 className="main-title">React Core Concepts Laboratory</h1>
        <p className="subtitle">
          Demonstrating State (useState), Class Components, Props, Three Hooks (useState, useRef, useEffect), and Function Components.
        </p>
      </header>

      {/* Navigation Filter Tabs */}
      <nav className="nav-tabs" aria-label="Practical Navigation">
        <button
          className={`tab-btn ${activeTab === "all" ? "active" : ""}`}
          onClick={() => setActiveTab("all")}
          id="tabAll"
        >
          View All Practicals
        </button>
        <button
          className={`tab-btn ${activeTab === "p2" ? "active" : ""}`}
          onClick={() => setActiveTab("p2")}
          id="tabP2"
        >
          Practical 2: State Counter
        </button>
        <button
          className={`tab-btn ${activeTab === "p3" ? "active" : ""}`}
          onClick={() => setActiveTab("p3")}
          id="tabP3"
        >
          Practical 3: Class Component
        </button>
        <button
          className={`tab-btn ${activeTab === "p4" ? "active" : ""}`}
          onClick={() => setActiveTab("p4")}
          id="tabP4"
        >
          Practical 4: Props
        </button>
        <button
          className={`tab-btn ${activeTab === "p5" ? "active" : ""}`}
          onClick={() => setActiveTab("p5")}
          id="tabP5"
        >
          Practical 5: Three Hooks
        </button>
        <button
          className={`tab-btn ${activeTab === "p6" ? "active" : ""}`}
          onClick={() => setActiveTab("p6")}
          id="tabP6"
        >
          Practical 6: Function Component
        </button>
      </nav>

      {/* Main Content Area */}
      <main>
        {/* Practical 2: React State Counter */}
        {(activeTab === "all" || activeTab === "p2") && <StateCounter />}

        {/* Practical 3: React Class Component */}
        {(activeTab === "all" || activeTab === "p3") && <ClassStudent />}

        {/* Practical 4: React Props */}
        {(activeTab === "all" || activeTab === "p4") && <StudentProps />}

        {/* Practical 5: Three Hooks Demo */}
        {(activeTab === "all" || activeTab === "p5") && <HooksDemo />}

        {/* Practical 6: React Function Component */}
        {(activeTab === "all" || activeTab === "p6") && <FunctionStudent />}
      </main>

      {/* Footer */}
      <footer>
        Web Application Frameworks Lab · Assignment 4 · React Practicals (Vite + React)
        <br />
        Student: Jey (Roll 9057) · GITAM University
      </footer>
    </div>
  );
}

export default App;
