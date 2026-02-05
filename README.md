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

##  FPGA Design Overview

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

###### Implementation

#### Top-Level Architecture

The top-level design integrates the event-driven control logic with the computation data path. Key components include:

1.  **Event Interface:** Captures incoming signals and converts them into an asynchronous event stream.
2.  **Scheduler & Router:** Distributes events to the PE array using a load-balancing algorithm.
3.  **PE Array:** A customizable grid of processing elements that perform the core convolution and activation operations.
4.  **Aggregation Unit:** Collects partial results from PEs to form the final detection output.


![event](https://github.com/user-attachments/assets/d4c93552-778e-41fb-bcce-a45be732f318)




##  Component-Level Architecture Description (Event-Driven & Sparse Connectivity)

| Component Level | Description | Details |
|----------------|-------------|---------|
| Cluster Array | 4×2 Event-Driven PE Clusters | Adjustable |
| 4×2 Event GLB Clusters | Adjustable |
| 4×2 Event Router Clusters | Adjustable |
| Event PE Cluster | 3×3 Event-Driven PEs | Sparse-activated |
| Event GLB Cluster | 3×2 SRAM Banks (iacts/events) | Event buffers |
|  | 4×2 SRAM Banks (psums) | Sparse psums |
| Event Router Cluster | 3 Event routers | Event-based |
|  | 3 Weight routers | Sparse weights |
|  | 4 Psum routers | Event-triggered |
| Control Layer | Layer-wise Event Controller | Dynamic execution |
| Event Handling | Global Event Queue | Asynchronous |

---

### Event-Driven Architecture Overview

Building upon conventional CNN accelerator designs, our architecture introduces a **fully event-driven processing paradigm with sparse connectivity**, enabling computation to occur **only when meaningful events are detected**. This fundamentally departs from frame-based execution and significantly reduces redundant computation, memory access, and power consumption.

As illustrated in Fig. X, the core of the system is organized as a **4×2 event-driven cluster array**, which can be scaled up or down depending on performance and resource requirements. For FPGA validation, the design is configured with a reduced cluster size to accommodate logic and memory constraints, while preserving architectural scalability for future ASIC implementations.

---

### Event Encoding and Sparse Data Preparation

The **event encoder group** is responsible for converting incoming sensor or image data into sparse event streams. Instead of processing full frames, only regions exhibiting significant changes generate events. These events are compactly represented and stored in event buffers, minimizing SRAM utilization.

Sparse activations and weights are handled natively by the architecture, ensuring that both memory access and computation scale with the number of active events rather than input size.

---

### Event-Driven Cluster Array

At the heart of the accelerator lies the **Event PE Cluster**, consisting of a **3×3 array of event-aware Processing Elements (PEs)**. Each PE remains idle until it receives a valid event, at which point computation is triggered. This sparse activation model drastically reduces idle switching activity and improves energy efficiency.

---

### Event Global Load Balancer (Event GLB)

The **Event GLB Cluster** functions as the distributed on-chip memory system. It includes:
- Dedicated SRAM banks for storing sparse input activations and events  
- Separate SRAM banks for partial sums (psums) generated during event-triggered computation  

This separation allows concurrent access patterns and reduces contention during high event density.

---

### Event Routing Network

The **Event Router Cluster** manages internal data movement within the cluster array. It consists of:
- Event routers for distributing event packets  
- Weight routers optimized for sparse weight access  
- Psum routers that forward results only when valid computations occur  

Compared to traditional always-on routing logic, the routers are **simplified and event-triggered**, activating only when data movement is required. This design choice enhances routing efficiency while reducing unnecessary switching activity.

---

### Layer-Level Event Control

A dedicated **Layer Controller** orchestrates event flow across different layers of the object detection pipeline. It manages:
- Event synchronization between layers  
- Dynamic enabling and disabling of clusters  
- Sparse execution control based on event density  

This enables seamless execution of multi-layer detection networks without requiring global frame synchronization.

---

### Key Architectural Advantages

- Sparse connectivity reduces memory footprint and computation load  
- Event-triggered execution minimizes latency and power consumption  
- Modular and scalable cluster design supports diverse object detection models  
- FPGA-friendly architecture with clear ASIC migration path  

---

This event-driven and sparsely connected architecture enables **real-time object detection with significantly lower latency and energy consumption than conventional CPU-based or frame-driven accelerators**, making it highly suitable for edge intelligence applications.

##  Global Buffer (GLB) Architecture (Event-Driven & Sparse)

#### Global Buffer Architecture

The **Global Buffer (GLB) cluster** acts as the primary interface between the **event-driven accelerator core** and external memory (DRAM), enabling efficient storage and distribution of sparse, event-based data. Unlike conventional frame-driven buffers, the GLB in this architecture is optimized to handle **asynchronous event streams and sparse activations**, ensuring minimal memory access and low latency.

The GLB cluster consists of **event iact SRAMs and psum SRAMs**, carefully aligned with the distribution of the **Event-Driven PE array** to provide sufficient bandwidth under bursty event conditions. Each Event PE Cluster is serviced by corresponding GLB banks, allowing concurrent access and parallel event processing.

---

### Event-Based Data Storage

- **Event Iact SRAMs**  
  The iact SRAMs store **event-encoded sparse activations** rather than dense feature maps. Since events arrive asynchronously and in variable quantities, the iact SRAMs are designed to support irregular access patterns efficiently.

- **Psum SRAMs**  
  Partial sums (psums) generated by event-triggered computation are stored in dedicated psum SRAMs. Psums are written only when valid events are processed, avoiding unnecessary memory writes and reducing power consumption.

- **Weight Handling (Weight Stationary)**  
  Similar to a weight-stationary dataflow, **weights are stored locally within each Event PE’s internal weight SRAM**. The GLB does not allocate dedicated SRAM banks for weights; instead, it provides **dedicated weight ports** that connect directly to the event-aware weight routers. This minimizes global memory traffic and preserves locality.

---

### Sparse Event Metadata Management

Due to the **variable-length nature of event streams**, the size and boundaries of event data blocks cannot be determined using fixed counters. To address this, the GLB incorporates **Register Files (RFs)** alongside the iact SRAM banks. These RFs act as **lookup tables (LUTs)** that record:

- Start addresses of event groups  
- End addresses of event groups  
- Mapping between events and assigned Event PEs  

An internal **Event FSM Controller** manages these RFs by detecting **event delimiters** that indicate the end of an event group. This mechanism provides clear boundaries between event packets and ensures correct event retrieval and dispatch.

---

### Independent SRAM Operation

All SRAM banks within the GLB cluster are synthesized using **OpenRAM** and are designed to operate **independently**. This independence enables:
- Concurrent reads and writes across different event streams  
- Improved throughput under high event density  
- Reduced contention between iact and psum accesses  

Such parallelism is critical for sustaining real-time performance in event-driven object detection workloads.

---

### Event-Safe Data Communication

To guarantee data integrity and correct synchronization between the GLB and downstream modules, the GLB employs a **two-way handshake protocol** using `Valid` and `Ready` signals. This protocol ensures that:
- Events are transferred only when the receiving module is ready  
- No event data is lost or duplicated during asynchronous operation  
- The accelerator remains robust under variable event arrival rates  

---

### Key Advantages of Event-Driven GLB Design

- Efficient handling of sparse, asynchronous event data  
- Reduced SRAM access and power consumption  
- High concurrency through independently operating SRAM banks  
- Seamless integration with event routers and event-driven PEs  

---

This event-driven GLB architecture plays a critical role in enabling **low-latency, energy-efficient real-time object detection**, ensuring that memory access scales with event activity rather than input size.

#  FPGA Verification

We implemented and verified the proposed **event-driven object detection accelerator** on an FPGA platform using a **2×2 event cluster configuration** deployed on the **Xilinx ZCU102 FPGA board**. The complete RTL design was synthesized using **Xilinx Vivado**, and the generated bitstream was programmed onto the ZCU102 to validate functional correctness, timing behavior, and real-time performance of the accelerator. This FPGA-based implementation enabled detailed evaluation of the event-driven control logic, sparse routing network, and event-aware processing elements under realistic hardware conditions.

For data transmission, the design leverages **PL-side high-speed interfaces** of the ZCU102 to receive event data directly from a host PC. A **custom UART-based communication protocol** was implemented to support asynchronous event streams, allowing sparse, event-driven data to be transferred efficiently to the programmable logic (PL). This setup ensures reliable communication while preserving the asynchronous nature of event-based processing.

The FPGA demonstration focuses on a **real-time object detection pipeline driven by event-based inputs**. On the host PC side, a **Python-based graphical user interface (GUI)** was developed to capture input data, generate sparse events based on motion or pixel-level changes, and transmit these events to the FPGA for inference. Once received, the event-driven accelerator processes the incoming event stream in real time and outputs detection results with low latency.

This verification framework closely mirrors practical deployment scenarios and highlights the advantages of the proposed event-driven architecture over traditional CPU-based approaches. The successful implementation on the ZCU102 FPGA validates the accelerator’s capability to efficiently handle sparse, asynchronous events, achieve real-time inference, and operate effectively in high-performance edge and embedded vision applications.

<img width="1008" height="642" alt="Screenshot 2026-02-05 223754" src="https://github.com/user-attachments/assets/de3254a7-14bc-490e-993a-c9dc3cb6393e" />


#Customized CNN Layer for Real-Time Object Detection (ZCU102 Demo)

To demonstrate real-time object detection on the **Xilinx ZCU102 FPGA**, we designed a **customized lightweight CNN layer** optimized specifically for **event-driven execution and low-latency inference**. Unlike conventional CNN layers that process dense feature maps, this customized layer operates on **sparse, event-based activations**, ensuring that computation is performed only when relevant events are present.

The CNN layer integrates **event-triggered convolution, simplified activation logic, and sparse partial-sum accumulation**, making it well-suited for FPGA deployment under strict timing and power constraints. The layer configuration is tailored to balance detection accuracy with hardware efficiency, enabling real-time processing on the ZCU102 without relying on CPU-based acceleration.

This customized CNN layer serves as the core inference block in the ZCU102 demonstration, validating the feasibility of **event-driven, hardware-accelerated object detection** for high-performance edge and embedded vision applications.

![WhatsApp Image 2026-02-04 at 9 34 50 PM](https://github.com/user-attachments/assets/dfa05fd6-0596-4deb-9958-cfd84f52f244)



## License

This project is released under an open-source license.
See the `LICENSE` file for details.
