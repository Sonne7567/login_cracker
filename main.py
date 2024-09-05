import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog
from threading import Thread
from core import main

def select_username_file():
    file_path = filedialog.askopenfilename(title="选择用户名文件", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
    if file_path:
        entry_username_file.delete(0, tk.END)
        entry_username_file.insert(0, file_path)

def select_password_file():
    file_path = filedialog.askopenfilename(title="选择密码文件", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
    if file_path:
        entry_password_file.delete(0, tk.END)
        entry_password_file.insert(0, file_path)

def start_attack():
    url = entry_url.get()
    captcha_selector = entry_captcha_selector.get()
    login_xpath = entry_login_xpath.get()
    username_file = entry_username_file.get()
    password_file = entry_password_file.get()

    if not url or not captcha_selector or not login_xpath or not username_file or not password_file:
        messagebox.showerror("输入错误", "请填写所有字段并选择文件！")
        return

    log_text_widget.delete(1.0, tk.END)
    log_text_widget.insert(tk.END, "浏览器进程启动中，请稍后...\n")
    log_text_widget.see(tk.END)

    # 在后台线程中执行攻击操作
    Thread(target=main, args=(url, captcha_selector, login_xpath, username_file, password_file, log_text_widget)).start()

# GUI
root = tk.Tk()
root.title("登录破解工具")

label_url = tk.Label(root, text="目标网站URL:")
label_url.grid(row=0, column=0)
entry_url = tk.Entry(root, width=50)
entry_url.grid(row=0, column=1)

label_captcha_selector = tk.Label(root, text="验证码选择器 (CSS Selector):")
label_captcha_selector.grid(row=1, column=0)
entry_captcha_selector = tk.Entry(root, width=50)
entry_captcha_selector.grid(row=1, column=1)

label_login_xpath = tk.Label(root, text="登录按钮的完整XPath:")
label_login_xpath.grid(row=2, column=0)
entry_login_xpath = tk.Entry(root, width=50)
entry_login_xpath.grid(row=2, column=1)

label_username_file = tk.Label(root, text="用户名文件:")
label_username_file.grid(row=3, column=0)
entry_username_file = tk.Entry(root, width=40)
entry_username_file.grid(row=3, column=1)
button_username_file = tk.Button(root, text="选择文件", command=select_username_file)
button_username_file.grid(row=3, column=2)

label_password_file = tk.Label(root, text="密码文件:")
label_password_file.grid(row=4, column=0)
entry_password_file = tk.Entry(root, width=40)
entry_password_file.grid(row=4, column=1)
button_password_file = tk.Button(root, text="选择文件", command=select_password_file)
button_password_file.grid(row=4, column=2)

button_start = tk.Button(root, text="开始破解", command=start_attack)
button_start.grid(row=5, column=1)

log_text_widget = scrolledtext.ScrolledText(root, width=70, height=20, wrap=tk.WORD)
log_text_widget.grid(row=6, column=0, columnspan=3)

root.mainloop()
