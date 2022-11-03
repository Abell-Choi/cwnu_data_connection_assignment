# cwnu_data_connection_assignment
창원대학교 데이터 통신 과제

## Stack 
### Client Stack
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

### Server Stack
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

## 🔖 To Do List
### Client Side
- 서버에서 실제 데이터를 주고받고 하는 작업 필요
- init가 완료된 경우 send thread, recv thread로 나누어서 작업하는 것을 구현해야함
- 서버에서 노드 종료 신호 발생시 해당 작업을 중단 후 로그 저장

### Server Side
- 새로운 노드 접속시 새로운 Thread 생성 후 해당 Thread에서 작업되도록 구현
- 노드에서 Request 요청 시 해당 Request 검증 후 결과값 return 해주는 작업 필요
- 시스템을 종료하는 인터럽트의 방식을 생각해야함 -> keyboard Interrupt 는 클라이언트 노드에게 정보제공이 힘들다고 판단하기에 최대한 지양
- 키보드 입력 추가 -> 노드 종료 구현을 위함

test4