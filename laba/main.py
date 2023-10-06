from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import networkx as nx
import matplotlib.pyplot as plt


def find_common_hypernym2(word1, word2):
    synsets1 = wn.synsets(word1)
    synsets2 = wn.synsets(word2)

    common_hypernyms = []

    for synset1 in synsets1:
        for synset2 in synsets2:
            hypernyms = synset1.lowest_common_hypernyms(synset2)
            if hypernyms:
                common_hypernym = hypernyms[0]
                common_hypernyms.append((synset1, synset2, common_hypernym))

    return common_hypernyms

def visualize_path(synset1, synset2, common_hypernym):
    G = nx.DiGraph()

    path1 = synset1.hypernym_paths()[0]
    path2 = synset2.hypernym_paths()[0]

    for i in range(len(path1) - 1):
        G.add_node(path1[i].name())
        G.add_node(path1[i + 1].name())
        G.add_edge(path1[i].name(), path1[i + 1].name(), label=path1[i].lowest_common_hypernyms(path1[i + 1])[0].name())

    for i in range(len(path2) - 1):
        G.add_node(path2[i].name())
        G.add_node(path2[i + 1].name())
        G.add_edge(path2[i].name(), path2[i + 1].name(), label=path2[i].lowest_common_hypernyms(path2[i + 1])[0].name())

    G.add_node(common_hypernym.name())
    G.add_edge(path1[-1].name(), common_hypernym.name(), label=common_hypernym.name())
    G.add_edge(path2[-1].name(), common_hypernym.name(), label=common_hypernym.name())

    pos = nx.spring_layout(G, seed=42)
    labels = nx.get_edge_attributes(G, 'label')

    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=True, labels={node: node for node in G.nodes()}, node_size=2000, font_size=10, font_color='black', font_weight='bold')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.title(f"Шлях від {synset1.name()} та {synset2.name()} до {common_hypernym.name()}")
    plt.show()
def find_common_hypernyms(word1, word2):
    synsets1 = wn.synsets(word1)
    synsets2 = wn.synsets(word2)

    common_hypernyms = []

    for synset1 in synsets1:
        for synset2 in synsets2:
            # Find common hypernyms
            common_hypernyms.extend(synset1.lowest_common_hypernyms(synset2))

    return common_hypernyms


def find_intermediate_hypernyms(word1, word2):
    synsets1 = wn.synsets(word1)
    synsets2 = wn.synsets(word2)

    intermediate_hypernyms = []

    for synset1 in synsets1:
        for synset2 in synsets2:
            common_hypernyms = find_common_hypernyms(word1, word2)

            for common_hypernym in common_hypernyms:
                paths1 = synset1.hypernym_paths()
                paths2 = synset2.hypernym_paths()

                for path1 in paths1:
                    for path2 in paths2:
                        common_path_hypernym = common_hypernym
                        if common_path_hypernym in path1 and common_path_hypernym in path2:
                            intermediate_hypernyms.extend(path1[path1.index(common_path_hypernym):])
                            intermediate_hypernyms.extend(path2[path2.index(common_path_hypernym):])

    return intermediate_hypernyms

common_hypernyms = find_common_hypernyms("dog", "cat")
def build_hypernym_tree(word1, word2):
    G = nx.DiGraph()

    common_hypernyms = find_common_hypernyms(word1, word2)  # Define common_hypernyms here
    intermediate_hypernyms = find_intermediate_hypernyms(word1, word2)

    for synset in intermediate_hypernyms:
        hypernym = synset.name().split(".")[0]
        G.add_node(hypernym)

    # Додавання ребер між спільними батьківськими об'єктами і проміжними об'єктами
    for synset in intermediate_hypernyms:
        hypernym = synset.name().split(".")[0]

        # Додаємо ребро від спільного батьківського об'єкта до проміжного об'єкта
        G.add_edge(hypernym, word1, label=word1)
        G.add_edge(hypernym, word2, label=word2)

    # Знаходимо кореневий об'єкт, який є найвищим спільним батьківським об'єктом
    root_hypernym = common_hypernyms[0].name().split(".")[0]

    # Додаємо ребра від кореневого об'єкта до "dog" та "cat"
    G.add_edge(root_hypernym, word1, label=word1)
    G.add_edge(root_hypernym, word2, label=word2)

    return G
