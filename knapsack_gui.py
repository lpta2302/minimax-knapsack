from concurrent.futures import ThreadPoolExecutor
from random import randint
import threading
from turtle import width
from typing import List
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView

from components.background import Background
from components.custom_boxlayout import CustomBoxLayout
from components.hover_button import HoverButton
from item import Item
from knapsack_solver import KnapsackSolver, Problem


class KnapsackGUI(App):
    def build(self):
        Window.maximize()
        self.items: List[Item] = []
        self.selected_items = []
        self.capacity = 0
        # Root layout
        self.root = Background(orientation="horizontal", size_hint=(1,1))
        self.container = FloatLayout()
        self.root.add_widget(self.container)
        
        self.setup_side_layout()
        self.setup_mid_layout()
        return self.root
    
    def setup_side_layout(self):
        # Side layout container
        self.side_layout = CustomBoxLayout(orientation="vertical", padding=10, pos=(0,0), size_hint=(None, 1), width=320)
        
        # Header
        header = Label(text="Knapsack Solver", font_size=30, size_hint_y=None, height=60, halign="center")
        self.side_layout.add_widget(header)
        
        # Capacity Input
        capacity_label = Label(text="Capacity:", font_size=20, size_hint_y=None, height=40, halign="left")
        self.side_layout.add_widget(capacity_label)

        # Capacity input field
        self.budget_input_side = TextInput(multiline=False, font_size=20, size_hint_y=None, height=40)
        self.side_layout.add_widget(self.budget_input_side)

        # Solve Button
        container = BoxLayout(size_hint_y=None, height=50)
        solve_button = HoverButton(text="Value", size_hint_y=None, height=50, font_size=20)
        solve_button.bind(on_press=self.solve_knapsack)
        container.add_widget(solve_button)
        solve_button = HoverButton(text="Value CON", size_hint_y=None, height=50, font_size=20)
        solve_button.bind(on_press=lambda instance:self.solve_knapsack(instance, Problem.OPTIMIZE_VALUE_BOTH))
        container.add_widget(solve_button)
        self.side_layout.add_widget(container)
        
        # Status header
        status_header = CustomBoxLayout(orientation="horizontal", size_hint=(1,None), height=50)
        status_header.add_widget(Label(text=f"Value", font_size=20, halign="center", size_hint=(1, 1)))
        status_header.add_widget(Label(text=f"Weight", font_size=20, halign="center", size_hint=(1, 1)))
        self.side_layout.add_widget(status_header)
        # Status content
        status = CustomBoxLayout(orientation="horizontal", size_hint=(1,None), height=50)
        self.status_value = Label(text=f"0", font_size=20, halign="center", size_hint=(1, 1))
        self.status_weight = Label(text=f"0", font_size=20, halign="center", size_hint=(1, 1))
        status.add_widget(self.status_value)
        status.add_widget(self.status_weight)
        self.side_layout.add_widget(status)

        # Selected Items Header
        selected_items_header = Label(text="Selected Items", font_size=20, size_hint_y=None, height=40, halign="center")
        self.side_layout.add_widget(selected_items_header)
        
        table_header = BoxLayout(orientation="horizontal", size_hint=(1,None), height=50)
        table_header.add_widget(Label(size_hint=(None,1), width=60, text=f"No", font_size=20, halign="center"))
        table_header.add_widget(Label(text=f"Value", font_size=20, halign="center", size_hint=(1, 1)))
        table_header.add_widget(Label(text=f"Weight", font_size=20, halign="center", size_hint=(1, 1)))
        self.side_layout.add_widget(table_header)

        # List of Selected Items
        self.selected_items_layout = BoxLayout(orientation="vertical", size_hint_y=None, height=400, padding=10, spacing=5)
        self.selected_items_layout.bind(minimum_height=self.selected_items_layout.setter('height'))  # Important for scroll to work

        # Scrollable list of selected items
        self.selected_items_view = ScrollView(size_hint=(1, None), height=400, do_scroll_y=True)
        self.selected_items_view.add_widget(self.selected_items_layout)
        self.side_layout.add_widget(self.selected_items_view)
        self.side_layout.add_widget(BoxLayout(size_hint=(1,1)))
        
        # Add the side layout to the container
        self.container.add_widget(self.side_layout)

    def solve_knapsack(self, instance, problem = Problem.OPTIMIZE_VALUE):
        # Get the Capacity from the side layout
        try:
            budget = int(self.budget_input_side.text)
            self.capacity = budget  # Store Capacity
        except ValueError:
            self.selected_items_layout.clear_widgets()  # Clear the list if there's an error in input
            self.selected_items_layout.add_widget(Label(text="Error: Invalid Capacity input."))
            return
        
        # Create an instance of KnapsackSolver with the items and Capacity
        solver = KnapsackSolver(self.items, self.capacity, problem)
        _, self.selected_items = solver.solve()
        
        # Update the selected items list UI
        self.update_selected_items(problem)
        self.update_status(problem)
        self.update_item_list()

    def update_selected_box(self, box: BoxLayout):
        for index,item in enumerate(self.selected_items):
            # Add item details as Labels
            color = (0.9, 0.9, 0.9, 0.5) if index % 2 == 0 else (0.4, 0.6, 1, 0.5)
            item_layout = CustomBoxLayout(orientation="horizontal", size_hint=(1,None), height=40, color=color)
            item_layout.add_widget(Label(size_hint=(None,1), width=60, text=f"{index+1}", font_size=20, halign="center"))
            item_layout.add_widget(Label(text=f"{item.value}", font_size=20, halign="center"))
            item_layout.add_widget(Label(text=f"{item.weight}", font_size=20, halign="center"))

            box.add_widget(item_layout)

    def update_selected_items(self, problem):
        
        # Clear current selected items
        if problem == Problem.OPTIMIZE_VALUE or problem == Problem.OPTIMIZE_VALUE_BOTH:
            self.selected_items_layout.clear_widgets()
        
        if not self.selected_items:
            self.selected_items_layout.add_widget(Label(text="No items selected."))
        else:
            self.update_selected_box(self.selected_items_layout)
            
            
    def update_status(self, problem):
        total_value = sum(item.value for item in self.selected_items)
        total_weight = sum(item.weight for item in self.selected_items)
        self.status_value.text = f"{total_value}"
        self.status_weight.text = f"{total_weight}"
    # mid layout
    def setup_mid_layout(self):
        self.mid_layout = FloatLayout()
        self.mid_container = CustomBoxLayout(orientation="vertical",size_hint=(None, None),size=(800,800), padding=20, spacing=20, pos_hint={'center_x': 0.5, 'center_y': 0.5})
        
        # Input section
        input_section = GridLayout(cols=3, size_hint=(None, 1),
                                   height=50*5, width=200,
                                   row_default_height=50,
                                    row_force_default=True)

        # Adding Label and TextInput for Item Value
        item_value_label = Label(text="Item Value:", halign="left", valign="middle", font_size=20)
        input_section.add_widget(item_value_label)

        self.item_value_input = TextInput(multiline=False, font_size=20, padding_y=(15, 15))
        input_section.add_widget(self.item_value_input)
        
        input_section.add_widget(BoxLayout())

        # Adding Label and TextInput for Item Weight
        item_weight_label = Label(text="Item Weight:", halign="left", valign="middle", font_size=20)
        input_section.add_widget(item_weight_label)

        self.item_weight_input = TextInput(multiline=False, font_size=20, padding_y=(15, 15))
        input_section.add_widget(self.item_weight_input)
        
        input_section.add_widget(BoxLayout())

        # Reset Items Button
        padding_layout = BoxLayout(size_hint=(None, 1), width=220, padding=(10,5,10,5))
        reset_items_button = HoverButton(text="Reset Items", size_hint=(1,1), font_size=20)
        reset_items_button.bind(on_press=self.reset_items)
        padding_layout.add_widget(reset_items_button)
        input_section.add_widget(padding_layout)
        
        # Random An Item Button
        padding_layout = BoxLayout(size_hint=(None, 1), width=220, padding=(10,5,10,5))
        add_item_button = HoverButton(text="Random Item", size_hint=(1,1), font_size=20)
        add_item_button.bind(on_press=self.random_item)
        padding_layout.add_widget(add_item_button)
        input_section.add_widget(padding_layout)
        
        # Add An Item Button
        padding_layout = BoxLayout(size_hint=(None, 1), width=220, padding=(10,5,10,5))
        add_item_button = HoverButton(text="Add Item", size_hint=(1,1), font_size=20)
        add_item_button.bind(on_press=self.add_item)
        padding_layout.add_widget(add_item_button)
        input_section.add_widget(padding_layout)


        # Added items
        # Adding the section where we will display added items
        # header       
        item_layout = CustomBoxLayout(orientation="horizontal", size_hint=(1,None), height=50)
        item_layout.add_widget(Label(size_hint=(None,1), width=60, text=f"No", font_size=20, halign="center"))
        item_layout.add_widget(Label(text=f"Value", font_size=20, halign="center"))
        item_layout.add_widget(Label(text=f"Weight", font_size=20, halign="center"))
        item_layout.add_widget(Label())
        
        self.items_view = ScrollView(size_hint=(1, None), height=500, do_scroll_y=True)
        self.added_items_layout = BoxLayout(orientation="vertical", size_hint_y=None, spacing=5)
        self.added_items_layout.bind(minimum_height=self.added_items_layout.setter('height'))  # This is important for scroll to work
        self.items_view.add_widget(self.added_items_layout)
        
        self.mid_container.add_widget(input_section)
        self.mid_container.add_widget(item_layout)
        self.mid_container.add_widget(self.items_view)
        self.mid_layout.add_widget(self.mid_container)
        self.container.add_widget(self.mid_layout)

    def add_item(self, instance):
        # Add a new item based on the inputs
        try:
            value = int(self.item_value_input.text)
            weight = int(self.item_weight_input.text)
            item = Item(value, weight)
            self.items.append(item)
            self.update_item_list()
            self.item_value_input.text=""
            self.item_weight_input.text=""
        except ValueError:
            self.selected_items_label.text = "Error: Invalid input for item."
    def random_item(self, instance):
        # Add a new item based on the inputs
        value = randint(1,20)
        weight = randint(1,20)
        item = Item(value, weight)
        self.items.append(item)
        self.update_item_list()
    def reset_items(self, instance):
        # Reset the list of items
        self.items = []
        self.update_item_list()
    def update_item_list(self):
        selected_items = self.selected_items.copy()
        # Update the list of items in the BoxLayout
        self.added_items_layout.clear_widgets()  # Clear the existing items
        
        for index, item in enumerate(self.items):
            # Find the index of the matching selected item
            selected_index = next(
                (i for i, selected in enumerate(selected_items)
                if item.value == selected.value and item.weight == selected.weight),
                None
            )
            # If a match is found, pop it from selected_items
            if selected_index is not None:
                selected_items.pop(selected_index)
            
            # Add item details as Labels
            color = (0.9, 0.3, 0.4, 0.5) if selected_index is not None else (0.9, 0.9, 0.9, 0.5) if index % 2 == 0 else (0.4, 0.6, 1, 0.5)
            item_layout = CustomBoxLayout(orientation="horizontal", size_hint=(1,None), height=40, color=color)
            item_layout.add_widget(Label(size_hint=(None, 1), width=30, text=f"{index+1}", font_size=20, halign="center"))
            item_layout.add_widget(Label(text=f"{item.value}", font_size=20, halign="center"))
            item_layout.add_widget(Label(text=f"{item.weight}", font_size=20, halign="center"))

            # Add delete button for each item
            delete_button = HoverButton(text="Delete", size_hint_y=None, height=40)
            delete_button.bind(on_press=lambda instance, idx=index: self.delete_item(idx))  # Pass the index of the item
            item_layout.add_widget(delete_button)

            self.added_items_layout.add_widget(item_layout)

    def delete_item(self, index):
        # Remove the item at the specified index
        del self.items[index]
        self.update_item_list()
