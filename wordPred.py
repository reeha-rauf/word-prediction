import numpy as np

# Markov chain stored as adjacency list.
lexicon = {}

def update_lexicon(current, next_word):

    # Add the input word to the lexicon if it in there yet.
    if current not in lexicon:
        lexicon.update({current: {next_word: 1} })
        return

    # Recieve te probabilties of the input word.
    options = lexicon[current]

    # Check if the output word is in the propability list.
    nextW = next_word.strip().split(' ')
    for word in nextW:
        if word not in options:
            options.update({word : 1})
        else:
            options.update({word : options[word] + 1})

    # Update the lexicon
    lexicon[current] = options

# Populate lexicon
def predict_data():
    with open('dataset.txt', 'r') as dataset:
        for line in dataset:
            words = line.strip().split(' ')
            for i in range(len(words) - 1):
                update_lexicon(words[i], words[i+1]) 
    # Adjust propability
    for word, transition in lexicon.items():
        transition = dict((key, value / sum(transition.values())) for key, value in transition.items())
        lexicon[word] = transition

def predict_horror():
    with open('HorrorStories.txt', 'r', encoding='utf-8') as dataset:
        for line in dataset:
            words = line.strip().split(' ')
            for i in range(len(words) - 1):
                try:
                    ordered = words[i]+" " + words[i+1]
                    update_lexicon(ordered, words[i+2])
                except IndexError:
                    continue;
                
    # Adjust propability
    for word, transition in lexicon.items():
        transition = dict((key, value / sum(transition.values())) for key, value in transition.items())
        lexicon[word] = transition


# Predict next word
def predict():
    predict_data()
    while True:
        line = input('> ')
        if line == ":q":
            break;
        word = line.strip().split(' ')[-1]
        if word not in lexicon:
            print('Word not found')
            next_word = input("Enter next word: ")
            update_lexicon(word, next_word)
        else:
            options = lexicon[word]
            predicted = np.random.choice(list(options.keys()), p=list(options.values()))
            print(line + ' ' + predicted)


def horror(start):
    story = list(start.split())
    predict_horror()
    
    while True:
        if story[-1][-1] in ".?":  # Check for end punctuation
            con = input("Continue? (y/n): ")
            if con.lower() != 'y':
                break;
        word = story[-2]+ " " + story[-1] if len(story) >= 2 else story[-1]
    
        if word not in lexicon:
            next_word = input(f"Add a word/sentence to '{word}': ")
            update_lexicon(word, next_word)
        else:
            options = lexicon[word]
            predicted = np.random.choice(list(options.keys()), p=list(options.values()))
            story.append(predicted)
    final = ' '.join(story)
    print(final)


# predict()
horror("A")

