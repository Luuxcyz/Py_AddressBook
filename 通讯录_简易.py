import csv


# 定义函数：显示通讯录中的所有记录
def show_contacts():
    with open('contacts.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            print(row)


# 定义函数：增加一条记录
def add_contact():
    name = input('请输入姓名：')
    phone = input('请输入手机号码：')
    address = input('请输入通讯地址：')
    with open('contacts.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([get_next_id(), name, phone, address])
    print('添加成功！')


# 定义函数：删除一条记录
def delete_contact():
    id = input('请输入要删除的编号：')
    with open('contacts.csv', 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        rows = [row for row in reader if row[0] != id]
    with open('contacts.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['编号', '姓名', '手机号码', '通讯地址'])
        writer.writerows(rows)
    print('删除成功！')


# 定义函数：修改一条记录
def edit_contact():
    id = input('请输入要修改的编号：')
    name = input('请输入姓名：')
    phone = input('请输入手机号码：')
    address = input('请输入通讯地址：')
    with open('contacts.csv', 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        rows = [row if row[0] != id else [id, name, phone, address] for row in
                reader]
    with open('contacts.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['编号', '姓名', '手机号码', '通讯地址'])
        writer.writerows(rows)
    print('修改成功！')


# 定义函数：查询一条记录
def search_contact():
    keyword = input('请输入姓名或手机号码关键字：')
    with open('contacts.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        rows = [row for row in reader if
                (keyword in row[1]) or (keyword in row[2])]
        if len(rows) == 0:
            print('未找到符合条件的记录！')
        else:
            for row in rows:
                print(row)


# 定义函数：获取下一个ID
def get_next_id():
    with open('contacts.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        return str(len(list(reader)))


# 主程序
while True:
    print('==================通讯录===================')
    print('1.显示清单 2.增加记录 3.删除记录')
    print('4.修改记录 5.查询记录 6.退出程序')
    choice = input('请输入你的选择：')
    if choice == '1':
        show_contacts()
    elif choice == '2':
        add_contact()
    elif choice == '3':
        delete_contact()
    elif choice == '4':
        edit_contact()
    elif choice == '5':
        search_contact()
    elif choice == '6':
        print('程序已退出。')
        break
    else:
        print('无效的选择，请重新输入！')


