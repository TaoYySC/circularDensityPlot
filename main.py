import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import tkinter as tk
from tkinter import filedialog, messagebox

def loadDataset():
    df = sns.load_dataset('penguins').dropna()
    return df

def save2csv(df):
    new_df = pd.DataFrame({
        'x': df.bill_length_mm,
        'y': df.bill_depth_mm
    })
    new_df.to_csv('penguins_bill_data.csv', index=False)

def plotFigure(df):
    fig, ax = plt.subplots(figsize=(6, 6))
    kde_plot = sns.kdeplot(
        x=df.x,
        y=df.y,
        cmap="Greens",
        fill=True,
        bw_adjust=0.5,
        ax=ax
    )
    ax.set_aspect('equal')
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    center_x = (xlim[0] + xlim[1]) / 2
    center_y = (ylim[0] + ylim[1]) / 2
    radius = min((xlim[1] - xlim[0]), (ylim[1] - ylim[0])) / 2
    circle = Circle((center_x, center_y), radius, transform=ax.transData)
    for collection in ax.collections:
        collection.set_clip_path(circle)
    ax.set_xlim(center_x - radius, center_x + radius)
    ax.set_ylim(center_y - radius, center_y + radius)
    if ax.collections:
        norm = plt.Normalize(vmin=0, vmax=ax.collections[0].get_array().max())
        sm = plt.cm.ScalarMappable(cmap="Greens", norm=norm)
        sm.set_array([])
        cbar = plt.colorbar(sm, ax=ax, orientation='vertical')
        cbar.set_label('Density Level')
    ax.axis('off')
    plt.show()

def upload_file():
    global file_path
    file_path = filedialog.askopenfilename(
        filetypes=[("CSV Files", "*.csv"), ("Excel Files", "*.xlsx"), ("All Files", "*.*")]
    )
    if file_path:
        lbl_file_path.config(text=f"文件路径: {file_path}", fg="#ff9500")

def process_file():
    if file_path:
        try:
            if file_path.endswith(".csv"):
                df = pd.read_csv(file_path)
            elif file_path.endswith(".xlsx"):
                df = pd.read_excel(file_path)
            else:
                messagebox.showerror("错误", "不支持的文件格式！")
                return
            messagebox.showinfo("文件内容", f"文件读取成功！\n前5行数据:\n{df.head()}")
            plotFigure(df)
        except Exception as e:
            messagebox.showerror("错误", f"文件处理失败：{e}")
    else:
        messagebox.showwarning("警告", "请先上传文件！")

if __name__ == '__main__':
    # 创建主窗口
    root = tk.Tk()
    root.title("Ubuntu 风格的表格文件上传小程序")
    root.geometry("600x400")
    root.configure(bg="#333333")  # 深色背景

    # 定义全局变量来存储文件路径
    file_path = ""

    # 设置全局字体
    root.option_add("*Font", "Ubuntu 12")

    # 样式设置函数
    def style_button(btn):
        btn.configure(
            bg="#FF9500",  # Ubuntu 高亮色
            fg="white",
            activebackground="#FF6F00",
            activeforeground="white",
            bd=0,
            relief="flat",
            padx=20,
            pady=5
        )

    def style_label(lbl):
        lbl.configure(
            bg="#333333",
            fg="#E0E0E0",
            font=("Ubuntu", 10)
        )

    # 上传按钮
    btn_upload = tk.Button(root, text="上传文件", command=upload_file)
    style_button(btn_upload)
    btn_upload.pack(pady=20)

    # 显示文件路径的标签
    lbl_file_path = tk.Label(root, text="文件路径: ", wraplength=380)
    style_label(lbl_file_path)
    lbl_file_path.pack(pady=5)

    # 处理按钮
    btn_process = tk.Button(root, text="处理文件", command=process_file)
    style_button(btn_process)
    btn_process.pack(pady=20)

    # 运行主循环
    root.mainloop()
