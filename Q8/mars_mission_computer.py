import json
import os
import platform

try:
    import psutil
except ImportError:
    psutil = None


class MissionComputer:
    '화성 기지 미션 컴퓨터의 환경 정보와 시스템 상태를 관리한다.'

    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': None,
            'mars_base_external_temperature': None,
            'mars_base_internal_humidity': None,
            'mars_base_external_illuminance': None,
            'mars_base_internal_co2': None,
            'mars_base_internal_oxygen': None,
        }
        self.setting_file = 'setting.txt'

    def _bytes_to_gb(self, byte_size):
        '바이트 단위를 GB 단위 문자열로 변환한다.'
        return f'{byte_size / (1024 ** 3):.2f} GB'

    def _load_settings(self):
        'setting.txt 파일을 읽어 출력할 항목 설정을 반환한다.'
        default_settings = {
            'operating_system': True,
            'operating_system_version': True,
            'cpu_type': True,
            'cpu_core_count': True,
            'memory_size': True,
            'cpu_realtime_usage': True,
            'memory_realtime_usage': True,
        }

        try:
            with open(self.setting_file, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()

                    if not line or line.startswith('#') or '=' not in line:
                        continue

                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip().lower()

                    if key in default_settings:
                        default_settings[key] = value in ('true', '1', 'yes', 'on')
        except FileNotFoundError:
            pass
        except OSError as error:
            print(
                json.dumps(
                    {
                        'error': 'setting.txt 파일을 읽는 중 오류가 발생했습니다.',
                        'details': str(error),
                    },
                    ensure_ascii = False,
                    indent = 4,
                )
            )

        return default_settings

    def get_mission_computer_info(self):
        '미션 컴퓨터의 시스템 정보를 JSON 형식으로 출력한다.'
        settings = self._load_settings()
        info = {}

        try:
            os_name = platform.system()
            os_version = platform.version()
            cpu_type = platform.processor()

            if not cpu_type:
                cpu_type = platform.machine()

            cpu_core_count = os.cpu_count()

            if psutil is None:
                raise ImportError('psutil 라이브러리가 설치되어 있지 않습니다.')

            memory_size = self._bytes_to_gb(psutil.virtual_memory().total)

            if settings['operating_system']:
                info['operating_system'] = os_name
            if settings['operating_system_version']:
                info['operating_system_version'] = os_version
            if settings['cpu_type']:
                info['cpu_type'] = cpu_type if cpu_type else '확인 불가'
            if settings['cpu_core_count']:
                info['cpu_core_count'] = cpu_core_count
            if settings['memory_size']:
                info['memory_size'] = memory_size
        except ImportError as error:
            info = {
                'error': '시스템 정보 조회에 필요한 라이브러리를 불러올 수 없습니다.',
                'details': str(error),
            }
        except Exception as error:
            info = {
                'error': '시스템 정보를 가져오는 중 오류가 발생했습니다.',
                'details': str(error),
            }

        print(json.dumps(info, ensure_ascii = False, indent = 4))
        return info

    def get_mission_computer_load(self):
        '미션 컴퓨터의 실시간 부하 정보를 JSON 형식으로 출력한다.'
        settings = self._load_settings()
        load_info = {}

        try:
            if psutil is None:
                raise ImportError('psutil 라이브러리가 설치되어 있지 않습니다.')

            cpu_usage = psutil.cpu_percent(interval = 1)
            memory_usage = psutil.virtual_memory().percent

            if settings['cpu_realtime_usage']:
                load_info['cpu_realtime_usage'] = f'{cpu_usage:.1f}%'
            if settings['memory_realtime_usage']:
                load_info['memory_realtime_usage'] = f'{memory_usage:.1f}%'
        except ImportError as error:
            load_info = {
                'error': '시스템 부하 조회에 필요한 라이브러리를 불러올 수 없습니다.',
                'details': str(error),
            }
        except Exception as error:
            load_info = {
                'error': '시스템 부하를 가져오는 중 오류가 발생했습니다.',
                'details': str(error),
            }

        print(json.dumps(load_info, ensure_ascii = False, indent = 4))
        return load_info


if __name__ == '__main__':
    runComputer = MissionComputer()
    runComputer.get_mission_computer_info()
    runComputer.get_mission_computer_load()
