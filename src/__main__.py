import sys
import os
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QPushButton, QGridLayout, QLabel, QTextEdit, QWidget, QFileDialog
from scanner import Scanner
from parser import Parser
import networkx as nx
from graphviz import Digraph

current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the Graphviz bin path relative to the parent directory
graphviz_path = os.path.join(os.path.dirname(current_dir), "Graphviz-12.2.1-win64", "bin")

# Add Graphviz to PATH for the current process
os.environ["PATH"] += os.pathsep + graphviz_path

# class TINYParserWidget(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.initUI()
class TINYParserWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.nonterminals = [
            "program", "stmt-sequence", "statement", "repeat-stmt",
            "assign-stmt", "read-stmt", "write-stmt", "exp", "comparison-op",
            "simple-exp", "addop", "term", "mulop", "factor"
        ]
        self.initUI()

    def initUI(self):
        # Widgets
        lbl = QLabel('Enter TINY Language Code', self)
        self.input_code = QTextEdit()
        self.add_initial_code()

        # Buttons
        submit_button = QPushButton('Parse')
        upload_button = QPushButton('Upload Code File')  # New upload button

        # Connect buttons to actions
        submit_button.clicked.connect(self.submitted)
        upload_button.clicked.connect(self.upload_file)  # Connect upload action

        # Layout
        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(lbl, 1, 0)
        grid.addWidget(self.input_code, 1, 1, 1, 2)
        grid.addWidget(upload_button, 2, 1)  # Add upload button
        grid.addWidget(submit_button, 2, 2)  # Add parse button
        self.setLayout(grid)

        # Window Settings
        self.setGeometry(40, 40, 600, 900)
        self.setWindowTitle('TINY Parser')
        self.show()

    def add_initial_code(self):
        self.input_code.append("read x;")
        self.input_code.append("if 0<x then")
        self.input_code.append("    fact:=1;")
        self.input_code.append("    repeat")
        self.input_code.append("        fact:=fact*x;")
        self.input_code.append("        x:=x-1")
        self.input_code.append("    until x=0;")
        self.input_code.append("    write fact")
        self.input_code.append("end")

    def draw_with_graphviz(self, nodes_list, edges_list, same_rank_nodes):
        dot = Digraph(format="png")
        dot.attr(rankdir="TB", size="10,8.5")
        
        # Add nodes
        for node_number, node_data in nodes_list.items():
            label = f"{node_data[0]}\\n{node_data[1]}"
            dot.node(str(node_number), label=label, shape=node_data[2])

        # Add edges
        for edge in edges_list:
            dot.edge(str(edge[0]), str(edge[1]))

        # Handle same rank nodes
        for rank_group in same_rank_nodes:
            with dot.subgraph() as sub:
                sub.attr(rank="same")
                for node in rank_group:
                    sub.node(str(node))
        
        # Render graph
        output_path = os.path.join(os.getcwd(), "output_graph")
        dot.render(output_path, view=True)
        print(f"Graph saved to {output_path}.png")


    def upload_file(self):
        """Open a file dialog to upload a .txt file."""
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Upload Code File", "", "Text Files (*.txt);;All Files (*)", options=options)
        if file_name:
            try:
                with open(file_name, 'r') as file:
                    file_content = file.read()
                    self.input_code.setText(file_content)  # Set content to QTextEdit
                print(f"File '{file_name}' loaded successfully.")
            except Exception as e:
                print(f"Error reading file: {e}")

    def submitted(self):
        scanned_code = Scanner()
        scanned_code.set_tiny_code(self.input_code.toPlainText()) 
       

        scanned_code.scan()
        # print("Tokens List:", scanned_code.tokens_list)
        # print("Code List:", scanned_code.code_list)
        scanned_code.createOutputFile('ScannerToken.txt')

        parse_code = Parser()
        parse_code.set_tokens_list_and_code_list(
            scanned_code.tokens_list, scanned_code.code_list)

        # print(parse_code.code_list)
        # print(parse_code.tokens_list)
        
        parse_code.run()
        nodes_list = parse_code.nodes_table
        edges_list = parse_code.edges_table
        same_rank_nodes = parse_code.same_rank_nodes

        # Draw using Graphviz
        self.draw_with_graphviz(nodes_list, edges_list, same_rank_nodes)
        parse_code.clear_tables()

# Run the application
app = QApplication(sys.argv)
w = TINYParserWidget()
sys.exit(app.exec_())
