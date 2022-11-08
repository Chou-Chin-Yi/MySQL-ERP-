import tkinter as tk
from tkinter import ttk
from tkinter import *
import tkinter.messagebox as tkMessageBox
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
from openpyxl import Workbook
# ---------------MySQL初始設定--------------------
import pymysql as MySQldb              # pip install MySQLdb
db = MySQldb.connect(host="127.0.0.1",      # 連線到本身的電腦IP
                     user="admin",          # MySQL/PHPMyAdmin 新增的 用戶
                     passwd="admin",
                     db="mydatabase")       # MySQL/PHPMyAdmin 新增的 資料庫
cursor = db.cursor()
# -----------------------------------
window = tk.Tk()
window.title("訂單管理系統")
w = 600  # 視窗寬
h = 450  # 視窗高
window.minsize(width=w, height=h)
window.maxsize(width=w, height=h)


# 產品資訊 CLASS
class productInfo(object):
    def __init__(self, orderNumber, productName,
                 productMoney, remark, orderStatus):
        self.orderNumber = orderNumber
        self.productName = productName
        self.productMoney = productMoney
        self.remark = remark
        self.orderStatus = orderStatus

    def treeRun(self):
        # 把資料帶入
        infoProduct = [(self.orderNumber, self.productName, self.productMoney,
                        self.remark, self.orderStatus)]

        # 將資料 帶入tree 裡面
        for contact in infoProduct:
            tree.insert("", tk.END, values=contact)

        # 滑鼠點到會print
        def item_selected(event):
            for selected_item in tree.selection():
                item = tree.item(selected_item)
                record = item['values']
                print(record)

                # 將使用者選取的資料 顯示在畫面上
                orderNumValue.set(record[0])
                productNameEntryInput.set(record[1])
                productMoneyEntryInput.set(record[2])
                text.delete("1.0", tk.END)
                text.insert(tk.INSERT, record[3])
                orderFrameValue.set(record[4])

        # 重要的滑鼠點到動作
        tree.bind('<<TreeviewSelect>>', item_selected)


# 第一層 下拉選單 file ...
menubar = tk.Menu(window)
dataMenu = tk.Menu(menubar)
optionMenu = tk.Menu(menubar)
exitMenu = tk.Menu(menubar)


# 各別按下後 最發生甚麼事情
def dataDo():
    tkMessageBox.showinfo("尚未開放", "資訊功能尚未開放")


def exitDo():
    exit()


def saveData():
    excelData = []
    # 防止遺漏資料輸入
    if productNameEntry.get() != "" and productMoneyEntry.get() != "":
        excelData.append(orderNumValue.get())
        excelData.append(productNameEntry.get())
        excelData.append(productMoneyEntry.get())
        excelData.append(text.get("1.0", "end"))
        excelData.append(orderFrameValue.get())

        # 將資料放到列表裡面
        treeData = productInfo(orderNumValue.get(), productNameEntry.get(),
                               productMoneyEntry.get(),
                               text.get("1.0", "end"),
                               orderFrameValue.get())
        treeData.treeRun()  # 將資料 丟到 tree列表
        # MySQL 新增-------------------------
        sql = "INSERT INTO 訂單管理資料 (訂單編號, 商品名稱, 金額, 備註, 訂單狀況)" \
              " VALUES ('"+orderNumValue.get()+"'," \
                        "'"+productNameEntry.get()+"'," \
                        "'"+productMoneyEntry.get()+"'," \
                        "'"+text.get("1.0", "end")+"'," \
                        "'"+orderFrameValue.get()+"')"
        cursor.execute(sql)  # 執行新指令
        db.commit()  # 送出
        # -----------------------------------

        # 將圖型的數據存起來
        dataProductName.append(productNameEntry.get())
        dataMoney.append(productMoneyEntry.get())

        # 印出各個數據
        print("訂單編號:", orderNumValue.get())
        print("商品名稱:", productNameEntry.get())
        print("金額:", productMoneyEntry.get())
        print("備註:", text.get("1.0", "end") + "訂單狀況:", orderFrameValue.get())
    else:
        tkMessageBox.showerror("錯誤", "有資料未輸入")


def loadData():
    # 清除原本tree 上的資料
    clean = tree.get_children()
    for item in clean:
        tree.delete(item)

    sql = "SELECT * FROM `訂單管理資料`"
    cursor.execute(sql)  # 執行sql指令
    db.commit()  # 資料同步儲存
    MySQLList = cursor.fetchall()   # 資料轉成陣列

    # 將陣列資料 輸入到 tree 中
    for data in MySQLList:
        treeData = productInfo(data[0], data[1], data[2],
                               data[3], data[4])
        treeData.treeRun()

        dataProductName.append(data[1])     # 資料存到圖表
        dataMoney.append(data[2])           # 資料存到圖表


