#Import some required libraries  
from pycatia import catia  
from pycatia.mec_mod_interfaces.part_document import PartDocument  
import tkinter as tk  
#Connect to catia and the catia client window displays
caa = catia()  
caa.visible = True  
#Error prevention: If the opened file is a part document, run it directly. If not, create a new part document.
try:  
    part_Document: PartDocument = caa.active_document  
except:  
    documents = caa.documents  
    PartDocument = documents.add('Part')  
    part_Document: PartDocument = caa.active_document  
  
  
def Pdel():  
    DelUstr1 = part_Document.product.user_ref_properties.remove("物料编码")  
    DelUstr2 = part_Document.product.user_ref_properties.remove("物料名称")  
    DelUstr3 = part_Document.product.user_ref_properties.remove("材质")  
    DelUstr4 = part_Document.product.user_ref_properties.remove("备注")  
    DelUstr5 = part_Document.product.user_ref_properties.remove("重要描述")  
    DelUstr6 = part_Document.product.user_ref_properties.remove("规格")  
    part_Document.part.update  
  
def Padd():  
    Ustr1 = part_Document.product.user_ref_properties.create_string("物料编码", "物料编码")  
    Ustr2 = part_Document.product.user_ref_properties.create_string("物料名称", "物料名称")  
    Ustr3 = part_Document.product.user_ref_properties.create_string("材质", "材料")  
    Ustr4 = part_Document.product.user_ref_properties.create_string("备注", "备注")  
    Ustr5 = part_Document.product.user_ref_properties.create_string("重要描述", "重要描述")  
    Ustr6 = part_Document.product.user_ref_properties.create_string("规格", "规格")  
    part_Document.part.update  
  
#tk windows  
root = tk.Tk()  
root.geometry('200x50+200+200')  
root.title('添加CATIA自定义零件属性')  
root.attributes("-topmost", True)  
bt1 = tk.Button(root, text="添加自定义参数", command=Padd, width=12)  
bt1.grid(row=5, column=10)  
bt2 = tk.Button(root, text="清理自定义参数", command=Pdel, width=12)  
bt2.grid(row=5, column=20)  
root.mainloop()
