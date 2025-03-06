import os
import pandas as pd
import seaborn as sns
import matplotlib
matplotlib.use('TkAgg')  # 适配 macOS，确保 TkAgg 后端
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import matplotlib.colors as mcolors
import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

plt.rcParams['figure.dpi'] = 200  # 适配 macOS Retina 屏幕

def plotFigure(df, cmap_color="Greens"):
    # 确保数据是数值型
    df['x'] = pd.to_numeric(df['x'], errors='coerce')
    df['y'] = pd.to_numeric(df['y'], errors='coerce')

    if df.isnull().values.any():
        messagebox.showerror("错误", "数据包含无效数值，无法绘制！")
        return

    # 创建新的 Tkinter 窗口
    plot_window = tk.Toplevel(root)
    plot_window.title("Circular Density Plot")
    plot_window.geometry("700x700")

    # 创建 Matplotlib 图形
    fig, ax = plt.subplots(figsize=(6, 6))

    # 解析颜色映射
    if cmap_color.startswith("#"):
        try:
            cmap_color = mcolors.LinearSegmentedColormap.from_list("custom", [cmap_color])
        except ValueError:
            messagebox.showerror("错误", f"无法解析颜色 {cmap_color}，请使用有效颜色！")
            return
    else:
        cmap_color = sns.color_palette(cmap_color, as_cmap=True)

    # 绘制散点
    ax.scatter(df.x, df.y, color='black', alpha=0.5, s=10)

    # **修复 KDE 计算导致白屏**
    try:
        sns.kdeplot(x=df.x, y=df.y, cmap=cmap_color, fill=True, bw_adjust=0.5, ax=ax, alpha=0.8)
    except Exception as e:
        messagebox.showerror("KDE 计算错误", f"无法生成密度图: {e}")
        return

    # 设置坐标轴比例
    ax.set_aspect('equal')
    xlim, ylim = ax.get_xlim(), ax.get_ylim()
    center_x, center_y = sum(xlim) / 2, sum(ylim) / 2
    radius = min((xlim[1] - xlim[0]), (ylim[1] - ylim[0])) / 2

    # 画圆并裁剪
    circle = Circle((center_x, center_y), radius, transform=ax.transData)
    for collection in ax.collections:
        collection.set_clip_path(circle)

    ax.set_xlim(center_x - radius, center_x + radius)
    ax.set_ylim(center_y - radius, center_y + radius)
    ax.axis('off')

    # **将 Matplotlib 画布嵌入 Tkinter**
    canvas = FigureCanvasTkAgg(fig, master=plot_window)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill=tk.BOTH, expand=True)

    # **强制刷新画布**
    canvas.draw_idle()
    plot_window.update_idletasks()

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
            df = pd.read_csv(file_path) if file_path.endswith(".csv") else pd.read_excel(file_path)
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
        btn.configure(bg="#FF9500", fg="white", activebackground="#FF6F00", activeforeground="white", bd=0, relief="flat", padx=20, pady=5)

    def style_label(lbl):
        lbl.configure(bg="#333333", fg="#E0E0E0", font=("Ubuntu", 10))

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