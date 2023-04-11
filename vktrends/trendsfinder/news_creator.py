import openai 


class OpenAI:
    def __init__(self, trends_list, api_key, prompt):
        self.api_key = api_key
        self.trends_list = trends_list
        self.prompt = 'Представь, что ты программа, которая получает набор слов и генерирует на их основе категорию, характеризующий этот спискок. Выдай категорию на слова: {}.'.format(self.trends_list)
    
    def news(self):
        openai.api_key = self.api_key

        completion = openai.Completion.create(
            engine='text-davinci-003',
            prompt=self.prompt,
            max_tokens=1024,
            temperature=0.5,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        category = completion.choices[0].text
        if "Категория:" in category:
            return category

        return "Категория: " + category


# class News(OpenAI):
#     def __init__(self):
#         super.__init__(self)
#         self.prompt = 'Представь, что ты программа, которая получает набор слов и генерирует на их основе категорию, характеризующий этот спискок. Выдай категорию на слова: {}.'.format(self.trends_list)


if __name__ == "__main__":
    trends_list = 'тоталитарный северный стас лебедев корея история чеченский ужасающий live питер сажать гаага посадить путин трамп артемий закон иноагент рф фильм забастовка wilberries тарантино банкротство банк либерал соловьёв коммунист владимир а нтонов порешать рыночка социализм выступить встретить впервые хейтер всякий студент живой пообщаться татарский владлен оружие теракт ядерный ответ старик белоруссия шария чзп кремль яндекс интервью забыть назвать выпуск подписаться предатель проект родина уйти эфир блядь die российский изменить псевдокоммунист прямо пропагандон инет волноваться'
    model = OpenAI(api_key = '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', group_name='Стас Ай, Как Просто!', trends_list=trends_list)
    print(model.news())