import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd

def loadDataset():
    # Load the penguins dataset and drop missing values
    df = sns.load_dataset('penguins').dropna()
    return df

def save2csv(df):
    # Create a new DataFrame with specified columns
    new_df = pd.DataFrame({
        'x': df.bill_length_mm,
        'y': df.bill_depth_mm
    })
    # Save to a CSV file (optional)
    new_df.to_csv('penguins_bill_data.csv', index=False)

def plotFigure(df):
    # Create the plot
    fig, ax = plt.subplots(figsize=(6, 6))

    # Draw the 2D kernel density estimate (KDE) plot
    kde_plot = sns.kdeplot(
        x=df.x,
        y=df.y,
        cmap="Greens",
        fill=True,
        bw_adjust=0.5,
        ax=ax
    )

    # Set equal aspect ratio for the axes
    ax.set_aspect('equal')

    # Get axis limits
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()

    # Calculate the center and radius for the circular mask
    center_x = (xlim[0] + xlim[1]) / 2
    center_y = (ylim[0] + ylim[1]) / 2
    radius = min((xlim[1] - xlim[0]), (ylim[1] - ylim[0])) / 2

    # Create a circular mask
    circle = Circle((center_x, center_y), radius, transform=ax.transData)
    for collection in ax.collections:
        collection.set_clip_path(circle)

    # Set axis limits
    ax.set_xlim(center_x - radius, center_x + radius)
    ax.set_ylim(center_y - radius, center_y + radius)

    # Add a colorbar for the KDE plot
    # Get the first collection from kde_plot for colorbar scaling
    if ax.collections:
        norm = plt.Normalize(vmin=0, vmax=ax.collections[0].get_array().max())
        sm = plt.cm.ScalarMappable(cmap="Greens", norm=norm)
        sm.set_array([])

        # Display colorbar
        cbar = plt.colorbar(sm, ax=ax, orientation='vertical')
        cbar.set_label('Density Level')

    # Hide the axes
    ax.axis('off')

    # Show the plot
    plt.show()

# 文件上传函数
def upload_file():
    global file_path
    file_path = filedialog.askopenfilename(
        filetypes=[("CSV Files", "*.csv"), ("Excel Files", "*.xlsx"), ("All Files", "*.*")]
    )
    if file_path:
        lbl_file_path.config(text=f"文件路径: {file_path}")

# 点击按钮执行的函数
def process_file():
    if file_path:
        # 示例：读取文件并显示前5行（根据需要替换为具体的处理函数）
        try:
            if file_path.endswith(".csv"):
                df = pd.read_csv(file_path)
            elif file_path.endswith(".xlsx"):
                df = pd.read_excel(file_path)
            else:
                messagebox.showerror("错误", "不支持的文件格式！")
                return

            # 显示表格的前5行
            messagebox.showinfo("文件内容", f"文件读取成功！\n前5行数据:\n{df.head()}")
            plotFigure(df)
        except Exception as e:
            messagebox.showerror("错误", f"文件处理失败：{e}")
    else:
        messagebox.showwarning("警告", "请先上传文件！")


if __name__ == '__main__':
    # df = loadDataset()
    # save2csv(df)
    # plotFigure(df)
    # 创建主窗口
    root = tk.Tk()
    root.title("表格文件上传小程序")
    root.geometry("600x400")

    # 定义全局变量来存储文件路径
    file_path = ""
    # 创建上传按钮
    btn_upload = tk.Button(root, text="上传文件", command=upload_file, font=("Arial", 12))
    btn_upload.pack(pady=20)

    # 显示文件路径的标签
    lbl_file_path = tk.Label(root, text="文件路径: ", font=("Arial", 10), wraplength=380)
    lbl_file_path.pack(pady=5)

    # 创建处理按钮
    btn_process = tk.Button(root, text="处理文件", command=process_file, font=("Arial", 12))
    btn_process.pack(pady=20)

    # 运行主循环
    root.mainloop()