def delData():
    global dataProductName
    global dataMoney
    try:
        dataProductName = []    # 圖表資料初始化
        dataMoney = []          # 圖表資料初始化
        # 刪除所選的資料
        for selected_item in tree.selection():
            item = tree.item(selected_item)
            record = item['values']     # 將 tree 資料 轉成陣列
            tree.delete(selected_item)      # tree 上刪除

        strAns = str(record[0])     # 將訂單資料轉為字串
        # MySQL 刪除資料-------------------------------------
        sql = "DELETE FROM `訂單管理資料` where `訂單編號`='"+strAns+"';"
        cursor.execute(sql)  # 執行sql指令
        db.commit()  # 資料同步儲存
        # --------------------------------------------------

        # 將更改過後資料 匯入圖表
        for dataContent in tree.get_children():
            thing = tree.item(dataContent)
            dataIn = thing["values"]
            # 圖表資料匯入
            dataProductName.append(dataIn[1])
            dataMoney.append(dataIn[2])
    except:
        tkMessageBox.showerror("錯誤!!", "沒有選擇資料!!")


def editData():
    global dataProductName
    global dataMoney
    try:
        dataProductName = []  # 圖表資料初始化
        dataMoney = []  # 圖表資料初始化
        location = tree.selection()[0]      # 看哪個位置 被選取 改資料
        # 改過後資料存入 DataIn
        DataIn = [str(orderNumValue.get()), productNameEntry.get(), str(productMoneyEntry.get()),
                  text.get("1.0", "end"), orderFrameValue.get()]

        # 更改treeView 上看到的資料
        for x in range(0, len(columns)):
            tree.set(location, column=x, value=DataIn[x])

        # MySQL 編輯資料---------------------------------------------
        sql = "UPDATE `訂單管理資料` SET `訂單編號`='"+DataIn[0]+"'," \
                                      "`商品名稱`='"+DataIn[1]+"'," \
                                      "`金額`='"+DataIn[2]+"'," \
                                      "`備註`='"+DataIn[3]+"'," \
                                      "`訂單狀況`='"+DataIn[4]+"' WHERE `訂單編號` = '"+DataIn[0]+"';"
        cursor.execute(sql)  # 執行sql指令
        db.commit()  # 資料同步儲存
        # ---------------------------------------------------------

        # 將更改過後資料 匯入圖表
        for dataContent in tree.get_children():
            thing = tree.item(dataContent)
            dataIn = thing["values"]
            # 圖表資料匯入
            dataProductName.append(dataIn[1])
            dataMoney.append(dataIn[2])

        # 將畫面上輸入欄位資料清除
        orderNumValue.set("#####")
        productNameEntryInput.set("")
        productMoneyEntryInput.set("0")
        text.delete("1.0", tk.END)
        orderFrameValue.set("未處理")
    except:
        tkMessageBox.showerror("錯誤!!", "沒有選擇資料!!")


def savexlsx():
    wb = Workbook()
    sheet = wb.active

    # 標頭資料
    for i in range(1, len(columns) + 1):
        sheet.cell(row=1, column=i).value = columns[i - 1]

    for dataContent in tree.get_children():  # 將tree資料  匯入Excel
        thing = tree.item(dataContent)
        dataIn = thing["values"]
        sheet.append(dataIn)
        # 圖表資料匯入
        dataProductName.append(dataIn[1])
        dataMoney.append(dataIn[2])
    print("xlsx檔 儲存成功!!")
    wb.save("ERP_sample.xlsx")


# 資料選單
dataMenu.add_command(label="存成xlsx檔", command=savexlsx)
dataMenu.add_command(label="存入MySQL資料庫", command=saveData)
dataMenu.add_command(label="讀取舊檔", command=loadData)
menubar.add_cascade(label="資料", menu=dataMenu)

# 功能選單
optionMenu.add_command(label="編輯", command=editData)
menubar.add_cascade(label="功能", menu=optionMenu)

# 離開選單
exitMenu.add_command(label="離開", command=exitDo)
menubar.add_cascade(label="離開", menu=exitMenu)
window.config(menu=menubar)  # 顯示選單

# ---------------------------

# Label
dataLabel = tk.Label(window, text="訂單編號:\n商品名稱:\n金額:\n備註:",
                     font=("標楷體", 15), justify=RIGHT)
dataLabel.place(x=0, y=45)

# ---------------------------

# Enter
# 產品名稱
productNameEntryInput = StringVar()
productNameEntry = tk.Entry(window, textvariable=productNameEntryInput, bg="#f0fff0")
productNameEntry.place(x=100, y=70)

