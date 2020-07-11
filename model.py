class Post:
    def __init__(self):
        self.word = None
        self.hashTags = None
        self.oxford = None
        self.cambridge = None
        self.context = None

    def print_post(self):
        word = self.word.print_word()
        line_end = "─────────────"
        result = "{0}{1}\n{2}".format(word, line_end, self.hashTags)
        return result

    def print_links(self):
        result = ""
        divider = " | "
        if self.oxford:
            result += "Oxford Dictionary - " + self.oxford
        else:
            divider = ""
        if self.context:
            result += divider + "Context Reverso - " + self.context
        if self.cambridge:
            result += "\n" + "Cambridge Dictionary - " + self.cambridge
        if result != "":
            result = "`{0}`".format(result)
        return result


class Word:
    def __init__(self, word):
        self.word = word
        self.phoneticTranscription = None
        self.partOfSpeech = None
        self.synonyms = None
        self.definitions = []

    def print_word(self):
        line = "──────────────────────"
        if self.phoneticTranscription:
            phonetic_transcription = "*/{0}/*".format(self.phoneticTranscription)
            word = "🖍 _{0}_ — {1} {2}\n{3}".format(self.word, phonetic_transcription, self.partOfSpeech, line)
        else:
            word = "🖍 _{0}_ — {1}\n{2}".format(self.word, self.partOfSpeech, line)

        if self.synonyms:
            synonym_or_synonyms = "synonym"
            if "," in self.synonyms:
                synonym_or_synonyms = "synonyms"
            synonyms = "(_{0}_ — {1})".format(synonym_or_synonyms, self.synonyms)
            word += "\n{0}\n".format(synonyms)

        if not self.definitions:
            return word

        definitions = ""
        for definition in self.definitions:
            index = self.definitions.index(definition)
            if index + 1 != len(self.definitions):
                definitions += definition.print_definition(index) + '\n'
            else:
                definitions += definition.print_definition(index)

        result = "{0}\n{1}".format(word, definitions)
        return result


class Definition:
    def __init__(self, definition):
        self.definition = definition
        self.examples = []

    def print_definition(self, definition_number):
        definition_number += 1

        if definition_number == 1:
            arrow = " ➤ ❶ "
        elif definition_number == 2:
            arrow = " ➤ ❷ "
        elif definition_number == 3:
            arrow = " ➤ ❸ "
        elif definition_number == 4:
            arrow = " ➤ ❹ "
        elif definition_number == 5:
            arrow = " ➤ ❺ "
        else:
            arrow = " ➤ ❶ "

        definition = "_{0}{1}_".format(arrow, self.definition)

        examples = ""
        for example in self.examples:
            examples += " ➖ " + example + "\n"

        result = "{0}\n\n{1}".format(definition, examples)
        return result
