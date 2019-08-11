def createText():
    textToBeAdded = """\nQPushButton {
    color: blue;
}"""
    return textToBeAdded
    
textToBeAdded = createText()
with open("Style.qss", "a") as f:
    f.write(textToBeAdded)

new = textToBeAdded.replace("blue","orange")

with open("Style.qss", "r+") as f:
    old = f.read() # read everything in the file
    newText = old.replace(textToBeAdded,new)
    f.seek(0) # rewind
    f.write(newText) # write the new line before