import pandas as pd
import re
import itertools
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import distance
import networkx as nx
import function_words

data = pd.read_csv("doc_words.csv")
print(len(data))

docs = data["words"].values

fw = function_words.function_words

doc_words = []
for doc in docs:
    words = [x for x in doc.split() if x not in fw]
    doc_words.append(words)

print(len(doc_words))


word_cnt = {}
for words in doc_words:
    for word in words:
        if word not in word_cnt:
            word_cnt[word] = 1
        else:
            word_cnt[word] += 1

print(word_cnt)

word_cnt_df = pd.DataFrame(
    {"word": [k for k in word_cnt.keys()], "cnt": [v for v in word_cnt.values()]}
)

print("word_cnt_df")
print(len(word_cnt_df))

print(word_cnt_df[["cnt"]].describe())

"""
tmp = word_cnt_df[word_cnt_df["cnt"] > 3]
tmp.sort_values(by="cnt", ascending=False).plot(
    kind="bar", x="word", y="cnt", figsize=(15, 7), legend=False
)
# plt.show()
"""


vocab = {}
target_words = word_cnt_df[word_cnt_df["cnt"] > 5]["word"].values
for word in target_words:
    if word not in vocab:
        vocab[word] = len(vocab)

re_vocab = {}
for word, i in vocab.items():
    re_vocab[i] = word

print("vocab")
print(len(vocab))
print(vocab)


doc_combinations = [list(itertools.combinations(words, 2)) for words in doc_words]
combination_matrix = np.zeros((len(vocab), len(vocab)))

for doc_comb in doc_combinations:
    for comb in doc_comb:
        if comb[0] in target_words and comb[1] in target_words:
            combination_matrix[vocab[comb[0]], vocab[comb[1]]] += 1
            combination_matrix[vocab[comb[1]], vocab[comb[0]]] += 1

for i in range(len(vocab)):
    combination_matrix[i, i] /= 2

print(combination_matrix)

jaccard_matrix = 1 - distance.cdist(combination_matrix, combination_matrix, "jaccard")

print(jaccard_matrix)


nodes = []

for i in range(len(vocab)):
    for j in range(i + 1, len(vocab)):
        jaccard = jaccard_matrix[i, j]
        if jaccard > 0:
            nodes.append(
                [
                    re_vocab[i],
                    re_vocab[j],
                    word_cnt[re_vocab[i]],
                    word_cnt[re_vocab[j]],
                    jaccard,
                ]
            )

print(len(nodes))

G = nx.Graph()
G.nodes(data=True)

for pair in nodes:
    node_x, node_y, node_x_cnt, node_y_cnt, jaccard = (
        pair[0],
        pair[1],
        pair[2],
        pair[3],
        pair[4],
    )
    if not G.has_node(node_x):
        G.add_node(node_x, count=node_x_cnt)
    if not G.has_node(node_y):
        G.add_node(node_y, count=node_y_cnt)
    if not G.has_edge(node_x, node_y):
        G.add_edge(node_x, node_y, weight=jaccard)

plt.figure(figsize=(30, 30))
pos = nx.spring_layout(G, k=0.8)

node_size = [d["count"] * 100 for (n, d) in G.nodes(data=True)]
nx.draw_networkx_nodes(G, pos, node_color="bisque", alpha=0.8, node_size=node_size)
nx.draw_networkx_labels(G, pos, font_size=9, font_family="arial")

edge_width = [d["weight"] * 10 for (u, v, d) in G.edges(data=True)]
nx.draw_networkx_edges(G, pos, alpha=0.1, edge_color="darkred", width=edge_width)
plt.savefig("graph.jpg", dpi=300)

plt.axis("off")
# plt.show()
