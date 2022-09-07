# python-wordle

This is a Python implementation of a wordle assistant - mostly made to learn Python rather than to
do anything practical.  Use it if you like it.  If you just run it, it plays Wordle on a random word.
If you run it with "-w stain", it'll use 'stain' as the answer and you can play it from there.

The more interesting one to play with is accessed by running it with "-a", which let's you see
how many possible answers there are given the guesses/hints you received.  Note that the "hint"
characters are:

*space* - No match at all

*carat* - A yellow match - meaning the letter is there, but the position is wrong.

*equal* - A green match - meaning the letter letter at that position is equal to what's in the answer.

The "ratings" that come out of "rate" and "suggest" are the number of possible matches that will
remain if you make that guess.

The performance for 'rate' and 'suggest' isn't great.  "suggest" with no data will take a very long
time (not sure how long, but longer than is sensible).  And alas, there's no way to cancel it.
It'd sure be nice if there were a way - I looked into trapping ctrl+c, but gave up after a while
because it just didn't work well at all in Windows.  Oddly, Ctrl+C works immediately in the terminal
Window inside VSCode but doesn't register immediately in either cmd.exe or Windows Terminal, making
it pretty much useless.  I don't care enough about it to try and figure it out.
