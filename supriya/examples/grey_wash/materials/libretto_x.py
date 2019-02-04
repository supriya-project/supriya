import supriya

"""
Via https://github.com/julianchurchill/text-adventure/blob/master/config/1/res/raw/walkthrough.txt
"""

material = []

voices = ["Daniel", "Tessa", "Karen", "Thomas"]

texts = [
    "Examine bags of junk.",
    "Examine pile of leaves.",
    "Go clock tower door.",
    "Go down.",
    "Go east.",
    "Go north.",
    "Go passageway.",
    "Go ramshackle shed.",
    "Go south.",
    "Go up.",
    "Go west.",
    "Take clock face.",
    "Take clock hour hand.",
    "Take clock minute hand.",
    "Take dust of the ancients.",
    "Take frayed rope.",
    "Take old dirty bone.",
    "Take skeleton key.",
    "Take spade.",
    "Use clock face with clock mechanism.",
    "Use clock hour hand with clock mechanism.",
    "Use clock minute hand with clock mechanism.",
    "Use frayed rope with candlestick.",
    "Use old dirty bone with massive wolf.",
    "Use skeleton key with locked door.",
    "Use spade with mound of earth.",
]

for voice in voices:
    for text in texts:
        material.append(supriya.Say(text, voice=voice))

libretto_x = tuple(material)
