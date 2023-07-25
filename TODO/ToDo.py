import flet as ft
import shelve

class Task(ft.UserControl):
    def __init__(self, input_text, remove_task, task_index):
        super().__init__()
        self.input = input_text
        self.remove_task = remove_task
        self.task_index = task_index

    def build(self):
        self.task_cb = ft.Checkbox(label=self.input,
                                   expand=True)
        
        self.edit_tf = ft.TextField(value=self.input,
                                   expand=True)
        
        self.task_view = ft.Row(
            visible=True,
            controls=[    
                self.task_cb, 
                ft.IconButton(icon=ft.icons.CREATE_OUTLINED,
                                            on_click=self.edit_clicked),
                ft.IconButton(icon=ft.icons.DELETE_OUTLINE,
                                            on_click=self.remove_clicked)
            ])

        self.edit_view = ft.Row(
            visible=False,
            controls=[
                self.edit_tf,
                ft.IconButton(icon=ft.icons.CHECK, on_click=self.save_clicked)
            ])

        return ft.Column(
            controls=[
                self.task_view, self.edit_view
            ])
    
    def edit_clicked(self, e):
        self.task_view.visible = False
        self.edit_view.visible = True
        self.update()

    def remove_clicked(self, e):
        self.remove_task(self)
        

    def save_clicked(self, e):
        self.task_cb.label = self.edit_tf.value
        self.task_view.visible = True
        self.edit_view.visible = False
        self.update()

class ToDo(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.tasks_db = shelve.open("tasks_db")
        self.tasks = ft.Column()
        self.task_index = 1

    def build(self):
        self.input = ft.TextField(hint_text="Tarefa",
                                  border_color=ft.colors.WHITE70,
                                  expand=True)
        

        view = ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(value="Tarefas",
                        style=ft.TextThemeStyle.HEADLINE_MEDIUM),
                ft.Row(
                    controls=[
                        self.input,
                        ft.FloatingActionButton(icon=ft.icons.ADD,
                                                on_click=self.add_clicked)
                    ]
                ),
                self.tasks
            ]
        )

        return view
    
    def add_clicked(self, e):
        if self.input.value != "":
            self.save_tasks_db(self.task_index, self.input.value)
            print(self.input.value)
            
            task = Task(self.input.value, self.remove_task, self.task_index)
            self.tasks.controls.append(task)
            self.input.value = ""
            
            self.task_index += 1
            self.update()

    def remove_task(self, task):
        self.tasks.controls.remove(task)
        self.remove_task_db(task.task_index)
        self.update()

    # DADOS
    def save_tasks_db(self, task_index, task_text):
        self.tasks_db[str(task_index)] = task_text
        self.tasks_db.sync()

    def remove_task_db(self, task_index):
        del self.tasks_db[str(task_index)]  
        self.tasks_db.sync()

    def restore_tasks(self):
        tasks_dict = self.tasks_db  
        if tasks_dict:  
            for task_index, task_text in tasks_dict.items():
                task = Task(task_text, self.remove_task, int(task_index))  
                self.tasks.controls.append(task)
                self.task_index = max(self.task_index, int(task_index) + 1)


def main(page: ft.Page):
    page.theme_mode = "dark"
    page.window_height = 600
    page.window_width  = 400

    page.title = "Lista de Tarefas"

    todo = ToDo()
    todo.restore_tasks()

    page.add(
        todo
    )
    

ft.app(target=main)