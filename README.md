# RTOS FreeRTOS Simulation — ESP32 Vehicle ECU

## Project Overview
A Python-based simulation of FreeRTOS real-time operating system behavior
demonstrating preemptive task scheduling, priority-based execution, inter-task
communication using queues, and fault-triggered emergency stop on an ESP32
Vehicle ECU system.

## FreeRTOS Concepts Demonstrated
| Concept | Implementation |
|---------|---------------|
| Task Creation | 4 concurrent tasks with assigned priorities |
| Preemptive Scheduling | Safety Monitor preempts all tasks on fault |
| Task Priorities | Priority 1 (lowest) to Priority 4 (highest) |
| Queue | sensor_queue for inter-task data passing |
| Event Flag | fault_event triggers system-wide halt |
| Watchdog Pattern | Safety Monitor watches for fault conditions |

## Task Architecture
| Task | Priority | Interval | Function |
|------|----------|----------|----------|
| Safety Monitor | 4 (Highest) | Continuous | Detects faults, triggers emergency stop |
| Sensor Read | 3 | 500ms | Reads temperature and RPM sensor data |
| CAN Transmit | 2 | 1 second | Sends sensor data over CAN Bus (ID: 0x100) |
| Data Logger | 1 (Lowest) | 2 seconds | Logs system status and queue size |

## How Preemption Works
1. Sensor Read, CAN Transmit, and Data Logger run normally
2. At t=6s, Safety Monitor detects an overheat fault condition
3. Safety Monitor (Priority 4) immediately preempts all lower priority tasks
4. Emergency stop is triggered — all tasks are suspended
5. Fault code 0xFF is sent over CAN Bus

## How to Run
python rtos_simulation.py

No additional libraries required — uses Python standard library only.

## Real-World Application
This simulation mirrors the FreeRTOS task architecture used in automotive
ECUs and autonomous vehicle systems where safety-critical tasks must preempt
normal operations instantly on fault detection — such as in Drive-By-Wire
braking systems.

## Technologies Used
- Python 3 (threading, queue, time, random modules)
- FreeRTOS concepts (task priorities, queues, event flags, preemption)
