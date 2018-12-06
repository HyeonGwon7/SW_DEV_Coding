class Display:
    def select_display():
        print("=============== 자율 주행 ===============")
        print("\n")
        print("======== 주행 모드를 선택하세요  ========")
        print("\n")
        print("====== 직진 모드 (1번을 입력하세요) =====")
        print("\n")
        print("== 장애물 인식 모드 (2번을 입력하세요) ==")
        print("\n")
        print("====== 통합 모드 (3번을 입력하세요) =====")
        print("\n")
        print("=========================================")

    def control_display(num):
        print("=============== 자율 주행 ===============")
        print("\n")
        if(num==1):
            print("직진 모드를 구동하시겠습니까?(Y/N)")
        elif(num==2):
            print("장애물 인식 모드를 구동하시겠습니까?(Y/N)")
        elif(num==3):
            print("통합 모드를 구동하시겠습니까?(Y/N)")
        else:
            print("다시 입력하세요")
        print("\n")
        print("=========================================")

    def finish_display(cha):
        print("=============== 자율 주행 ===============")
        print("\n")
        if(cha=="y"or cha=="Y"):
            print("모드가 실행됩니다. ")
        elif(cha=="n"or cha=="N"):
            print("종료 됩니다.")
        else:
            print("다시 입력하세요")
        print("\n")
        print("=========================================")

        
