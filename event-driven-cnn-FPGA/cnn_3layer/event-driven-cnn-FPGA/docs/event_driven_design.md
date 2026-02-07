# Event-Driven Sparse CNN Accelerator Design

## 1. Introduction

This document describes the event-driven sparse CNN acceleration approach adopted in this project to enhance performance, power efficiency, and FPGA resource utilization on a Xilinx Zynq SoC platform.

Conventional CNN accelerators perform dense, clock-driven computation, where all convolution operations are executed for every input pixel and kernel weight, regardless of whether the input contributes meaningful information. This leads to unnecessary multiply–accumulate (MAC) operations, increased latency, higher power consumption, and inefficient use of FPGA resources.

To overcome these limitations, this project introduces an **event-driven sparse CNN micro-architecture**, in which computation is triggered only when significant input activations occur.

---

## 2. Dense CNN vs Event-Driven CNN

### 2.1 Dense CNN Processing

In a conventional CNN accelerator:

- All pixels are streamed through the convolution engine.
- Every kernel weight is applied to every input position.
- MAC units operate continuously on every clock cycle.
- Zero or near-zero inputs still consume computation and power.
- Control logic is clock-driven rather than data-driven.

This leads to:

- High dynamic power consumption  
- Redundant MAC operations  
- Increased latency for sparse or low-contrast inputs  

---

### 2.2 Event-Driven Sparse CNN Processing

In the proposed event-driven CNN:

- Input pixels are first evaluated for significance.
- Only pixels above a programmable threshold generate **events**.
- MAC operations are executed only for event locations.
- Idle MAC units are clock-gated when no events are present.
- Data movement and buffering are minimized.

This results in:

- Reduced MAC count  
- Lower memory bandwidth  
- Lower dynamic power  
- Improved latency and throughput  

---

## 3. High-Level Architecture

The event-driven CNN accelerator consists of the following major blocks:

1. Event Generator  
2. Event Queue / FIFO  
3. Event Scheduler  
4. Sparse Control Unit  
5. MAC Array (Processing Elements)  
6. Activation + Pooling Unit  
7. Output Buffer  
8. ARM Interface (AXI-Lite + AXI-Stream)  

---

## 4. Event Generator

### Function

The Event Generator monitors incoming pixels or feature map values and determines whether they are significant enough to trigger computation.

### Operation

- Input: `pixel_value`, `pixel_valid`  
- Output: `event_valid`, `event_x`, `event_y`, `event_value`  

### Logic

```
If |pixel_value| ≥ THRESHOLD:
    Generate event packet:
      {x, y, channel, pixel_value}
Else:
    No event generated
```

### Purpose

- Suppresses zero or near-zero activations.
- Converts dense pixel streams into sparse event streams.

---

## 5. Event Queue (FIFO)

### Function

Buffers events between the Event Generator and the MAC scheduler.

### Purpose

- Absorbs bursty event arrivals.
- Decouples input rate from compute rate.
- Provides flow control.

---

## 6. Event Scheduler

### Function

Selects the next event to be processed and generates the corresponding convolution window addresses.

### Responsibilities

- Dequeues events from FIFO.
- Computes convolution kernel offsets.
- Generates memory read addresses for:
  - Input window
  - Kernel weights
- Issues execution commands to MAC array.

---

## 7. Sparse Control Unit

### Function

Controls whether MAC units should operate or remain idle.

### Features

- Enables MACs only when events are valid.
- Disables MACs when FIFO is empty.
- Performs clock gating of inactive logic.
- Tracks outstanding events.

---

## 8. MAC Array (Processing Elements)

### Function

Performs convolution MAC operations for event-triggered windows.

### Operation

- Each event triggers:
  - K×K MAC operations
  - One output accumulation
- Supports:
  - Weight reuse
  - Partial sum accumulation

---

## 9. Activation and Pooling Unit

### Function

Processes MAC outputs.

### Operations

- ReLU activation
- Optional max pooling or average pooling

### Event-Driven Behavior

- Activated only when MAC outputs are valid.
- Otherwise remains idle.

---

## 10. Output Buffer

### Function

Stores computed output activations.

### Behavior

- Writes only when valid outputs occur.
- Skips empty or zero-valued regions.

---

## 11. ARM Interface

### Interfaces

- AXI-Lite:
  - Configuration
  - Threshold setting
  - Start/stop control
  - Status registers

- AXI-Stream:
  - Input pixel streaming
  - Output feature streaming

---

## 12. Integration into Existing CNN RTL

The baseline CNN accelerator is modified as follows:

| Baseline Block        | Event-Driven Modification            |
|----------------------|--------------------------------------|
| Input Stream         | Event Generator added                |
| FIFO Buffers         | Event Queue inserted                 |
| PE Controller        | Driven by Event Scheduler            |
| MAC Array            | Enabled only on event_valid          |
| Global Controller    | Extended for sparse mode             |
| Clocking             | Clock-gated idle blocks              |

---

## 13. Expected Benefits

### 13.1 Latency

- Fewer convolution windows processed.
- Reduced execution cycles per frame.

### 13.2 Throughput

- Higher effective frame rate under sparse inputs.
- Less contention for compute resources.

### 13.3 Power Efficiency

- Reduced MAC activity.
- Reduced memory access.
- Clock gating of idle logic.

### 13.4 FPGA Resource Efficiency

- Smaller MAC arrays sufficient for target throughput.
- Lower BRAM bandwidth requirements.
- Improved DSP utilization efficiency.

---

## 14. Alignment with Project Performance Targets

| Metric        | Improvement Mechanism                          |
|---------------|-----------------------------------------------|
| Latency       | Skip zero-activation windows                  |
| Throughput    | Event-based scheduling                        |
| Power         | MAC gating + reduced memory access            |
| LUT / DSP     | Smaller active compute footprint              |
| BRAM          | Sparse buffer writes                          |

---

## 15. Why This Is Novel for the Competition

- Moves beyond dense CNN acceleration.
- Introduces data-driven computation.
- Demonstrates architectural innovation.
- Shows deep hardware/software co-design insight.
- Aligns strongly with edge AI constraints.

---

## 16. Summary

This event-driven sparse CNN accelerator introduces a data-driven execution model that improves latency, throughput, power efficiency, and FPGA resource utilization compared to conventional dense CNN accelerators.

This architectural enhancement directly supports the competition’s objectives of:

- Real-time inference  
- Minimum 2× speedup  
- Improved power efficiency  
- Efficient FPGA utilization  

and provides a clear technical differentiator from baseline CNN accelerator implementations.

