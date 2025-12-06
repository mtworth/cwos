# CommentWorks

**Privacy-first local AI that reads open-ended survey comments and instantly outputs themes, tags, and sentiment.**

*CommentWorks* is a small utility built with a small language model to analyze free comments. Because of its size, it can run on a standard desktop, no third party APIs or GPUs required. 

## Features

- **100% Local & Private** - Your data never leaves your machine
- **Offline Ready** - No internet required after initial model download
- **Lightweight** - Optimized small models, minimal dependencies
- **Fast** - Process thousands of comments in minutes
- **Simple API** - Two core functions: `detect_themes()` and `assign_themes()`
- **DataFrame Friendly** - Works seamlessly with pandas (but doesn't require it)

## Installation

```bash
pip install git+https://github.com/[username]/commentworks.git
```

**Requirements:** Python 3.8+

## Quick Start

```python
import commentworks as cw

# Detect themes across multiple comments
reviews = [
    "Great food but service was slow",
    "Loved the ambiance, pricey though",
    "Quick service, average quality"
]

themes = cw.detect_themes(reviews)
print(themes)
# ['food quality', 'service speed', 'ambiance', 'pricing']

# Assign themes to a single comment
comment = "Amazing food but too expensive"
assigned = cw.assign_themes(
    comment,
    possible_themes=["food quality", "service", "pricing", "ambiance"]
)
print(assigned)
# ['food quality', 'pricing']
```

## Usage

### Theme Detection

Discover what themes are present across a collection of comments:

```python
import commentworks as cw

comments = [
    "Battery life is amazing, camera is just okay",
    "Great camera quality but battery drains fast",
    "Love the battery life and build quality"
]

themes = cw.detect_themes(comments)
# Returns: ['battery life', 'camera quality', 'build quality']
```

**Input formats:**
- List of strings: `["comment 1", "comment 2"]`
- Single string: `"just one comment"`
- Pipe-separated: `"comment 1 | comment 2 | comment 3"`

### Theme Assignment

Tag individual comments with relevant themes from a predefined list:

```python
import commentworks as cw

# Single comment
comment = "The food was great but service was terrible"
themes = cw.assign_themes(
    comment,
    possible_themes=["food quality", "service", "ambiance", "pricing"]
)
# Returns: ['food quality', 'service']

# Batch processing (more efficient for multiple comments)
comments = [
    "Amazing atmosphere",
    "Overpriced for the quality",
    "Fast service, good value"
]
results = cw.assign_themes(comments, possible_themes=["ambiance", "pricing", "service"])
# Returns: [['ambiance'], ['pricing'], ['service', 'pricing']]
```

### Using with Pandas

CommentWorks works great with pandas DataFrames:

```python
import pandas as pd
import commentworks as cw

# Load your data
df = pd.read_csv('reviews.csv')

# Detect themes across all comments
all_themes = cw.detect_themes(df['comment'].tolist())

# Assign themes to each row
df['themes'] = df['comment'].apply(
    lambda x: cw.assign_themes(x, possible_themes=all_themes)
)

# Export results
df.to_csv('reviews_with_themes.csv', index=False)
```

See [examples/dataframe_example.py](examples/dataframe_example.py) for a complete example.

## Examples

The `examples/` directory contains ready-to-run scripts:

- **[basic_usage.py](examples/basic_usage.py)** - Simple example using Python lists
- **[dataframe_example.py](examples/dataframe_example.py)** - Complete pandas workflow with sample data
- **[reviews.csv](examples/reviews.csv)** - Sample dataset of product/restaurant reviews

Run an example:
```bash
python examples/basic_usage.py
```

## How It Works

CommentWorks uses small language models (270M-2B parameters) fine-tuned specifically for analyzing open-ended feedback. The models are optimized to:

1. **Detect themes** - Identify common topics across multiple comments
2. **Assign themes** - Tag individual comments with relevant categories

Models are downloaded automatically from HuggingFace on first use and cached locally.

**Default model:** `maxwellt/commentworks_os` (270M parameters)

## Advanced Usage

### Custom Model

Use your own fine-tuned model:

```python
themes = cw.detect_themes(
    comments,
    model_name="your-username/your-model"
)
```

### GPU Acceleration

Run on GPU for faster processing:

```python
themes = cw.detect_themes(comments, device="cuda")
```

## Alpha Status Warning

**CommentWorks is in early alpha.** This means:

- The API may change in future versions
- Models are experimental and may produce inconsistent results
- Not recommended for production use yet
- Breaking changes may occur without notice

We welcome feedback and contributions!

## Use Cases

- Analyze customer feedback surveys
- Process product reviews at scale
- Categorize support tickets
- Research qualitative data analysis

## Requirements

- Python 3.8 or higher
- `transformers>=4.30.0`
- `torch>=2.0.0`

Optional:
- `pandas` for DataFrame integration (not required)

## Contributing

This is an experimental open-source project. Issues, feedback, and pull requests are welcome!

## License

Apache 2.0 License - see [LICENSE](LICENSE) file for details.

---

**Questions?** Open an issue on [GitHub](https://github.com/[username]/commentworks/issues).
