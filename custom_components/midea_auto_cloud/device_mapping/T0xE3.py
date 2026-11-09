from homeassistant.const import Platform, UnitOfTemperature, UnitOfVolume, UnitOfTime, PERCENTAGE, PRECISION_HALVES
from homeassistant.components.sensor import SensorStateClass, SensorDeviceClass
from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.components.switch import SwitchDeviceClass

DEVICE_MAPPING = {
    "default": {
        "rationale": ["off", "on"],
        "queries": [{}, {"query_type": "status"}, {"device_type": "controller"}],
        "centralized": [],
        # fork 定制：本机型（JSLQ27-M10S Plus，type 0xE3）的温度字段不是一套单位。
        # 设备 Lua 全部原样透传（out=cmd[16]、temperature=cmd[17]、return=cmd[25]、
        # in=cmd[37]、person_tem_*=cmd[33/34/40]），缩放只能在映射层做。
        #
        # 0.5 ℃ 计数：设定值 temperature、出水 out_water_tem、回水 return_water_tem
        #   - 设定：设定 38 ℃ 时上报 76；历史里 37.5→38 ℃ 时字节 75→76
        #   - 出水/回水：机器闲置时上报 42=21 ℃，与室温同向起伏；
        #     若当整度读则是 42 ℃，闲置静水不可能维持在这个温度
        # 1 ℃ 计数：in_water_tem（进水）、person_tem_one/two/three（个人预设）
        #   - 进水：官方 App 首页直接原样显示「进水温度 20℃」
        #   - 个人预设：设备自身行为可证 —— 本机 person_tem_one=40 时，
        #     启用该模式后设定值被写成 40 ℃（即半度编码的 80），说明 40 就是 40 ℃
        "calculate": {
            "get": [
                {"lvalue": "[target_temperature]", "rvalue": "[temperature] / 2"},
                {"lvalue": "[out_water_tem_c]", "rvalue": "[out_water_tem] / 2"},
                {"lvalue": "[return_water_tem_c]", "rvalue": "[return_water_tem] / 2"},
            ],
            "set": [
                # 必须套 int()：Lua 端 string.char() 只接受整数
                {"lvalue": "[temperature]", "rvalue": "int([target_temperature] * 2)"},
            ],
        },
        "entities": {
            Platform.SWITCH: {
                "power": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "bubble": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "cold_water": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "cold_water_master": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "bathtub": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "safe": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "cold_water_dot": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "change_litre_switch": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "cold_water_ai": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                "cold_water_pressure": {
                    "device_class": SwitchDeviceClass.SWITCH,
                },
                # fork 定制：Lua 里 person_mode_one 这条命令要求同一帧带上
                # person_tem_one（cmd[14]），只发开关会因为缺字节发不出去，
                # HA 报 “Failed to send command”。官方 App 也是两个字段一起发。
                "person_mode_one": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "include_current": ["person_tem_one"],
                },
                "person_mode_two": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "include_current": ["person_tem_two"],
                },
                "person_mode_three": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "include_current": ["person_tem_three"],
                },
                "lamp_control1_power": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "translation_key": "light",
                    "merge_attributes": ["lamp_control2_power", "lamp_control3_power"],
                },
                "lamp_control2_power": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "translation_key": "lamp_control2_power",
                    "merge_attributes": ["lamp_control1_power", "lamp_control3_power"],
                },
                "lamp_control3_power": {
                    "device_class": SwitchDeviceClass.SWITCH,
                    "translation_key": "lamp_control3_power",
                    "merge_attributes": ["lamp_control1_power", "lamp_control2_power"],
                },
                # "gesture_function": {
                #     "device_class": SwitchDeviceClass.SWITCH,
                # }
            },
            Platform.CLIMATE: {
                "water_heater": {
                    "power": "power",
                    "hvac_modes": {
                        "off": {"power": "off"},
                        "heat": {"power": "on", "mode": "shower"}
                    },
                    # fork 定制：改读 calculate 换算后的摄氏度属性，不再直接用原始半度计数
                    "target_temperature": "target_temperature",
                    # fork 定制：出水和设定值同为 0.5 ℃ 编码，读换算后的值
                    "current_temperature": "out_water_tem_c",
                    # fork 定制：设备实际可设范围是 32–60 ℃（原映射写 20，设备会拒绝）
                    "min_temp": 32,
                    "max_temp": 60,
                    "temperature_unit": UnitOfTemperature.CELSIUS,
                    "precision": PRECISION_HALVES,
                }
            },
            Platform.SELECT: {
                "mode": {
                    "options": {
                        "shower": {"mode": "shower"},
                        "bath": {"mode": "bath"},
                        "mixed": {"mode": "mixed"},
                        "eco": {"mode": "eco"},
                        "kitchen": {"mode": "kitchen"},
                        "thalposis": {"mode": "thalposis"},
                        "intelligence": {"mode": "intelligence"},
                        "unfreeze": {"mode": "unfreeze"},
                        "wash_bowl": {"mode": "wash_bowl"},
                        "high_temperature": {"mode": "high_temperature"},
                        "baby": {"mode": "baby"},
                        "adult": {"mode": "adult"},
                        "old": {"mode": "old"}
                    }
                },
                "power_level": {
                    "options": {
                        "low": {"power_level": 0},
                        "medium": {"power_level": 1},
                        "high": {"power_level": 2},
                        "max": {"power_level": 3}
                    }
                },
                "type_machine": {
                    "options": {
                        "standard": {"type_machine": 20},
                        "premium": {"type_machine": 21},
                        "deluxe": {"type_machine": 22}
                    }
                },
                "capacity": {
                    "options": {
                        "small": {"capacity": 1},
                        "medium": {"capacity": 2},
                        "large": {"capacity": 3}
                    }
                },
                # "gesture_function_type": {
                #     "options": {
                #         "none": {"gesture_function_type": "0"},
                #         "wave": {"gesture_function_type": "1"},
                #         "touch": {"gesture_function_type": "2"},
                #         "proximity": {"gesture_function_type": "3"}
                #     }
                # }
            },
            Platform.SENSOR: {
                "out_water_tem": {
                    # fork 定制：出水是 0.5 ℃ 编码，改读换算后的摄氏度
                    "attribute": "out_water_tem_c",
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "water_volume": {
                    "device_class": SensorDeviceClass.VOLUME,
                    "unit_of_measurement": UnitOfVolume.LITERS,
                    "state_class": SensorStateClass.TOTAL_INCREASING
                },
                "zero_cold_tem": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "bath_out_volume": {
                    "device_class": SensorDeviceClass.VOLUME,
                    "unit_of_measurement": UnitOfVolume.LITERS,
                    "state_class": SensorStateClass.TOTAL_INCREASING
                },
                "return_water_tem": {
                    # fork 定制：回水同出水，0.5 ℃ 编码
                    "attribute": "return_water_tem_c",
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "change_litre": {
                    "device_class": SensorDeviceClass.VOLUME,
                    "unit_of_measurement": UnitOfVolume.LITERS,
                    "state_class": SensorStateClass.TOTAL_INCREASING
                },
                "bathtub_water_level": {
                    "device_class": SensorDeviceClass.VOLUME,
                    "unit_of_measurement": UnitOfVolume.LITERS,
                    "state_class": SensorStateClass.TOTAL_INCREASING
                },
                "temperature": {
                    # fork 定制：实体 ID 保持不变，但改读换算后的摄氏度；
                    # 不写 attribute 的话这里会显示原始的 76 这种半度计数。
                    "attribute": "target_temperature",
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "gas_lift_percent": {
                    "device_class": SensorDeviceClass.POWER_FACTOR,
                    "unit_of_measurement": PERCENTAGE,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "person_tem_one": {
                    # 1 ℃ 编码，与 App 显示一致，不做换算
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "person_tem_two": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "person_tem_three": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "in_water_tem": {
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "unit_of_measurement": UnitOfTemperature.CELSIUS,
                    "state_class": SensorStateClass.MEASUREMENT
                },
                "error_code": {
                    "device_class": SensorDeviceClass.ENUM
                }
            }
        }
    }
}
