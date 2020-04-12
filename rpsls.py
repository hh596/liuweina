#coding:gbk
"""
��һ��С��Ŀ��Rock-paper-scissors-lizard-Spock
���ߣ���ά��
���ڣ�2020/4/9
"""

import random



# 0 - ʯͷ
# 1 - ʷ����
# 2 - ֽ
# 3 - ����
# 4 - ����

# ����Ϊ�����Ϸ����Ҫ�õ����Զ��庯��

def name_to_number(name):
    """
    ����Ϸ�����Ӧ����ͬ������
    """
    if name=="ʯͷ":
	    number=0
    elif name=="ʷ����":  
	    number=1
    elif name=="��":
	    number=2
    elif name=="����":
	    number=3
    elif name=="����":
	    number=4
    return number
		

def number_to_name(number):
    """
    ������ (0, 1, 2, 3, or 4)��Ӧ����Ϸ�Ĳ�ͬ����
    """
    if number==0:
	    name="ʯͷ"
    elif number==1:
	    name="ʷ����"
    elif number==2:
	    name="��"
    elif number==3:
	    name="����"
    elif number==4:
	    name="����"
    return name  
	
		
def rpsls(player_choice):
    """
    �û�����������һ��ѡ�񣬸���RPSLS��Ϸ��������Ļ�������Ӧ�Ľ��

    """
    if (player_choice!="ʯͷ")and(player_choice!="ʷ����")and(player_choice!="��")and(player_choice!="����")and(player_choice!="����"):
        print("Error: No Correct Name") # ����û���ѡ����ʯͷ/����/��/����/ʷ�����е�����һ�����������Error: No Correct Name��
    else:
        print("----------------") # ���"-------- "���зָ�
        print("����ѡ��Ϊ:"+player_choice) # ��ʾ�û�������ʾ���û�ͨ�����̽��Լ�����Ϸѡ��������룬�������player_choice
        player_choice_number=name_to_number(player_choice) # ����name_to_number()�������û�����Ϸѡ�����ת��Ϊ��Ӧ���������������player_choice_number
        comp_number=int(random.randrange(0,5)) # ����random.randrange()�Զ�����0-4֮��������������Ϊ��������ѡ�����Ϸ���󣬴������comp_number
        comp_choice=number_to_name(comp_number) # ����number_to_name()����������������������ת��Ϊ��Ӧ����Ϸ����
        print("�������ѡ��Ϊ:"+comp_choice) # ����Ļ����ʾ�����ѡ����������
        if player_choice==comp_choice: # ����if/elif/else ��䣬����RPSLS������û�ѡ��ͼ����ѡ������жϣ�������Ļ����ʾ�жϽ��
	        print("���ͼ��������һ����") # ����û��ͼ����ѡ��һ��������ʾ�����ͼ��������һ���ء�
        elif (player_choice_number==0 and comp_number==3)or(player_choice_number==0 and comp_number==4)or(player_choice_number==1 and comp_number==0)or(player_choice_number==1 and comp_number==4)or(player_choice_number==2 and comp_number==0)or(player_choice_number==2 and comp_number==1)or(player_choice_number==3 and comp_number==1)or(player_choice_number==3 and comp_number==2)or(player_choice_number==4 and comp_number==2)or(player_choice_number==4 and comp_number==3):
	        print("��Ӯ��") # ����û���ʤ������ʾ����Ӯ�ˡ�
        else:
	        print("�����Ӯ��") # ��֮����ʾ�������Ӯ�ˡ�

    
# �Գ�����в���
print("��ӭʹ��RPSLS��Ϸ")
print("----------------")
print("����������ѡ��:")
player_choice=input()
rpsls(player_choice)
