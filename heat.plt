#!/usr/bin/env gnuplot

files = system('ls output*.csv')
i = 1

set terminal pngcairo size 1920,1080 enhanced
set datafile separator ','
set yrange[0:1050]
set xrange[0:10240]

do for [file in files] {
  set output sprintf('%s.png', file)
  set title sprintf("Step %06d", 1000*i)
  plot file using 1:2
  i = i + 1
}
