from matplotlib import pyplot as plt, colors, cm
import numpy as np

hue = np.arange(0, 2* np.pi, 1/360)
hue_array = np.ones_like(hue)

hsv_map = plt.get_cmap('hsv')
norm = colors.Normalize(0, 2*np.pi)

tick_units = np.pi/3

fig = plt.figure(figsize=(5, 5))
# rgb_color = colors.hsv_to_rgb(hue)
ax = plt.subplot(polar=True)

theta_ticks = np.arange(0, 6, 1) * tick_units
ax.xaxis.set_ticks(theta_ticks)
ax.xaxis.set_ticklabels(
    ['0\N{DEGREE SIGN}\nred',
     '60\N{DEGREE SIGN}\nyellow',
     '120\N{DEGREE SIGN}\ngreen',
     '180\N{DEGREE SIGN}\ncyan',
     '240\N{DEGREE SIGN}\nblue',
     '300\N{DEGREE SIGN}\npurple'], fontsize=16
)
ax.tick_params(pad=-70, rotation='auto', grid_alpha=0.3)

for n in theta_ticks:
    ax.plot([n, n], [1.0, 1.1], linewidth=4, color=[0, 0, 0])

ax.plot(hue, np.full_like(hue, 0.7), c=[0,0,0])
ax.scatter(hue, hue_array, c=hue, s=80, cmap=hsv_map)
ax.set_rlim([0.5, 1.1])
ax.set_yticks([])
ax.set_theta_zero_location('N')
ax.set_theta_direction(-1)
plt.show()

