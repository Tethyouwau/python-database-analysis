from tkinter import Tk, Label, Entry, Button, filedialog

# Создаем окно
root = Tk()

# Добавляем метки и поля ввода для путей
label_excel = Label(root, text="Путь к Excel-файлу:")
entry_excel = Entry(root)
label_word = Label(root, text="Путь к Word-шаблону:")
entry_word = Entry(root)

# Добавляем кнопки для подтверждения выбора
button_confirm = Button(root, text="Подтвердить", command=lambda: print(entry_excel.get(), entry_word.get()))

# Добавляем кнопку для выбора файла
button_choose_excel = Button(root, text="Выбрать Excel-файл", command=lambda: choose_file('excel'))
button_choose_word = Button(root, text="Выбрать Word-шаблон", command=lambda: choose_file('word'))

# Располагаем элементы на экране
label_excel.pack()
entry_excel.pack()
label_word.pack()
entry_word.pack()
button_choose_excel.pack()
button_choose_word.pack()
button_confirm.pack()

# Функция для выбора файла
def choose_file(type):
    if type == 'excel':
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xlsm *.xlsb *.ods")])
        if file_path:
            # Чтение данных из Excel-файла
            df = pd.read_excel(file_path)

            # Создание шаблона Word
            word_template = 'path/to/your/word_template.docx'
            document = Document(word_template)

            # Замена тегов в новом документе
            for tag in df.columns:
                document.replace_all(tag, str(df[tag].iloc[0]))

            # Переименование документа по уникальному идентификатору
            unique_id_column = 'Уникальный идентификатор'  # Замените на название вашей колонки
            unique_id = df[unique_id_column].iloc[0]
            output_file = f"{output_dir}/{unique_id}.docx"
            document.save(output_file)
    elif type == 'word':
        file_path = filedialog.askopenfilename(filetypes=[("Word files", "*.docx *.docm *.dotx *.dotm")])
        if file_path:
            pass  # Здесь можно добавить логику для выбора Word-шаблона


# Запускаем цикл обработки событий
root.mainloop()
