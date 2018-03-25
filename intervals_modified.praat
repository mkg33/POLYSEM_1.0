	#Mark non-silent intervals of a Sound object in a TextGrid.
#
#	J J A Pacilly, 20-jun-2006, for Conny Kutsch Lojenga
#	J J A Pacilly, 24-jan-2010, for Lilie Roosman,
#	  use different minimum length for silent vs. non-silent intervals
#	J J A Pacilly, 16-jan-2013, some improvements for Willemijn Heeren
#	J J A Pacilly, 24-feb-2017, update syntax
#   modified by Maja Gwozdz, 02-May-2017


 threshold = 40
 minimum_Silence = 0.2
 minimum_Signal = 0.1

#add file here:

Read from file... 'file$'

idSnd = selected("Sound")
name$ = selected$("Sound")
idTG  = To TextGrid: "Tmp 'name$' Tmp", ""
selectObject: idSnd
selectObject = idTG
idInt = To Intensity: 100, 0, "yes"

#add TG here:


#
#	Find Threshold crossings
#
interval  = 1
intensity = Get value in frame: 1
if intensity < threshold
  sound = 0
else
  sound = 1
  endif

nrframes = Get number of frames
for frame from 2 to nrframes
  selectObject: idInt
  intensity = Get value in frame: frame
  if sound == 0 and intensity > threshold or sound == 1 and intensity < threshold
    time = Get time from frame number: frame
    selectObject: idTG
    if sound == 0
      Insert boundary: 1, time
      Set interval text: 1, interval+1, "."
      sound = 1
    else
      Insert boundary: 1, time
      Set interval text: 1, interval, "."
      sound = 0
      endif
    interval = interval + 1
    endif
  endfor

removeObject: idInt


Set interval text: 3, 1, "#add label here:"



#
#	Copy only Intervals which meet criteria
#
selectObject: idTG
nrIntervals = Get number of intervals: 1
defInterval = 1
prevLabel$  = "*"



for interval to nrIntervals
  start  = Get starting point: 1, interval
  end    = Get end point: 1, interval
  label$ = Get label of interval: 1, interval
  duration = end - start
  if label$  = "" and duration > minimum_Silence or
...  label$ != "" and duration > minimum_Signal
    if prevLabel$ != label$
      if interval != 1
        Insert boundary: 2, start
        defInterval = defInterval + 1
        endif
      if label$ != ""
        Set interval text: 2, defInterval, "non-silent interval"
        endif
      prevLabel$ = label$
      endif
    endif
  endfor




Remove tier: 1




Write to text file... 'idTG$'






# cleaning up
select all
Remove
clearinfo
printline The file has been processed.
printline The TextGrid has been output to #add outpath here:
