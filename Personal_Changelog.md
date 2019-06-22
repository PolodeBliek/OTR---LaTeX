##22-06
**10:05**
**TESSERACT PROBLEM**
STATE: UNTREATED
IMPORTANCE: FATAL
SYMPTOMS: (py)Tesseract currently doesn't recognize text, very weird problem.

OBSERVATION: Currently I've manually cropped to relatively same sizes of the same tables/images and parsed it through the standalone OCRTest.py software and it does give the results wanted. Tesseract should be able to handle the text elements which re almost exactly the same but it doesn't.

DIAGNOSING:
Possibilities:
* The float64 to uint8 conversion isn't implemented, most likely as this step is skipped with the standalone OCRTest by manually cropping the image beforehand in standalone photo (windows) software
* Crop isn't perfect on all text elements, sometimes lines are still visible at border (both vertical and horizontal; can be fixed by re-implementing the -5, +5 crop procedure previously removed)

**ADDITIONAL TESSERACT PROBLEM/TEXT ELEMENTS LENGTH**
STATE:      UNTREATED
IMPORTANCE: FATAL
PROBLEM:    Not all text elements are parsed through PyTesseract

OBSERVATION:
When (py)Tesseract doesn't recognize a certain piece of text it doesn't return anything what so ever, this seems to _corrupt_ the variable assigned to it. The value isn't None or an empty string, have yet to find out what this mystery is.

DIAGNOSING: Mystery

**UNRECOGNIZED NEGATIVE COLUMN/ROW SPLITS**
STATE:      POSSIBLE CURE - NEEDS TESTING
IMPORTANCE: HIGH
PROBLEM:    Not all splits of rows and columns are recognized

OBSERVATION:
Doesn't recognize negative space columns or rows in certain (see example9)

DIAGNOSING:
Problem related to 1 of 2 factors:
1. Table has partial actual columns or rows which makes the process of finding negative column/rows splits difficult because not the entire negative split is actually perfect negative space
2. Not clear negative split, table isn't properly designed and there isn't a clear divide. Would argue this isn't my problem but the problem of the makers of the table but hey, guess I'll have to deal with it. USE LATEX FOR FUCKS SAKE

CURE:
1. Keep locations of (actual) splits in mind when looking for these negative space columns or rows.
2. Individual text elements searching, needs to be further researched, can't mess negative space columns with things like normal text spaces or new lines.
