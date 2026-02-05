# Event-Driven Hardware Accelerator for Real-Time Object Detection

This project presents a **low-latency, energy-efficient hardware accelerator for real-time object detection**, designed to outperform conventional **CPU-based inference** by leveraging an **event-driven processing architecture**.

Instead of processing full image frames continuously, the accelerator activates computation **only when meaningful events occur**, significantly reducing processing time, power consumption, and memory overhead.

---

## Project Overview

* **Real-Time Object Detection** with ultra-low latency
* **Event-Driven Execution Model** to eliminate redundant computation
* **Hardware-Accelerated Pipeline** faster than CPU-based processing
* **Optimized for Edge Devices** with strict power and timing constraints

This architecture is suitable for applications such as:
* Surveillance systems
* Autonomous robots
* Smart traffic monitoring
* Industrial vision systems

---

## Repository Contents

* **Verilog / RTL Code**
    Hardware modules for the accelerator, including:
    * Event detection logic
    * Processing Elements (PEs)
    * Feature extraction blocks
    * Control and scheduling FSMs
* **Python Code**
    Scripts for:
    * Dataset preprocessing
    * Event generation and simulation
    * Test vector creation and verification
* **Bitstream Files**
    Precompiled FPGA bitstreams for deployment and testing.
* **Research Paper & Reports**
    Documentation covering:
    * Architecture design
    * Event-driven computation model
    * Latency and power analysis
    * Comparison with CPU-based object detection
* **Demo Video**
    Demonstration of real-time object detection and latency improvements
    *(Link to be added)*

---

## Architecture Overview

### Event-Driven Processing Model
Traditional object detection systems process entire image frames, even when no significant changes occur. This project uses an **event-driven model**, where computation is triggered only by:
* Pixel intensity changes
* Motion-based regions of interest (RoIs)
* Feature activation thresholds

### Accelerator Pipeline
1.  **Event Generator:** Converts sensor or image data into sparse event streams.
2.  **Event Scheduler:** Dynamically assigns events to available processing elements.
3.  **Processing Elements (PEs):** Perform convolution, feature extraction, and classification.
4.  **Detection Output Module:** Outputs object class, bounding box coordinates, and confidence scores.

This approach minimizes idle cycles and enables faster-than-CPU inference.

---

## 🛠 FPGA Design Overview

### Open-Source FPGA Prototype
* Fully open-source FPGA implementation
* Focused on validating real-time, event-driven execution
* Optimized for **latency reduction rather than peak throughput**

### CPU vs Event-Driven Accelerator Comparison

| Feature | CPU-Based Detection | Event-Driven Accelerator |
| :--- | :--- | :--- |
| **Execution Style** | Frame-based | Event-based |
| **Latency** | High | Ultra-low |
| **Power Consumption** | High | Low |
| **Redundant Computation** | Yes | No |
| **Parallelism** | Limited | Massive (Hardware) |

---

## Supported Models

* Lightweight CNN-based object detection models
* Custom feature-based detection pipelines
* Event-optimized detection networks

> **Note:** Current top-level control logic is tailored for a **single object detection model**. Supporting additional models requires modifying the control FSM or adding a software driver.

---

## Customization Options

### Processing Element Scaling
* PE array size can be increased by duplicating existing modules.
* *Note: Automatic parameterization is not yet implemented.*

### Event Sensitivity Control
* Thresholds can be tuned to trade off between detection accuracy and power efficiency.

---

## Known Issues & Limitations

* Control logic is currently model-specific.
* Manual scaling of PE arrays is required.
* Basic event filtering is implemented; advanced noise suppression is not yet included.

---

## TODOs & Future Work

* **Software Driver Development**
    * Enable PS–PL communication for dynamic configuration and data management.
* **Automatic Parameterization**
    * Support scalable PE arrays using Verilog parameters.
* **Advanced Event Filtering**
    * Improve robustness in noisy real-world environments.
* **Neuromorphic Sensor Support**
    * Direct integration with event-based vision sensors (DVS).

---

## Project Abstract

Real-time object detection on edge devices is constrained by high computational load, power consumption, and latency when using CPU-based inference pipelines. These systems process full image frames continuously, leading to inefficient use of resources.

This project introduces an **event-driven hardware accelerator for real-time object detection**, where computation is triggered only by relevant events. By eliminating frame-based redundancy and exploiting massive hardware parallelism, the proposed architecture achieves **significantly lower latency and power consumption** compared to CPU implementations. The modular and scalable design enables efficient deployment on FPGA and future ASIC platforms for real-time edge intelligence.

---

##  Contributions

* **Event-Driven Accelerator Architecture**
    Designed a novel event-driven hardware accelerator for real-time object detection, where computation is triggered only by meaningful events instead of continuous frame-based processing. This architecture significantly reduces redundant operations, lowers latency, and improves energy efficiency compared to traditional CPU-based inference.

* **Event Queue and Scheduling Mechanism (`event_queue.v`)**
    Introduced an event queue module to buffer, prioritize, and manage incoming events efficiently. This module enables asynchronous event handling, supports bursty event traffic, and ensures smooth scheduling without stalling downstream processing elements.

* **Dynamic Event Routing Network (`event_router.v`)**
    Implemented a flexible event router that dynamically dispatches events to available Processing Elements (PEs). The routing logic maximizes hardware utilization, balances workloads across PEs, and eliminates centralized bottlenecks in event distribution.

* **Event-Aware Processing Elements (`PE_event.v`)**
    Developed event-driven Processing Elements that remain idle until a valid event is received. Computation is activated only on demand, minimizing idle power consumption while maintaining high throughput during active object detection phases.

* **Layer-Level Event Control and Synchronization (`layer_controller.v`)**
    Designed a layer controller to manage event flow across multiple layers of the object detection pipeline. This module coordinates layer transitions, handles event dependencies, and ensures correct synchronization between successive processing stages.

* **Low-Latency Event-Based Dataflow**
    By integrating event-driven control with massively parallel hardware execution, the proposed dataflow eliminates unnecessary memory accesses and clock cycles, achieving faster inference and lower power consumption than CPU-based object detection systems.


---


## System Hierarchy Diagram

The diagram below illustrates the interaction between the Event Generator, the Scheduler, and the Processing Element (PE) Array.

![System Hierarchy Diagram](event.jpg)

---

## Implementation

### Top-Level Architecture

The top-level design integrates the event-driven control logic with the computation data path. Key components include:

1.  **Event Interface:** Captures incoming signals and converts them into an asynchronous event stream.
2.  **Scheduler & Router:** Distributes events to the PE array using a load-balancing algorithm.
3.  **PE Array:** A customizable grid of processing elements that perform the core convolution and activation operations.
4.  **Aggregation Unit:** Collects partial results from PEs to form the final detection output.


![event](https://github.com/user-attachments/assets/d4c93552-778e-41fb-bcce-a45be732f318)


<p align="center">
   <img width="462" height="386" alt="System Hierarchy Diagram" src="https://github.com/user-attachments/assets/1f5b5569-8884-4038-8ec9-15bbf6b168bf" />
</p>


## License

This project is released under an open-source license.
See the `LICENSE` file for details.
