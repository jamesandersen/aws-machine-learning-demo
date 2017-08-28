import numpy as np
import itertools
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.ticker as ticker

def plot_correlation_matrix(data):
    """Plots a correlation matrix of the data set"""
    sns.reset_orig()
    fig = plt.figure(figsize=(15,15))
    ax = fig.add_subplot(111)
    cax = ax.matshow(data.corr(), cmap=plt.cm.Blues)
    fig.colorbar(cax)

    ax.set_xticklabels(data, rotation=60)
    ax.set_yticklabels(data)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(1))

    plt.show()

def plot_history(history, save_file = None):
    """Plost accuracy and loss for a Keras history object"""

    plt.rcParams["figure.figsize"] = [16, 5]
    plt.rcParams["axes.titlesize"] = 18
    plt.rcParams["axes.labelsize"] = 16
    plt.rcParams["xtick.labelsize"] = 12
    plt.rcParams["ytick.labelsize"] = 12
    plt.rcParams['legend.loc'] = 'upper right'
    plt.rcParams['legend.framealpha'] = 0.7
    plt.rcParams["legend.fontsize"] = 14

    # Plot accuracy
    plt.subplot(1, 2, 1)
    plt.plot(history.history['acc'])
    plt.plot(history.history['val_acc'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'valid.'], loc='upper left')

    # Plot loss
    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'valid.'], loc='upper left')

    # adjust size
    plt.tight_layout()
    if save_file is None:
        plt.show()
    else:
        plt.savefig(save_file)
        plt.close()

def fmt_pct(x, pos):
    """Format as percentage"""
    return '{:.0%}'.format(x)

def plot_confusion_matrix(conf_matrix, classes,
                          title='Confusion matrix', save_file = None):
    """
    This function prints and plots the confusion matrix.
    The style is *roughly* similar to the AWS machine learning confusion matrix
    """

    correct_mask = np.ones(conf_matrix.shape, dtype=bool)
    wrong_mask = np.zeros(conf_matrix.shape, dtype=bool)
    for i in range(conf_matrix.shape[0]):
        correct_mask[i,i] = False
        wrong_mask[i,i] = True
        row_sum = sum(conf_matrix[i])
        for j in range(conf_matrix.shape[1]):
            conf_matrix[i, j] = conf_matrix[i, j] / row_sum

    correct_matrix = np.ma.masked_array(conf_matrix, mask=correct_mask)
    wrong_matrix = np.ma.masked_array(conf_matrix, wrong_mask)

    fig,ax = plt.subplots(figsize=(8, 8))
    blue_map = colors.LinearSegmentedColormap.from_list('custom blue', ['#f1eef6', '#025a90'], N=10)
    blue_map.set_under(color='white')

    red_map = colors.LinearSegmentedColormap.from_list('custom blue', ['#feeddd', '#a83500'], N=10)
    red_map.set_under(color='white')
    
    plot_correct = ax.imshow(correct_matrix,interpolation='nearest',cmap=blue_map, vmin=0.000001, vmax=1)
    plot_wrong = ax.imshow(wrong_matrix,interpolation='nearest',cmap=red_map, vmin=0.000001, vmax=1)
    
    colorbar_wrong = plt.colorbar(plot_wrong, shrink=0.35, orientation='horizontal', pad=-0.11, format=ticker.FuncFormatter(fmt_pct))
    colorbar_correct = plt.colorbar(plot_correct, shrink=0.35, orientation='horizontal', pad=0.03)
    plt.xlabel('Predicted Values')
    plt.ylabel('True Values')
    ax.xaxis.set_label_position('top')
    ax.xaxis.tick_top()
    ax.set_xticklabels([''] + classes)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.set_yticklabels([''] + classes)
    ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
    colorbar_correct.ax.text(-0.3,0.25,'CORRECT',rotation=0)
    colorbar_wrong.ax.text(-0.35,0.25,'INCORRECT',rotation=0)
    plt.setp(colorbar_correct.ax.get_xticklabels(), visible=False)

    thresh = conf_matrix.max() / 2.
    for i, j in itertools.product(range(conf_matrix.shape[0]), range(conf_matrix.shape[1])):
        cell_label = "{:.1%}".format(conf_matrix[i, j])
        plt.text(j, i, cell_label,
                 horizontalalignment="center",
                 color="white" if conf_matrix[i, j] > thresh else "black")

    plt.tight_layout()
    if save_file is None:
        plt.show()
    else:
        plt.savefig(save_file, dpi=72)
        plt.close()