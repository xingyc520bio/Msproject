

## Journal Entry: Visualizing Sequence Data with Biotite

#### Date: June 18, 2024

### Introduction

Today, I embarked on a journey to visualize sequence data searched from NCBI of D68 using Biotite. My dataset is contained within an XML file named `sequence.xml`.

### Step 1: Preparing the Environment

Firstly, I ensured that Biotite was installed in my Python environment. If not already installed, I used pip to install it:

```bash
pip install biotite
```

### Step 2: Parsing the XML File

I began by parsing the XML file using Python's `xml.etree.ElementTree` module:

```python
import xml.etree.ElementTree as ET

tree = ET.parse('sequence.xml')
root = tree.getroot()
```

### Step 3: Extracting Sequence Data

I traversed the XML tree to extract the sequence data according to its structure:

```python
sequences = []
for seq_elem in root.findall('.//sequence'):
    sequence_id = seq_elem.get('id')
    sequence_data = seq_elem.text
    sequences.append((sequence_id, sequence_data))
```

### Step 4: Converting to Biotite Sequence Objects

I converted the extracted data into Biotite's `Sequence` objects:

```python
from biotite.sequence import NucleotideSequence

biotite_sequences = [NucleotideSequence(seq_data) for _, seq_data in sequences]
```

### Step 5: Sequence Analysis (Optional)

Depending on my specific needs, I utilized Biotite's tools for sequence alignment, searching, or other analyses.

### Step 6: Visualizing the Sequences

I used Biotite's visualization tools to create graphical representations of the sequences:

```python
from biotite.sequence.graphics import sequence_bar_plot
import matplotlib.pyplot as plt

for seq in biotite_sequences:
    sequence_bar_plot(seq)
    plt.title(f"Nucleic Acid Sequence")
    plt.show()
```

### Step 7: Saving or Displaying the Visualizations

Finally, I saved or displayed the visualizations using Matplotlib's functions.

### Conclusion

The process of visualizing sequence data with Biotite was both enlightening and productive. It allowed me to gain insights into the structure and composition of my sequences, which is essential for my ongoing research.
