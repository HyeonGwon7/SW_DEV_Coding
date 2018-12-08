#-*- coding:utf-8 -*-
class Display:
	mode = 0
	sel = ""
	def select_display(self):

		print("=============== aa ===============")
		print("\n")
		print("======== aaa  ========")
		print("\n")
		print("====== 직진 모드 (1번을 입력하세요) =====")
		print("\n")
		print("== 장애물 인식 모드 (2번을 입력하세요) ==")
		print("\n")
		print("====== 통합 모드 (3번을 입력하세요) =====")
		print("\n")
		global mode
		print("=========================================")
		mode = int(input("선택모드를 입력하세요 : "))
		if mode >3:
			while True:
				print("1,2,3중에 입력하세요")
				mode = int(input("선택모드를 입력하세요 : "))
				if  mode >0 and mode <= 3:
					break

	def control_display(self,num):

		print("\n")
		print("=============== 자율 주행 ===============")
		print("\n")
		global sel
		sel = ""
		if(num==1):
			
			sel = raw_input("직진 모드로 구동하시겠습니까?(Y/N) : ")
			if (sel != "Y" and sel != "N" and sel != "y" and sel != "n"):
				while True:
					sel = raw_input("다시입력하세요(Y/N) : ")
					if sel == "Y" or sel == "N" or sel == "y" or sel == "n":
						return sel
						break
			else:
				return sel

		elif(num==2):
			sel = raw_input("장애물 인식 모드를 구동하시겠습니까?(Y/N) : ")
                        if sel != "Y" and sel != "N" and sel != "y" and sel != "n":
                                while True:
                                        sel = raw_input("다시입력하세요(Y/N) : ")
                                        if sel == "Y" or sel == "N" or sel == "y" or sel == "n":
                                                #주행
                                                break
			else:
				return sel

		elif(num==3):
			sel = raw_input("통합 모드를 구동하시겠습니까?(Y/N) : ")
                        if sel is not "Y" or sel is not "N" or sel is not "y" or sel is not "n":
                                while True:
                                        sel = raw_input("다시입력하세요(Y/N) : ")
                                        if sel == "Y" or sel == "N" or sel == "y" or sel == "n":
                                                #주행
                                                break

		print("\n")
		print("=========================================")
		print("\n")

	def finish_display(self,cha):
		print("\n")
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
		print("\n")

	def check_num(self,num,sel):
		# 직진 주행
		if(num == 1 and (sel =="y" or sel == "Y")): 
			return 1
		#장애물 인식
		elif(num == 2 and (sel =="y" or sel == "Y")):
			return 2
 		#통합 모드
		elif(num == 3 and (sel=="y" or sel=="Y")):
			return 3
		#종료
		elif(sel =="N" or sel=="n"):
			return 4 


class main:
	a=Display()
#선택
	a.select_display()
#주행
	a.control_display(mode)

	a.finish_display(sel)
	print(a.check_num(mode,sel))
