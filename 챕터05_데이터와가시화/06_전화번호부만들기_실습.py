"""
- 이름이 동일한 사람이 없다고 가정하고 사람을 찾을 때도 이름으로만 찾는다.
- 사전 안의 사전 {"홍정모":{"Phone":"1234-1234", "Email":"jh@abc.efg"}}
- 파일에 전화번호부를 저장해서 다시 시작할때 이전 데이터가 다시 불러들여지도록 구현
- 파일 저장 형식은 자유 (csv, json, pickle 등 자유)
- 스크립트 모드에서 구현 권장
- 디버거를 적극적으로 사용
"""

import os
import json


def main_menu() -> int:
    """사용자의 입력을 받아서 검증하고 적절하다면 정수로 반환합니다."""

    return 5  # 교체


def show_all():
    """모든 데이터 출력"""

    pass


def find_person():
    """이름을 입력받고 그 이름으로 찾아서 해당 데이터 출력"""

    pass


def update_person():
    """사람 추가 또는 수정
    사용자로부터 이름, 전화번호, 이메일을 입력받아서
    이미 있는 이름이면 업데이트를 하고
    없는 이름이면 새로 추가
    """

    pass


def delete_person():
    """이름을 입력받아서 데이터 삭제"""

    pass


# 프로그램 실행의 시작
# 시작할 때 저장파일이 존재하면 읽어들여서 데이터 초기화
# 메인메뉴에서 사용자 입력을 받은 후에 알맞게 기능 수행
# 종료할 때 데이터 저장

# 전화번호부 저장용 dict (전역변수)
contact_data = {}

if os.path.isfile("my_contacts.json"):
    # 저장 파일이 있을 경우 읽어서 dict 초기화
    pass

# main_menu()로 받아온 사용자의 입력에 따라 함수 호출
while (selected := main_menu()) != 5:  # 5는 종료 메뉴

    pass

else:
    # 종료하기 전 파일로 데이터 저장
    pass

    print("종료합니다.")
