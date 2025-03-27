from pycatia import catia
from pycatia.mec_mod_interfaces.part_document import PartDocument
import tkinter as tk
from tkinter import messagebox

# 受保护的标准属性（名称和值双重验证）
PROTECTED_PROPERTIES = {
    "物料编码": "物料编码",
    "物料名称": "物料名称",
    "规格型号": "规格型号",
    "材质": "材质",
    "类别": "类别",
    "备注": "备注"
}


def connect_to_catia():
    """连接 CATIA 并返回 CATIA 应用对象"""
    caa = catia()
    caa.visible = True
    return caa


def get_or_create_part_document(caa):
    """获取当前活动的 CATIA 零件文档，如果没有，则创建新文档"""
    try:
        return caa.active_document
    except Exception:
        messagebox.showwarning("文档创建", "未找到活动文档，正在创建新零件文档")
        return caa.documents.add('Part')


def delete_properties(part_document):
    """安全删除非标准属性，并检测是否有重复项"""
    try:
        user_props = part_document.product.user_ref_properties
        existing_props = {prop.name: prop.value for prop in user_props}
        protected_set = set(PROTECTED_PROPERTIES.items())

        to_delete = []
        seen_props = set()

        for prop_name, prop_value in existing_props.items():
            if (prop_name, prop_value) not in protected_set:
                # 如果属性名已出现过（说明有重复项），加入删除列表
                if prop_name in seen_props:
                    to_delete.append(prop_name)
                else:
                    seen_props.add(prop_name)

        for prop_name in to_delete:
            try:
                user_props.remove(prop_name)
            except Exception as e:
                messagebox.showerror("删除错误",
                                     f"删除属性 '{prop_name}' 失败\n错误类型: {type(e).__name__}\n详情: {str(e)}")

        part_document.part.update()

        if to_delete:
            messagebox.showinfo("清理完成", f"已清理 {len(to_delete)} 个重复或非标属性")
        else:
            messagebox.showinfo("无非标属性", "没有需要删除的非标属性")

    except Exception as e:
        messagebox.showerror("操作失败", f"属性清理失败\n错误类型: {type(e).__name__}\n详情: {str(e)}")


def add_properties(part_document):
    """智能添加缺失的标准属性，防止重复添加"""
    try:
        user_props = part_document.product.user_ref_properties
        existing_props = {prop.name: prop.value for prop in user_props}

        to_add = {}

        for name, value in PROTECTED_PROPERTIES.items():
            if name in existing_props:
                # 如果属性已存在但值不同，则更新
                if existing_props[name] != value:
                    user_props.remove(name)  # 先删除原有的
                    to_add[name] = value
            else:
                to_add[name] = value

        for prop_name, prop_value in to_add.items():
            try:
                user_props.create_string(prop_name, prop_value)
            except Exception as e:
                messagebox.showerror("添加错误",
                                     f"添加属性 '{prop_name}' 失败\n错误类型: {type(e).__name__}\n详情: {str(e)}")

        part_document.part.update()

        if to_add:
            messagebox.showinfo("更新完成", f"成功补全 {len(to_add)} 个标准属性")
        else:
            messagebox.showinfo("无需更新", "所有标准属性已存在且符合规范")

    except Exception as e:
        messagebox.showerror("操作失败", f"属性添加失败\n错误类型: {type(e).__name__}\n详情: {str(e)}")


def create_tkinter_window(part_document):
    """创建 Tkinter GUI 界面"""
    root = tk.Tk()
    root.geometry('350x150+300+300')
    root.title('CATIA 高级属性管理')
    root.attributes("-topmost", True)

    btn_style = {
        'width': 18,
        'height': 2,
        'font': ('微软雅黑', 10, 'bold'),
        'borderwidth': 3
    }

    action_frame = tk.Frame(root)
    action_frame.pack(pady=20)

    tk.Button(action_frame, text="智能补全标准属性",
              command=lambda: add_properties(part_document),
              **btn_style, bg='#4CAF50', fg='white').grid(row=0, column=0, padx=10)

    tk.Button(action_frame, text="安全清理非标属性",
              command=lambda: delete_properties(part_document),
              **btn_style, bg='#F44336', fg='white').grid(row=0, column=1, padx=10)

    root.mainloop()


def main():
    """主函数"""
    try:
        caa = connect_to_catia()
        part_doc = get_or_create_part_document(caa)
        create_tkinter_window(part_doc)
    except Exception as e:
        messagebox.showerror("系统错误",
                             f"程序启动失败\n错误类型: {type(e).__name__}\n详情: {str(e)}")


if __name__ == "__main__":
    main()
