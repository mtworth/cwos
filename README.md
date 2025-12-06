# commentworks

_**commentworks**_ is a small language model and python utility for local, private comment analysis. It can be used to find and assign novel themes in unstructured response data.  

## Motivations 

Data analysts face a growing volume of open-ended information rich responses, but much of this information remains hard to process at scale. While large language models have transformed text analysis, they often pose privacy, cost, and governance challenges, especially for public-sector and community organizations handling sensitive feedback.
_commentworks_ is an attempt to investigate how small, local language models can fill this gap, helping teams extract themes and insights without sending data to third parties. 

## Features

- **100% Local & Private** - Your data never leaves your machine
- **Lightweight** - 500MB model, runs on CPU. No need for a fancy GPU. 
- **Simple API** - Two functions: `detect_themes()` and `assign_themes()`. 
- **DataFrame Friendly** - Works with pandas or plain Python lists.

_Please note that commentworks is an early stage experimental language model project. It is not recommended for use at scale in production pipelines._

## Installation

```bash
pip install git+https://github.com/mtworth/cwos.git
```

**Requirements:** Python 3.8+

## Quick Start

```python
import commentworks as cw

# Detect themes across comments
reviews = ["Great food but slow service", "Loved the ambiance, pricey though"]
themes = cw.detect_themes(reviews)
# Returns: ['food quality', 'service speed', 'ambiance', 'pricing']

# Assign themes to comments
comment = "Amazing food but too expensive"
assigned = cw.assign_themes(comment, possible_themes=["food quality", "service", "pricing"])
# Returns: ['food quality', 'pricing']
```

**See [examples/usage_demo.ipynb](examples/usage_demo.ipynb) for a complete walkthrough with both Python lists and pandas DataFrames.**


## How It Works

_commentworks_ uses **Gemma3-270M**, a small language model fine-tuned with synthetic data for comment analysis tasks. We chose Gemma-270M for its strong instruction-following capabilities after fine-tuning.

- **Model:** Fine-tuned version of `google/gemma-270m`
- **Size:** ~500MB
- **Training:** Synthetic data covering diverse comment analysis scenarios
- **Deployment:** HuggingFace Transformers library

The model downloads automatically on first use from HuggingFace and caches locally.

## Roadmap

_commentworks_ is in active development. Upcoming features we hope to get to:

- **Model Evaluations** - Benchmark performance on real-world comment datasets
- **Training Dataset Release** - Open-source synthetic training data
- **WebLLM GUI** - Browser-based interface for non-technical users
- **New Tasks:**
  - Sentiment detection (positive/negative/neutral)
  - Aspect-based topic modeling
- **Smart Sampling** - Improved algorithms for theme detection on large datasets. We currently recommend using a random sample for large datasets for theme detection, but hope to work on embedding based topic clustering for smarter sampling. 

## Requirements

- Python 3.8+
- `transformers>=4.30.0`
- `torch>=2.0.0`

## Contributing

Issues, feedback, and pull requests welcome! This is an open-source experiment.

## License

Apache 2.0 - see [LICENSE](LICENSE)

---

**Questions?** Open an issue on [GitHub](https://github.com/[username]/commentworks/issues)
