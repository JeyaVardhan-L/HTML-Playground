import React, { useState } from "react";
import StateCounter from "./components/StateCounter";
import ClassStudent from "./components/ClassStudent";
import StudentProps from "./components/StudentProps";
import HooksDemo from "./components/HooksDemo";
import FunctionStudent from "./components/FunctionStudent";

/**
 * Main Application Component for React Practicals
 * Houses Practicals 2 through 6 in a simple tabbed layout.
 */
function App() {
  const [activeTab, setActiveTab] = useState("all");

  return (
    <div className="app-container">
      {/* Top Header */}
      <header className="site-header">
        <span className="site-label">Assignment 4 — WAF Lab / React Practicals</span>
        <h1>React Core Concepts</h1>
        <p>
          State (useState), Class Components, Props, three Hooks (useState, useRef, useEffect), and Function Components.
        </p>
      </header>

      {/* Navigation */}
      <nav className="nav-tabs" aria-label="Practical navigation">
        <button
          className={`tab-btn ${activeTab === "all" ? "active" : ""}`}
          onClick={() => setActiveTab("all")}
          id="tabAll"
        >
          All
        </button>
        <button
          className={`tab-btn ${activeTab === "p2" ? "active" : ""}`}
          onClick={() => setActiveTab("p2")}
          id="tabP2"
        >
          P2: State
        </button>
        <button
          className={`tab-btn ${activeTab === "p3" ? "active" : ""}`}
          onClick={() => setActiveTab("p3")}
          id="tabP3"
        >
          P3: Class Component
        </button>
        <button
          className={`tab-btn ${activeTab === "p4" ? "active" : ""}`}
          onClick={() => setActiveTab("p4")}
          id="tabP4"
        >
          P4: Props
        </button>
        <button
          className={`tab-btn ${activeTab === "p5" ? "active" : ""}`}
          onClick={() => setActiveTab("p5")}
          id="tabP5"
        >
          P5: Three Hooks
        </button>
        <button
          className={`tab-btn ${activeTab === "p6" ? "active" : ""}`}
          onClick={() => setActiveTab("p6")}
          id="tabP6"
        >
          P6: Function Component
        </button>
      </nav>

      {/* Main Content Area */}
      <main>
        {(activeTab === "all" || activeTab === "p2") && <StateCounter />}
        {(activeTab === "all" || activeTab === "p3") && <ClassStudent />}
        {(activeTab === "all" || activeTab === "p4") && <StudentProps />}
        {(activeTab === "all" || activeTab === "p5") && <HooksDemo />}
        {(activeTab === "all" || activeTab === "p6") && <FunctionStudent />}
      </main>

      {/* Footer */}
      <footer>
        Web Application Frameworks Lab · Assignment 4 · Jey (Roll 9057) · GITAM University
      </footer>
    </div>
  );
}

export default App;
