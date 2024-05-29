import time
from pymavlink import mavutil

# Ініціалізація з'єднання з польотним контролером
master = mavutil.mavlink_connection('/dev/serial0', baud=115200)
master.wait_heartbeat()

# Функція для надсилання команд
def send_command(command, param1=0, param2=0, param3=0, param4=0, param5=0, param6=0, param7=0):
    master.mav.command_long_send(
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_CMD_DO_SET_MODE,
        0,
        command,
        param1, param2, param3, param4, param5, param6, param7
    )

# Функція для отримання даних телеметрії
def get_telemetry():
    msg = master.recv_match(type='ATTITUDE', blocking=True)
    if msg:
        return {
            'roll': msg.roll,
            'pitch': msg.pitch,
            'yaw': msg.yaw,
            'rollspeed': msg.rollspeed,
            'pitchspeed': msg.pitchspeed,
            'yawspeed': msg.yawspeed
        }
    return None

# Функція для зміни режиму польоту
def set_mode(mode):
    mode_id = master.mode_mapping().get(mode)
    if mode_id is not None:
        master.mav.set_mode_send(
            master.target_system,
            mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
            mode_id
        )

# Функція для керування рухом (наприклад, зміна висоти)
def change_altitude(altitude):
    master.mav.command_long_send(
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
        0,
        0, 0, 0, 0, 0, 0, altitude
    )

# Основний цикл
while True:
    # Захоплення даних телеметрії
    telemetry = get_telemetry()
    if telemetry:
        print(f"Telemetry: Roll={telemetry['roll']}, Pitch={telemetry['pitch']}, Yaw={telemetry['yaw']}")
    
    # Зміна режиму польоту на GUIDED
    set_mode('GUIDED')

    # Надсилання команди для зміни висоти
    change_altitude(10)  # Наприклад, підняти БПЛА на 10 метрів

    # Затримка
    time.sleep(5)
