import telebot
import model
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, \
    ReplyKeyboardRemove

token = "yourToken"
bot = telebot.TeleBot(token)

post_dict = {}  # saves posts data


def main_menu_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Create post", callback_data="create_post"))
    return markup


def post_markup(message):
    post = post_dict[message.chat.id]
    word = post.words[-1]
    definition_number = len(word.definitions) + 1
    markup = InlineKeyboardMarkup()
    add_definition_button = InlineKeyboardButton("Add definition #{0}".format(definition_number),
                                                 callback_data="add_definition")
    add_tags_button = InlineKeyboardButton("Add tags", callback_data="add_tags")
    add_links_button = InlineKeyboardButton("Add dictionary links", callback_data="add_links")
    add_synonyms_button = InlineKeyboardButton("Add synonyms", callback_data="add_synonyms")
    add_new_word_button = InlineKeyboardButton("Add new word", callback_data="add_new_word")
    cancel_button = InlineKeyboardButton("Cancel", callback_data="cancel")
    finish_button = InlineKeyboardButton("Finish", callback_data="finish")

    markup.add(add_definition_button)
    if not word.synonyms:
        markup.add(add_synonyms_button)
    if word.definitions:
        markup.add(add_new_word_button)
    if not post.hashTags:
        markup.add(add_tags_button)
    if not post.oxford and not post.cambridge and not post.context:
        markup.add(add_links_button)

    markup.row(cancel_button, finish_button)

    return markup


def skip_markup():
    markup = ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add(KeyboardButton('Skip'))
    return markup


def parts_of_speech_markup():
    markup = ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add(KeyboardButton('noun'), KeyboardButton('verb'), KeyboardButton('adjective'), KeyboardButton('adverb'),
               KeyboardButton('conjunction'), KeyboardButton('Idiom'), KeyboardButton('phrasal verb'))
    return markup


def tags_markup(message):
    markup = ReplyKeyboardMarkup(one_time_keyboard=True, row_width=2)
    post = post_dict[message.chat.id]
    word = post.words[0]
    if word.partOfSpeech == "Idiom":
        markup.add(KeyboardButton('#Idioms #B1'), KeyboardButton('#Idioms #B2'),
                   KeyboardButton('#Idioms #C1'), KeyboardButton('#Idioms #C2'))
    elif word.partOfSpeech == "phrasal verb":
        markup.add(KeyboardButton('#PhrasalVerb #B1'), KeyboardButton('#PhrasalVerb #B2'),
                   KeyboardButton('#PhrasalVerb #C1'), KeyboardButton('#PhrasalVerb #C2'))
    else:
        markup.add(KeyboardButton('#Words #B1'), KeyboardButton('#Words #B2'), KeyboardButton('#Words #C1'),
                   KeyboardButton('#Words #C2'))
    return markup


@bot.message_handler(commands=['start'])
def process_start(message):
    bot.send_message(message.chat.id, "Create new post here.",
                     reply_markup=main_menu_markup())


@bot.callback_query_handler(func=lambda call: True)
def test_callback(call):
    if call.data == "create_post":
        bot.answer_callback_query(call.id, "Creating post!")
        post = model.Post()
        post_dict[call.message.chat.id] = post
        msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text="Creating post. Send word for vocabulary post.")
        bot.register_next_step_handler(msg, process_word_name)
    if call.data == "add_definition":
        bot.answer_callback_query(call.id, "Adding definition!")
        post = post_dict[call.message.chat.id]
        word = post.words[-1]
        definition_number = len(word.definitions) + 1
        msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text="Creating definition #{0}.Send definition.".format(definition_number))
        bot.register_next_step_handler(msg, process_adding_definition)
    if call.data == "add_synonyms":
        bot.answer_callback_query(call.id, "Adding synonyms!")
        msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text="Add some synonyms in this format: synonym1, synonym2, synonym3.")
        bot.register_next_step_handler(msg, process_synonyms)
    if call.data == "add_tags":
        bot.answer_callback_query(call.id, "Adding tags!")
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Adding tags!")
        msg = bot.send_message(chat_id=call.message.chat.id, text='Chose one set of tags from options down below.',
                               reply_markup=tags_markup(call.message))
        bot.register_next_step_handler(msg, process_adding_tags)
    if call.data == "add_links":
        bot.answer_callback_query(call.id, "Adding links!")
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Adding links!")
        msg = bot.send_message(chat_id=call.message.chat.id, text='Add link for Oxford Dictionary! You can skip by '
                                                                  'pressing button "Skip"', reply_markup=skip_markup())
        bot.register_next_step_handler(msg, process_adding_links_oxford)
    if call.data == "add_new_word":
        bot.answer_callback_query(call.id, "Adding new word!")
        msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text="Adding new word! Send word for vocabulary post.")
        bot.register_next_step_handler(msg, process_word_name)
    if call.data == "cancel":
        bot.answer_callback_query(call.id, "Canceling creating post!")
        post_dict.pop(call.message.chat.id)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Create new post here.", reply_markup=main_menu_markup())
    if call.data == "finish":
        bot.answer_callback_query(call.id, "This is your post!")
        post = post_dict[call.message.chat.id]
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=post.print_post(), parse_mode="Markdown")
        links = post.print_links()
        if links:
            bot.send_message(call.message.chat.id, links, parse_mode="Markdown")
        post_dict.pop(call.message.chat.id)
        bot.send_message(call.message.chat.id, "Create new post here.",
                         reply_markup=main_menu_markup())


