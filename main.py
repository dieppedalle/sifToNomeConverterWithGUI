# main.py is used to convert .sif files to .nom
import re
import sys

from Tkinter import *




listMeshes = list()
listFaces = list()
newFaces = list()

def convertFileToString(filename):
    """
    Function is open input file and store it as a string
    """
    with open(filename, 'r') as myfile:
        data=myfile.read()
    return data

def tokenize(chars):
    """
    Convert file from a string to an array of tokens
    """
    return chars.replace('(', ' ( ').replace(')', ' ) ').split()

def parse(tokens):
    """
    Parses the file to remove parenthesis
    """
    if (len(tokens)==0):
        raise SyntaxError("File is empty")
    currentToken = tokens.pop(0)

    if currentToken == '(':
        currentList = list()
        while tokens[0] != ')':
            currentList.append(parse(tokens))
        tokens.pop(0)
        return currentList
    elif currentToken == ')':
        raise SyntaxError("Missing opening parenthesis")
    else:
        return currentToken

totalNumberVertices = 0
numberVertices = 0
def eval(x, outputFile, isSquare):
    """
    Writes the converted files to an output file
    """
    global numberVertices
    global totalNumberVertices
    if not isinstance(x, list):
        return x
    elif x[0] == "vertices":
        numberVertices = int(x[1])
        currentVertex = 0

        # Converts vertices to .nom syntax
        for i in range(numberVertices):
            outputFile.write("point v" + str(totalNumberVertices + i) + " (" + x[(2+i)][1] + " " + x[(2+i)][2] + " " + x[(2+i)][3] + ") endpoint\n")
        outputFile.write("\n")
        totalNumberVertices += numberVertices
    elif x[0] == "triangles":
        listFaces = []
        newFaces = []
        numberTriangles = int(x[1])
        currentTriangle = 0

        meshName = "SIFmesh" + str(len(listMeshes))
        listMeshes.append(meshName)

        outputFile.write("mesh " + meshName + "\n")

        for i in range(numberTriangles):
            listFaces.append(x[(2+i)][1:])

        # Checks if we need to convert triangle faces to rectangles

        for element in listFaces:
            if len(element)>3:
                listFaces.remove(element)
                newFaces.append(element)

        print(isSquare)
        if isSquare == "True":

            mergeFaces(listFaces, newFaces)

        for i, element in enumerate(listFaces):
            outputFile.write("face f" + str(i) + " (")

            for i, vertex in enumerate(element):
                if i != 0:
                    outputFile.write(" ")
                outputFile.write("v" + str(totalNumberVertices-numberVertices + int(vertex)))
            outputFile.write(") endface\n")

        #print(newFaces)
        # Checks whether ot not there are any rectangle faces to add
        for i, element in enumerate(newFaces):
            outputFile.write("face f" + str(len(listFaces)+i) + " (")

            for i, vertex in enumerate(element):
                if i != 0:
                    outputFile.write(" ")
                outputFile.write("v" + str(totalNumberVertices-numberVertices + int(vertex)))
            outputFile.write(") endface\n")
        outputFile.write("endmesh\n\n")

    else:
        # Continue to process data
        proc = eval(x[0], outputFile, isSquare)
        args = [eval(arg, outputFile, isSquare) for arg in x[1:]]

def createMeshes(outputFile):
    """
    Writes all the meshes created to the outputFile
    """
    for i, mesh in enumerate(listMeshes):
        outputFile.write("instance  mesh" + str(i) + " " + mesh + " scale (1 1 1)  endinstance\n")

def createOutputFile():
    """
    Create an output stream
    """
    outputFile = open(outputName, "w")
    outputFile.write("####  CONVERTED FROME A SIF  FILE  ####\n\n")
    return outputFile

def removeComments(stringFile):
    """
    Removes all of the comments from the string
    """
    stringFile=stringFile.replace('\n', ' ')
    return (re.sub("(\(\*).*?(\*\))", "", stringFile))

def mergeFaces(listFaces, newFaces):
    """
    Function used to merge triangles faces into rectangle faces
    """
    while len(listFaces) != 0:
        currentList = listFaces.pop(0)
        for i, element in enumerate(listFaces):
            if len(list(set(currentList).intersection(element))) == 2:
                #Added
                indexToInsert1 = currentList.index(list(set(currentList).intersection(element))[0])+1
                indexToInsert2 = currentList.index(list(set(currentList).intersection(element))[1])+1

                indexToInsert = min(indexToInsert1 % 3, indexToInsert2 % 3)
                elementToInsert = list(set(element) - set(list(set(currentList).intersection(element))))[0]

                currentList.insert(indexToInsert, elementToInsert)

                newFaces.append(currentList)

                listFaces.pop(i)
                break;

def main():
    """
    main Function
    """
    global listMeshes
    global listFaces
    global newFaces

    global totalNumberVertices
    global numberVertices
    totalNumberVertices = 0
    numberVertices = 0

    listMeshes = list()
    listFaces = list()
    newFaces = list()
    # Parsing the string
    stringFile = convertFileToString(inputName)
    removeComments(stringFile)
    tokens = tokenize(stringFile)
    arrayFile = parse(tokens)

    outputFile = createOutputFile()

    # Convert .sif to .nom
    eval(arrayFile, outputFile, squarefaces)
    createMeshes(outputFile)





inputName = ""
outputName = ""
squarefaces = ""

def show_entry_fields():
   print("First Name: %s\nLast Name: %s" % (e1.get(), e2.get()))

   global inputName
   global outputName
   global squarefaces
   # Reads the argument from the command
   inputName = e1.get()
   outputName = e2.get()

   # Checks if need to convert triangle faces to rectangles
   #print var1.get()

   if var1.get() == 1:
       squarefaces = "True"
   else:
       squarefaces = "False"

   main()

master = Tk()
master.title("sifToNome Converter")
Label(master, text="Input Path", justify=LEFT, anchor="w", width=9).grid(row=0)
Label(master, text="Output Path", justify=LEFT, anchor="w", width=9).grid(row=1)

e1 = Entry(master, width=40)
e2 = Entry(master, width=40)

e1.grid(row=0, column=1)
e2.grid(row=1, column=1)

var1 = IntVar()
Checkbutton(master, text="Make Rectangular Faces", variable=var1).grid(row=2, columnspan=2, sticky=W)

Button(master, text='Quit', command=master.quit).grid(row=3, column=0, sticky=W, pady=4)
Button(master, text='Convert', command=show_entry_fields).grid(row=3, column=1, sticky=W, pady=4)

mainloop( )
