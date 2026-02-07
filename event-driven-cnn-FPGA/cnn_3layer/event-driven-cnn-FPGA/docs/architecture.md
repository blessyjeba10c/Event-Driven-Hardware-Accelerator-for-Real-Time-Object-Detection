# System Architecture

## 1. Overview

This project implements a **hardware-accelerated CNN inference system** on a **Xilinx Zynq SoC**, targeting **real-time edge AI workloads** such as image classification or lightweight object detection.

The architecture follows a **heterogeneous hardware/software co-design approach**, where:

- The **Arm Processing System (PS)** manages control-oriented and flexible tasks.
- The **FPGA Programmable Logic (PL)** accelerates compute-intensive CNN operations.
- A novel **event-driven sparse execution model** is introduced to improve performance, power efficiency, and FPGA resource utilization beyond conventional frame-based CNN accelerators.

The system is designed to demonstrate **quantitative performance improvements** over a **CPU-only CNN implementation** on the Arm processor.

---

## 2. High-Level Architecture

---

## 3. Functional Partitioning (PS vs PL)

### 3.1 Arm Processing System (PS)

The Arm processor handles tasks that require flexibility, control flow, or software ecosystems:

- Image capture (USB camera or stored dataset)
- Image preprocessing (resize, normalization, grayscale conversion)
- CNN configuration and parameter loading
- Accelerator control via AXI-Lite
- Post-processing (classification decision / bounding box decoding)
- Performance measurement and logging

This design choice minimizes FPGA complexity while allowing rapid experimentation and debugging.

---

### 3.2 FPGA Programmable Logic (PL)

The FPGA fabric accelerates **data-parallel and compute-heavy CNN operations**, including:

- Convolution
- Activation (ReLU)
- Pooling
- Feature map buffering

In addition, the PL introduces **event-driven sparse computation**, which is the key architectural innovation of this project.

---

## 4. Baseline CNN Accelerator Architecture

The baseline design is derived from an **open-source 3-layer CNN FPGA implementation**, consisting of:

- Input Feature Map Buffer (BRAM)
- Convolution Engine (MAC-based)
- Activation Unit (ReLU)
- Pooling Unit
- Output Feature Map Buffer

Baseline execution characteristics:

- Frame-based processing
- Dense convolution over all pixels
- Fixed computation regardless of input sparsity

This baseline serves as the **reference architecture** for performance comparison.

---

## 5. Proposed Event-Driven Sparse CNN Architecture

### 5.1 Motivation

Conventional CNN accelerators compute convolution for **all pixels**, even when:

- Input pixels are zero or near-zero
- Feature maps contain large inactive regions
- Many MAC operations contribute negligible output

This results in:
- Unnecessary computation
- Higher power consumption
- Inefficient DSP and memory usage

---

### 5.2 Event-Driven Execution Concept

Instead of processing every pixel, the proposed architecture introduces **event-based activation**:

- An **event** is generated only when an input pixel or feature exceeds a programmable threshold.
- Convolution is triggered **only for active events**, skipping inactive regions.
- This naturally introduces **spatial sparsity** into CNN execution.

---

### 5.3 Modified PL Block Diagram


## 6. Key Architectural Enhancements

### 6.1 Event Generator

- Monitors input feature maps
- Generates events when pixel magnitude exceeds a threshold
- Reduces unnecessary data movement

### 6.2 Sparse Convolution Engine

- Performs convolution only for event-triggered locations
- Skips zero-valued or inactive regions
- Significantly reduces DSP utilization per frame

### 6.3 Memory Access Optimization

- Fewer BRAM reads/writes due to sparse execution
- Improved memory bandwidth efficiency
- Reduced switching activity → lower power consumption

---

## 7. Performance Improvement Strategy

| Metric        | Baseline CNN | Event-Driven CNN |
|--------------|-------------|------------------|
| Latency      | High (dense compute) | Reduced via sparse execution |
| Throughput   | Limited by MAC count | Higher effective FPS |
| Power        | Constant per frame | Lower due to fewer operations |
| DSP Usage    | Fixed per layer | Utilized only on events |
| BRAM Access  | Dense | Sparse |

The architecture is designed to achieve:

- **≥2× speedup** over CPU-only CNN execution
- Reduced inference latency
- Improved power efficiency
- Efficient utilization of FPGA resources

---

## 8. Scalability and Extensibility

- CNN depth can be increased (more layers)
- Thresholds can be tuned dynamically from PS
- Compatible with HLS-based or RTL-based accelerators
- Can be extended toward spiking / neuromorphic CNNs

---

## 9. Summary

This architecture combines:

- Proven CNN acceleration techniques
- FPGA-friendly dataflow design
- Event-driven sparse computation for efficiency

The result is a **novel yet practical FPGA-based edge AI accelerator** that goes beyond standard CNN acceleration by exploiting **input data sparsity**, making it highly suitable for **real-time embedded inference on Zynq/Kria platforms**.

---
