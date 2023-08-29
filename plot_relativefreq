import pickle
import matplotlib.pyplot as plt


with open('error_data.pickle', 'rb') as f:
    all_data = pickle.load(f)

aggregate_relative_frequencies = all_data['aggregate_relative_frequencies']


nationalities = ['es', 'de', 'en', 'fr']
proficiency_levels = [1, 2, 3]


fig, axes = plt.subplots(nrows=len(nationalities), ncols=len(proficiency_levels), figsize=(15, 12), sharex=True, sharey=True)
plt.subplots_adjust(wspace=0.05, hspace=0.20)


error_colors = {}


for i, nat in enumerate(nationalities):
    for j, level in enumerate(proficiency_levels):
        ax = axes[i, j] 
        

        frequencies = aggregate_relative_frequencies[level][nat]
        

        top_errors = sorted(frequencies, key=frequencies.get, reverse=True)[:8]
        top_frequencies = [frequencies[error] for error in top_errors]
        

        error_colors_subset = []
        for error in top_errors:
            error_type = error.split('_')[0]
            if error_type not in error_colors:
                error_colors[error_type] = plt.cm.tab10(len(error_colors))  
            error_colors_subset.append(error_colors[error_type])
        
        ax.bar(top_errors, top_frequencies, color=error_colors_subset)
        

        if top_frequencies:
            ax.set_ylim(0, max(top_frequencies) + 0.09)

        
        

        if j == 0:
            label = ax.set_ylabel(nat.upper(), rotation=0, labelpad=20)  
            label.set_y(0.4)  

        if i == 0:
            ax.set_title(f'Year of study: {level}')



plt.savefig('output_plot.png', dpi=300)



plt.tight_layout()
plt.show()