def process_word_name(message):
    word_name = message.text
    post = post_dict[message.chat.id]
    new_word = model.Word(word_name)
    post.words.append(new_word)
    post_dict[message.chat.id] = post
    msg = bot.send_message(message.chat.id, 'Send phonetic transcription. You can skip by pressing button "Skip"',
                           reply_markup=skip_markup())
    bot.register_next_step_handler(msg, process_phonetic_transcription)


def process_phonetic_transcription(message):
    if message.text != 'Skip':
        phonetic_transcription = message.text
        characters_to_replace = ['/', '\\', '[', ']']
        for char in characters_to_replace:
            phonetic_transcription = phonetic_transcription.replace(char, '')
        post = post_dict[message.chat.id]
        word = post.words[-1]
        word.phoneticTranscription = phonetic_transcription
        post_dict[message.chat.id] = post

    msg = bot.send_message(message.chat.id, "Choose part of the speech from options down below.",
                           reply_markup=parts_of_speech_markup())
    bot.register_next_step_handler(msg, process_part_of_speech)


def process_part_of_speech(message):
    part_of_speech = message.text
    post = post_dict[message.chat.id]
    word = post.words[-1]
    word.partOfSpeech = part_of_speech
    post_dict[message.chat.id] = post
    bot.send_message(message.chat.id, post.print_post(), reply_markup=post_markup(message), parse_mode="Markdown")


def process_synonyms(message):
    synonyms = message.text
    post = post_dict[message.chat.id]
    word = post.words[-1]
    word.synonyms = synonyms
    post_dict[message.chat.id] = post
    bot.send_message(message.chat.id, post.print_post(), reply_markup=post_markup(message), parse_mode="Markdown")


def process_adding_definition(message):
    definition = message.text
    new_definition = model.Definition(definition)
    post = post_dict[message.chat.id]
    word = post.words[-1]
    word.definitions.append(new_definition)
    post_dict[message.chat.id] = post
    msg = bot.send_message(message.chat.id, "Add some examples. Each example must start from a new line!")
    bot.register_next_step_handler(msg, process_adding_definition_examples)


def process_adding_definition_examples(message):
    definition_examples = message.text
    definition_examples_array = definition_examples.split("\n")
    post = post_dict[message.chat.id]
    word = post.words[-1]
    definition = word.definitions[-1]
    definition.examples = definition_examples_array
    post_dict[message.chat.id] = post
    bot.send_message(message.chat.id, post.print_post(), reply_markup=post_markup(message), parse_mode="Markdown")


def process_adding_tags(message):
    tags = message.text
    post = post_dict[message.chat.id]
    post.hashTags = tags
    post_dict[message.chat.id] = post
    bot.send_message(message.chat.id, post.print_post(), reply_markup=post_markup(message), parse_mode="Markdown")


def process_adding_links_oxford(message):
    if message.text != "Skip":
        link = message.text
        post = post_dict[message.chat.id]
        post.oxford = link
        post_dict[message.chat.id] = post

    msg = bot.send_message(message.chat.id, 'Add link for Cambridge Dictionary! You can skip by pressing button "Skip"',
                           reply_markup=skip_markup())
    bot.register_next_step_handler(msg, process_adding_links_cambridge)


def process_adding_links_cambridge(message):
    if message.text != "Skip":
        link = message.text
        post = post_dict[message.chat.id]
        post.cambridge = link
        post_dict[message.chat.id] = post

    msg = bot.send_message(message.chat.id, 'Add link for Context Reverso! You can skip by pressing button "Skip"',
                           reply_markup=skip_markup())
    bot.register_next_step_handler(msg, process_adding_links_context)


def process_adding_links_context(message):
    post = post_dict[message.chat.id]
    if message.text != "Skip":
        link = message.text
        post.context = link
        post_dict[message.chat.id] = post

    bot.send_message(message.chat.id, post.print_post(), reply_markup=post_markup(message), parse_mode="Markdown")


if __name__ == "__main__":
    bot.polling(none_stop=True)
