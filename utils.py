import string
import sys



def parse_indat(line):

    atoms = []

    tokens = string.split(line)
    del tokens[-1]

    delims = []

    for i in range(len(tokens)):
        if "-" in tokens[i]:
            delims.append(i)

            tokens[i] = int(tokens[i].lstrip("-"))
        else:
            tokens[i] = int(tokens[i])

    for n in reversed(delims):

        range_atoms = range(tokens[n-1], tokens[n] + 1)

        for i in range_atoms:
            atoms.append(i)
        del tokens[n]
        del tokens[n-1]

    for i in tokens:
        atoms.append(i)
    return atoms


def parse_layer(line):
    layers = []

    tokens = string.split(line.rstrip(",\n"), ",")

    for token in tokens:

        if "LAYER" in token or "IACTFG" in token:
            #layers.append(int(token[-1]))
    
            num = string.split(token, "=")[1]

            layers.append(int(num))
        else:
            layers.append(int(token))
    #print layers
    return layers


def parse_frgnam(line):

    nams = []

    tokens = string.split(line.rstrip(",\n"), ",")

    for token in tokens:

        if "FRGNAM(1)=" in token:
            #layers.append(int(token[-1]))
    
            nam = string.split(token, "=")[1]

            nams.append(nam.strip())
        else:
            nams.append(token.strip())
    #print nams
    return nams


def write_fragments(infile):


    f = open(infile)
    lines = f.readlines()

    frags = []
    fragnams = []
    layers = []
    coords = []

    mode = "search"

    for line in lines:

        if mode == "search":

            if "LAYER(" in line:
                mode = "layer"

            elif "INDAT" in line:
                mode = "indat"

            elif "FRGNAM" in line:
                mode = "frgnam"

            elif "FMOXYZ" in line:
                mode = "fmoxyz"


        if mode == "layer":

            #print line,
            line_layers = parse_layer(line)
            for l in line_layers:
                layers.append(l)

            if ",\n" not in line:
                mode = "search"
                continue



        elif mode == "indat":

            if "0\n" not in line:
                mode = "search"
                continue

            if "INDAT(1)=0" not in line:
                frg_atoms = parse_indat(line)
                frags.append(frg_atoms)


        elif mode == "frgnam":

            # print line

            nams = parse_frgnam(line)

            for nam in nams:

                fragnams.append(nam)

            if ",\n" not in line:
                mode = "search"
                continue


        elif mode == "fmoxyz":
            if "$END" in line:
                mode = "search"
                continue
            if "XYZ" not in line:
                coords.append(line[3:])


    acts = []
    mode = "search"
    for line in lines:

        if mode == "search":

            if "IACTFG" in line:
                mode = "iactfg"

        if mode == "iactfg":
            #print line
            line_layers = parse_layer(line)
            for l in line_layers:
                acts.append(l)
            if ",\n" not in line:
                mode = "search"
                continue

    for i in acts:

        layers[i-1] = 3


    for line in lines:

        if "ISFRG" in line:

            i = int(string.split(line.rstrip("\n"), "=")[1])

            layers[i-1] = 4

            break


    f.close()


    for i, frg in enumerate(frags):

        filename = "%s.xyz" % (fragnams[i])

        f = open(filename, "w")

        f.write("%i\n" % (len(frg)))
        f.write("Comment: %i\n" % (i))

        for n in frg:
            f.write(coords[n-1])

        f.write("\n")

        f.close()
        print "Wrote:", filename



def write_layers(infile):

    f = open(infile)
    lines = f.readlines()

    frags = []
    fragnams = []
    layers = []
    coords = []

    mode = "search"

    for line in lines:

        if mode == "search":

            if "LAYER(" in line:
                mode = "layer"

            elif "INDAT" in line:
                mode = "indat"

            elif "FRGNAM" in line:
                mode = "frgnam"

            elif "FMOXYZ" in line:
                mode = "fmoxyz"


        if mode == "layer":

            #print line,
            line_layers = parse_layer(line)
            for l in line_layers:
                layers.append(l)

            if ",\n" not in line:
                mode = "search"
                continue



        elif mode == "indat":

            if "0\n" not in line:
                mode = "search"
                continue

            if "INDAT(1)=0" not in line:
                frg_atoms = parse_indat(line)
                frags.append(frg_atoms)


        elif mode == "frgnam":

            # print line

            nams = parse_frgnam(line)

            for nam in nams:

                fragnams.append(nam)

            if ",\n" not in line:
                mode = "search"
                continue


        elif mode == "fmoxyz":
            if "$END" in line:
                mode = "search"
                continue
            if "XYZ" not in line:
                coords.append(line[3:])


    acts = []
    mode = "search"
    for line in lines:

        if mode == "search":

            if "IACTFG" in line:
                mode = "iactfg"

        if mode == "iactfg":
            #print line
            line_layers = parse_layer(line)
            for l in line_layers:
                acts.append(l)
            if ",\n" not in line:
                mode = "search"
                continue

    for i in acts:

        layers[i-1] = 3


    for line in lines:

        if "ISFRG" in line:

            i = int(string.split(line.rstrip("\n"), "=")[1])

            layers[i-1] = 4

            break


    f.close()

    L = dict()

    L[1] = []
    L[2] = []
    L[3] = []
    L[4] = []



    for i, frg in enumerate(frags):

        ilay = layers[i]


        for n in frg:
            L[ilay].append(coords[n-1])


    for i in range(1, 5):

        if len(L[i]) == 0:
            continue

        filename  = "L%02i_atoms.xyz" % (i)
        f = open(filename, "w")

        f.write("%i\n" % (len(L[i])))
        f.write("Layer %i\n" % (i))

        for coord in L[i]:
            f.write(coord)


        f.write("\n")

        f.close()
        print "Wrote:", filename



