import threading
import queue
import time
import random

print("=" * 55)
print("   FreeRTOS RTOS Simulation — ESP32 Vehicle ECU")
print("=" * 55)
print()

# Shared data queue (simulates FreeRTOS queue)
sensor_queue = queue.Queue(maxsize=10)
fault_event = threading.Event()
stop_event = threading.Event()

# ─────────────────────────────────────────
# TASK 1: Sensor Read Task (Priority 3)
# Reads simulated sensor data every 500ms
# ─────────────────────────────────────────
def sensor_read_task():
    print("[RTOS] Task Started: Sensor Read Task | Priority: 3")
    iteration = 0
    while not stop_event.is_set():
        if fault_event.is_set():
            time.sleep(0.1)
            continue
        iteration += 1
        temperature = round(random.uniform(65.0, 95.0), 1)
        rpm = random.randint(1000, 4000)
        data = {"temp": temperature, "rpm": rpm, "tick": iteration}
        if not sensor_queue.full():
            sensor_queue.put(data)
        print(f"  [Sensor Read]    Tick {iteration:02d} | Temp={temperature}°C | RPM={rpm}")
        time.sleep(0.5)

# ─────────────────────────────────────────
# TASK 2: CAN Transmit Task (Priority 2)
# Reads from queue and transmits every 1 sec
# ─────────────────────────────────────────
def can_transmit_task():
    print("[RTOS] Task Started: CAN Transmit Task | Priority: 2")
    while not stop_event.is_set():
        if fault_event.is_set():
            time.sleep(0.1)
            continue
        if not sensor_queue.empty():
            data = sensor_queue.get()
            print(f"  [CAN Transmit]   Tick {data['tick']:02d} | Sending -> ID=0x100 | Temp={data['temp']}°C | RPM={data['rpm']}")
        time.sleep(1.0)

# ─────────────────────────────────────────
# TASK 3: Data Logger Task (Priority 1)
# Logs system status every 2 seconds
# ─────────────────────────────────────────
def data_logger_task():
    print("[RTOS] Task Started: Data Logger Task  | Priority: 1")
    log_count = 0
    while not stop_event.is_set():
        if fault_event.is_set():
            time.sleep(0.1)
            continue
        log_count += 1
        print(f"  [Data Logger]    Log #{log_count:02d} | Queue size={sensor_queue.qsize()} | System: NORMAL")
        time.sleep(2.0)

# ─────────────────────────────────────────
# TASK 4: Safety Monitor Task (Priority 4)
# Highest priority — triggers emergency stop
# ─────────────────────────────────────────
def safety_monitor_task():
    print("[RTOS] Task Started: Safety Monitor    | Priority: 4 (HIGHEST)")
    time.sleep(6)  # Let other tasks run first
    print()
    print("  !! [Safety Monitor] FAULT DETECTED — Overheat Condition !!")
    print("  !! [Safety Monitor] PREEMPTING ALL TASKS — EMERGENCY STOP !!")
    fault_event.set()
    time.sleep(1)
    print("  !! [Safety Monitor] System Halted. All tasks suspended.")
    print("  !! [Safety Monitor] Sending fault code 0xFF over CAN Bus.")
    print()
    stop_event.set()

# ─────────────────────────────────────────
# RTOS Scheduler — Start all tasks
# ─────────────────────────────────────────
print("[RTOS] Initializing FreeRTOS Scheduler...")
print("[RTOS] Creating tasks with assigned priorities...")
print()

t1 = threading.Thread(target=sensor_read_task, name="SensorRead")
t2 = threading.Thread(target=can_transmit_task, name="CANTransmit")
t3 = threading.Thread(target=data_logger_task, name="DataLogger")
t4 = threading.Thread(target=safety_monitor_task, name="SafetyMonitor")

t1.start()
t2.start()
t3.start()
t4.start()

t1.join()
t2.join()
t3.join()
t4.join()

print("[RTOS] All tasks terminated.")
print("[RTOS] Simulation Complete.")
print("=" * 55)
