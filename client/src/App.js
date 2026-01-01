import React, { useState, useEffect } from "react";

const App = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [log, setLog] = useState([]);

  // Function to poll the Python Server
  const performScan = async () => {
    setLoading(true);
    try {
      const response = await fetch("http://127.0.0.1:5000/api/scan");
      const result = await response.json();

      setData(result);

      // Add to log history
      const newLog = `[${new Date().toLocaleTimeString()}] SNR: ${
        result.snr_ratio
      } | ${result.status}`;
      setLog((prev) => [newLog, ...prev].slice(0, 5)); // Keep last 5 logs
    } catch (error) {
      console.error("Connection Lost:", error);
    }
    setLoading(false);
  };

  // Auto-scan every 3 seconds
  useEffect(() => {
    const interval = setInterval(performScan, 3000);
    return () => clearInterval(interval);
  }, []);

  // -- STYLES --
  const styles = {
    container: {
      backgroundColor: "#0a0a0a",
      color: "#00ff00",
      minHeight: "100vh",
      fontFamily: "Courier New, monospace",
      padding: "20px",
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
    },
    monitor: {
      border: "2px solid #333",
      borderRadius: "10px",
      padding: "30px",
      width: "600px",
      backgroundColor: "#000",
      boxShadow: "0 0 20px rgba(0, 255, 0, 0.2)",
    },
    statusBox: (status) => ({
      padding: "20px",
      textAlign: "center",
      fontSize: "2em",
      fontWeight: "bold",
      backgroundColor: status === "ALERT" ? "#330000" : "#001100",
      color: status === "ALERT" ? "#ff0000" : "#00ff00",
      border: `2px solid ${status === "ALERT" ? "red" : "green"}`,
      animation: status === "ALERT" ? "blink 1s infinite" : "none",
      marginBottom: "20px",
    }),
    dataGrid: {
      display: "grid",
      gridTemplateColumns: "1fr 1fr",
      gap: "10px",
      marginBottom: "20px",
    },
    logBox: {
      borderTop: "1px solid #333",
      paddingTop: "10px",
      opacity: 0.7,
      fontSize: "0.9em",
    },
    btn: {
      padding: "15px",
      width: "100%",
      fontSize: "1.2em",
      cursor: "pointer",
      backgroundColor: data?.status === "ALERT" ? "red" : "#333",
      color: "white",
      border: "none",
      marginTop: "20px",
      opacity: data?.status === "ALERT" ? 1 : 0.5,
      pointerEvents: data?.status === "ALERT" ? "auto" : "none",
    },
  };

  return (
    <div style={styles.container}>
      <h1>PROJECT DEEPSCAN // MISSION CONTROL</h1>

      <div style={styles.monitor}>
        {/* STATUS INDICATOR */}
        <div style={styles.statusBox(data?.status)}>
          {loading ? "SCANNING..." : data?.status || "OFFLINE"}
        </div>

        {/* METRICS */}
        {data && (
          <div style={styles.dataGrid}>
            <div>
              SNR RATIO: <strong>{data.snr_ratio}</strong>
            </div>
            <div>
              DEPTH: <strong>{data.depth}m</strong>
            </div>
            <div>
              FREQ TARGET: <strong>15 Hz</strong>
            </div>
            <div>
              SECTOR: <strong>{data.location}</strong>
            </div>
          </div>
        )}

        {/* LOGS */}
        <div style={styles.logBox}>
          {log.map((entry, index) => (
            <div key={index}>{entry}</div>
          ))}
        </div>

        {/* ACTION BUTTON */}
        <button
          style={styles.btn}
          onClick={() => alert("DRONE DEPLOYED. CAMERA FEED INITIALIZING...")}
        >
          {data?.status === "ALERT"
            ? "⚠️ DEPLOY INTERCEPTOR DRONE"
            : "SYSTEM IDLE"}
        </button>
      </div>

      <style>{`@keyframes blink { 50% { opacity: 0.5; } }`}</style>
    </div>
  );
};

export default App;
