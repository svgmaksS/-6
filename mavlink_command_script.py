import time
from pymavlink import mavutil

# Ініціалізація з'єднання з польотним контролером
master = mavutil.mavlink_connection('/dev/serial0', baud=115200)
master.wait_heartbeat()

# Функція для надсилання команд
def send_command(command):
    master.mav.command_long_send(
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_CMD_DO_SET_MODE,
        0,
        command,
        0, 0, 0, 0, 0, 0
    )

# Основний цикл
while True:
    # Захоплення даних телеметрії
    msg = master.recv_match(type='HEARTBEAT', blocking=True)
    print(f"Received message: {msg}")

    # Надсилання команди (наприклад, режим 1)
    send_command(1)

    # Затримка
    time.sleep(1)
