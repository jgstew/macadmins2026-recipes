# Step 1 — a plain Python script.
#
# Run it:  python3 stages/01_hello.py
#
# This works fine as a script, but it is NOT an AutoPkg processor. AutoPkg never
# runs loose scripts like this: it has no way to hand it values or to collect a
# result. Everything in the steps that follow turns this one line into something
# AutoPkg can actually run inside a recipe.

print("Hello World!")
