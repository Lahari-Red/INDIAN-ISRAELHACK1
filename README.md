# Drone Dispatch System (DDS) - Medical Supplies Delivery

[![India-Israel Hackathon 2025](https://img.shields.io/badge/India--Israel%20Hackathon-2025-blue)]()

## Project Overview

The **Drone Dispatch System (DDS)** is a web-based platform designed to simulate autonomous drone delivery of critical medical supplies during emergencies. Developed by *Team Drone Developers (T080)* from Thapar Institute of Engineering & Technology, Patiala, this project aims to enable quick, reliable delivery of medical essentials to remote, rural, and disaster-affected areas where traditional logistics often fail or delay.

DDS currently operates as a fully virtual proof-of-concept focused on urgent, time-sensitive deliveries using simulated drones following machine learning-optimized routes.

---

## Problem Statement

Despite rapid advances in drone technology, **the potential for emergency medical supply delivery using drones remains largely unexplored and underutilized**. Existing systems, such as Zipline and Swoop Aero, are typically:

- Limited to specific geographic locations
- Dependent on expensive infrastructure and hardware
- Lacking flexibility and fully autonomous operation
- Missing accessible open-source platforms for drone management simulation or training

Urgent and specialized delivery solutions that can operate efficiently under dynamic conditions are missing in various regions, especially rural or disaster-affected zones.

---

## Solution Description

The DDS platform allows verified users to:

- Choose from predefined medical payloads (e.g., blood, vaccines, first aid, anti-venom, PPE kits)
- Specify delivery drop-off coordinates (latitude and longitude)
- Autonomously dispatch drones to deliver supplies using machine learning-optimized routes
- Visualize drone movement and delivery progress in real-time on a 2D map interface powered by Leaflet.js
- Monitor and continuously optimize drone operations for safety and efficiency
- Log all delivery activity and performance data for review and improvement

**Note:** DDS currently simulates deliveries virtually with no physical drones but provides an operational blueprint for future real-world deployment.

---

## Unique Selling Points (USPs)

- Secure and encrypted dispatch system  
- Intelligent autonomous navigation (developed in-house)  
- Scalable swarm coordination enabling multi-drone delivery  
- Realistic virtual simulation for testing and training purposes  
- Rapid deployment and cost-effective design suitable for urgent scenarios  

---

## Target Audience

- Remote and rural communities with limited access to timely medical care  
- Hospitals and clinics requiring emergency medical supplies  
- Emergency responders needing critical supplies quickly onsite  
- Public health agencies and NGOs engaged in disaster and epidemic response  

---

## Technology Stack

| Component      | Technology          |
|----------------|---------------------|
| Backend        | Flask (Python)      |
| Frontend       | HTML, CSS, JavaScript, Leaflet.js (Map API) |
| Database       | Aiven Cloud         |
| Route Optimization | Machine Learning  |

---

## Implementation Plan

1. **Develop Core Systems:**  
   - Modular medical supply payloads  
   - Basic machine learning route selection  
   - Flask backend API  
   - 2D map web portal for request entry and live tracking

2. **Integrate & Simulate:**  
   - Connect backend, ML routing, and frontend  
   - Simulate delivery routes on the map  
   - Enable delivery data logging and route updates

3. **Test & Refine:**  
   - Run multiple delivery scenarios  
   - Collect performance data  
   - Iteratively improve system logic and user experience  

---

## Business Model

- Partner with private and public hospitals/clinics for subscription or contract-based recurring deliveries  
- Offer emergency per-delivery services funded by governments during crises such as epidemics or wars  
- Expand to civilian markets by partnering with retail delivery services for non-medical items  
- License the platform to operators for ongoing revenue  

---

## Impact Assessment

| Benefit                | Description                                                  |
|------------------------|--------------------------------------------------------------|
| Faster Emergency Response | Rapid delivery to remote/disaster zones saving lives        |
| Increased Healthcare Reach | Improved access to medical supplies in underserved areas   |
| Operational Efficiency   | Optimized delivery workflows reduce costs and save resources |
| Cost Savings            | Virtual-first development lowers expenses versus traditional methods |

---

## Challenges & Mitigation

- **Regulations:** Comply with aviation authorities, establishing frameworks for BVLOS operations and controlled airspace  
- **Safety:** Implement operational protocols, real-time monitoring, risk assessments, and fail-safe mechanisms  
- **Sustainability:** Financial planning with diverse revenue streams, careful deployment location selection, and strategic partnerships  

---

## Future Roadmap

- Form strategic partnerships with hospitals (e.g., REUS Hospital) for real-world impact  
- Integrate computer vision to enable safer landings, payload recognition, and enhanced autonomous navigation  
- Transition from virtual simulations to real-world drone deployments  

---

## Team Members

| Name             | Role                    | Contact                                   |
|------------------|-------------------------|-------------------------------------------|
| Lakshita Agarawal | AI/ML Implementation       | lakshitaaggarwal2411@gmail.com            |
| Lahari Reddy     |   Frontend (UI/UX)    | bomminenilahari@gmail.com                  |
| Kamesh Yadav     | Backend Developer        | yadavkamesh91@gmail.com                    |
| Kaamya           | Frontend (UI/UX)            | kmathpal_be24@thapar.edu                   |
| Aryan            | Backend Developer        | aryanawasthi017@gmail.com                  |
| Abhinab Chhetri  | Drone Logic & Visualization | abhinab2k05@gmail.com                    |

---

## Contact

For inquiries, collaboration, or feedback, reach out to the team at:  
**achheri_be23@thapar.edu**

---

Thank you for your interest in DDS! Contributions, suggestions, and questions are welcome.

---

