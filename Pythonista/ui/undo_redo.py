import ui

class redo_undo:
    def __init__(self, main,  *args, **kwargs):
        # undo/redo View
        self.history_view = ui.TextView(
            text='HISTORY',
            frame=(25, 275, 600, 400),
            editable=False,
            background_color='#dedede')
        main.add_subview(self.history_view)
        
        # Undo Button
        undo_btn=ui.Button()
        undo_btn.frame=(25, 2, 100, 46)
        undo_btn.background_color='#686868'
        undo_btn.tint_color='#000000'
        undo_btn.title='undo'
        undo_btn.action=self.undo
        main.add_subview(undo_btn)
        
        # Redo Button
        redo_btn=ui.Button()
        redo_btn.frame=(127, 2, 100, 46)
        redo_btn.background_color='#686868'
        redo_btn.tint_color='#000000'
        redo_btn.title='redo'
        redo_btn.action=self.redo
        main.add_subview(redo_btn)
        
        self.history=[]
        self.current_index=len(self.history)
        self.textview=None
        
    def append(self, text):
        if self.current_index < len(self.history):
            self.history=self.history[:self.current_index]
        self.current_index=len(self.history)
        self.history.append(text)   
        self.current_index+=1
        
        self.update_history(self.current_index)
    
    def update_history(self, index):
        self.history_view.text=''
        i=0
        for x in self.history:
            if i == index:
                self.history_view.text+=str(i)+' '+x+' <--'+'\n'
            elif x == self.history[-1] and index == len(self.history):
                self.history_view.text+=str(i)+' '+x+' <--'+'\n'
            else:
                self.history_view.text+=str(i)+' '+x+'\n'
            i+=1
    def redo(self, sender):
        if self.current_index == len(self.history):
            return 
        if self.current_index < len(self.history):
            self.current_index+=1
            self.textview.text = self.history[self.current_index-1]     
        self.update_history(self.current_index-1)
        
    def undo(self, sender):     
        if self.current_index == 0:
            return 
        self.current_index-=1
        self.textview.text = self.history[self.current_index-1] 
        self.update_history(self.current_index-1)
        
    def textview_should_begin_editing(self, textview):
        if textview.text=='INPUT TEXT ..':
            textview.text=''
        self.textview=textview
        return True
        
    def textview_did_change(self, textview):
        self.append(textview.text)
        self.update_history(self.current_index)
        pass

class Main(ui.View):
    def __init__(self, *args, **kwargs):
        # Main Window
        self.width = 650
        self.height = 1000
        self.background_color="#8b8b8b"
        self.update_interval=1
        
        # Text Input Window
        self.tv = ui.TextView(
            text='INPUT TEXT ..',
            frame=(25, 50, 600, 200),
            background_color='#dedede')
        self.add_subview(self.tv)
        self.tv.delegate=redo_undo(self)
        
if __name__ == '__main__':
    Main().present('sheet', hide_title_bar=True)

