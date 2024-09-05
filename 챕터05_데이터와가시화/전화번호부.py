""" 간단한 전화번호부 만들기
실행을 하면 메뉴가 뜨고 입력을 기다리고 있을 것

"""

import sqlite3
import os, json


def main_menu() -> int:
    """사용자의 입력을 받아서 검증하고 적절하다면 정수로 반환"""
    while user_input := input(
        "(1) 찾기 (2) 추가/변경 (3) 삭제 (4) 모두 보기 (5) 종료 : "
    ):
        if user_input in ("1", "2", "3", "4", "5"):
            return int(user_input)
        else:
            print("잘못된 명령입니다.")
    pass


def find_person():
    """이름을 입력받고 그 이름을 찾아서 해당 데이터 출력"""
    user_input = input("이름을 입력해주세요: ")

    if user_input in contact_data:
        print(
            "{} {} {}".format(
                user_input,
                contact_data[user_input]["Phone"],
                contact_data[user_input]["Email"],
            )
        )
    else:
        print(f'"{user_input}"를 찾지 못했습니다.')


def update_person():
    """사람 추가 또는 수정
    사용자로부터 이름, 전화번호, 이메일을 받아서
    이미 있는 이름이면 업데이트를 하고
    없는 이름이면 새로 추가
    """

    name = input("이름을 입력해주세요 : ")
    phone = input("전화번호를 입력해주세요 : ")
    email = input("이메일을 입력해주세요 : ")

    contact_data[name] = {"Phone": phone, "Email": email}


def delete_person():
    """이름을 입력받아서 삭제"""
    user_input = input("이름을 입력해주세요 : ")
    if user_input in contact_data:
        del contact_data[user_input]
    else:
        print(f'"{user_input}"을 찾지 못했습니다.')


def show_all():
    """모든 데이터 출력"""
    if not contact_data:
        print("현재 등록된 연락처가 없습니다.")
    else:
        for k, v in contact_data.items():
            print("{} {} {}".format(k, v["Phone"], v["Email"]))


# 전화번호 컨테이너를 전역변수로 정의
contact_data = {}

# 저장파일이 있을 경우 읽어서 dict 초기화
if os.path.isfile("my_contacts.json"):
    with open("my_contacts.json", encoding="utf-8") as f:
        contact_data = json.load(f)

# main_menu()로 받은 사용자의 입력에 따라 함수 호출
while (selected := main_menu()) != 5:
    if selected == 1:
        find_person()
    elif selected == 2:
        update_person()
    elif selected == 3:
        delete_person()
    elif selected == 4:
        show_all()
else:
    with open("my_contacts.json", "w", encoding="utf-8") as f:
        json.dump(contact_data, f, indent=2)

    print("종료합니다.")
