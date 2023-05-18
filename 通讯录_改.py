import csv
import os
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# 定义常量
COLUMN_NAMES = ['编号', '姓名', '手机号码', '通讯地址']
FILE_PATH = 'contacts.csv'  # 定义联系人信息存储的csv文件的路径


class ContactManager:
    def __init__(self, master):  # 初始化窗口
        self.master = master
        self.master.title('通讯录管理系统')

        # 如果文件不存在，则创建文件并写入表头
        if not os.path.isfile(FILE_PATH):
            with open(FILE_PATH, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(COLUMN_NAMES)

        # 设置搜索关键字变量
        self.keyword = tk.StringVar()

        # 创建控件
        self.label_title = tk.Label(master, text='通讯录管理系统', font=('Arial', 18))  # 创建标题标签
        self.label_name = tk.Label(master, text='姓名或手机号码：')  # 创建搜索标签
        self.entry_name = tk.Entry(master, width=30, textvariable=self.keyword)  # 创建搜索框，并绑定关键字变量
        self.button_search = tk.Button(master, text='搜索', command=self.search_contact)  # 创建搜索按钮
        self.button_show_all = tk.Button(master, text='显示全部', command=self.show_all_contacts)  # 创建显示全部按钮
        self.tree = ttk.Treeview(master, columns=COLUMN_NAMES, show='headings')  # 创建表格控件
        self.tree.heading('编号', text='编号')
        self.tree.heading('姓名', text='姓名')
        self.tree.heading('手机号码', text='手机号码')
        self.tree.heading('通讯地址', text='通讯地址')
        self.button_add = tk.Button(master, text='添加联系人', command=self.add_contact)  # 创建添加联系人按钮
        self.button_edit = tk.Button(master, text='编辑联系人', command=self.edit_contact)  # 创建编辑联系人按钮
        self.button_delete = tk.Button(master, text='删除联系人', command=self.delete_contact)  # 创建删除联系人按钮
        self.button_exit = tk.Button(master, text='退出系统', command=master.quit)  # 创建退出系统按钮

        # 布局控件
        self.label_title.grid(row=0, column=0, columnspan=4, pady=(10, 20))  # 设置标题标签的位置
        self.label_name.grid(row=1, column=0)  # 设置搜索标签的位置
        self.entry_name.grid(row=1, column=1, padx=5)  # 设置搜索框的位置
        self.button_search.grid(row=1, column=2)  # 设置搜索按钮的位置
        self.button_show_all.grid(row=1, column=3)  # 设置显示全部按钮的位置
        self.tree.grid(row=2, column=0, columnspan=4, padx=5, pady=5)  # 设置表格控件的位置
        self.button_add.grid(row=3, column=0, pady=5)  # 设置添加联系人按钮的位置
        self.button_edit.grid(row=3, column=1, pady=5)  # 设置编辑联系人按钮的位置
        self.button_delete.grid(row=3, column=2, pady=5)  # 设置删除联系人按钮的位置
        self.button_exit.grid(row=3, column=3, pady=5)  # 设置退出系统按钮的位置

        # 显示全部联系人
        self.show_all_contacts()

    def read_csv(self):
        with open(FILE_PATH, newline='') as f:
            reader = csv.reader(f)
            rows = list(reader)
        return rows[1:]  # 将数据从第二行开始读入

    def write_csv(self, rows):
        with open(FILE_PATH, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(COLUMN_NAMES)  # 写入列标题
            writer.writerows(rows)  # 写入联系人数据

    def search_contact(self):
        keyword = self.keyword.get()  # 获取搜索框中的关键字
        rows = self.read_csv()  # 读取所有联系人数据
        filtered_rows = []  # 新建一个空列表，用于存储符合搜索关键字的联系人数据
        for row in rows:
            if keyword in row[1] or keyword in row[2]:  # 如果搜索关键字在姓名或手机号码中出现
                filtered_rows.append(row)  # 将该联系人数据加入到已筛选的联系人列表中
        else:
            self.show_contacts(filtered_rows)  # 显示已筛选的联系人数据

    def show_all_contacts(self):
        rows = tuple(self.read_csv())  # 读取所有联系人数据，并将其转换为元组类型
        self.show_contacts(rows)  # 显示全部联系人数据

    def show_contacts(self, rows):
        self.tree.delete(*self.tree.get_children())  # 清空表格控件
        for row in rows:  # 循环遍历要显示的联系人数据
            self.tree.insert('', 'end', values=row)  # 将每一行数据加入到表格控件中

    def create_contact_window(self, title, name='', phone='', address='', save_command=None):
        window = tk.Toplevel(self.master)  # 新建一个顶级窗口，用于创建添加和编辑联系人的窗口
        window.title(title)  # 设置窗口标题

        # 创建控件
        label_name = tk.Label(window, text='姓名：')  # 创建“姓名”标签
        entry_name = tk.Entry(window, width=30)  # 创建“姓名”输入框
        label_phone = tk.Label(window, text='手机号码：')  # 创建“手机号码”标签
        entry_phone = tk.Entry(window, width=30)  # 创建“手机号码”输入框
        label_address = tk.Label(window, text='通讯地址：')  # 创建“通讯地址”标签
        entry_address = tk.Entry(window, width=30)  # 创建“通讯地址”输入框
        button_save = tk.Button(window, text='保存',
                                command=lambda: save_command(window, entry_name.get(), entry_phone.get(),
                                                             entry_address.get()))  # 创建保存按钮，并调用保存函数
        button_cancel = tk.Button(window, text='取消', command=window.destroy)  # 创建取消按钮

        # 布局控件
        label_name.grid(row=0, column=0, pady=5)  # 设置“姓名”标签的位置
        entry_name.grid(row=0, column=1, padx=5, pady=5)  # 设置“姓名”输入框的位置
        label_phone.grid(row=1, column=0, pady=5)  # 设置“手机号码”标签的位置
        entry_phone.grid(row=1, column=1, padx=5, pady=5)  # 设置“手机号码”输入框的位置
        label_address.grid(row=2, column=0, pady=5)  # 设置“通讯地址”标签的位置
        entry_address.grid(row=2, column=1, padx=5, pady=5)  # 设置“通讯地址”输入框的位置
        button_save.grid(row=3, column=0, pady=5)  # 设置保存按钮的位置
        button_cancel.grid(row=3, column=1, pady=5)  # 设置取消按钮的位置

        # 显示选中联系人的信息
        entry_name.insert(0, name)  # 将选中联系人的姓名显示在输入框中
        entry_phone.insert(0, phone)  # 将选中联系人的手机号码显示在输入框中
        entry_address.insert(0, address)  # 将选中联系人的通讯地址显示在输入框中

    def add_contact(self):
        def save_command(window, name, phone, address):
            if not name or not phone:
                messagebox.showerror('错误', f'姓名和手机号码不能为空！')
                return
            rows = self.read_csv()  # 读取所有联系人数据
            id_list = [int(row[0]) for row in rows]  # 获取已有联系人的编号列表
            new_id = max(id_list) + 1 if id_list else 1  # 计算新联系人的编号
            new_row = [str(new_id), name, phone, address]  # 新联系人的数据
            rows.append(new_row)  # 将新联系人的数据加入到联系人数据列表中
            self.write_csv(rows)  # 保存所有联系人数据
            window.destroy()  # 关闭添加联系人窗口
            self.show_all_contacts()  # 显示所有联系人数据

        self.create_contact_window('添加联系人', save_command=save_command)  # 调用创建联系人窗口的函数

    def edit_contact(self):
        selected_items = self.tree.selection()  # 获取选中的联系人数据
        if not selected_items:
            messagebox.showwarning('警告', '请选择要编辑的联系人！')
            return
        selected_item = selected_items[0]  # 获取选中的联系人数据
        item_values = self.tree.item(selected_item)['values']  # 获取选中的联系人数据的值列表

        def save_command(window, name, phone, address):
            if not name or not phone:
                messagebox.showerror('错误', '姓名和手机号码不能为空！')
                return
            rows = self.read_csv()  # 读取所有联系人数据
            selected_item_index = self.tree.index(selected_item)
            rows[selected_item_index][1] = name  # 更新选中联系人的姓名
            rows[selected_item_index][2] = phone  # 更新选中联系人的手机号码
            rows[selected_item_index][3] = address  # 更新选中联系人的通讯地址
            self.write_csv(rows)  # 保存所有联系人数据
            window.destroy()  # 关闭编辑联系人窗口
            self.show_all_contacts()  # 显示所有联系人数据

        self.create_contact_window('编辑联系人', name=item_values[1], phone=item_values[2], address=item_values[3],
                                   save_command=save_command)  # 调用创建联系人窗口的函数，并将选中联系人的信息作为默认值显示在输入框中

    def delete_contact(self):
        selected_items = self.tree.selection()  # 获取选中的联系人数据
        if not selected_items:
            messagebox.showwarning('警告', '请选择要删除的联系人！')
            return
        confirm = messagebox.askyesno('确认', '是否删除选中的联系人？')  # 弹出提示框，确认删除选中的联系人
        if not confirm:
            return
        rows = self.read_csv()  # 读取所有联系人
        for selected_item in selected_items:
            selected_item_index = self.tree.index(selected_item)
            rows.pop(selected_item_index)
        self.write_csv(rows)
        self.show_all_contacts()


if __name__ == '__main__':
    root = tk.Tk()
    app = ContactManager(root)
    root.mainloop()