def find_common_hypernym1(word1, word2):
    # Отримуємо синоніми (synsets) для обох слів
    synsets1 = wn.synsets(word1)
    synsets2 = wn.synsets(word2)

    common_hypernyms = []

    # Пройдемося по всіх синонімах для першого слова
    for synset1 in synsets1:
        # Пройдемося по всіх синонімах для другого слова
        for synset2 in synsets2:
            # Знаходимо спільних батьківських об'єктів (гіпероніми)
            hypernyms = synset1.lowest_common_hypernyms(synset2)
            if hypernyms:
                common_hypernym = hypernyms[0]
                distance_synset1 = synset1.shortest_path_distance(common_hypernym)
                distance_synset2 = synset2.shortest_path_distance(common_hypernym)
                common_hypernyms.append((synset1, synset2, common_hypernym, distance_synset1, distance_synset2))

        if common_hypernyms:
            for synset1, synset2, common_hypernym, distance_synset1, distance_synset2 in common_hypernyms:
                print(
                    f"Пара синсетів: {synset1.name()} - {synset2.name()} - Спільний батьківський об'єкт: {common_hypernym.name()}")
                print(f"Визначення синсету 1: {synset1.definition()}")
                print(f"Визначення синсету 2: {synset2.definition()}")
                print(f"Визначення спільного батьківського об'єкта: {common_hypernym.definition()}")
                print(f"Довжина шляху для синсету 1: {distance_synset1}")
                print(f"Довжина шляху для синсету 2: {distance_synset2}\n")
        else:
            print("Спільний батьківський об'єкт не знайдено")
    else:
        print("Спільний батьківський об'єкт не знайдено")

def preprocess(text):
    # Tokenize the input text into words
    tokens = word_tokenize(text.lower())

    # Remove stop words and punctuation
    stop_words = set(stopwords.words('english'))
    content_words = [word for word in tokens if word.isalnum() and word not in stop_words]

    return content_words

def lesk(word, context):
    # Get WordNet synsets for the ambiguous word
    word_synsets = wn.synsets(word)

    if not word_synsets:
        return None  # Word not found in WordNet

    best_sense = None
    max_overlap = -1

    for sense in word_synsets:
        # Get the gloss (definition) of the sense
        gloss = sense.definition()

        # Preprocess the gloss
        gloss_words = preprocess(gloss)

        # Preprocess the context
        context_words = preprocess(context)

        # Calculate the overlap between gloss words and context words
        overlap = len(set(gloss_words) & set(context_words))

        if overlap > max_overlap:
            max_overlap = overlap
            best_sense = sense

    return best_sense

if __name__ == "__main__":

    while True:
        print("Оберіть функцію:")
        print("1 - змістовна близкість. Найлижчий спільний батьківський об'кєт")
        print("2 - побудова графу для візуалізації проміжних об'єктів")
        print("3 - визначення значення багатозначного слова залежно від контексту")
        print("4 - побудова шляху для кожної пари синсетів")
        print("5 - вийти")

        choice = input("Введіть номер функції: ")

        if choice == "1":
            word1 = input("Введіть перше слово: ")
            word2 = input("Введіть друге слово: ")
            find_common_hypernym1(word1, word2)

        elif choice == "2":
            word1 = input("Введіть перше слово: ")
            word2 = input("Введіть друге слово: ")
            G = build_hypernym_tree(word1, word2)

            pos = nx.spring_layout(G, seed=42)
            labels = {node: node for node in G.nodes()}  # Використовуємо імена вузлів як підписи

            plt.figure(figsize=(12, 8))
            # Визначаємо кольори вузлів
            node_colors = [
                'red' if node.split(".")[0] in [h.name().split(".")[0] for h in common_hypernyms] else 'skyblue' for
                node in G.nodes()]
            nx.draw(G, pos, with_labels=True, labels=labels, node_size=2000, node_color=node_colors, font_size=10,
                    font_color='black', font_weight='bold')
            edge_labels = nx.get_edge_attributes(G, 'label')
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
            plt.title(f"Гіперонімічне дерево з ієрархією та проміжними об'єктами: {word1} та {word2}")
            plt.show()

        elif choice == "3":
            context = input("Введіть речення: ")
            ambiguous_word = input("Введіть неоднозначне слово: ")
            disambiguated_sense = lesk(ambiguous_word, context)
            if disambiguated_sense:
                print("Ambiguous Word:", ambiguous_word)
                print("Context:", context)
                print("Disambiguated Sense:", disambiguated_sense.name(), "-", disambiguated_sense.definition())
            else:
                print("No sense found for the ambiguous word in WordNet.")

        elif choice == "4":
            word1 = input("Введіть перше слово: ")
            word2 = input("Введіть друге слово: ")

            common_hypernyms = find_common_hypernym2(word1, word2)

            if common_hypernyms:
                for synset1, synset2, common_hypernym in common_hypernyms:
                    visualize_path(synset1, synset2, common_hypernym)
            else:
                print("Спільний батьківський об'єкт не знайдено")

        elif choice == "5":
            break

        else:
            print("Невірний вибір. Спробуйте ще раз.")




