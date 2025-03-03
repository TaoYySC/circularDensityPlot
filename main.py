import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
import matplotlib.colors as mcolors


def loadDataset():
    df = sns.load_dataset('penguins').dropna()
    return df


def save2csv(df):
    new_df = pd.DataFrame({
        'x': df.bill_length_mm,
        'y': df.bill_depth_mm
    })
    new_df.to_csv('penguins_bill_data.csv', index=False)


def plotFigure(df, cmap_color="Greens"):
    fig, ax = plt.subplots(figsize=(6, 6))

    # 处理 HTML 颜色代码
    if cmap_color.startswith("#"):
        try:
            cmap_color = sns.light_palette(mcolors.hex2color(cmap_color), as_cmap=True)
        except ValueError:
            messagebox.showerror("错误", f"无法解析颜色 {cmap_color}，请使用有效颜色！")
            return

    # 增强颗粒感
    scatter = ax.scatter(df.x, df.y, color='black', alpha=0.5, s=10)  # 小点颗粒感

    kde_plot = sns.kdeplot(
        x=df.x,
        y=df.y,
        cmap=cmap_color,
        fill=True,
        bw_adjust=0.3,  # 调整带宽参数使得颗粒感增强
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

    # 动态调整 density 颜色条位置，使其完全位于画布内部
    bbox = ax.get_position()
    cbar_x = min(bbox.x1 + 0.02, 0.9)  # 确保不超出画布
    cbar_y = max(bbox.y0 + 0.05, 0.15)  # 确保不会过低
    cbar_width = 0.02  # 缩小宽度
    cbar_height = 0.2  # 缩小高度
    ax_density = fig.add_axes([cbar_x, cbar_y, cbar_width, cbar_height])

    if ax.collections:
        max_val = max([col.get_array().max() for col in ax.collections if col.get_array() is not None], default=1)
        norm = plt.Normalize(vmin=0, vmax=max_val)
        sm = plt.cm.ScalarMappable(cmap=cmap_color, norm=norm)
        sm.set_array([])
        cbar = plt.colorbar(sm, cax=ax_density, orientation='vertical')
        # cbar.set_label("Density", labelpad=-10)
        ax_density.tick_params(labelsize=8)  # 让刻度字体变小，确保在画布内部

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
            plotFigure(df, selected_color.get())
        except Exception as e:
            messagebox.showerror("错误", f"文件处理失败：{e}")
    else:
        messagebox.showwarning("警告", "请先上传文件！")


def choose_color():
    color = colorchooser.askcolor(title="选择颜色")[1]
    if color:
        selected_color.set(color)
        lbl_color_display.config(bg=color)


if __name__ == '__main__':
    root = tk.Tk()
    root.title("circularDensityPlot")
    root.geometry("600x400")
    root.configure(bg="#333333")
    file_path = ""
    selected_color = tk.StringVar(value="Greens")


    def style_button(btn):
        btn.configure(
            bg="#FF9500",
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


    btn_upload = tk.Button(root, text="上传文件", command=upload_file)
    style_button(btn_upload)
    btn_upload.pack(pady=10)

    lbl_file_path = tk.Label(root, text="文件路径: ", wraplength=380)
    style_label(lbl_file_path)
    lbl_file_path.pack(pady=5)

    btn_process = tk.Button(root, text="处理文件", command=process_file)
    style_button(btn_process)
    btn_process.pack(pady=10)

    lbl_color = tk.Label(root, text="选择颜色: ")
    style_label(lbl_color)
    lbl_color.pack(pady=5)

    btn_color = tk.Button(root, text="选择", command=choose_color)
    style_button(btn_color)
    btn_color.pack(pady=5)

    lbl_color_display = tk.Label(root, width=20, height=2, bg="#008000")
    lbl_color_display.pack(pady=5)

    root.mainloop()
