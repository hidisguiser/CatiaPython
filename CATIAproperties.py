from pycatia import catia
from pycatia.mec_mod_interfaces.part_document import PartDocument
import tkinter as tk

# 常量定义，用于存储属性名称
PROPERTIES = ["物料编码", "物料名称", "材质", "备注", "重要描述", "规格"]

# 连接到CATIA并显示CATIA客户端窗口
def connect_to_catia():
    caa = catia()
    caa.visible = True
    return caa

# 获取或创建PartDocument
def get_or_create_part_document(caa):
    try:
        part_document = caa.active_document
    except Exception as e:
        print(f"未找到活动文档，创建新文档。错误信息: {e}")
        documents = caa.documents
        part_document = documents.add('Part')
    return part_document

# 删除自定义属性
def delete_properties(part_document):
    for prop in PROPERTIES:
        try:
            part_document.product.user_ref_properties.remove(prop)
        except Exception as e:
            print(f"删除属性 '{prop}' 失败: {e}")
    part_document.part.update()

# 添加自定义属性
def add_properties(part_document):
    for prop in PROPERTIES:
        try:
            part_document.product.user_ref_properties.create_string(prop, prop)
        except Exception as e:
            print(f"添加属性 '{prop}' 失败: {e}")
    part_document.part.update()

# 创建Tkinter窗口
def create_tkinter_window(part_document):
    root = tk.Tk()
    root.geometry('200x50+200+200')
    root.title('添加CATIA自定义零件属性')
    root.attributes("-topmost", True)

    bt1 = tk.Button(root, text="添加自定义参数", command=lambda: add_properties(part_document), width=12)
    bt1.grid(row=5, column=10)

    bt2 = tk.Button(root, text="清理自定义参数", command=lambda: delete_properties(part_document), width=12)
    bt2.grid(row=5, column=20)

    root.mainloop()

# 主函数
def main():
    caa = connect_to_catia()
    part_document = get_or_create_part_document(caa)
    create_tkinter_window(part_document)

if __name__ == "__main__":
    main()
