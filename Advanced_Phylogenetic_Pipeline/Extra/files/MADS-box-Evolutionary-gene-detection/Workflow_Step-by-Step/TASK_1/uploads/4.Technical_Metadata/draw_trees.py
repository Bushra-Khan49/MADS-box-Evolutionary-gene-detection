import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from Bio import Phylo

def draw_tree(tree_path, output_png, title):
    tree = Phylo.read(tree_path, 'newick')
    # Count terminals to set fig size appropriately
    terminals = len(tree.get_terminals())
    fig_height = max(10, terminals * 0.25)
    fig = plt.figure(figsize=(15, fig_height))
    ax = fig.add_subplot(1, 1, 1)
    
    Phylo.draw(tree, do_show=False, axes=ax, label_func=lambda n: n.name if n.name else '')
    plt.title(title)
    plt.savefig(output_png, bbox_inches='tight', dpi=300)
    plt.close(fig)

trees = [
    ('Rice_ClustalO_ML.treefile', 'Rice_Full_Proteome.png', 'Rice ML Tree (Full Proteome)'),
    ('Rice_MADS_Domain_ML.treefile', 'Rice_MADS_Domain.png', 'Rice + AT MADS Domain Tree'),
    ('Rice_Kbox_Domain_ML.treefile', 'Rice_Kbox_Domain.png', 'Rice + AT K-box Domain Tree')
]

for t, o, title in trees:
    try:
        draw_tree(t, o, title)
        print(f"Generated {o}")
    except Exception as e:
        print(f"Error on {t}: {e}")
