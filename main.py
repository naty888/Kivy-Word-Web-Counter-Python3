# Terminal Text Editor (Android app)
# Aplication from HiveMind
# Code written by Zero Davila 2016

import requests
import operator
from bs4 import BeautifulSoup
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView

kv = '''
#: import FadeTransition kivy.uix.screenmanager.FadeTransition

ScreenManager:
    transition: FadeTransition()
    MainScreen:
    SecondScreen:

<ScrollableLabel>:
    text: app.text

    Label:
        text: root.text
        font_size: 15
        text_size: self.width, None
        color: [0,1,0,1]
        size_hint_y: None
        pos_hint: {"left":1, "top":1}
        height: self.texture_size[1]

<ScrollableLabel2>:
    text: app.text2

    Label:
        text: root.text
        font_size: 15
        text_size: self.width, None
        color: [0,1,0,1]
        size_hint_y: None
        pos_hint: {"left":1, "top":1}
        height: self.texture_size[1]

<MainScreen>:
    name: "main"
    FloatLayout:

        BoxLayout:
            orientation: "vertical"
            padding: 10
            spacing: 10

            Label:
                size_hint_y: .1

            TextInput:
                id: txt_inpt
                text: "Website URL"
                background_color: [1,1,1,.1]
                foreground_color: [0,1,0,1]
                cursor_color: [0,1,0,1]
                font_size: 18
                size_hint_y: .1
                on_text: root.check_status(f_but)

            ScrollableLabel

        Button:
            id: "log_button"
            pos_hint: {'x': 0.63, 'center_y': .8}
            size_hint: (.3, .07)
            background_color: [.4, .4, .4, 1]
            color: [0, 1, 0, 1]
            text: "Show"
            on_press: app.crawl(txt_inpt.text)
            on_release: app.read_top()
            on_release: app.read_log()

    ActionBar:
        pos_hint: {"top":1}
        background_color: [1,1,1,1]
        ActionView:
            use_separator: True
            ActionPrevious:
                title: "Web Word Counter"
                with_previous: False
                color: [0,1,0,1]
            ActionOverflow:
            ActionButton:
                text: "Log"
                on_release: app.root.current = "second"
                color: [0,1,0,1]
            ActionButton:
                text: "Del first"
                on_press: root.delete_first()
                on_release: app.read_top()
                color: [0,1,0,1]
            ActionButton:
                text: "Del last"
                on_press: root.delete_last()
                on_release: app.read_top()
                color: [0,1,0,1]
            ActionButton:
                text: "Clear"
                on_press: root.clear_label()
                on_release: app.read_top()
                color: [0,1,0,1]

<SecondScreen>:
    name: "second"
    FloatLayout:

        BoxLayout:
            orientation: "vertical"
            padding: 10
            spacing: 10
            Label:
                size_hint_y: .1

            ScrollableLabel2

    ActionBar:
        pos_hint: {"top":1}
        background_color: [1,1,1,1]
        ActionView:
            use_separator: True
            ActionPrevious:
                title: "Web Word Counter"
                with_previous: False
                color: [0,1,0,1]
            ActionOverflow:
            ActionButton:
                text: "Back"
                on_release: app.root.current = "main"
                color: [0,1,0,1]
            ActionButton:
                text: "Del first"
                on_press: root.delete_first()
                on_release: app.read_log()
                color: [0,1,0,1]
            ActionButton:
                text: "Del last"
                on_press: root.delete_last()
                on_release: app.read_log()
                color: [0,1,0,1]
            ActionButton:
                text: "Clear"
                on_press: root.clear_label()
                on_release: app.read_log()
                color: [0,1,0,1]
'''


class ScrollableLabel(ScrollView):
    pass


class ScrollableLabel2(ScrollView):
    pass


class MainScreen(Screen):

    def clear_label(self):
        # Deletes all
        with open("top.txt", "w", encoding='utf-8') as a:
            a.write("" + "\n\n")
            a.close()

    def delete_first(self):
        # Deletes first line of text file
        with open('top.txt', 'r', encoding='utf-8') as fin:
            data = fin.read().splitlines(True)
        with open('top.txt', 'w', encoding='utf-8') as fout:
            fout.writelines(data[1:])

    def delete_last(self):
        # Deletes last line of text file
        with open('top.txt', 'r', encoding='utf-8') as fin:
            data = fin.read().splitlines(True)
        with open('top.txt', 'w', encoding='utf-8') as fout:
            fout.writelines(data[:-1])


class SecondScreen(Screen):
    text = StringProperty("")

    def clear_label(self):
        # Deletes all
        with open("log.txt", "w", encoding='utf-8') as b:
            b.write("" + "\n\n")
            b.close()

    def delete_first(self):
        # Deletes first line of text file
        with open('log.txt', 'r', encoding='utf-8') as fin:
            data = fin.read().splitlines(True)
        with open('log.txt', 'w', encoding='utf-8') as fout:
            fout.writelines(data[1:])

    def delete_last(self):
        # Deletes last line of text file
        with open('log.txt', 'r', encoding='utf-8') as fin:
            data = fin.read().splitlines(True)
        with open('log.txt', 'w', encoding='utf-8') as fout:
            fout.writelines(data[:-1])

# ---------> This is where the magic happens <-----------

def run(url):

    word_count = {}

    def create_dictionary(clean_word_list):
        for word in clean_word_list:
            if word in word_count:
                word_count[word] += 1
            else:
                word_count[word] = 1
        for key, value in sorted(word_count.items(), key=operator.itemgetter(1), reverse=True):  # 0 for key, 1 for value
            top.append(key)
            top.append(value)

    def clean_up_list(word_list):
        clean_word_list = []
        for word in word_list:
            symbols = "!@#$%^&*()_+>?<:\\\",.;[]{}=|"
            for i in range(0, len(symbols)):
                word = word.replace(symbols[i], "")
            if len(word) > 0:
                clean_word_list.append(word)
        create_dictionary(clean_word_list)

    top = []
    word_list = []
    source_code = requests.get(url).text
    soup = BeautifulSoup(source_code, "html5lib")

    try:
        with open("log.txt", mode='at', encoding='utf-8') as b:
            b.write(str(soup))
            b.close()
    except:
        with open("log.txt", mode='wt', encoding='utf-8') as b:
            b.write(str(soup))
            b.close()

    for post_text in soup.findAll('a', {"class": ""}):
        content = post_text.string
        word = content.lower().split()
        for each_word in word:
            word_list.append(each_word)
        clean_up_list(word_list)

    try:
        with open("top.txt", mode='at', encoding='utf-8') as a:
            a.write('\n'.join(str(t) for t in top))
            a.close()
    except:
        with open("top.txt", mode='wt', encoding='utf-8') as a:
            a.write('\n'.join(str(t) for t in top))
            a.close()


class MyApp(App):
    text = StringProperty("")
    text2 = StringProperty("")
    text3 = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with open("top.txt", "r", encoding='utf-8') as a:
            contents = a.read()
            self.text = str(contents)
        with open("log.txt", "r", encoding='utf-8') as b:
            contents2 = b.read()
            self.text2 = str(contents2)

    def crawl(self, url):
        # This is where we reference the magic
        self.text3 = url
        run(url)

    def read_top(self):
        with open("top.txt", "r", encoding='utf-8') as a:
            contents = a.read()
            self.text = str(contents)

    def read_log(self):
        with open("log.txt", "r", encoding='utf-8') as b:
            contents2 = b.read()
            self.text2 = str(contents2)

    def build(self):
        return Builder.load_string(kv)

if __name__ == "__main__":
    MyApp().run()
