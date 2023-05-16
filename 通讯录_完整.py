import csv
import os
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


class ContactManager:
    def __init__(self, master):
        self.master = master
        self.master.title('通讯录管理系统')

        # 设置通讯录文件路径
        self.file_path = 'contacts.csv'

        # 如果文件不存在，则创建文件并写入表头
        if not os.path.isfile(self.file_path):
            with open(self.file_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['编号', '姓名', '手机号码', '通讯地址'])

        # 创建控件
        self.label_title = tk.Label(master, text='通讯录管理系统', font=('Arial', 18))
        self.label_name = tk.Label(master, text='姓名或手机号码：')
        self.entry_name = tk.Entry(master, width=30)
        self.button_search = tk.Button(master, text='搜索', command=self.search_contact)
        self.button_show_all = tk.Button(master, text='显示全部', command=self.show_contacts)
        self.tree = ttk.Treeview(master, columns=('编号', '姓名', '手机号码', '通讯地址'), show='headings')
        self.tree.column('编号', width=100)
        self.tree.column('姓名', width=150)
        self.tree.column('手机号码', width=200)
        self.tree.column('通讯地址', width=300)
        self.tree.heading('编号', text='编号')
        self.tree.heading('姓名', text='姓名')
        self.tree.heading('手机号码', text='手机号码')
        self.tree.heading('通讯地址', text='通讯地址')
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        self.button_add = tk.Button(master, text='增加',
                                    command=self.add_contact)
        self.button_delete = tk.Button(master, text='删除',
                                       command=self.delete_contact)
        self.button_edit = tk.Button(master, text='修改',
                                     command=self.edit_contact)

        # 设置控件布局
        self.label_title.grid(row=0, column=0, columnspan=3, pady=10)
        self.label_name.grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)
        self.entry_name.grid(row=1, column=1, padx=10, pady=5)
        self.button_search.grid(row=1, column=2, padx=10, pady=5)
        self.button_show_all.grid(row=2, column=1, padx=10, pady=5)
        self.tree.grid(row=3, column=0, columnspan=3, padx=10, pady=10)
        self.button_add.grid(row=4, column=0, padx=10, pady=10)
        self.button_delete.grid(row=4, column=1, padx=10, pady=10)
        self.button_edit.grid(row=4, column=2, padx=10, pady=10)

        # 显示所有联系人
        self.show_contacts()

    def show_contacts(self):
        # 清空树状表格
        self.tree.delete(*self.tree.get_children())

        # 显示通讯录内容
        with open(self.file_path, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                self.tree.insert('', tk.END, values=row)

    def add_contact(self):
        input_str = self.entry_name.get().strip()
        input_list = input_str.split(',')
        name = input_list[0].strip()
        phone = input_list[1].strip() if len(input_list) > 1 else ''
        address = input_list[2].strip() if len(input_list) > 2 else ''

        # 检查输入是否合法
        if not name:
            messagebox.showerror('错误', f'请填写{name}！')
            return

        # 判断是否手机或固话
        if name.isdigit():
            if len(name) == 11:
                phone = name
                name = ''
            elif len(name) == 7:
                phone = name
                name = ''
            else:
                messagebox.showerror('错误', '请输入正确的手机号码或固话号码！')
                return

        # 打开通讯录文件并获取最大编号
        with open(self.file_path, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # 跳过第一行表头
            id_list = [int(row[0]) for row in reader if row[0].isdigit()]
            next_id = max(id_list) + 1 if id_list else 1

        # 将记录添加到通讯录文件
        with open(self.file_path, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([next_id, name, phone, address])

        # 清空输入框
        self.entry_name.delete(0, tk.END)

        # 显示成功提示
        messagebox.showinfo('提示', '添加成功！')

        # 刷新树状表格
        self.show_contacts()

    def delete_contact(self):

        # 获取当前选中行的ID
        selection = self.tree.selection()
        if not selection:
            messagebox.showerror('错误', '请选择要删除的联系人！')
            return

        id = int(self.tree.item(selection)['values'][0])

        # 确认删除操作
        confirm = messagebox.askyesno('确认', '确定要删除选中的联系人吗？')
        if not confirm:
            return

        # 删除指定ID的记录
        with open(self.file_path, 'r', newline='') as f:
            reader = csv.reader(f)
            next(reader)  # 跳过第一行表头
            rows = [row for row in reader if int(row[0]) != id]

        # 写入更新后的记录
        with open(self.file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['编号', '姓名', '手机号码', '通讯地址'])
            writer.writerows(rows)

        # 刷新树状表格
        self.show_contacts()

        # 显示成功信息
        messagebox.showinfo('提示', '删除成功！')

    def edit_contact(self):
        # Get the ID of the contact to be edited
        selection = self.tree.selection()
        if not selection:
            messagebox.showerror('错误', '请选择要修改的联系人！')
            return

        id = int(self.tree.item(selection)['values'][0])

        # 查找具有指定ID的联系人
        with open(self.file_path, 'r', newline='') as f:
            reader = csv.reader(f)
            next(reader)  # skip header row
            contact = None
            for row in reader:
                if int(row[0]) == id:
                    contact = row
                    break

        # 显示一个对话框以允许用户编辑联系信息
        if contact:
            # Create a new window for editing the contact information
            edit_window = tk.Toplevel(self.master)
            edit_window.title('修改联系人信息')

            # 为每个联系人字段创建标签和输入字段
            tk.Label(edit_window, text='姓名：').grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
            name_entry = tk.Entry(edit_window, width=30)
            name_entry.grid(row=0, column=1, padx=5, pady=5)
            name_entry.insert(0, contact[1])
            tk.Label(edit_window, text='手机号码：').grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
            phone_entry = tk.Entry(edit_window, width=30)
            phone_entry.grid(row=1, column=1, padx=5, pady=5)
            phone_entry.insert(0, contact[2])
            tk.Label(edit_window, text='通讯地址：').grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
            address_entry = tk.Entry(edit_window, width=50)
            address_entry.grid(row=2, column=1, padx=5, pady=5)
            address_entry.insert(0, contact[3])

            # 创建更新联系信息的保存按钮
            def save_contact():
                name = name_entry.get().strip()
                phone = phone_entry.get().strip()
                address = address_entry.get().strip()

                # 验证输入
                if not name:
                    messagebox.showerror('错误', '请填写姓名！')
                    return

                # 更新CSV文件中的联系方式
                with open(self.file_path, 'r+', newline='') as f:
                    reader = csv.reader(f)
                    writer = csv.writer(f)
                    next(reader)  # 跳过标题行
                    rows = []
                    for row in reader:
                        if int(row[0]) == id:
                            row[1] = name
                            row[2] = phone
                            row[3] = address
                        rows.append(row)
                    f.seek(0)
                    writer.writerow(['编号', '姓名', '手机号码', '通讯地址'])
                    writer.writerows(rows)
                    f.truncate()

                # 刷新所有联系人的显示
                self.show_contacts()

                # 显示成功消息
                messagebox.showinfo('提示', '修改成功！')

                # 关闭编辑窗口
                edit_window.destroy()

            save_button = tk.Button(edit_window, text='保存',
                                    command=save_contact)
            save_button.grid(row=3, column=1, padx=5, pady=5, sticky=tk.E)

        else:
            messagebox.showerror('错误', '未找到指定联系人！')

    def search_contact(self):
        keyword = self.entry_name.get().strip()

        # 检查输入是否合法
        if not keyword:
            messagebox.showerror('错误', '请输入姓名或手机号码关键字！')
            return

        # 清空树状表格
        self.tree.delete(*self.tree.get_children())

        # 查找符合条件的记录
        with open(self.file_path, 'r') as f:
            reader = csv.reader(f)
            rows = [row for row in reader if
                    (keyword in row[1]) or (keyword in row[2])]

        # 显示查找结果
        if not rows:
            messagebox.showinfo('提示', '未找到符合条件的记录！')
        else:
            for row in rows:
                self.tree.insert('', tk.END, values=row)

    def on_select(self, event):
        selection = self.tree.selection()
        if not selection:
            return
        values = self.tree.item(selection)['values']
        if values:
            self.entry_name.delete(0, tk.END)
            self.entry_name.insert(0, values[1] if values[1] else values[2])




def main():
    # 创建主窗口
    root = tk.Tk()

    # 创建通讯录管理器对象并运行
    ContactManager(root)
    root.mainloop()


if __name__ == '__main__':
    main()
