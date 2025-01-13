# rotulator

I use this small program to generate CSV files for factorial designs in plant experiments and then create paper labels to attach to the pots. The workflow is a bit awkward, but it gets the job done, and I've been using it for years

First, create a YAML file with a template to especify the experimental design:

```
rotulator -t
vim template.yaml
```

Modify the template to specify the factors and their levels, number of replicates, and if blocks are needed.

Then, create the csv:

```
rotulator -d template.yaml > experiment.csv
```


