# rotulator

I use this small program to generate CSV files for factorial designs in plant experiments and then create paper labels to attach to the pots. The workflow is awkward, but it gets the job done, and I've been using it for years. 

# Installation

```
git clone https://github.com/fdecunta/rotulator.git
cd rotulator
sudo make install
```

Remove with:

```
sudo make uninstall
```


# How to use

1. **Create a YAML file with a template** to specify your experimental design:

```
rotulator -t
vim template.yaml
```

**Modify the template** to define the factors, their levels, number of replicates, and whether blocks are needed.

2. **Generate the CSV file** for your experiment:

```
rotulator -d template.yaml > experiment.csv
```

3. **Create the labels for the pots**:

```
rotulator -l experiment.csv > exp_labels.csv
```

This command will generate a CSV with three columns of labels, each containing the information for an individual experimental unit.

4. **Format and print the labels**: Open exp_labels.csv in LibreOffice Calc or any spreadsheet program, format the text as needed, and then print the labels.

