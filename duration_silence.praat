#add name here:
#add dir here:
#add grid here:
#Specify the name of the output file

outfile$ = dir$+"xxx.txt"


Read from file... 'dir$''name$'.wav
select Sound 'name$'

Read from file... 'dir$''text$'.TextGrid
select TextGrid 'text$'

nInterv = Get number of intervals... 1
for j from 1 to 'nInterv'

lab$ = Get label of interval... 1 'j'
if lab$ = ""
beg = Get starting point... 1 'j'
end = Get end point... 1 'j'
dur= end-beg
mid = (dur/2)+beg
durms = dur*1000


fileappend 'outfile$' 'durms:0' 'newline$'
endif
endfor


