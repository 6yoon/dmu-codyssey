def read_csv_file(filename):
    # CSV 파일을 읽어서 헤더와 데이터 목록을 반환한다.
    rows = []

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()

                if not line:
                    continue

                parts = line.split(',')
                cleaned_row = []

                for item in parts:
                    cleaned_row.append(item.strip())

                rows.append(cleaned_row)

    except FileNotFoundError:
        print(f'파일을 찾을 수 없습니다: {filename}')
        return None, None
    except PermissionError:
        print(f'파일에 접근할 권한이 없습니다: {filename}')
        return None, None
    except OSError as error:
        print(f'파일을 읽는 중 오류가 발생했습니다: {error}')
        return None, None

    if not rows:
        print('파일 내용이 비어 있습니다.')
        return None, None

    header = rows[0]
    data = rows[1:]

    return header, data


def get_column_widths(header, data):
    # 각 컬럼의 출력 너비를 계산한다.
    widths = []

    for i in range(len(header)):
        max_width = len(header[i])

        for row in data:
            if i < len(row):
                cell_length = len(row[i])
                if cell_length > max_width:
                    max_width = cell_length

        widths.append(max_width + 2)

    return widths


def print_table(header, data, title):
    # 리스트 형태 데이터를 표 형태로 출력한다.
    if not header:
        print('헤더 정보가 없습니다.')
        return

    widths = get_column_widths(header, data)

    print('\n' + '=' * 70)
    print(title)
    print('=' * 70)

    for i in range(len(header)):
        print(f'{header[i]:<{widths[i]}}', end='')
    print()

    print('-' * 70)

    for row in data:
        if len(row) != len(header):
            continue

        for i in range(len(row)):
            print(f'{row[i]:<{widths[i]}}', end='')
        print()

    print('=' * 70)


def convert_to_list_object(header, data):
    #CSV 내용을 파이썬 리스트 객체로 변환한다.
    #각 행은 딕셔너리 형태로 저장한다.
    inventory_list = []

    for row in data:
        if len(row) != len(header):
            continue

        item = {}

        for i in range(len(header)):
            item[header[i]] = row[i]

        inventory_list.append(item)

    return inventory_list


def sort_by_flammability(inventory_list):
    #인화성 지수를 기준으로 내림차순 정렬한다.
    def get_flammability(item):
        try:
            return float(item['Flammability'])
        except (ValueError, KeyError):
            return 0.0

    return sorted(inventory_list, key=get_flammability, reverse=True)


def filter_danger_items(inventory_list, threshold):
    #인화성 지수가 threshold 이상인 항목만 추출한다.
    danger_list = []

    for item in inventory_list:
        try:
            flammability = float(item['Flammability'])
            if flammability >= threshold:
                danger_list.append(item)
        except (ValueError, KeyError):
            continue

    return danger_list


def print_inventory_list(inventory_list, title):
    #딕셔너리 리스트를 표 형태로 출력한다.
    if not inventory_list:
        print('\n' + '=' * 70)
        print(title)
        print('=' * 70)
        print('출력할 데이터가 없습니다.')
        print('=' * 70)
        return

    header = list(inventory_list[0].keys())
    data = []

    for item in inventory_list:
        row = []

        for key in header:
            row.append(str(item.get(key, '')))

        data.append(row)

    print_table(header, data, title)


def save_to_csv(filename, inventory_list):
    #딕셔너리 리스트를 CSV 파일로 저장한다.
    if not inventory_list:
        print('저장할 데이터가 없습니다.')
        return

    header = list(inventory_list[0].keys())

    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(','.join(header) + '\n')

            for item in inventory_list:
                row_values = []

                for key in header:
                    row_values.append(str(item.get(key, '')))

                file.write(','.join(row_values) + '\n')

        print(f'\n딕셔너리 리스트가 CSV 파일로 저장되었습니다: {filename}')

    except PermissionError:
        print(f'파일에 쓸 권한이 없습니다: {filename}')
    except OSError as error:
        print(f'CSV 파일 저장 중 오류가 발생했습니다: {error}')


def save_to_binary(filename, inventory_list):
    # 딕셔너리 리스트를 바이트 형태로 변환하여 이진 파일로 저장한다.
    if not inventory_list:
        print('저장할 데이터가 없습니다.')
        return

    try:
        lines = []

        # header
        header = list(inventory_list[0].keys())
        lines.append(','.join(header))

        # data
        for item in inventory_list:
            row = []

            for key in header:
                row.append(str(item.get(key, '')))

            lines.append(','.join(row))

        # 문자열로 합치기
        text_data = '\n'.join(lines)

        # 문자열 → 바이트 변환
        binary_data = text_data.encode('utf-8')

        # 이진 파일로 저장
        with open(filename, 'wb') as file:
            file.write(binary_data)

        print(f'\n이진 파일 저장 완료: {filename}')

    except PermissionError:
        print(f'파일에 쓸 권한이 없습니다: {filename}')
    except OSError as error:
        print(f'이진 파일 저장 중 오류가 발생했습니다: {error}')


def read_from_binary(filename):
    # 이진 파일 내용을 그대로 출력한다.
    try:
        with open(filename, 'rb') as file:
            binary_data = file.read()

        print('\n' + '=' * 70)
        print('Mars_Base_Inventory_List.bin 원본 출력')
        print('=' * 70)

        print(binary_data)

        print('=' * 70)

    except FileNotFoundError:
        print(f'이진 파일을 찾을 수 없습니다: {filename}')
    except PermissionError:
        print(f'이진 파일에 접근할 권한이 없습니다: {filename}')
    except OSError as error:
        print(f'이진 파일을 읽는 중 오류가 발생했습니다: {error}')


def main():
    input_file = 'Mars_Base_Inventory_List.csv'
    output_csv_file = 'Mars_Base_Inventory_danger.csv'
    output_bin_file = 'Mars_Base_Inventory_List.bin'
    threshold = 0.7

    header, raw_data = read_csv_file(input_file)

    if header is None or raw_data is None:
        return

    print_table(header, raw_data, '원본 CSV 데이터 출력')

    inventory_list = convert_to_list_object(header, raw_data)

    print('\n리스트(List) 객체 변환 결과 예시')
    print(inventory_list[:3])

    sorted_inventory = sort_by_flammability(inventory_list)
    print_inventory_list(sorted_inventory, '인화성 지수 기준 내림차순 정렬 결과')

    danger_items = filter_danger_items(sorted_inventory, threshold)
    print_inventory_list(danger_items, '인화성 지수 0.7 이상 위험 물질 목록')

    save_to_csv(output_csv_file, danger_items)
    save_to_binary(output_bin_file, sorted_inventory)
    read_from_binary(output_bin_file)


main()