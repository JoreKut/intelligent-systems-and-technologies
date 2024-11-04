import streamlit as st
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap

from schelling_model import EntitiesFractionConfig, SchellingModel

st.title("Schelling's Model of Segregation")

population_size = st.sidebar.slider("Размер поля", 10, 70, 25)
empty_ratio = st.sidebar.slider("Доля свободных", 0., 1., .2)

red_fraction = st.sidebar.slider("Отношение видов Красные% - Синие%", 0., 100., 50., format="%f%%")

n_iterations = st.sidebar.number_input("Number of Iterations", 10)

entity_fraction_config = EntitiesFractionConfig(
    red_fraction=red_fraction / 100.0,
    blue_fraction=1.0 - red_fraction / 100.,
)
model_map = SchellingModel(
    n=population_size,
    entity_fraction_config=entity_fraction_config,
    empty_fraction=empty_ratio,
    web_view=True,
)

# Plot the graphs at initial stage
plt.style.use("ggplot")
plt.figure(figsize=(8, 4))

# Left hand side graph with Schelling simulation plot
cmap = ListedColormap(['red', 'white', 'royalblue'])
plt.subplot(121)
plt.axis('off')
plt.pcolor(model_map.field, cmap=cmap, edgecolors='w', linewidths=1)

# Right hand side graph with Mean Similarity Ratio graph
plt.subplot(122)
plt.xlabel("Iterations")
plt.xlim([0, n_iterations])
plt.ylim([0, 200])
plt.title("Unsatisfied entities", fontsize=15)

unsatisfied_count_list = [model_map.get_unsatisfied_count()]

city_plot = st.pyplot(plt)
progress_bar = st.progress(0)

if st.sidebar.button('Run Simulation'):

    for i in range(n_iterations):
        model_map.do_iteration()
        model_map.recalculate_ranks()

        unsatisfied_count_list.append(model_map.get_unsatisfied_count())
        plt.figure(figsize=(8, 4))

        plt.subplot(121)
        plt.axis('off')
        plt.pcolor(model_map.field, cmap=cmap, edgecolors='w', linewidths=1)

        plt.subplot(122)
        plt.xlabel("Iterations")
        plt.xlim([0, n_iterations])
        plt.ylim([0, 200])

        plt.title("Mean Unsatisfied Entity Count", fontsize=15)
        plt.plot(list(range(1, len(unsatisfied_count_list) + 1)), unsatisfied_count_list)
        plt.text(1, 180.95, "Количество несчастных: %.4f" % model_map.get_unsatisfied_count(), fontsize=10)

        city_plot.pyplot(plt)
        plt.close("all")
        progress_bar.progress((i + 1.) / n_iterations)

        if model_map.is_everyone_satisfied():
            progress_bar.progress(1)
            break
