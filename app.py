import customtkinter
import pandas as pd
from PIL import Image, ImageTk


customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    
    WIDTH = 780
    HEIGHT = 520
    
    def __init__(self):
        super().__init__()

        self.added_items = []
        self.added_labels = []
        self.cost_labels = []
        self.total_cost = 0
        self.all_counts_vars = []
        self.total_var = customtkinter.StringVar(value="0")

        self.all_items = pd.read_csv('test.csv')

        for i in range(len(self.all_items["count"])):
            self.all_counts_vars.append(customtkinter.StringVar(value=self.all_items["count"][i]))

        self.title("Mariam's Inventory Management")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")

        # ============ create two frames ============

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self, width=380, corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        # ============ frame_left ============

        self.frame_left.grid_rowconfigure(0, minsize=50)
        self.frame_left.grid_rowconfigure(5, weight=1)
        self.frame_left.grid_rowconfigure(8, minsize=30)
        self.frame_left.grid_rowconfigure(11, minsize=30)

        left_label = customtkinter.CTkLabel(self.frame_left, text="Inventory", bg_color=("#C0C2C5","#363A3D"))
        left_label.grid(row=1, column=0, pady=10, padx=10)

        first_img = ImageTk.PhotoImage(Image.open("./images/"+self.all_items["img"][0]).resize((20,20), Image.ANTIALIAS))
        second_img = ImageTk.PhotoImage(Image.open("./images/"+self.all_items["img"][1]).resize((20,20), Image.ANTIALIAS))
        third_img = ImageTk.PhotoImage(Image.open("./images/"+self.all_items["img"][2]).resize((20,20), Image.ANTIALIAS))
        add_button_1 = customtkinter.CTkButton(self.frame_left, image=first_img, textvariable=self.all_counts_vars[0], command=lambda:self.add_item(self.all_items.iloc[0],0))
        add_button_2 = customtkinter.CTkButton(self.frame_left, image=second_img, textvariable=self.all_counts_vars[1], command=lambda:self.add_item(self.all_items.iloc[1],1))
        add_button_3 = customtkinter.CTkButton(self.frame_left, image=third_img, textvariable=self.all_counts_vars[2], command=lambda:self.add_item(self.all_items.iloc[2],2))
        add_button_1.grid(row=2, column=0, pady=10, padx=10)
        add_button_2.grid(row=3, column=0, pady=10, padx=10)
        add_button_3.grid(row=4, column=0, pady=10, padx=10)

        remove_button = customtkinter.CTkButton(self.frame_left, text="remove last item", command=self.remove_item, fg_color="#DB9435", hover_color="#A34F00")
        clear_button = customtkinter.CTkButton(self.frame_left, text="clear all items", command=self.clear_items, fg_color="#DB3E39", hover_color="#821D1A")
        remove_button.grid(row=11, column=0, pady=3, padx=10)
        clear_button.grid(row=12, column=0, pady=10, padx=10)

        # ============ frame_right ============
        self.frame_right.rowconfigure((0, 1, 2, 3), weight=1)
        self.frame_right.rowconfigure(7, weight=10)
        self.frame_right.columnconfigure((0, 1), weight=1)
        self.frame_right.columnconfigure(2, weight=0)

        self.frame_title = customtkinter.CTkFrame(master=self.frame_right)
        self.frame_title.grid(row=0, column=0, columnspan=2, rowspan=1, pady=20, padx=20, sticky="nsew")
        self.frame_title.rowconfigure(0, weight=1)
        self.frame_title.columnconfigure(0, weight=1)

        self.items_label = customtkinter.CTkLabel(self.frame_title, text="Items")
        self.costs_label = customtkinter.CTkLabel(self.frame_title, text="Cost")
        self.items_label.grid(row=0, column=0, pady=0, padx=10, sticky="w")
        self.costs_label.grid(row=0, column=1, pady=0, padx=10)

        self.frame_total = customtkinter.CTkFrame(master=self.frame_right)
        self.frame_total.grid(row=11, column=0, columnspan=2, rowspan=1, pady=20, padx=20, sticky="nsew")
        self.frame_total.rowconfigure(0, weight=1)
        self.frame_total.columnconfigure(0, weight=1)

        total_label = customtkinter.CTkLabel(self.frame_total, text="Total: ")
        total = customtkinter.CTkLabel(self.frame_total, textvariable=self.total_var)
        total_label.grid(row=0, column=0, pady=0, padx=10, sticky="w")
        total.grid(row=0, column=1, pady=0, padx=10)

        sell_button = customtkinter.CTkButton(self.frame_right, text="Sell items", command=self.sell_items, fg_color="#67BF63", hover_color="#4A8A48")
        sell_button.grid(row=12, rowspan=1, columnspan=2, pady=20, padx=20, sticky="nwse")


    def add_item(self, item, item_no):
        self.added_items.append((item, item_no))

        self.added_label = customtkinter.CTkLabel(self.frame_right, text=item["item"])
        self.added_label.grid(row=len(self.added_items), column=0, pady=3, padx=10)
        self.added_labels.append(self.added_label)

        cost_label = customtkinter.CTkLabel(self.frame_right, text=item["cost"])
        cost_label.grid(row=len(self.added_items), column=1, pady=3, padx=2)
        self.cost_labels.append(cost_label)

        self.total_cost = self.total_cost + item["cost"]
        self.total_var.set(str(self.total_cost))

        count = int(self.all_counts_vars[item_no].get())
        self.all_counts_vars[item_no].set(str(count-1))

    def remove_item(self):
        (item, item_no) = self.added_items.pop()
        self.added_labels[-1].after(100, self.added_labels[-1].destroy)
        self.added_labels.pop()
        self.cost_labels[-1].after(100, self.cost_labels[-1].destroy)
        self.cost_labels.pop()
        self.total_cost = self.total_cost - item["cost"]
        self.total_var.set(str(self.total_cost))
        count = int(self.all_counts_vars[item_no].get())
        self.all_counts_vars[item_no].set(str(count+1))

    def clear_items(self):
        for i in range(len(self.added_labels)):
            self.added_labels[i].after(50, self.added_labels[i].destroy)
            self.cost_labels[i].after(50, self.cost_labels[i].destroy)
        self.added_items = []
        self.added_labels = []
        self.cost_labels = []
        self.total_var.set(str(0))
        self.total_cost = 0
        for i in range(len(self.all_items["count"])):
            self.all_counts_vars[i].set(self.all_items["count"][i])

    def sell_items(self):
        for i in range(len(self.all_items["count"])):
            self.all_items.loc[i, 'count'] = int(self.all_counts_vars[i].get())
        self.all_items.to_csv('./test.csv', index=False)
        self.clear_items()

if __name__ == "__main__":
    app = App()
    app.mainloop()