# 產品金額
productMoneyEntryInput = StringVar()
productMoneyEntry = tk.Entry(window, textvariable=productMoneyEntryInput, bg="#afeeee")
productMoneyEntry.place(x=100, y=90)

# ---------------------------

# spinBox 訂單編號
orderNumValue = tk.StringVar(value="1")
orderNumBox = ttk.Spinbox(
    window,
    from_=1, to=999999999,
    textvariable=orderNumValue,
    wrap=True)
orderNumBox.place(x=100, y=50)

# 多行輸入 備註
text = tk.Text(window, height=1, width=20, bg="#e68ab8")
text.place(x=100, y=110)
text.insert("1.0", "")

# ----------------------------------


# 訂單狀況 label frame
# 框框名稱
orderFrame = ttk.LabelFrame(window, text="訂單狀況")
orderFrame.place(x=350, y=45)

orderFrameName = ["結案", "未處理", "已寄出", "已收到"]  # 表單內容
orderFrameValue = tk.StringVar()  # 元件的變數
orderFrameValue.set("未處理")  # 初始值
for x in range(0, len(orderFrameName)):
    orderFrameButton = tk.Radiobutton(orderFrame, text=orderFrameName[x],
                                      variable=orderFrameValue,
                                      value=orderFrameName[x])
    orderFrameButton.pack()

# ---------------------------

# 列表 tree box
columns = ["訂單編號", "商品名稱", "金額", "備註", "訂單狀況"]


treeFrame = ttk.LabelFrame(window)
treeFrame.place(x=0, y=165)
tree = ttk.Treeview(treeFrame, columns=columns, show="headings")
tree.pack(side=LEFT)

treeScrollbar = ttk.Scrollbar(treeFrame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=treeScrollbar.set)
treeScrollbar.pack(side=RIGHT, fill=Y)
# 對應且輸入各個列表標題的名稱
for x in range(0, len(columns)):
    tree.column(columns[x], anchor=CENTER,
                stretch=NO, width=int((w-20) / len(columns)))
    tree.heading(columns[x], text=columns[x])

# 圖型數據初始值
dataProductName = []
dataMoney = []

# 儲存按鈕
saveButton = tk.Button(text="Save MySQL", font=("標楷體", 15), command=saveData)
saveButton.place(x=20, y=410)
editButton = tk.Button(text="Edit MySQL", font=("標楷體", 15), command=editData)
editButton.place(x=150, y=410)
loadButton = tk.Button(text="Load MySQL", font=("標楷體", 15), command=loadData)
loadButton.place(x=280, y=410)
delButton = tk.Button(text="Delete MySQL", font=("標楷體", 15), command=delData)
delButton.place(x=410, y=410)


# 跑柱狀圖
def moneyRun():
    try:
        # 圖表打中文 需要這兩行
        plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
        plt.rcParams['axes.unicode_minus'] = False

        # 轉成數字
        for i in range(0, len(dataMoney)):
            dataMoney[i] = int(dataMoney[i])

        # 柱體 設置 x y 寬度
        plt.bar(dataProductName, dataMoney, width=0.5)

        # y軸設定至內容物最高值
        high = max(dataMoney)
        plt.ylim([0, high])

        plt.xlabel("商品名稱")  # x軸名稱
        plt.ylabel("金額")  # y軸名稱
        plt.show()

    except:
        tkMessageBox.showerror("錯誤", "目前還沒有資料儲存")


# ----------------------------
# toolbar 工具欄

toolbar = tk.Frame(window, bd=0.5, relief=RAISED)
toolbar.pack(side=TOP, fill=X)  # 讓他在最上方且整排

# 工具欄圖片區
img = Image.open("bar1.jpg")
eImg1 = ImageTk.PhotoImage(img)
img = Image.open("open.jpg")
eImg2 = ImageTk.PhotoImage(img)
img = Image.open("save.jpg")
eImg3 = ImageTk.PhotoImage(img)
img = Image.open("exit.jpg")
eImg4 = ImageTk.PhotoImage(img)

# 工具欄按鈕
barButton = Button(toolbar, image=eImg1, relief=FLAT, command=moneyRun)
barButton.pack(side=LEFT, padx=2, pady=2)
readButton = Button(toolbar, image=eImg2, relief=FLAT, command=loadData)
readButton.pack(side=LEFT)
saveButton2 = Button(toolbar, image=eImg3, relief=FLAT, command=savexlsx)
saveButton2.pack(side=LEFT)
exitButton = Button(toolbar, image=eImg4, relief=FLAT, command=exitDo)
exitButton.pack(side=LEFT)


window.mainloop()
