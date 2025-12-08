# 🌌 **blueNovasCam**

A simple and powerful ESP32-CAM streaming system with Firebase support and Python scripts to fetch data, display live video, and keep everything running smoothly.

---

## 🔍 **Check ESP32-CAM Power Status**
Before running, check if your ESP32-CAM is:
- 🔌 **Powered ON**
- 📡 **Reachable on its IP**

If the ESP is offline, turn on.

---

## 🚀 **Auto Run (Recommended)**  
Runs **all scripts together**:

- Checks if ESP32-CAM is ON  
- Starts `esp.py` (camera stream)  
- Starts `fetch.py` (Firebase sync)  
- Both run at the same time  
- One command only  

### ▶ Command
```bash
python3 run.py

---

## change url as yours

---
### Manually runs.

### ▶ Command
```bash
python3 esp.py

### ▶ Command
```bash
python3 fetch.py
