import datetime
import random


class DummySensor:
    #테스트용 더미 센서. 환경 값을 무작위로 생성해 반환한다

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
        #random 범위 내 값을 생성해 env_values에 채운다
        self.env_values['mars_base_internal_temperature'] = random.uniform(
            18.0, 30.0
        )
        self.env_values['mars_base_external_temperature'] = random.uniform(
            0.0, 21.0
        )
        self.env_values['mars_base_internal_humidity'] = random.uniform(50.0, 60.0)
        self.env_values['mars_base_external_illuminance'] = random.uniform(500.0, 715.0)
        self.env_values['mars_base_internal_co2'] = random.uniform(0.02, 0.1)
        self.env_values['mars_base_internal_oxygen'] = random.uniform(4.0, 7.0)

    def get_env(self):
        #env_values를 반환하고, 요청 시 로그를 파일에 남긴다.
        log_line = self._format_log_line()
        script_dir = __file__.rsplit('\\', 1)[0]
        log_file = script_dir + '\\mars_env_log.txt'
        with open(log_file, 'a', encoding='utf-8') as file:
            file.write(log_line + '\n')
        return self.env_values

    def _format_log_line(self):
        now = datetime.datetime.now().isoformat(timespec='seconds')
        internal_temperature = self.env_values['mars_base_internal_temperature']
        external_temperature = self.env_values['mars_base_external_temperature']
        internal_humidity = self.env_values['mars_base_internal_humidity']
        external_illuminance = self.env_values['mars_base_external_illuminance']
        internal_co2 = self.env_values['mars_base_internal_co2']
        internal_oxygen = self.env_values['mars_base_internal_oxygen']

        return (
            f'datetime={now}\n'
            f'mars_base_internal_temperature={internal_temperature:.2f}\n'
            f'mars_base_external_temperature={external_temperature:.2f}\n'
            f'mars_base_internal_humidity={internal_humidity:.2f}\n'
            f'mars_base_external_illuminance={external_illuminance:.2f}\n'
            f'mars_base_internal_co2={internal_co2:.4f}\n'
            f'mars_base_internal_oxygen={internal_oxygen:.2f}'
        )


if __name__ == '__main__':
    ds = DummySensor()
    ds.set_env()
    env = ds.get_env()
    print('DummySensor env_values:')
    print(env)