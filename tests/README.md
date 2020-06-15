# Test Files

These are the test files I use to validate my library algorithms and structure.

I feel that it'll be useful to programmers to see how various functions can be used

## Important

Due to .ojn and .ojm having data about the song, I will not be including them.

I understand that ojn only has the note data but I will not be including it just as a precaution as it still contains
the song instrumental sequencing / patterns.

## Plug and Test

The tests are very simple to swap variables with, note that most files can be quickly accessed using RSC_PATH imports,
e.g. `OSU_ESCAPES`. 

However, if you want to use a custom file, you'd have to change the file path or append to RSC_PATH.

## Profiling

Some tests will have a `@profile` decorator, you can uncomment it to check what processes took the longest.
