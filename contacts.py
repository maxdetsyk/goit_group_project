from datetime import date, timedelta


"""
1. Сохранять контакты с именами, адресами, номерами телефонов, email и днями рождения в книгу контактов.
"""


"""
2. Выводить список контактов у которых день рождения через заданное количество дней от текущей даты.
"""
    def days_to_birthday(self):
        """
        If birthday is added: counts days before next one.
        """

        if self.birthday.value is None:
            print(f"No b-day added for {self.name.value}")
            return

        date_now = date.today()
        birthday_date = self.birthday.value
        birthday_date = birthday_date.replace(year=date_now.year)
        # Check if user's birthday passed this year => year + 1
        if birthday_date <= date_now:
            birthday_date = birthday_date.replace(year=date_now.year + 1)

        days_delta = birthday_date - date_now
        return days_delta.days


    def birthday_in_next_x_days(self, step: int = 7):
        try:
            step = int(step)
        except ValueError:
            raise ValueError("Input a number")
        result = []
        for record in self.data.values():
            if record.birthday and record.birthday.value:
                if record.days_to_birthday() <= step:
                    birthday = f'{record.name.value} {record.birthday.value.strftime("%d-%m-%Y")}'
                    result.append(birthday)
        return result


"""
3. Проверять правильность введенного номера телефона и email во время создания или редактирования записи и уведомлять пользователя в случае некорректного ввода.
"""


"""
4. Совершать поиск по контактам из книги контактов.
"""


"""
5. Редактировать и удалять записи из книги контактов.
"""
