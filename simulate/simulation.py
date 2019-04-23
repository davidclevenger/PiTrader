import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

#idx = [0]
fig = plt.figure()
my_plot = fig.add_subplot(111)
portfolio_value = [10000.0]

def animate(i):
    global a
    global portfolio_value

    #idx.append(len(idx))

    last = portfolio_value[len(portfolio_value)-1]
    new_value = np.random.normal(1.001 * last, last * 0.004)
    portfolio_value.append(new_value)

    my_plot.clear()
    my_plot.set_title("Portfolio Value")
    my_plot.set_xlabel("Days since inception")
    my_plot.set_ylabel("Value (USD)")
    my_plot.plot(portfolio_value)

if __name__ == "__main__":

    my_plot.plot(portfolio_value)
    ani = animation.FuncAnimation(fig, animate, interval=1000, blit=False, frames=5)
    plt.show()


