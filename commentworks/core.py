"""
Core functions for CommentWorks theme detection and assignment.
"""

from typing import Union, List, Optional
from transformers import pipeline


DEFAULT_MODEL = "maxwellt/commentworks_os"


def detect_themes(
    comments: Union[str, List[str]],
    model_name: str = DEFAULT_MODEL,
    device: str = "cpu"
) -> List[str]:
    """
    Detect themes across one or more comments.

    Args:
        comments: A single comment string, list of comments, or pipe-separated string
        model_name: HuggingFace model to use (default: maxwellt/commentworks_os)
        device: Device to run on (default: "cpu")

    Returns:
        List of detected theme strings

    Examples:
        >>> comments = [
        ...     "Great food but slow service",
        ...     "Loved the ambiance, pricey though"
        ... ]
        >>> themes = detect_themes(comments)
        >>> print(themes)
        ['food quality', 'service speed', 'ambiance', 'pricing']

        >>> # Also works with a single string
        >>> themes = detect_themes("The battery life is amazing")
        >>> print(themes)
        ['battery life', 'performance']
    """
    # Handle different input types
    if isinstance(comments, str):
        comment_text = comments
    elif isinstance(comments, list):
        comment_text = " | ".join(comments)
    else:
        raise TypeError("comments must be a string or list of strings")

    # Initialize pipeline
    pipe = pipeline("text-generation", model=model_name, device=device)

    # Build prompt
    prompt = f"""Task: theme detection

Identify the main themes from these comments:

{comment_text}"""

    messages = [{"role": "user", "content": prompt}]

    # Generate response
    result = pipe(messages)
    assistant_message = result[0]["generated_text"][-1]["content"]

    # Parse themes from comma-separated string
    themes = [theme.strip() for theme in assistant_message.split(",")]

    return themes


def assign_themes(
    comments: Union[str, List[str]],
    possible_themes: List[str],
    model_name: str = DEFAULT_MODEL,
    device: str = "cpu"
) -> Union[List[str], List[List[str]]]:
    """
    Assign themes to one or more comments from a predefined list.

    Args:
        comments: A single comment string or list of comment strings
        possible_themes: List of possible theme strings to choose from
        model_name: HuggingFace model to use (default: maxwellt/commentworks_os)
        device: Device to run on (default: "cpu")

    Returns:
        If single comment: List of assigned theme strings
        If multiple comments: List of lists, one theme list per comment

    Examples:
        >>> comment = "Great food but service was slow"
        >>> themes = assign_themes(
        ...     comment,
        ...     possible_themes=["food quality", "service", "ambiance", "pricing"]
        ... )
        >>> print(themes)
        ['food quality', 'service']

        >>> # Batch processing
        >>> comments = ["Great food", "Slow service"]
        >>> themes = assign_themes(comments, possible_themes=["food quality", "service"])
        >>> print(themes)
        [['food quality'], ['service']]
    """
    # Initialize pipeline once
    pipe = pipeline("text-generation", model=model_name, device=device)

    # Format possible themes
    themes_str = ", ".join(possible_themes)

    # Handle single vs batch
    is_single = isinstance(comments, str)
    comment_list = [comments] if is_single else comments

    results = []
    for comment in comment_list:
        # Build prompt
        prompt = f"""Task: theme tagging

Comment: {comment}

Possible themes: {themes_str}

Select the relevant themes:"""

        messages = [{"role": "user", "content": prompt}]

        # Generate response
        result = pipe(messages)
        assistant_message = result[0]["generated_text"][-1]["content"]

        # Parse themes from comma-separated string
        selected_themes = [theme.strip() for theme in assistant_message.split(",")]
        results.append(selected_themes)

    # Return single list for single comment, list of lists for batch
    return results[0] if is_single else results
