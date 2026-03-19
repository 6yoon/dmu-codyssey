from __future__ import annotations

import csv
import sys
from pathlib import Path
from typing import List, Dict


NEGATIVE_KEYWORDS = [
    "unstable", "explosion", "error", "fail", "failure", "critical",
    "warning", "fault", "leak", "overheat", "shutdown",
]


def read_log_file(path: Path) -> List[Dict[str, str]]:
    # CSV 로그 파일을 읽고 각 행을 딕셔너리로 반환한다.
    # 파일 처리 중 발생할 수 있는 예외는 호출한 쪽에서 처리한다.
    rows: List[Dict[str, str]] = []
    with path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row:
                rows.append(row)
    return rows

def print_logs(rows: List[Dict[str, str]]) -> None:
    # 로그를 시간 순서대로(정상 순서) 화면에 출력한다.
    for row in rows:
        print(f"{row['timestamp']},{row['event']},{row['message']}")

def print_logs_reverse(rows: List[Dict[str, str]]) -> None:
    # 로그를 시간의 역순으로 화면에 출력한다.
    # 마지막에 기록된 로그부터 먼저 보이도록 reversed를 사용한다.
    for row in reversed(rows):
        print(f"{row['timestamp']},{row['event']},{row['message']}")



def find_problem_logs(rows: List[Dict[str, str]]) -> List[Dict[str, str]]:
    # 메시지 안의 이상 키워드를 기준으로 문제 로그만 추려낸다.
    problems: List[Dict[str, str]] = []
    for row in rows:
        message = row.get("message", "").lower()
        if any(keyword in message for keyword in NEGATIVE_KEYWORDS):
            problems.append(row)
    return problems



def save_problem_logs(problem_rows: List[Dict[str, str]], output_path: Path) -> None:
    # 문제로 판단한 로그만 별도 파일에 저장한다.
    # 원본과 같은 CSV 형식으로 저장해 다시 확인하기 쉽게 만든다.
    with output_path.open("w", encoding="utf-8", newline="") as file:
        file.write("timestamp,event,message\n")
        for row in problem_rows:
            file.write(f"{row['timestamp']},{row['event']},{row['message']}\n")



def main() -> int:
    # 로그를 읽고 출력, 역순 출력, 문제 로그 저장까지 전체 흐름을 수행한다.
    log_path = Path("mission_computer_main.log")
    problem_output_path = Path("problem_logs.log")

    try:
        rows = read_log_file(log_path)
        print("[로그 전체 출력 - 시간 순]")
        print_logs(rows)    
        print("[로그 전체 출력 - 시간 역순]")
        print_logs_reverse(rows)

        problem_rows = find_problem_logs(rows)
        save_problem_logs(problem_rows, problem_output_path)

        print(f"\n[문제 로그 저장 완료] {problem_output_path}")
        return 0

    except FileNotFoundError:
        print("로그 파일을 찾을 수 없습니다.", file=sys.stderr)
        return 1
    except PermissionError:
        print("로그 파일에 접근할 권한이 없습니다.", file=sys.stderr)
        return 1
    except UnicodeDecodeError:
        print("로그 파일의 인코딩을 읽을 수 없습니다.", file=sys.stderr)
        return 1
    except KeyError:
        print("CSV 헤더(timestamp, event, message)를 확인해주세요.", file=sys.stderr)
        return 1
    except Exception as error:
        print(f"예상하지 못한 오류가 발생했습니다: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
