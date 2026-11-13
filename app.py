#!/usr/bin/env python3
"""Torelkiva Desktop 2.1 — lokale Tkinter-app, zonder netwerkdiensten.

Niet geschikt voor iOS; Windows en Linux met tkinter. Geen wachtzinopslag.
"""
from __future__ import annotations
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path
from vertaler import to_nederlands, to_torelkiva, UnsupportedSentenceError
from taal import vind, woorden
from schrift import sentence_svg

BACKGROUND = '#f5f7fb'
TEXT = '#17243b'
ACCENT = '#2755b6'

class TorelkivaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Torelkiva 2.2 — Marco Beenen × ChatGPT')
        self.geometry('890x680')
        self.minsize(710, 540)
        self.configure(bg=BACKGROUND)
        style = ttk.Style(self)
        if 'clam' in style.theme_names(): style.theme_use('clam')
        style.configure('TFrame', background=BACKGROUND)
        style.configure('TLabel', background=BACKGROUND, foreground=TEXT, font=('Arial', 10))
        style.configure('Head.TLabel', background=BACKGROUND, foreground=TEXT, font=('Arial', 17, 'bold'))
        style.configure('TNotebook', background=BACKGROUND)
        style.configure('TButton', padding=(12, 7))

        header = ttk.Frame(self, padding=(18, 14))
        header.pack(fill='x')
        ttk.Label(header, text='TORELKIVA 2.2', style='Head.TLabel').pack(anchor='w')
        ttk.Label(header, text='Taal, eigen schrift en lokale versleuteling • begonnen op 12 november 2026').pack(anchor='w')
        self.tabs = ttk.Notebook(self)
        self.tabs.pack(fill='both', expand=True, padx=18, pady=(4, 10))
        self.build_translate()
        self.build_dictionary()
        self.build_script()
        self.build_crypto()
        ttk.Label(self, text='Ontwikkeld op initiatief van Marco Beenen met ChatGPT (OpenAI) • geen officiële OpenAI-goedkeuring', font=('Arial', 9)).pack(pady=(0, 12))

    @staticmethod
    def textbox(parent, rows=8, readonly=False):
        wrapper = ttk.Frame(parent)
        widget = tk.Text(wrapper, height=rows, wrap='word', undo=not readonly, font=('Consolas', 11), relief='solid', borderwidth=1)
        scroll = ttk.Scrollbar(wrapper, orient='vertical', command=widget.yview)
        widget.configure(yscrollcommand=scroll.set)
        widget.pack(side='left', fill='both', expand=True)
        scroll.pack(side='right', fill='y')
        if readonly: widget.configure(state='disabled')
        return wrapper, widget

    @staticmethod
    def set_text(widget, text):
        widget.configure(state='normal')
        widget.delete('1.0', tk.END)
        widget.insert('1.0', text)
        widget.configure(state='disabled')

    @staticmethod
    def get_text(widget):
        return widget.get('1.0', 'end-1c')

    def clipboard_text(self, text):
        self.clipboard_clear()
        self.clipboard_append(text)
        self.update()

    def build_translate(self):
        tab = ttk.Frame(self.tabs, padding=16)
        self.tabs.add(tab, text='Vertalen')
        ttk.Label(tab, text='Gecontroleerde vertaler — één eenvoudige zin per keer').pack(anchor='w')
        bar = ttk.Frame(tab)
        bar.pack(fill='x', pady=8)
        self.direction = tk.StringVar(value='nl')
        ttk.Radiobutton(bar, text='Nederlands → Torelkiva', value='nl', variable=self.direction).pack(side='left', padx=(0, 16))
        ttk.Radiobutton(bar, text='Torelkiva → Nederlands', value='tk', variable=self.direction).pack(side='left')
        ttk.Label(tab, text='Invoer').pack(anchor='w')
        fr, self.translate_input = self.textbox(tab, 4)
        fr.pack(fill='both', expand=True, pady=(5, 10))
        self.translate_input.insert('1.0', 'Ik begrijp jou niet.')
        buttons = ttk.Frame(tab)
        buttons.pack(fill='x')
        ttk.Button(buttons, text='Vertaal', command=self.do_translate).pack(side='left')
        ttk.Button(buttons, text='Kopieer resultaat', command=lambda: self.clipboard_text(self.get_text(self.translate_output))).pack(side='left', padx=7)
        ttk.Label(tab, text='Resultaat').pack(anchor='w', pady=(12, 2))
        fr, self.translate_output = self.textbox(tab, 4, readonly=True)
        fr.pack(fill='both', expand=True)
        ttk.Label(tab, text='Let op: dit is nog geen algemene Nederlandse vertaler. Onbekende zinnen worden geweigerd.').pack(anchor='w', pady=8)

    def do_translate(self):
        try:
            text = self.get_text(self.translate_input)
            result = to_torelkiva(text) if self.direction.get() == 'nl' else to_nederlands(text)
            self.set_text(self.translate_output, result)
        except (UnsupportedSentenceError, ValueError) as exc:
            self.set_text(self.translate_output, 'Niet ondersteund: ' + str(exc))

    def build_dictionary(self):
        tab = ttk.Frame(self.tabs, padding=16)
        self.tabs.add(tab, text='Woordenboek')
        ttk.Label(tab, text='Zoek een Nederlands of Torelkiva-woord').pack(anchor='w')
        bar = ttk.Frame(tab); bar.pack(fill='x', pady=10)
        self.query = ttk.Entry(bar)
        self.query.pack(side='left', fill='x', expand=True)
        self.query.bind('<Return>', lambda _e: self.do_lookup())
        ttk.Button(bar, text='Zoek', command=self.do_lookup).pack(side='left', padx=8)
        ttk.Button(bar, text='Alle woorden', command=lambda: self.show_words(woorden())).pack(side='left')
        self.tree = ttk.Treeview(tab, columns=('torel','nl','type'), show='headings', height=15)
        for name,label,width in [('torel','Torelkiva',160),('nl','Nederlands',320),('type','Woordsoort',190)]:
            self.tree.heading(name, text=label); self.tree.column(name, width=width, minwidth=90)
        self.tree.pack(fill='both', expand=True)
        self.show_words(woorden())

    def show_words(self, rows):
        self.tree.delete(*self.tree.get_children())
        for row in rows:
            self.tree.insert('', tk.END, values=(row['torelkiva'],row['nederlands'],row['soort']))

    def do_lookup(self):
        self.show_words(vind(self.query.get()) if self.query.get().strip() else woorden())

    def build_script(self):
        tab = ttk.Frame(self.tabs, padding=16)
        self.tabs.add(tab, text='Torel-schrift')
        ttk.Label(tab, text='Teken de tekst als eigen letterschrift (dit versleutelt niets)').pack(anchor='w')
        frame,self.script_input=self.textbox(tab, 10)
        frame.pack(fill='both',expand=True,pady=12)
        self.script_input.insert('1.0','Mi viroem sila.')
        ttk.Button(tab, text='Opslaan als SVG',command=self.save_script).pack(anchor='w')
        ttk.Label(tab,text='SVG is te openen in een browser. Maximaal 2.000 tekens.').pack(anchor='w',pady=10)

    def save_script(self):
        try:
            svg=sentence_svg(self.get_text(self.script_input))
            path=filedialog.asksaveasfilename(title='Sla Torel-schrift op',defaultextension='.svg',filetypes=[('SVG-afbeelding','*.svg')])
            if path:
                target=Path(path)
                if target.exists():
                    if not messagebox.askyesno('Bestaand bestand','Wil je dit bestaande SVG-bestand overschrijven?'):
                        return
                target.write_text(svg,encoding='utf-8')
                messagebox.showinfo('Klaar',f'Schrift opgeslagen als:\n{target}')
        except (ValueError, OSError) as exc:
            messagebox.showerror('Kan schrift niet opslaan',str(exc))

    def build_crypto(self):
        tab=ttk.Frame(self.tabs,padding=16)
        self.tabs.add(tab,text='Versleutelen')
        ttk.Label(tab,text='AES-256-GCM • scrypt • lokaal • TK1-compatibel').pack(anchor='w')
        ttk.Label(tab,text='Tekst of versleutelde TK1-code').pack(anchor='w',pady=(12,4))
        fr,self.crypto_input=self.textbox(tab,5)
        fr.pack(fill='both',expand=True)
        passbar=ttk.Frame(tab);passbar.pack(fill='x',pady=12)
        ttk.Label(passbar,text='Geheime wachtzin:').pack(side='left',padx=(0,8))
        self.password=tk.StringVar()
        self.password_entry=ttk.Entry(passbar,textvariable=self.password,show='•')
        self.password_entry.pack(side='left',fill='x',expand=True)
        ttk.Button(passbar,text='Wissen',command=lambda:self.password.set('')).pack(side='left',padx=8)
        buttons=ttk.Frame(tab);buttons.pack(fill='x')
        ttk.Button(buttons,text='Versleutel',command=lambda:self.do_crypto(True)).pack(side='left')
        ttk.Button(buttons,text='Ontsleutel',command=lambda:self.do_crypto(False)).pack(side='left',padx=8)
        ttk.Button(buttons,text='Kopieer resultaat',command=lambda:self.clipboard_text(self.get_text(self.crypto_output))).pack(side='left')
        fr,self.crypto_output=self.textbox(tab,5,readonly=True)
        fr.pack(fill='both',expand=True,pady=(10,0))
        ttk.Label(tab,text='Gebruik een lange wachtzin. De wachtzin wordt niet opgeslagen. Onthoud hem zelf.').pack(anchor='w',pady=8)

    def do_crypto(self,encrypt):
        pwd=self.password.get()
        # Er gebeurt niets online; wachtzinnen of berichtinhoud worden niet gelogd.
        try:
            from torelkiva import encrypt_text,decrypt_text
            result=encrypt_text(self.get_text(self.crypto_input),pwd) if encrypt else decrypt_text(self.get_text(self.crypto_input),pwd)
            self.set_text(self.crypto_output,result)
        except (ValueError, UnicodeError, ImportError, RuntimeError) as exc:
            messagebox.showerror('Versleuteling mislukt',str(exc))
        finally:
            self.password.set('')

if __name__=='__main__':
    TorelkivaApp().mainloop()
