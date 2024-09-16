import customtkinter as ctk

class Root(ctk.CTk):
	def __init__(self, debug=False):
		super().__init__()
		
		ctk.set_appearance_mode("white")
		self.config(cursor="none")

		#self.bind("<Escape>", self.exit)

		self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0")
		self.attributes('-topmost', True)
		if not debug:
			self.overrideredirect(True)
	    
		self.grid_rowconfigure(0, weight=1)
		self.grid_columnconfigure(0, weight=1)

	def exit(self, event):
		self.overrideredirect(False)
		self.destroy()