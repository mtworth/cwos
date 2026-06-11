# commentworks

_**commentworks**_ is a small language model and python utility for local, private comment analysis. It can be used to find and assign novel themes in unstructured response data.  

## Motivations 

Data analysts face a growing volume of open-ended information rich responses (surveys, product reviews, ticket comments, etc.), but much of this information remains hard to process at scale. While large language models have transformed text analysis, they often pose privacy, cost, and governance challenges, especially for public-sector and community organizations handling sensitive feedback.

_commentworks_ is an attempt to investigate how small, local language models can fill this gap, helping teams extract themes and insights without sending data to third parties. 

## Boring Tiny Tool wrapper

For analysts who do not want to write Python, this repo includes a tiny local Streamlit wrapper:

```bash
pip install "git+https://github.com/mtworth/cwos.git#egg=commentworks[app]"
streamlit run app.py
```

The wrapper intentionally does one small workflow:

1. Upload a CSV
2. Pick the comment column
3. Detect candidate themes from a sample
4. Review or edit the theme list
5. Tag every non-empty comment
6. Download the tagged CSV

Privacy notes:

- The app runs on `localhost`.
- Comment text is processed by the local Python process.
- Streamlit usage stats are disabled in `.streamlit/config.toml`.
- The default model may download once from HuggingFace, then runs from the local cache.
- Outputs are suggested tags, not ground truth. Review themes before using them in reporting.

## Features

- **100% Local & Private** - Your data never leaves your machine
- **Lightweight** - 500MB model, runs on CPU. No need for a fancy GPU.
- **Simple API** - Initialize once, use many times with `detect_themes()` and `assign_themes()`
- **DataFrame Friendly** - Works with pandas or plain Python lists
- **Local App** - Upload CSVs, detect themes, assign tags, and export results from a tiny local UI

_Please note that commentworks is an early stage experimental language model project. It is not recommended for use at scale in production pipelines._

## Installation

```bash
pip install git+https://github.com/mtworth/cwos.git
```

For the local wrapper app:

```bash
pip install "git+https://github.com/mtworth/cwos.git#egg=commentworks[app]"
```

**Requirements:** Python 3.8+

## Quick Start

```python
import commentworks as cw

# Initialize model (downloads automatically on first use)
model = cw.commentworks()

# Detect themes across comments
reviews = ["Great food but slow service", "Loved the ambiance, pricey though"]
themes = model.detect_themes(reviews)
# Returns: ['food quality', 'service speed', 'ambiance', 'pricing']

# Assign themes to comments
comment = "Amazing food but too expensive"
assigned = model.assign_themes(comment, possible_themes=["food quality", "service", "pricing"])
# Returns: ['food quality', 'pricing']
```

**See [examples/usage_demo.ipynb](examples/usage_demo.ipynb) for a complete walkthrough with both Python lists and pandas DataFrames.**

## Local app

From the repository root:

```bash
streamlit run app.py
```

The app opens in your browser and runs locally. It does not require an API key, user account, database, or cloud LLM.

## How It Works

_commentworks_ uses **Gemma3-270M**, a small language model fine-tuned with synthetic data for comment analysis tasks. We chose Gemma-270M for its strong instruction-following capabilities after fine-tuning.

- **Model:** Fine-tuned version of `google/gemma-270m`
- **Size:** ~500MB
- **Training:** Synthetic data covering diverse comment analysis scenarios
- **Deployment:** HuggingFace Transformers library

The model downloads automatically on first use from HuggingFace and caches locally.

## Roadmap

_commentworks_ is in active development. Upcoming features we hope to get to:

- **Function Clarity** -- Reframe theme detection as a hypothesis, rather than true detection.
- **Tag Robustness Analysis** -- Each comment gets tagged by multiple prompts, showing range of certainty within the model.
- **Smart Sampling** - Improved algorithms for theme detection on large datasets. We currently recommend using a random sample for large datasets for theme detection, but hope to work on embedding based topic clustering for smarter sampling. 
- **Model Evaluations** - Benchmark performance on real-world comment datasets
- **Training Dataset Release** - Open-source synthetic training data
- **Streamlit demo** -- a simple GUI demo just so folks can understand speed and quality on test datasets 
- **New Tasks:**
  - Sentiment (positive/negative/neutral)
  - Aspect-based topic modeling
  - Lexicon normalization? (clean-up some messy spellings) 
  - Single select tagging

## Requirements

- Python 3.8+
- `transformers>=4.30.0`
- `torch>=2.0.0`

## Contributing

Issues, feedback, and pull requests welcome! This is an open-source experiment.

## License

Apache 2.0 - see [LICENSE](LICENSE)

---

**Questions?** Open an issue on [GitHub](https://github.com/mtworth/cwos/issues)
