import random
import string
import tkinter as tk
from tkinter import ttk
from collections import defaultdict

# Fonctions existantes inchangées
def multiplication_easy():
    a = random.randint(11, 19)
    b = random.randint(2, 9)
    answer = a * b
    return f"{a} × {b} = ?", answer

def multiplication_hard():
    a = random.randint(11, 19)
    b = random.randint(11, 19)
    answer = a * b
    return f"{a} × {b} = ?", answer

def multiplication_table(tables, previous_multiplier=None):
    number = random.choice(tables)
    available_multipliers = list(range(3, 10))
    if previous_multiplier is not None and previous_multiplier in available_multipliers:
        available_multipliers.remove(previous_multiplier)

    b = random.choice(available_multipliers)
    answer = number * b
    return f"{number} × {b} = ?", answer, b

def letter_rank_question():
    letter = random.choice(string.ascii_uppercase)
    answer = ord(letter) - ord('A') + 1
    return f"Quelle est la position de la lettre '{letter}' dans l'alphabet ?", answer

def cube_question():
    n = random.randint(1, 12)
    answer = n ** 3
    return f"Quel est le cube de {n} ?", answer

def square_question():
    n = random.randint(1, 25)
    answer = n ** 2
    return f"Quel est le carré de {n} ?", answer

def multiples_question():
    base = random.randint(11, 19)
    multiples = [base * random.randint(1, 10) for _ in range(4)]
    return f"Les nombres {', '.join(map(str, multiples))} sont des multiples de quel nombre ?", base

class TrainingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Entraînement TAGE MAGE")
        self.root.geometry("950x550")

        # Configuration du style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TFrame', background='#2c3e50')
        self.style.configure('TButton', font=('Arial', 12), background='#3498db', foreground='white')
        self.style.map('TButton', background=[('active', '#2980b9')])
        self.style.configure('TLabel', background='#2c3e50', foreground='white', font=('Arial', 12))
        self.style.configure('Header.TLabel', font=('Arial', 20, 'bold'))
        self.style.configure('Question.TLabel', font=('Arial', 24))

        # Structure de l'interface
        self.main_container = ttk.Frame(root)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.left_frame = ttk.Frame(self.main_container)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.history_frame = ttk.Frame(self.main_container)
        self.history_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        self.title_label = ttk.Label(self.left_frame, text="Entraînement TAGE MAGE", style='Header.TLabel')
        self.title_label.pack(pady=10)

        self.question_frame = ttk.Frame(self.left_frame)
        self.question_frame.pack(fill=tk.X, pady=20)

        self.question_label = ttk.Label(self.question_frame, text="Bienvenue ! Choisissez un mode.",
                                      style='Question.TLabel', anchor='center')
        self.question_label.pack(fill=tk.X)

        self.answer_frame = ttk.Frame(self.left_frame)
        self.answer_frame.pack(pady=10)

        self.answer_label = ttk.Label(self.answer_frame, text="Réponse:")
        self.answer_label.pack(side=tk.LEFT, padx=5)

        self.answer_entry = ttk.Entry(self.answer_frame, font=("Arial", 18), width=15, justify='center')
        self.answer_entry.pack(side=tk.LEFT, padx=5)
        self.answer_entry.bind("<Return>", self.check_answer)

        self.menu_frame = ttk.Frame(self.left_frame)
        self.menu_frame.pack(pady=20)

        self.style.configure('Easy.TButton', background='#2980b9')
        self.style.configure('Hard.TButton', background='#c0392b')
        self.style.configure('Table.TButton', background='#27ae60')
        self.style.configure('Quit.TButton', background='#e74c3c')
        self.style.configure('List.TButton', background='#8e44ad')

        self.easy_button = ttk.Button(self.menu_frame, text="Multiplications faciles",
                                    command=lambda: self.start_training("easy"), style='Easy.TButton')
        self.easy_button.grid(row=0, column=0, padx=10, pady=5)

        self.hard_button = ttk.Button(self.menu_frame, text="Multiplications difficiles",
                                    command=lambda: self.start_training("hard"), style='Hard.TButton')
        self.hard_button.grid(row=0, column=1, padx=10, pady=5)

        self.table_button = ttk.Button(self.menu_frame, text="Tables spécifiques",
                                     command=self.select_table, style='Table.TButton')
        self.table_button.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

        self.table_selection_frame = ttk.Frame(self.left_frame)
        self.table_prompt = ttk.Label(self.table_selection_frame,
                                    text="Entrez les tables à travailler (2-20, séparées par des espaces):")
        self.table_prompt.pack(pady=10)

        self.table_entry = ttk.Entry(self.table_selection_frame, font=("Arial", 18), width=20, justify='center')
        self.table_entry.pack(pady=10)
        self.table_entry.bind("<Return>", self.start_table_training)

        self.quit_button = ttk.Button(self.left_frame, text="Quitter",
                                    command=self.end_session, style='Quit.TButton')  # Modifié pour end_session
        self.quit_button.pack(pady=10)

        self.history_label = ttk.Label(self.history_frame, text="Historique", style='Header.TLabel')
        self.history_label.pack(pady=10)

        self.history_container = ttk.Frame(self.history_frame)
        self.history_container.pack(fill=tk.BOTH, expand=True)

        self.history_scrollbar = ttk.Scrollbar(self.history_container)
        self.history_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.history_list = tk.Listbox(self.history_container, font=("Arial", 14),
                                     bg="#ecf0f1", height=20, width=30)
        self.history_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.history_list.config(yscrollcommand=self.history_scrollbar.set)
        self.history_scrollbar.config(command=self.history_list.yview)

        self.stats_label = ttk.Label(self.history_frame, text="Stats: 0 correct / 0 total")
        self.stats_label.pack(pady=10)

        # Variables d'état
        self.current_question = None
        self.correct_answer = None
        self.current_mode = None
        self.current_tables = []
        self.last_multiplier = None
        self.attempts = 0
        self.correct_count = 0
        self.total_questions = 0
        self.listing_multiples = False
        self.current_multiple_index = 1
        self.question_stats = defaultdict(lambda: {'correct': 0, 'total': 0})  # Suivi des stats par question

    def select_table(self):
        self.menu_frame.pack_forget()
        self.table_selection_frame.pack(pady=20)

    def start_table_training(self, event=None):
        try:
            input_tables = self.table_entry.get().strip().split()
            tables = []
            for t in input_tables:
                num = int(t)
                if 2 <= num <= 20 and num not in tables:
                    tables.append(num)
            if tables:
                self.current_tables = tables
                self.table_selection_frame.pack_forget()
                self.last_multiplier = None
                self.start_training("table")
            else:
                self.table_prompt.config(text="Entrez au moins une table valide (2-20, séparées par des espaces)")
        except ValueError:
            self.table_prompt.config(text="Entrez des nombres valides (2-20, séparées par des espaces)")

    def start_training(self, mode):
        self.menu_frame.pack_forget()
        if hasattr(self, 'table_selection_frame'):
            self.table_selection_frame.pack_forget()
        self.current_mode = mode
        self.new_question(mode)

        if mode == "table":
            self.control_frame = ttk.Frame(self.left_frame)
            self.control_frame.pack(pady=10)

            self.change_button = ttk.Button(self.control_frame, text="Modifier tables (c)",
                                          command=self.modify_tables)
            self.change_button.pack(side=tk.LEFT, padx=5)

            self.list_button = ttk.Button(self.control_frame, text="Lister les multiples (l)",
                                        command=self.start_listing_multiples, style='List.TButton')
            self.list_button.pack(side=tk.LEFT, padx=5)

            self.root.bind('c', lambda event: self.modify_tables())
            self.root.bind('l', lambda event: self.start_listing_multiples())

            self.tables_label = ttk.Label(self.left_frame, text=f"Tables en cours : {', '.join(map(str, self.current_tables))}")
            self.tables_label.pack(pady=5)

    def modify_tables(self):
        self.control_frame.pack_forget()
        if hasattr(self, 'tables_label'):
            self.tables_label.pack_forget()
        self.table_selection_frame.pack(pady=20)
        self.table_entry.delete(0, tk.END)
        self.table_entry.insert(0, " ".join(map(str, self.current_tables)))
        self.table_prompt.config(text="Modifiez les tables (2-20, séparées par des espaces):")
        self.listing_multiples = False

    def start_listing_multiples(self):
        self.listing_multiples = True
        self.current_multiple_index = 1
        self.question_label.config(text=f"Écrivez le premier multiple de {self.current_tables[0]}:")
        self.answer_entry.delete(0, tk.END)
        self.answer_entry.focus()

        if hasattr(self, 'control_frame'):
            self.list_button.pack_forget()
            self.return_button = ttk.Button(self.control_frame, text="Retour aux multiplications (r)",
                                          command=self.return_to_multiplications)
            self.return_button.pack(side=tk.LEFT, padx=5)
            self.root.unbind('l')
            self.root.bind('r', lambda event: self.return_to_multiplications())

    def return_to_multiplications(self):
        self.listing_multiples = False
        self.return_button.pack_forget()
        self.list_button = ttk.Button(self.control_frame, text="Lister les multiples (l)",
                                    command=self.start_listing_multiples, style='List.TButton')
        self.list_button.pack(side=tk.LEFT, padx=5)
        self.root.unbind('r')
        self.root.bind('l', lambda event: self.start_listing_multiples())
        self.new_question("table")

    def new_question(self, mode):
        self.listing_multiples = False
        if mode == "easy":
            questions = [multiplication_easy] * 3 + [random.choice([cube_question, square_question, letter_rank_question, multiples_question])]
        elif mode == "hard":
            questions = [multiplication_hard] * 3 + [random.choice([cube_question, square_question, letter_rank_question, multiples_question])]
        elif mode == "table":
            self.ask_table_question()
            return

        random.shuffle(questions)
        self.ask_question(questions[0])

    def ask_table_question(self):
        question, answer, new_multiplier = multiplication_table(self.current_tables, self.last_multiplier)
        self.current_question = question
        self.correct_answer = answer
        self.last_multiplier = new_multiplier

        self.question_label.config(text=self.current_question)
        self.answer_entry.delete(0, tk.END)
        self.answer_entry.focus()
        self.attempts = 0
        if self.current_mode == "table":
            self.question_stats[question.split('=')[0].strip()]['total'] += 1  # Incrémente le total pour cette question

    def ask_question(self, question_func):
        self.current_question, self.correct_answer = question_func()
        self.question_label.config(text=self.current_question)
        self.answer_entry.delete(0, tk.END)
        self.answer_entry.focus()
        self.attempts = 0

    def check_answer(self, event):
        try:
            user_answer = int(self.answer_entry.get())
            self.answer_entry.delete(0, tk.END)

            if self.listing_multiples:
                expected_answer = self.current_tables[0] * self.current_multiple_index
                if user_answer == expected_answer:
                    self.history_list.insert(0, f"✓ {user_answer}")
                    self.history_list.itemconfig(0, {'fg': 'green'})
                    self.current_multiple_index += 1

                    if self.current_multiple_index <= 10:
                        self.question_label.config(text=f"Multiple suivant de {self.current_tables[0]}:")
                    else:
                        self.question_label.config(text=f"Bravo ! Tous les multiples de {self.current_tables[0]} ont été listés.")
                        self.root.after(1500, self.return_to_multiplications)
                else:
                    self.question_label.config(text=f"Incorrect, entrez le multiple {self.current_multiple_index} de {self.current_tables[0]}:")
                return

            if user_answer == self.correct_answer:
                self.correct_count += 1
                self.total_questions += 1
                if self.current_mode == "table":
                    self.question_stats[self.current_question.split('=')[0].strip()]['correct'] += 1
                self.history_list.insert(0, f"✓ {self.current_question.split('=')[0]}= {self.correct_answer}")
                self.history_list.itemconfig(0, {'fg': 'green'})
                if self.current_mode == "table_retry":
                    self.ask_retry_question()  # Passer à la question suivante dans la liste des erreurs
                else:
                    self.new_question(self.current_mode)
            else:
                self.attempts += 1
                if self.attempts < 1:
                    self.question_label.config(text=f"{self.current_question}\nIncorrect, réessaie !")
                else:
                    self.total_questions += 1
                    self.question_label.config(text=f"{self.current_question}\nFaux : La bonne réponse était {self.correct_answer}.")
                    self.history_list.insert(0, f"✗ {self.current_question.split('=')[0]}= {self.correct_answer}")
                    self.history_list.itemconfig(0, {'fg': 'red'})
                    self.root.after(1500, lambda: self.new_question(self.current_mode))

                # Ajoutez cette ligne pour passer à la question suivante dans le mode révision
                if self.current_mode == "table_retry":
                    self.ask_retry_question()

            self.stats_label.config(text=f"Stats: {self.correct_count} correct / {self.total_questions} total")

        except ValueError:
            self.answer_entry.delete(0, tk.END)
            self.question_label.config(text=f"{self.current_question}\nMerci de saisir un nombre valide.")


    def end_session(self):
        if self.current_mode == "table":
            # Analyser les erreurs
            errors = {q: stats for q, stats in self.question_stats.items() if stats['correct'] < stats['total']}

            if errors:
                # Trier les erreurs par table et par nombre d'erreurs
                sorted_errors = sorted(errors.items(), key=lambda x: (int(x[0].split('×')[0]), -x[1]['total']))

                # Préparer le podium
                podium = sorted(sorted_errors, key=lambda x: -x[1]['total'])[:3]

                error_summary = "Vos erreurs :\n"
                for q, stats in sorted_errors:
                    error_summary += f"{q}= {int(q.split('×')[0]) * int(q.split('×')[1])} : {stats['correct']}/{stats['total']} correct\n"

                podium_summary = "Podium des erreurs :\n"
                for i, (q, stats) in enumerate(podium):
                    podium_summary += f"{i+1}. {q}= {int(q.split('×')[0]) * int(q.split('×')[1])} : {stats['correct']}/{stats['total']} correct\n"

                self.question_label.config(text=error_summary + "\n" + podium_summary)

                # Proposer une partie avec les erreurs
                self.control_frame.pack_forget()
                if hasattr(self, 'tables_label'):
                    self.tables_label.pack_forget()

                self.retry_frame = ttk.Frame(self.left_frame)
                self.retry_frame.pack(pady=10)

                self.retry_button = ttk.Button(self.retry_frame, text="Rejouer avec ces calculs",
                                             command=lambda: self.start_retry_session([q for q, _ in sorted_errors]))
                self.retry_button.pack(pady=5)

                self.menu_button = ttk.Button(self.retry_frame, text="Retour au menu",
                                            command=self.return_to_menu)
                self.menu_button.pack(pady=5)
            else:
                self.question_label.config(text="Bravo ! Aucune erreur dans les tables.")
                self.root.after(2000, self.return_to_menu)
        else:
            self.root.quit()

    def start_retry_session(self, error_questions):
        self.retry_frame.pack_forget()
        self.current_mode = "table_retry"
        self.error_questions = error_questions
        self.correct_count = 0
        self.total_questions = 0
        self.question_stats = defaultdict(lambda: {'correct': 0, 'total': 0})
        self.ask_retry_question()

        self.control_frame = ttk.Frame(self.left_frame)
        self.control_frame.pack(pady=10)

        self.tables_label = ttk.Label(self.left_frame, text="Mode révision des erreurs")
        self.tables_label.pack(pady=5)

    def ask_retry_question(self):
        if not self.error_questions:
            self.question_label.config(text="Félicitations ! Vous avez corrigé toutes vos erreurs.")
            self.root.after(2000, self.return_to_menu)
            return

        question = self.error_questions.pop(0)  # Prendre la première question de la liste des erreurs
        self.current_question = question + " = ?"
        self.correct_answer = int(question.split('×')[0]) * int(question.split('×')[1])
        self.question_label.config(text=self.current_question)
        self.answer_entry.delete(0, tk.END)
        self.answer_entry.focus()
        self.attempts = 0
        self.question_stats[question]['total'] += 1

    def return_to_menu(self):
        if hasattr(self, 'control_frame'):
            self.control_frame.pack_forget()
        if hasattr(self, 'tables_label'):
            self.tables_label.pack_forget()
        if hasattr(self, 'retry_frame'):
            self.retry_frame.pack_forget()
        self.menu_frame.pack(pady=20)
        self.question_label.config(text="Choisissez un mode.")
        self.root.unbind('c')
        self.root.unbind('l')
        self.root.unbind('r')
        self.current_mode = None
        self.current_tables = []
        self.question_stats.clear()

if __name__ == "__main__":
    root = tk.Tk()
    app = TrainingApp(root)
    root.mainloop()
