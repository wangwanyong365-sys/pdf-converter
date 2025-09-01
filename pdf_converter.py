import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import PyPDF2
import os

class PDFConverter:
    def __init__(self, root):
        self.root = root
        # 设置软件标题为 "PDF 转换器"
        self.root.title("PDF 转换器")
        self.root.geometry("650x550")
        self.root.minsize(500, 450)

        # 设置主题
        self.style = ttk.Style(self.root)
        self.style.theme_use("clam")  # 可尝试 "alt", "default", "vista" 等主题

        self.pdf_files = []
        self.output_dir = ""
        
        self.create_widgets()
    
    def create_widgets(self):
        # ---- 主框架 ----
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(expand=True, fill=tk.BOTH)
        
        # 使网格布局自适应窗口大小
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # ---- 标题 ----
        title_label = ttk.Label(main_frame, text="PDF 转换器", font=("微软雅黑", 20, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky=tk.N)
        
        # ---- 文件选择区域 ----
        files_frame = ttk.LabelFrame(main_frame, text="文件操作", padding="10")
        files_frame.grid(row=1, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))
        files_frame.columnconfigure(0, weight=1)
        files_frame.rowconfigure(1, weight=1)

        # 文件选择按钮
        select_buttons_frame = ttk.Frame(files_frame)
        select_buttons_frame.grid(row=0, column=0, columnspan=2, pady=5, sticky=(tk.W, tk.E))
        
        ttk.Button(select_buttons_frame, text="选择PDF文件", command=self.select_pdf_files, width=20).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(select_buttons_frame, text="选择输出目录", command=self.select_output_dir, width=20).pack(side=tk.LEFT)

        # 文件列表框和滚动条
        listbox_frame = ttk.Frame(files_frame)
        listbox_frame.grid(row=1, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))
        listbox_frame.columnconfigure(0, weight=1)
        listbox_frame.rowconfigure(0, weight=1)

        self.file_listbox = tk.Listbox(listbox_frame, height=10, selectmode=tk.EXTENDED)
        self.file_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        scrollbar = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=self.file_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.file_listbox.config(yscrollcommand=scrollbar.set)
        
        # ---- 转换选项 ----
        options_frame = ttk.LabelFrame(main_frame, text="转换选项", padding="10")
        options_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))
        
        self.merge_var = tk.BooleanVar()
        ttk.Checkbutton(options_frame, text="将所有PDF合并为一个TXT文件", variable=self.merge_var).pack(side=tk.LEFT)
        
        # ---- 转换按钮和状态栏 ----
        action_frame = ttk.Frame(main_frame)
        action_frame.grid(row=3, column=0, columnspan=2, pady=(20, 0), sticky=(tk.W, tk.E))
        action_frame.columnconfigure(0, weight=1)

        self.convert_button = ttk.Button(action_frame, text="转换为 TXT", command=self.convert_to_txt, style="Accent.TButton")
        self.convert_button.grid(row=0, column=0, columnspan=2, ipady=5, sticky=(tk.W, tk.E))
        
        self.status_label = ttk.Label(action_frame, text="准备就绪", anchor=tk.W, foreground="gray")
        self.status_label.grid(row=1, column=0, columnspan=2, pady=(10, 0), sticky=(tk.W, tk.E))
        
        # 自定义按钮样式
        self.style.configure("Accent.TButton", font=("微软雅黑", 12, "bold"), padding=10)

    def select_pdf_files(self):
        files = filedialog.askopenfilenames(
            title="请选择一个或多个PDF文件",
            filetypes=[("PDF 文件", "*.pdf"), ("所有文件", "*.*")]
        )
        if files:
            self.pdf_files = list(files)
            self.file_listbox.delete(0, tk.END)
            for file in self.pdf_files:
                self.file_listbox.insert(tk.END, os.path.basename(file))
            self.update_status(f"已选择 {len(self.pdf_files)} 个PDF文件", "blue")
    
    def select_output_dir(self):
        directory = filedialog.askdirectory(title="请选择输出文件夹")
        if directory:
            self.output_dir = directory
            self.update_status(f"输出目录: {self.output_dir}", "blue")
    
    def convert_to_txt(self):
        if not self.pdf_files:
            messagebox.showerror("错误", "请至少选择一个PDF文件！")
            return
        
        if not self.output_dir:
            messagebox.showerror("错误", "请选择一个输出目录！")
            return
        
        self.convert_button.config(state=tk.DISABLED)
        self.update_status("正在转换中，请稍候...", "orange")
        self.root.update_idletasks() # 强制更新UI

        try:
            if self.merge_var.get() and len(self.pdf_files) > 1:
                self.convert_and_merge()
            else:
                self.convert_separately()
            
            messagebox.showinfo("成功", "文件转换成功！")
            self.update_status("转换完成！", "green")
            
        except Exception as e:
            messagebox.showerror("错误", f"转换失败: {str(e)}")
            self.update_status("转换失败！", "red")
        finally:
            self.convert_button.config(state=tk.NORMAL)

    def convert_separately(self):
        total_files = len(self.pdf_files)
        for i, pdf_file in enumerate(self.pdf_files, 1):
            try:
                self.update_status(f"正在转换: ({i}/{total_files}) {os.path.basename(pdf_file)}", "orange")
                self.root.update_idletasks()
                
                with open(pdf_file, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    text_content = ""
                    
                    for page in pdf_reader.pages:
                        text_content += page.extract_text() or "" + "\n\n"
                    
                    base_name = os.path.splitext(os.path.basename(pdf_file))[0]
                    output_file = os.path.join(self.output_dir, f"{base_name}.txt")
                    
                    with open(output_file, 'w', encoding='utf-8') as txt_file:
                        txt_file.write(text_content)
                        
            except Exception as e:
                raise Exception(f"转换文件 {os.path.basename(pdf_file)} 失败: {str(e)}")
    
    def convert_and_merge(self):
        merged_text = ""
        total_files = len(self.pdf_files)

        for i, pdf_file in enumerate(self.pdf_files, 1):
            try:
                self.update_status(f"正在合并: ({i}/{total_files}) {os.path.basename(pdf_file)}", "orange")
                self.root.update_idletasks()

                with open(pdf_file, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    base_name = os.path.splitext(os.path.basename(pdf_file))[0]
                    
                    merged_text += f"=== {base_name} ===\n\n"
                    
                    for page in pdf_reader.pages:
                        merged_text += page.extract_text() or "" + "\n\n"
                    
                    merged_text += "\n" + "="*50 + "\n\n"
                    
            except Exception as e:
                raise Exception(f"处理文件 {os.path.basename(pdf_file)} 失败: {str(e)}")
        
        output_file = os.path.join(self.output_dir, "合并后的文件.txt")
        with open(output_file, 'w', encoding='utf-8') as txt_file:
            txt_file.write(merged_text)

    def update_status(self, text, color):
        """更新状态标签的文本和颜色"""
        self.status_label.config(text=text, foreground=color)

def main():
    root = tk.Tk()
    app = PDFConverter(root)
    root.mainloop()

if __name__ == "__main__":
    main()
