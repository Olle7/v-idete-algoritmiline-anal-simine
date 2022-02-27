max_j=5
for j_initial in range( 0,max_j ):
    for j_final in range( 0,max_j ):
        if transition_probability( j_initial, j_final ) == 1.0:
            frequencies_in_GHz.append( transition_energy(j_initial,j_final, B )/h*(10**9)
            intensities.append(intensity( j_initial, B, temperature ) )


plt.stem( frequencies_in_GHz, intensities, basefmt='-')
plt.xlabel('Frequencies/GHz')
plt.ylabel('Intensities')
plt.title( 'Raman spectrum for CO at 298 K')
plt.show()