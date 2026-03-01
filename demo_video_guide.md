# 🎥 Foresight-RX Demo Video Guide

This guide provides a scene-by-scene walkthrough for recording a winning hackathon demo video. Aim for a **2-3 minute** total duration.

---

## 🎬 Scene 1: The Landing (Normal State)
**Visuals:** Open the browser to `http://localhost:8000`. Show the clean, dark-mode dashboard.
**What to Point Out:**
- **Status Header:** Highlight the "System Status: SAFE" badge (Green).
- **Live Metrics:** Show the "Anomaly Score" chart moving at the bottom (Baseline).
- **CPU & I/O Cards:** Point to the real-time system stats being pulled from the `psutil` backend.
**Talk Track:** 
> "Welcome to the Foresight-RX Dashboard. Right now, the system is in its normal state. Our AI has established a 'healthy rhythm' for this machine, monitoring CPU spikes and file entropy in the background."

---

## 🎬 Scene 2: The Core Features (Technical Overview)
**Visuals:** Hover over the different metric cards and the chart tooltips.
**What to Explain:**
- **The Charts:** Explain that these aren't just random lines; they represent the **Reconstruction Error** of our PyTorch Autoencoder.
- **The Dashboard Tech:** Mention that this is a zero-dependency React UI served instantly via CDN for maximum performance and portability.
- **Real OS Connection:** Briefly mention that these numbers are coming from your actual Operating System, not a mock script.

---

## 🎬 Scene 3: The Attack Simulation (The Climax)
**Visuals:** Zoom in or focus on the **"Trigger Attack Simulation"** button. **CLICK IT.**
**What happens on screen:**
1. **File Writes Spike:** The "Writes/Sec" graph should shoot up immediately.
2. **Anomaly Score Rises:** Within 2-3 seconds, the Score graph will climb rapidly into the Red zone.
3. **Status Change:** The big header flash-updates to **"CRITICAL: ALERT"** or **"Ransomware Detected"**.
**Talk Track:**
> "Now, I'm triggering a simulated Zero-Day Ransomware attack. Our simulator is currently encrypting local files. Watch as the AI detects the sudden surge in I/O and the shift toward high-entropy data. The anomaly score breaks the threshold, and the system immediately identifies the threat."

---

## 🎬 Scene 4: Analysis & Reset (The "Smart" Part)
**Visuals:** Point to the specific moment on the chart where the jump happened. Then click **"Reset System"**.
**What to Point Out:**
- **Precision:** Show how the AI caught the behavior almost instantly.
- **Reset Flow:** Show the dashboard returning to Green "SAFE" status as the simulator cleans up.
**Talk Track:**
> "Foresight-RX doesn't just block; it understands. By identifying the *behavioral fingerprint* of the attack, we catch the ransomware before it can finish its encryption cycle. We can then reset the environment to a known good state."

---

## 🎬 Scene 5: Security & Conclusion
**Visuals:** (Optional) Briefly show the `security_audit_report.md` or the `src/` folder structure.
**Closing Words:**
> "Built with security-first principles—protected against path traversal and CORS exploits—Foresight-RX is ready for real-world deployment. Thank you for watching."

---

## 💡 Pro-Tips for the Video:
1. **Cursor Highlighter:** Use a screen recorder that highlights your mouse clicks to make it easy for judges to follow.
2. **Zoom In:** Don't be afraid to zoom into the specific chart changes; judges love seeing the data react.
3. **Keep it Fast:** Don't wait too long between clicking 'Trigger' and 'Reset'. The speed of detection is your biggest selling point!
