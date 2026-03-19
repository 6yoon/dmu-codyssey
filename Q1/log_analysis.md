# mission_computer_main.log 분석 보고서

## 분석 대상
- 파일명: `mission_computer_main.log`
- 형식: `timestamp,event,message`
- 분석 목적: 로그 내용을 바탕으로 문제 원인을 정리하고, 문제 로그만 별도로 분리한다.

## 로그 흐름
로그 전반부는 발사 준비, 이륙, 궤도 진입, 위성 배치, 재진입, 착륙, 임무 완료까지 정상 흐름을 기록하고 있다. 특히 `Mission completed successfully`와 `Touchdown confirmed`가 먼저 나타나므로, 11시 30분 전까지는 임무가 정상 종료된 것으로 보인다.

그런데 이후 11시 35분에 `Oxygen tank unstable.`가 기록되고, 11시 40분에 `Oxygen tank explosion.`가 이어서 나타난다. 즉, 정상 종료 이후 산소 탱크 상태가 불안정해졌고, 그 직후 폭발이 발생했다.

## 사고 원인 판단
가장 직접적인 사고 원인은 **산소 탱크 폭발(Oxygen tank explosion)** 로 판단된다.

그 근거는 다음과 같다.
- `2023-08-27 11:35:00,INFO,Oxygen tank unstable.`
- `2023-08-27 11:40:00,INFO,Oxygen tank explosion.`

따라서 사고는 , **산소 탱크의 불안정 상태가 먼저 나타난 뒤 폭발로 이어진 과정**으로 해석하는 것이 가장 타당하다.
