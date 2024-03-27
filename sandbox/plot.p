set multiplot layout 5,5 rowsfirst
unset key
unset xtics
unset ytics

plot 'reduced_embedding.dat' u 1:1 index 0 w dots lc rgb 'red', '' u 1:1 index 1 w dots lc rgb 'green', '' u 1:1 index 2 w dots lc rgb 'blue'
plot 'reduced_embedding.dat' u 1:2 index 0 w dots lc rgb 'red', '' u 1:2 index 1 w dots lc rgb 'green', '' u 1:2 index 2 w dots lc rgb 'blue'
plot 'reduced_embedding.dat' u 1:3 index 0 w dots lc rgb 'red', '' u 1:3 index 1 w dots lc rgb 'green', '' u 1:3 index 2 w dots lc rgb 'blue'
plot 'reduced_embedding.dat' u 1:4 index 0 w dots lc rgb 'red', '' u 1:4 index 1 w dots lc rgb 'green', '' u 1:4 index 2 w dots lc rgb 'blue'
plot 'reduced_embedding.dat' u 1:5 index 0 w dots lc rgb 'red', '' u 1:5 index 1 w dots lc rgb 'green', '' u 1:5 index 2 w dots lc rgb 'blue'

 plot 'reduced_embedding.dat' u 2:1 index 0 w dots lc rgb 'red', '' u 2:1 index 1 w dots lc rgb 'green', '' u 2:1 index 2 w dots lc rgb 'blue'
 plot 'reduced_embedding.dat' u 2:2 index 0 w dots lc rgb 'red', '' u 2:2 index 1 w dots lc rgb 'green', '' u 2:2 index 2 w dots lc rgb 'blue'
 plot 'reduced_embedding.dat' u 2:3 index 0 w dots lc rgb 'red', '' u 2:3 index 1 w dots lc rgb 'green', '' u 2:3 index 2 w dots lc rgb 'blue'
 plot 'reduced_embedding.dat' u 2:4 index 0 w dots lc rgb 'red', '' u 2:4 index 1 w dots lc rgb 'green', '' u 2:4 index 2 w dots lc rgb 'blue'
 plot 'reduced_embedding.dat' u 2:5 index 0 w dots lc rgb 'red', '' u 2:5 index 1 w dots lc rgb 'green', '' u 2:5 index 2 w dots lc rgb 'blue'

 plot 'reduced_embedding.dat' u 3:1 index 0 w dots lc rgb 'red', '' u 3:1 index 1 w dots lc rgb 'green', '' u 3:1 index 2 w dots lc rgb 'blue'
 plot 'reduced_embedding.dat' u 3:2 index 0 w dots lc rgb 'red', '' u 3:2 index 1 w dots lc rgb 'green', '' u 3:2 index 2 w dots lc rgb 'blue'
 plot 'reduced_embedding.dat' u 3:3 index 0 w dots lc rgb 'red', '' u 3:3 index 1 w dots lc rgb 'green', '' u 3:3 index 2 w dots lc rgb 'blue'
 plot 'reduced_embedding.dat' u 3:4 index 0 w dots lc rgb 'red', '' u 3:4 index 1 w dots lc rgb 'green', '' u 3:4 index 2 w dots lc rgb 'blue'
 plot 'reduced_embedding.dat' u 3:5 index 0 w dots lc rgb 'red', '' u 3:5 index 1 w dots lc rgb 'green', '' u 3:5 index 2 w dots lc rgb 'blue'

 plot 'reduced_embedding.dat' u 4:1 index 0 w dots lc rgb 'red', '' u 4:1 index 1 w dots lc rgb 'green', '' u 4:1 index 2 w dots lc rgb 'blue'
 plot 'reduced_embedding.dat' u 4:2 index 0 w dots lc rgb 'red', '' u 4:2 index 1 w dots lc rgb 'green', '' u 4:2 index 2 w dots lc rgb 'blue'
 plot 'reduced_embedding.dat' u 4:3 index 0 w dots lc rgb 'red', '' u 4:3 index 1 w dots lc rgb 'green', '' u 4:3 index 2 w dots lc rgb 'blue'
 plot 'reduced_embedding.dat' u 4:4 index 0 w dots lc rgb 'red', '' u 4:4 index 1 w dots lc rgb 'green', '' u 4:4 index 2 w dots lc rgb 'blue'
 plot 'reduced_embedding.dat' u 4:5 index 0 w dots lc rgb 'red', '' u 4:5 index 1 w dots lc rgb 'green', '' u 4:5 index 2 w dots lc rgb 'blue'

 plot 'reduced_embedding.dat' u 5:1 index 0 w dots lc rgb 'red', '' u 5:1 index 1 w dots lc rgb 'green', '' u 5:1 index 2 w dots lc rgb 'blue'
 plot 'reduced_embedding.dat' u 5:2 index 0 w dots lc rgb 'red', '' u 5:2 index 1 w dots lc rgb 'green', '' u 5:2 index 2 w dots lc rgb 'blue'
 plot 'reduced_embedding.dat' u 5:3 index 0 w dots lc rgb 'red', '' u 5:3 index 1 w dots lc rgb 'green', '' u 5:3 index 2 w dots lc rgb 'blue'
 plot 'reduced_embedding.dat' u 5:4 index 0 w dots lc rgb 'red', '' u 5:4 index 1 w dots lc rgb 'green', '' u 5:4 index 2 w dots lc rgb 'blue'
 plot 'reduced_embedding.dat' u 5:5 index 0 w dots lc rgb 'red', '' u 5:5 index 1 w dots lc rgb 'green', '' u 5:5 index 2 w dots lc rgb 'blue'