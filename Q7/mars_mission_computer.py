import json
import random
import time


class DummySensor:
    '테스트용 더미 센서. 환경 값을 무작위로 생성해 반환한다.'

    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': None,
            'mars_base_external_temperature': None,
            'mars_base_internal_humidity': None,
            'mars_base_external_illuminance': None,
            'mars_base_internal_co2': None,
            'mars_base_internal_oxygen': None,
        }

    def set_env(self):
        '임의의 환경 값을 생성해 env_values에 저장한다.'
        self.env_values['mars_base_internal_temperature'] = round(
            random.uniform(18.0, 30.0), 2
        )
        self.env_values['mars_base_external_temperature'] = round(
            random.uniform(0.0, 21.0), 2
        )
        self.env_values['mars_base_internal_humidity'] = round(
            random.uniform(50.0, 60.0), 2
        )
        self.env_values['mars_base_external_illuminance'] = round(
            random.uniform(500.0, 715.0), 2
        )
        self.env_values['mars_base_internal_co2'] = round(
            random.uniform(0.02, 0.1), 4
        )
        self.env_values['mars_base_internal_oxygen'] = round(
            random.uniform(4.0, 7.0), 2
        )

    def get_env(self):
        '최신 환경 값을 반환한다.'
        self.set_env()
        return self.env_values


class MissionComputer:
    '미션 컴퓨터. 더미 센서에서 환경 값을 받아 저장하고 출력한다.'

    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': None,
            'mars_base_external_temperature': None,
            'mars_base_internal_humidity': None,
            'mars_base_external_illuminance': None,
            'mars_base_internal_co2': None,
            'mars_base_internal_oxygen': None,
        }
        self.ds = DummySensor()
        self.history = []

    def print_average(self):
        '누적된 5분간의 환경 값 평균을 출력한다.'
        if not self.history:
            return

        average_values = {}

        for key in self.env_values:
            total = 0
            for item in self.history:
                total += item[key]
            average_values[key] = round(total / len(self.history), 2)

        print('5-minute average:')
        print(json.dumps(average_values, indent=4))
        print()

    def get_sensor_data(self):
        '5초마다 센서 값을 받아 저장하고 JSON 형태로 출력한다.'
        start_time = time.time()
        last_average_time = start_time

        try:
            while True:
                sensor_data = self.ds.get_env()

                for key, value in sensor_data.items():
                    self.env_values[key] = value

                self.history.append(self.env_values.copy())

                print(json.dumps(self.env_values, indent=4))
                print()

                current_time = time.time()

                if current_time - last_average_time >= 300:
                    self.print_average()
                    self.history = []
                    last_average_time = current_time

                time.sleep(5)

        except KeyboardInterrupt:
            print('System stopped....')


RunComputer = MissionComputer()
RunComputer.get_sensor_data()