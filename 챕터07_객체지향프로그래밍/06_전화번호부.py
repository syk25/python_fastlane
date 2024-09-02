""" 개인 학습용이며 인터넷에 공개할 수 없습니다.
©2022 HongLab, Inc. All Rights Reserved

- 이름이 동일한 사람이 없다고 가정하고 사람을 찾을 때도 이름으로만 찾는다.
- 사전 안의 사전 {"홍정모":{"Phone":"1234-1234", "Email":"jh@abc.efg"}}
- 파일에 전화번호부를 저장해서 다시 시작할때 이전 데이터가 다시 불러들여지도록 구현
- 파일 저장 형식은 자유 (csv, json, pickle 등 자유)
- 스크립트 모드에서 구현 권장
- 디버거를 적극적으로 사용
"""

import os
import json


def show_all():
    """모든 데이터 출력"""

    if contact_data:
        for k, v in contact_data.items():
            print("{} {} {}".format(k, v["Phone"], v["Email"]))
    else:
        print("현재 등록된 연락처가 없습니다.")


def find_person():
    """이름을 입력받고 그 이름으로 찾아서 해당 데이터 출력"""

    user_input = input("이름을 입력해주세요 : ")

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
    사용자로부터 이름, 전화번호, 이메일을 입력받아서
    이미 있는 이름이면 업데이트를 하고
    없는 이름이면 새로 추가
    """

    name = input("이름을 입력해주세요 : ")
    phone = input("전화번호를 입력해주세요 : ")
    email = input("이메일을 입력해주세요 : ")

    contact_data[name] = {"Phone": phone, "Email": email}


def delete_person():
    """이름을 입력받아서 데이터 삭제"""

    user_input = input("이름을 입력해주세요 : ")

    if user_input in contact_data:
        del contact_data[user_input]
    else:
        print(f'"{user_input}"를 찾지 못했습니다.')


def main_menu() -> int:
    """사용자의 입력을 받아서 검증하고 적절하다면 정수로 반환합니다."""

    while user_input := input("(1) 찾기 (2) 추가/변경 (3) 삭제 (4) 모두 보기 (5) 종료 : "):
        if user_input in ("1", "2", "3", "4", "5"):
            return int(user_input)
        else:
            print("잘못된 명령입니다.")


# 프로그램 실행의 시작
# 시작할 때 저장파일이 존재하면 읽어들여서 데이터 초기화
# 메인메뉴에서 사용자 입력을 받은 후에 알맞게 기능 수행
# 종료할 때 데이터 저장

# 전화번호부 저장용 dict (전역변수)
contact_data = {}


def main():

    global contact_data

    if os.path.isfile("my_contacts.json"):
        # 저장 파일이 있을 경우 읽어서 dict 초기화
        with open("my_contacts.json", encoding="utf8") as f:
            contact_data = json.load(f)

    # main_menu()로 받아온 사용자의 입력에 따라 함수 호출
    while (selected := main_menu()) != 5:  # 5는 종료 메뉴

        {1: find_person, 2: update_person, 3: delete_person, 4: show_all}[selected]()

    else:
        # 종료하기 전 파일로 데이터 저장
        with open("my_contacts.json", "w", encoding="utf8") as f:
            json.dump(contact_data, f, indent=2)

        print("종료합니다.")


if __name__ == "__main__":
    main()
