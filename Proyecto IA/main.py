# main.py
import tkinter as tk
from tkinter import ttk, messagebox
from simulacion_economica import SimulacionEconomica
import sys
import traceback

def main():
    def handle_exception(exc_type, exc_value, exc_traceback):
        error_msg = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        try:
            messagebox.showerror('Error Fatal', 
                f'Ha ocurrido un error inesperado:\n\n{error_msg}')
        except:
            print(f'Error Fatal:\n{error_msg}', file=sys.stderr)
        sys.exit(1)

    sys.excepthook = handle_exception

    try:
        root = tk.Tk()
        root.title("Simulador de Política Monetaria")
        
        style = ttk.Style()
        style.theme_use('clam')
        
        app = SimulacionEconomica(root)
        
        def on_closing():
            if app.simulacion_activa:
                if messagebox.askokcancel("Confirmar salida", 
                    "Hay una simulación en curso. ¿Desea cerrar la aplicación?"):
                    app.pausar_simulacion()
                    root.destroy()
            else:
                root.destroy()
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
        
        root.update_idletasks()
        width = root.winfo_width()
        height = root.winfo_height()
        x = (root.winfo_screenwidth() // 2) - (width // 2)
        y = (root.winfo_screenheight() // 2) - (height // 2)
        root.geometry(f'{width}x{height}+{x}+{y}')
        
        root.mainloop()
        
    except Exception as e:
        handle_exception(type(e), e, e.__traceback__)

if __name__ == "__main__":
    main()
