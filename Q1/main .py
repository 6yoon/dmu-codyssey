NEGATIVE_KEYWORDS = [
    "unstable", "explosion", "error", "fail", "failure", "critical",
    "warning", "fault", "leak", "overheat", "shutdown",
]


def read_log_file(path):
    # 로그 파일을 한 줄씩 읽고 timestamp, event, message로 분리한다.
    # 첫 줄 헤더는 건너뛰고, 나머지 줄은 딕셔너리 형태로 저장한다.
    rows = []

    with open(path, "r", encoding="utf-8") as file:
        first_line = True

        for line in file:
            line = line.strip()

            if not line:
                continue

            if first_line:
                first_line = False
                continue

            parts = line.split(",", 2)
            if len(parts) != 3:
                continue

            row = {
                "timestamp": parts[0].strip(),
                "event": parts[1].strip(),
                "message": parts[2].strip(),
            }
            rows.append(row)

    return rows


def print_logs(rows):
    # 로그를 시간 순서대로 화면에 출력한다.
    for row in rows:
        print(row["timestamp"] + "," + row["event"] + "," + row["message"])


def print_logs_reverse(rows):
    # 로그를 시간의 역순으로 화면에 출력한다.
    for i in range(len(rows) - 1, -1, -1):
        row = rows[i]
        print(row["timestamp"] + "," + row["event"] + "," + row["message"])


def find_problem_logs(rows):
    # 메시지 안의 이상 키워드를 기준으로 문제 로그만 골라낸다.
    problems = []

    for row in rows:
        message = row["message"].lower()

        for keyword in NEGATIVE_KEYWORDS:
            if keyword in message:
                problems.append(row)
                break

    return problems


def save_problem_logs(problem_rows, output_path):
    # 문제 로그만 별도 파일에 저장한다.
    with open(output_path, "w", encoding="utf-8") as file:
        file.write("timestamp,event,message\n")

        for row in problem_rows:
            line = row["timestamp"] + "," + row["event"] + "," + row["message"] + "\n"
            file.write(line)


def main():
    # 로그를 읽고 정상 출력, 역순 출력, 문제 로그 저장까지 수행한다.
    log_path = "mission_computer_main.log"
    problem_output_path = "problem_logs.log"

    try:
        rows = read_log_file(log_path)

        print("[로그 전체 출력 - 시간 순]")
        print_logs(rows)

        print("\n[로그 전체 출력 - 시간 역순]")
        print_logs_reverse(rows)

        problem_rows = find_problem_logs(rows)
        save_problem_logs(problem_rows, problem_output_path)

        print("\n[문제 로그 저장 완료] " + problem_output_path)
        return 0

    except FileNotFoundError:
        print("로그 파일을 찾을 수 없습니다.")
        return 1
    except PermissionError:
        print("로그 파일에 접근할 권한이 없습니다.")
        return 1
    except UnicodeDecodeError:
        print("로그 파일의 인코딩을 읽을 수 없습니다.")
        return 1
    except Exception as error:
        print("예상하지 못한 오류가 발생했습니다:", error)
        return 1


if __name__ == "__main__":
    main()