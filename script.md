# 🎙️ Foresight-RX Demo Script

**Purpose:** This script is designed as a walkthrough for demonstrating the Foresight-RX prototype during a hackathon pitch or technical presentation.

---

## 🕒 [0:00 - 0:30] Introduction: The Problem
**Speaker:** 
"Hello everyone. Today, ransomware attacks don't just happen instantly. They follow a pattern: they breach, they establish a foothold, and finally, they execute massive, rapid encryption across the filesystem. 

Traditional antivirus solutions often rely on matching known 'signatures'. But what happens when the attackers use a brand new, never-before-seen variant? Traditional AV fails.

That's why we built **Foresight-RX**, an AI-driven *Early Warning System* that detects the **behavior** of ransomware before the damage is done."

---

## 🕒 [0:30 - 1:15] Architecture & Data Collection (The Baseline)
**Speaker:**
*(Open the codebase or architectural diagram)*

"We built Foresight-RX with a robust, real-time Python backend and a fast React frontend.

The core of our detection relies on **Live OS-Level Monitoring**. Instead of scanning static files, our `ProcessMonitor` and `FileMonitor` continuously track metrics like:
1. **CPU Spikes** and **Process Birth Rates** (Tracking recursive worker spanning).
2. **File I/O Rates** (How fast are files being modified or renamed?).
3. **Shannon Entropy Delta** (Ransomware fundamentally changes human-readable text into high-entropy, random-looking encrypted blobs).

We feed this live telemetry into our feature extraction pipeline."

---

## 🕒 [1:15 - 2:00] The AI Engine (The Brain)
**Speaker:**
"To actually detect zero-day attacks, we don't look for bad behavior; we learn what **normal** behavior looks like.

We implemented a **Deep Learning Autoencoder** using PyTorch. During training, the Autoencoder learns the exact rhythm of a healthy system. 

When live data is fed in, the model attempts to reconstruct it. If a strange process suddenly starts encrypting files and renaming extensions, the Autoencoder won't recognize the pattern. The 'Reconstruction Error' spikes, generating a high **Anomaly Score**. 

We built this model with hardware flexibility in mind—it seamlessly falls back to CPU if an AMD ROCm or CUDA GPU isn't available, ensuring it runs on any enterprise endpoint."

---

## 🕒 [2:00 - 3:00] Live Demonstration (The React Dashboard)
**Speaker:**
*(Open `http://localhost:8000` in the browser)*

"Let's look at the live Foresight-RX Dashboard. You can see our system status is currently **Safe**. The anomaly score is very low, hovering near zero. The network and system are operating normally.

Now, let's simulate a zero-day ransomware attack. Our simulator will spawn a high-speed worker that encrypts files in our dummy directory and alters their extensions."

*(Click the **Trigger Attack Simulation** Button)*

"Watch the live metrics. 

1. First, you'll see a spike in the **File Writes/Sec**.
2. Immediately after, our feature extractor detects a sudden, massive rise in **File Entropy** as the files are encrypted.
3. Our PyTorch engine processes this, and the **Anomaly Score** skyrockets past the critical threshold.
4. The system status shifts instantly to **CRITICAL: Ransomware Likely**.

Behind the scenes, the `AlertManager` has logged this event, which in a production environment would immediately trigger automated endpoint isolation."

---

## 🕒 [3:00 - 3:30] Security & Future Scope (Conclusion)
**Speaker:**
"Before bringing this here, we ran a comprehensive DevSecOps pipeline on our codebase. It is defended against Cross-Origin attacks, path traversal, and unsafe PyTorch model deserialization.

Foresight-RX proves that by monitoring *behavior* and applying *anomaly detection*, we can stop new ransomware variants that signature-based systems miss entirely. 

Thank you."
