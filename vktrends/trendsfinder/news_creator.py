import openai 


class OpenAI:
    def __init__(self, group_name, trends_list, api_key):
        self.api_key = api_key
        self.group_name = group_name
        self.trends_list = trends_list
        self.prompt = 'Представь, что ты создатель VK группы "{}" и придумай серьёзную, но смешную сатирическую новость от имени создателя группы, содержащую слова {}'.format(self.group_name, self.trends_list)
    
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

        return completion.choices[0].text


if __name__ == "__main__":
    model = OpenAI(api_key = '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', group_name='Стас Ай, Как Просто!', trends_list='смотреть, блять, эфиры, первый, phone, новый, обзор, такое, фильмы, спасибо, тв, прости, доносить, зарево, ленина, документальные, делал, гасить, изменить, инету')
    print(model.news())