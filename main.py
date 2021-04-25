import threading
import time
import tkinter as tk
import tkinter.ttk as ttk
import log
import collections
from functools import partial
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
from ttkthemes import ThemedTk

class main():
    cards = []
    playerCards = []
    dealerCards = []
    #variableClass = []

    def __init__(self):
        self.interface_start()
        self.logging_info()
        threading.Thread(target = self.root.mainloop())
    
    def logging_info(self):
        log.logQueue("Program Online")
        self.root.after(100,self.queue_read(0))
    
    def queue_read(self, interaction):
        stuff = log.logQueue()
        try:
            message = stuff.pop(0)
            label_log = ttk.Label(self.viewPort, style = 'Table.TLabel', text=" - ".join([time.strftime("%H:%M", time.localtime()),message]))
            label_log.grid(row = interaction, column = 0, padx = 0, pady = 0, sticky = 'nsw')
            interaction = interaction + 1
        except:
            pass
        self.root.after(100, self.queue_read, interaction)
        
    def interface_start(self):
        #Initiate Style   
        self.root = ThemedTk(theme="scidgrey")
        self.s = ttk.Style()
        self.s.configure('TButton', font=('Segoe UI', 12))
        self.s.configure('TLabel', font=('Segoe UI', 12))
        self.s.configure('TTitle', font=('Segoe UI', 25) )
        self.s.configure('Title.TLabel', font=('Segoe UI', 25))
        self.s.configure('Table.TLabel', font=('Segoe UI', 10),background='#ffffff',foreground='black')
        self.s.configure('TFrame.TFrame',background='#ffffff')
        self.s.configure('Bold.TLabel', font=('Segoe UI', 10,'bold'))
        self.s.configure('White.TLabel', font=('Segoe UI', 12) )
        self.s.configure('WhiteBold.TLabel', font=('Segoe UI', 12,'bold'))
        self.s.configure('TEntry', font=('Segoe UI', 13))

        #root
        self.root.title('BlackJack Counter')
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.rootTable = ttk.Frame(self.root)
        self.rootTable.grid(row=0,column=0,sticky='nsew')
        self.rootTable.columnconfigure(1, weight=8)
        self.rootTable.columnconfigure(0, weight=1)
        self.rootTable.rowconfigure(1, weight=1)

        #lbl_title
        self.titleLabel = ttk.Label(
            self.rootTable, style="Title.TLabel", text="Blackjack Counter")
        self.titleLabel.grid(row=0, column=0, sticky='nsew',
                            pady=(10, 0), padx=(10, 0))    

        self.newGameButt = ttk.Button(
            master=self.rootTable, style="TButton", text="New Game", command=lambda: self.new_game())
        self.newGameButt.grid(
            row=0, column=1, padx=10, pady=(10, 0), sticky='new') 
        

        #table
        self.mainTable = ttk.Frame(master=self.rootTable)
        self.mainTable.grid(row=1, column=1, sticky="nsew", padx=(5, 10), pady=(0,10))
        self.mainTable.columnconfigure(0, weight=1)
        self.mainTable.rowconfigure(0, weight=1)

        #logTable4
        self.logTable = ttk.Frame(master=self.mainTable, borderwidth=1, relief=tk.GROOVE,style='TFrame.TFrame')
        self.logTable.grid(row=0, column=2, sticky='nsew', padx=5, pady=5)
        self.logTable.columnconfigure(0, weight=1)
        self.logTable.rowconfigure(0, weight=1)
        
        #barScroll
        self.barScroll = ttk.Scrollbar(
            self.logTable, orient="vertical")
        
        #cnv_contracts
        self.logCanvas = tk.Canvas(self.logTable, bg='#ffffff')
        self.logCanvas.grid(row=0, column=0, sticky='nsew')
        self.logCanvas.columnconfigure(0, weight=1)
        self.logCanvas.config(yscrollcommand=self.barScroll.set)
        self.barScroll.grid(row=0, column=1, sticky='ns')
        self.barScroll.config(command=self.logCanvas.yview)

        #view_port
        self.viewPort = ttk.Frame(self.logCanvas,style='TFrame.TFrame')
        self.viewPort.columnconfigure(0, weight=1)

        self.logCanvas.create_window(0, 0, window=self.viewPort, anchor="nw",
                                         tags='self.viewPort')

        #Scrollbar init
        self.viewPort.bind("<Configure>", self.on_frame_configure)
        self.logCanvas.bind('<Configure>', self.frame_width)

        #sidemenutable
        self.sideMenuTable = ttk.Frame(master=self.rootTable)
        self.sideMenuTable.grid(row=1, column=0, sticky="nsew",
                          padx=(10, 5), pady=(10,0))
        self.sideMenuTable.columnconfigure(0, weight=1)

        contHelper = 1
        listLabel = []
        listBox = []
        for listPos in range(0,4):
            self.cardLabel = ttk.Label(
                master=self.sideMenuTable, style="TLabel", text="Card" + " " + str(listPos+1))
            self.cardLabel.grid(row=contHelper, column=0, sticky='nw', padx=5, pady=(0,0))

            self.cardList = ttk.Entry(
                master=self.sideMenuTable, style="TEntry")
            self.cardList.grid(row=contHelper + 1, column=0, sticky='nw', padx=5, pady=(0,2))
            listLabel.append(self.cardLabel)
            listBox.append(self.cardList)
            contHelper = contHelper + 2
            
        contHelper = 1  
        listPos = 1
        listLabelDealer = []
        listBoxDealer = [] 
        for listPos in range(0,4):
            self.cardLabelDealer = ttk.Label(
                master=self.sideMenuTable, style="TLabel", text="Dealer Card" + " " + str(listPos+1))
            self.cardLabelDealer.grid(row=contHelper, column=1, sticky='nw', padx=5, pady=(0,0))

            self.cardListDealer = ttk.Entry(
                master=self.sideMenuTable, style="TEntry")
            self.cardListDealer.grid(row=contHelper + 1, column=1, sticky='nw', padx=5, pady=(0,2))
            listLabelDealer.append(self.cardLabelDealer)
            listBoxDealer.append(self.cardListDealer)
            contHelper = contHelper + 2
            
        #buttons
        self.addcardButt = ttk.Button(
            master=self.sideMenuTable, style="TButton", text="Analyse", command=partial(self.new_card, listBox, listBoxDealer))
        self.addcardButt.grid(
            row=15, column=0, padx=5, pady=(1, 10), sticky='new')

        self.newhandButt = ttk.Button(
            master=self.sideMenuTable, style="TButton", text="New Hand", command=partial(self.new_hand, listBox, listBoxDealer))
        self.newhandButt.grid(
            row=16, column=0, padx=5, pady=(1, 10), sticky='new')
    
    def analyse_play(self):
        import calculator_bj as bj
        aCount = 0
        valuePlayer = 0
        valueDealer = 0
        remarkPlayer = []
        remarkDealer = []
        for eachCard in main.playerCards:
            if eachCard == "k" or eachCard == "q" or eachCard == "j":
                eachCard = 10
            if not eachCard == "a":
                valuePlayer = valuePlayer + int(eachCard)
            else:
                aCount = aCount + 1
                remarkPlayer.append(aCount)
        aCount = 0
        for eachCard in main.dealerCards:
            if eachCard == "k" or eachCard == "q" or eachCard == "j":
                eachCard = 10
            if not eachCard == "a":
                valueDealer = valueDealer + int(eachCard)
            else:
                aCount = aCount + 1
                remarkDealer.append(aCount)
        decisionMaker = bj.decision(valuePlayer, valueDealer, remarkPlayer)
        log.logQueue(decisionMaker)
    
    def new_card(self, playerC, dealerC):
        checkQuant = 0
        for eachVal in main.playerCards:
            if eachVal != "":
                checkQuant = checkQuant + 1
        checkList = checkQuant - 1
        for eachBox in playerC:
            if checkList < playerC.index(eachBox):
                card = eachBox.get()
                if not card == "":
                    main.playerCards.append(card)
        checkQuant = 0
        for eachVal in main.dealerCards:
            if eachVal != "":
                checkQuant = checkQuant + 1
        checkList = checkQuant - 1
        for eachBox in dealerC:
            if checkList < dealerC.index(eachBox):
                card = eachBox.get()
                if not card == "":
                    main.dealerCards.append(card)
        self.analyse_play()
        
    def new_hand(self, playerC, dealerC):
        for eachBox in playerC:
            eachBox.delete(0, 'end')
        for eachBox in dealerC:
            eachBox.delete(0, 'end')
        main.playerCards = []
        main.dealerCards = []
        
    def new_game(self):
        log.logQueue("Feature not implemented yet")

    def on_frame_configure(self, event):
        self.logCanvas.configure(
            scrollregion=self.logCanvas.bbox('all'))

    def frame_width(self, event):
        canvasWidth = event.width
        self.logCanvas.itemconfig('self._viewPort', width=canvasWidth)

if __name__ == "__main__":
    main()