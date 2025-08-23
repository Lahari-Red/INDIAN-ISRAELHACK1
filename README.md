# Drone Dispatch System (DDS) - Medical Supplies Delivery

[![India-Israel Hackathon 2025](https://img.shields.io/badge/India--Israel%20Hackathon-2025-blue)]()

![DDS Hero](static/photos/header.jpg)

 
*Swift, Safe, Smart Deliveries using Autonomous Drones*

---

## Project Overview
The Drone Dispatch System (DDS) is a cutting-edge, web-based platform engineered to redefine emergency medical logistics through autonomous drone technology. Designed to ensure life-saving medical supplies reach the most inaccessible and disaster-struck regions within minutes, DDS leverages intelligent algorithms, real-time tracking, and advanced route optimization for unmatched speed, safety, and reliability.

Built by Team Drone Developers (T080) from Thapar Institute of Engineering & Technology, Patiala, this system represents a powerful leap toward the future of healthcare delivery, where every second counts and technology saves lives.

---

## Problem Statement
<img src="static/photos/solution.jpeg" alt="DDS Hero" width="500">

Despite major progress in drone technology, its life-saving potential for emergency medical delivery remains largely untapped. Traditional logistics fail in disaster zones and remote areas, causing deadly delays. Existing drone solutions are costly, geographically limited, and lack autonomy, leaving a critical gap for a scalable, intelligent, and rapid-response system.

---

## Solution Description


The **Drone Dispatch System (DDS)** platform empowers verified users with **features optimized  for life-saving operations**:
✅ **Select Essential Medical Payloads**  
Choose from a range of critical medical supplies — vaccines, blood units, emergency kits, anti-venom, and more — ensuring timely aid during crises.  
✅ **Pinpoint Exact Delivery Coordinates**  
Input precise latitude and longitude to deliver supplies to the most **remote, rural, or disaster-struck areas** without error.  
✅ **Track Drones in Real-Time**  
Monitor live drone movements on an **interactive Leaflet.js-powered map**, providing **full mission transparency and control**.  
✅ **Highy Optimization Navigation**  
Experience **smart route optimization**, where drones dynamically adapt for the **fastest, safest, and most efficient paths** — overcoming obstacles, weather disruptions, and terrain challenges.  
✅ **Secure & Verified Access**  
Only authorized users can schedule dispatches, ensuring **security, integrity, and accountability** in emergency deliveries.  


---

## **In-House Navigation Model**
<img width="700" height="500" alt="Drone Dispatch System - Google Chrome 8_23_2025 10_45_55 PM" src="https://github.com/user-attachments/assets/912d5832-ea17-4109-b10a-579f50b7f77d" />

Our in-house navigation system overlays a color-coded zone framework to manage drone delivery operations efficiently and safely:

Red Zones: These are strictly no-fly zones where drone operations are either prohibited or permitted only with explicit central government authorization. Red zones commonly cover high-security or sensitive areas such as military installations, airports, government buildings, and other critical infrastructure. Drones are not allowed to enter or deliver within these zones without proper clearance to ensure safety and regulatory compliance.

Outer Range (Yellow Zone): This outer operational boundary extends beyond the inner range but within the drone’s authorized flight perimeter. If a delivery point is in the yellow zone, the drone completes the delivery and then proceeds to the nearest designated safe zone (green zone) for landing and waiting before returning to base. This approach helps maintain safety during extended range flights.

Inner Range (Blue Zone): This zone is the drone’s efficient two-way travel range, closer to the base station. For destinations within this blue inner range, the drone completes deliveries and returns directly to base without intermediate stops.

Safe Zones (Green Zones): Strategically positioned landing or standby spots where drones can safely land, recharge, or wait between deliveries. Safe zones support extended missions by providing secure points within or near the outer range for drones to rest before continuing or returning.

This zone-based navigation strategy leverages informed routing and strict compliance with regulatory no-fly zones (red), while optimizing delivery efficiency and safety during both short-range (blue) and longer-range (yellow) operations.



---

## Technology Stack
| Component      | Technology |
|---------------|-----------|
| **Backend**   | Flask (Python) |
| **Frontend**  | HTML, CSS, JavaScript, Leaflet.js |
| **Database**  | Aiven Cloud |
| **Route Optimization** | Machine Learning |

---

## Screenshots
### **Dashboard**
### **Admin Dashboard**
The **Admin Dashboard** gives full control to administrators:  
 -Manage **users, admins, and vaccine inventory**  
 -Monitor **drone status, availability, and battery health**  
 -Track **active, completed, and failed deliveries** in real time  

<img src="static/photos/dashboard.jpg" alt="DDS Hero" width="700">


### **Tracking Page**
The **Tracking Page** lets users:  
-**Select vaccines and enter delivery coordinates**  
 -**Verify location within operational range** using distance calculation  
 -**Track real-time drone status** and mission progress with live updates  

<img src="static/photos/tracking.jpg" alt="DDS Hero" width="700">

---

## Future Roadmap
- ✅ Partnerships with hospitals
- ✅ Computer vision for safe landing
- ✅ Swarm drone coordination

---

## Team Members
| Name | Role | Contact |
|------|------|---------|
| Lakshita | Path Optimization Model /Ml | lakshitaaggarwal2411@gmail.com |
| Lahari | Frontend | bomminenilahari@gmail.com |
| Kamesh | Backend | yadavkamesh91@gmail.com |
| Kaamya | UI/UX | kmathpal_be24@thapar.edu |
| Aryan | Backend | aryanawasthi017@gmail.com |
| Abhinab | Drone Logic & Visualization | abhinab2k05@gmail.com |

---

## Contact
📧 achheri_be23@thapar.edu  
🌐 *Contributions Welcome!*

---
