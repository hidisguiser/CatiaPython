from pycatia import catia
from pycatia.mec_mod_interfaces.part_document import PartDocument
import tkinter as tk
from tkinter import messagebox

# 常量定义（受保护的属性不会被删除）
PROTECTED_PROPERTIES = ["物料编码", "物料名称", "规格型号", "材质", "类别", "备注"]

def connect_to_catia():
    caa = catia()
    caa.visible = True
    return caa

def get_or_create_part_document(caa):
    try:
        return caa.active_document
    except Exception as e:
        messagebox.showwarning("文档创建", "未找到活动文档，正在创建新零件文档")
        return caa.documents.add('Part')

def delete_properties(part_document):
    """删除非常量属性"""
    try:
        all_props = list(part_document.product.user_ref_properties)
        deleted_count = 0
        
        for prop in all_props:
            if prop.name in PROTECTED_PROPERTIES:  # 跳过受保护属性
                continue
                
            try:
                part_document.product.user_ref_properties.remove(prop.name)
                deleted_count += 1
            except Exception as e:
                messagebox.showerror("删除错误", f"删除属性 '{prop.name}' 失败\n错误详情: {str(e)}")
        
        part_document.part.update()
        messagebox.showinfo("删除完成", f"已清理 {deleted_count} 个非标准属性")
    except Exception as e:
        messagebox.showerror("严重错误", f"获取属性列表失败\n错误详情: {str(e)}")

def add_properties(part_document):
    """仅添加常量属性且自动去重"""
    try:
        existing_props = [prop.name for prop in part_document.product.user_ref_properties]
        added_count = 0
        
        for prop in PROTECTED_PROPERTIES:
            if prop in existing_props:
                continue  # 静默跳过已有属性
                
            try:
                part_document.product.user_ref_properties.create_string(prop, prop)
                added_count += 1
            except Exception as e:
                messagebox.showerror("添加错误", f"添加属性 '{prop}' 失败\n错误详情: {str(e)}")
        
        part_document.part.update()
        if added_count > 0:
            messagebox.showinfo("添加完成", f"新增 {added_count} 个标准属性")
        else:
            messagebox.showwarning("无新增", "所有标准属性已存在")
    except Exception as e:
        messagebox.showerror("严重错误", f"获取属性列表失败\n错误详情: {str(e)}")

def create_tkinter_window(part_document):
    root = tk.Tk()
    root.geometry('280x100+200+200')
    root.title('CATIA属性管理工具')
    root.attributes("-topmost", True)

    # 增强按钮样式
    btn_style = {
        'width': 14,
        'height': 1,
        'font': ('微软雅黑', 10)
    }

    action_frame = tk.Frame(root)
    action_frame.pack(pady=15)

    tk.Button(action_frame, text="初始化标准属性", 
             command=lambda: add_properties(part_document),
             **btn_style, bg='#4CAF50', fg='white').grid(row=0, column=0, padx=8)
    
    tk.Button(action_frame, text="清理非标属性", 
             command=lambda: delete_properties(part_document),
             **btn_style, bg='#f44336', fg='white').grid(row=0, column=1, padx=8)

    root.mainloop()

def main():
    try:
        caa = connect_to_catia()
        part_doc = get_or_create_part_document(caa)
        create_tkinter_window(part_doc)
    except Exception as e:
        messagebox.showerror("启动失败", f"程序初始化失败\n错误详情: {str(e)}")

if __name__ == "__main__":
    main()
