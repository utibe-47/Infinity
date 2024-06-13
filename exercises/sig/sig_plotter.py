import matplotlib.pyplot as plt


class Plotter:

    @staticmethod
    def plot_scatter(data, y_label, name, save_plot=False):
        plt.scatter(data.index, data[y_label])
        plt.xlabel('Date')
        plt.ylabel(y_label[0])
        if save_plot:
            plt.savefig(name + '.png')
        plt.show()

    @staticmethod
    def plot(data, y_label, name, save_plot=False):
        data.plot(y=y_label, use_index=True, kind="line", figsize=(10, 10))
        plt.xlabel('Date')
        if save_plot:
            plt.savefig(name + '.png')
        plt.show()
