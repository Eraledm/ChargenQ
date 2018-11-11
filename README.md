# ChargenQ

In the current literature, it is useful to report changes in charge density associated with biomolecules. However, in order to get such information from output files generated from software like Quantum Espresso could be repetitive and long time-consuming. With this in mind, we present ChargenQ, which is a set of scripts developed in *python* thus, from the typically files from charge density of Quantum Espresso, ChargenQ delivery a new file, that It could be visualized with a very popular software of biomolecular visualization: [Pymol](https://pymol.org/2/), then, ChargenQ lets you change the color of the molecule based on polarization or partial charge.


## Getting Started

ChargenQ is divided by two scripts ChargenFilter and ChargenColor.

### ChargenFilter

ChargenFilter formats the outputs of [Quantum Espresso](https://www.quantum-espresso.org/) to convert it to a PQR
format, allowing to have partial charges.

```console
optional arguments:
  -h, --help            show this help message and exit
  -x INPUT_XYZ, --input-xyz INPUT_XYZ
                        name of pw.x output file with atomic positions
  -t {scf,relax}, --type-calc {scf,relax}
                        type of calculus output from -x argument
  -e INPUT_ENERGY, --input-energy INPUT_ENERGY
                        name of file with atomic energy
  -c INPUT_CHARGES, --input-charges INPUT_CHARGES
                        name of file with atomic charge
  -o OUTPUT, --output OUTPUT
                        name of output file
  -p, --polarization    change charge for polarization
  -v
```

Examples:

```console
python ChargenFilter.py -t relax -x clc2.out -c Cclc2.out -e Eclc2.out -o Vclc2
```

```console
python ChargenFilter.py -t scf -x clc2.out -c Cclc2.out -e Eclc2.out -o Clc2_file
```

### ChargenColor

ChargenColor could be installed on Pymol following [these](https://pymolwiki.org/index.php/Plugins) instrucctions.

### Prerequisites

You will need Python on your computer or server. Check [this](https://wiki.python.org/moin/BeginnersGuide/Download) out.

## Authors

* **Manuel de la Rosa** - [Eraledm](https://github.com/Eraledm)
* **P. Guillermo  Nieto Delgado** - [Profile](https://scholar.google.com/citations?user=0jRFmd0AAAAJ&hl=en)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
