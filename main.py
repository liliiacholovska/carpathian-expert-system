import customtkinter as ctk

from knowledge_base import QUESTIONS
from expert_system import calculate_results, get_explanation


ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")


class ExpertSystemApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Експертна система — Тур у Карпати")
        self.geometry("900x650")
        self.resizable(False, False)

        self.current_question = 0
        self.selected_answers = []
        self.selected_labels = []
        self.selected_categories = []

        self.show_start_screen()

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    def show_start_screen(self):
        self.clear_window()

        main_frame = ctk.CTkFrame(
            self,
            fg_color="#F4F7F2",
            corner_radius=0
        )
        main_frame.pack(fill="both", expand=True)

        title = ctk.CTkLabel(
            main_frame,
            text="ТУР У КАРПАТИ",
            font=("Arial", 36, "bold"),
            text_color="#234D20"
        )
        title.pack(pady=(120, 15))

        subtitle = ctk.CTkLabel(
            main_frame,
            text="Експертна система підбору\nоптимального варіанта відпочинку",
            font=("Arial", 20),
            text_color="#444444"
        )
        subtitle.pack(pady=10)

        description = ctk.CTkLabel(
            main_frame,
            text=(
                "Відповідайте на декілька запитань,\n"
                "а система проаналізує ваші побажання."
            ),
            font=("Arial", 16),
            text_color="#666666"
        )
        description.pack(pady=25)

        start_button = ctk.CTkButton(
            main_frame,
            text="Розпочати",
            width=220,
            height=50,
            corner_radius=12,
            font=("Arial", 18, "bold"),
            command=self.start_test
        )
        start_button.pack(pady=20)

    def start_test(self):
        self.current_question = 0
        self.selected_answers = []
        self.selected_labels = []
        self.selected_categories = []

        self.show_question()

    def show_question(self):
        self.clear_window()

        question_data = QUESTIONS[self.current_question]

        main_frame = ctk.CTkFrame(
            self,
            fg_color="#F4F7F2",
            corner_radius=0
        )
        main_frame.pack(fill="both", expand=True)

        progress_text = (
            f"Питання {self.current_question + 1} "
            f"із {len(QUESTIONS)}"
        )

        progress_label = ctk.CTkLabel(
            main_frame,
            text=progress_text,
            font=("Arial", 15),
            text_color="#5D6D5A"
        )
        progress_label.pack(pady=(50, 10))

        progress = ctk.CTkProgressBar(
            main_frame,
            width=500,
            height=12
        )

        progress.set(
            (self.current_question + 1) / len(QUESTIONS)
        )

        progress.pack(pady=(0, 40))

        question_label = ctk.CTkLabel(
            main_frame,
            text=question_data["question"],
            font=("Arial", 26, "bold"),
            text_color="#234D20",
            wraplength=700
        )
        question_label.pack(pady=(10, 35))

        answers_frame = ctk.CTkFrame(
            main_frame,
            fg_color="transparent"
        )
        answers_frame.pack()

        for answer_text, answer_id in question_data["answers"]:
            button = ctk.CTkButton(
                answers_frame,
                text=answer_text,
                width=400,
                height=50,
                corner_radius=10,
                font=("Arial", 17),
                command=lambda value=answer_id,
                text=answer_text,
                category=question_data["category"]:
                    self.select_answer(
                        value,
                        text,
                        category
                    )
            )

            button.pack(pady=8)

    def select_answer(
        self,
        answer_id,
        answer_text,
        category
    ):
        self.selected_answers.append(answer_id)
        self.selected_labels.append(answer_text)
        self.selected_categories.append(category)

        self.current_question += 1

        screens = {
            True: self.show_results,
            False: self.show_question
        }

        screens[
            self.current_question == len(QUESTIONS)
        ]()

    def show_results(self):
        self.clear_window()

        results = calculate_results(
            self.selected_answers
        )

        best = results[0]
        alternative = results[1]

        explanation = get_explanation(
            self.selected_answers,
            self.selected_labels,
            self.selected_categories,
            best["tour"]
        )

        main_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="#F4F7F2",
            corner_radius=0
        )
        main_frame.pack(fill="both", expand=True)

        title = ctk.CTkLabel(
            main_frame,
            text="РЕЗУЛЬТАТ ЕКСПЕРТНОЇ СИСТЕМИ",
            font=("Arial", 18, "bold"),
            text_color="#5D6D5A"
        )
        title.pack(pady=(35, 10))

        recommendation_text = ctk.CTkLabel(
            main_frame,
            text="Рекомендований варіант",
            font=("Arial", 16),
            text_color="#555555"
        )
        recommendation_text.pack()

        recommendation = ctk.CTkLabel(
            main_frame,
            text=best["tour"],
            font=("Arial", 38, "bold"),
            text_color="#234D20"
        )
        recommendation.pack(pady=(5, 5))

        percentage = ctk.CTkLabel(
            main_frame,
            text=f'Відповідність: {best["percentage"]}%',
            font=("Arial", 20, "bold")
        )
        percentage.pack(pady=5)

        progress = ctk.CTkProgressBar(
            main_frame,
            width=450,
            height=18
        )

        progress.set(best["percentage"] / 100)
        progress.pack(pady=15)

        score = ctk.CTkLabel(
            main_frame,
            text=(
                f'Експертна оцінка: '
                f'{best["score"]} із '
                f'{len(self.selected_answers) * 5} балів'
            ),
            font=("Arial", 15),
            text_color="#555555"
        )
        score.pack(pady=(0, 20))

        explanation_frame = ctk.CTkFrame(
            main_frame,
            width=600,
            fg_color="#FFFFFF",
            corner_radius=15
        )
        explanation_frame.pack(
            padx=100,
            pady=10,
            fill="x"
        )

        explanation_title = ctk.CTkLabel(
            explanation_frame,
            text="Чому система рекомендує цей варіант?",
            font=("Arial", 19, "bold"),
            text_color="#234D20"
        )
        explanation_title.pack(
            pady=(20, 15)
        )

        for item in explanation:
            criterion_text = (
                f'{item["category"]}: '
                f'{item["criterion"]}'
                f'   —   {item["weight"]}/5'
            )

            criterion = ctk.CTkLabel(
                explanation_frame,
                text=criterion_text,
                font=("Arial", 15),
                anchor="w"
            )

            criterion.pack(
                padx=35,
                pady=4,
                fill="x"
            )

        info = ctk.CTkLabel(
            explanation_frame,
            text=(
                "\nОцінки сформовані на основі "
                "вагової бази знань експертної системи."
            ),
            font=("Arial", 13),
            text_color="#777777"
        )

        info.pack(
            padx=20,
            pady=(10, 20)
        )

        alternative_frame = ctk.CTkFrame(
            main_frame,
            fg_color="#E5EDE2",
            corner_radius=12
        )

        alternative_frame.pack(
            padx=100,
            pady=20,
            fill="x"
        )

        alternative_title = ctk.CTkLabel(
            alternative_frame,
            text="Альтернативний варіант",
            font=("Arial", 15),
            text_color="#555555"
        )

        alternative_title.pack(
            pady=(15, 3)
        )

        alternative_label = ctk.CTkLabel(
            alternative_frame,
            text=(
                f'{alternative["tour"]} — '
                f'{alternative["percentage"]}%'
            ),
            font=("Arial", 20, "bold"),
            text_color="#234D20"
        )

        alternative_label.pack(
            pady=(0, 15)
        )

        ranking_frame = ctk.CTkFrame(
            main_frame,
            fg_color="#FFFFFF",
            corner_radius=15
        )

        ranking_frame.pack(
            padx=100,
            pady=10,
            fill="x"
        )

        ranking_title = ctk.CTkLabel(
            ranking_frame,
            text="Рейтинг усіх варіантів",
            font=("Arial", 19, "bold"),
            text_color="#234D20"
        )

        ranking_title.pack(
            pady=(20, 15)
        )

        for index, result in enumerate(results, start=1):
            row = ctk.CTkFrame(
                ranking_frame,
                fg_color="transparent"
            )

            row.pack(
                padx=30,
                pady=5,
                fill="x"
            )

            name_label = ctk.CTkLabel(
                row,
                text=f'{index}. {result["tour"]}',
                width=160,
                anchor="w",
                font=("Arial", 15, "bold")
            )

            name_label.pack(side="left")

            bar = ctk.CTkProgressBar(
                row,
                width=280,
                height=12
            )

            bar.set(
                result["percentage"] / 100
            )

            bar.pack(
                side="left",
                padx=15
            )

            percent_label = ctk.CTkLabel(
                row,
                text=f'{result["percentage"]}%',
                width=50,
                font=("Arial", 15)
            )

            percent_label.pack(side="left")

        ranking_bottom = ctk.CTkLabel(
            ranking_frame,
            text="",
            height=10
        )

        ranking_bottom.pack()

        restart_button = ctk.CTkButton(
            main_frame,
            text="Пройти ще раз",
            width=220,
            height=45,
            font=("Arial", 16, "bold"),
            command=self.start_test
        )

        restart_button.pack(
            pady=(5, 35)
        )


app = ExpertSystemApp()
app.mainloop()