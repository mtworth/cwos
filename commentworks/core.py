"""
Core commentworks class for theme detection and assignment.
"""

from typing import Union, List
from transformers import pipeline


DEFAULT_MODEL = "maxwellt/commentworks_os"


class commentworks:
    """
    Local AI model for analyzing open-ended comments.

    The commentworks class loads a fine-tuned language model for detecting
    and assigning themes in comment data. The model runs locally and all
    data stays on your machine.

    Args:
        model_name: HuggingFace model to use (default: maxwellt/commentworks_os)
        device: Device to run on (default: "cpu", can use "cuda" for GPU)

    Examples:
        >>> import commentworks as cw
        >>> model = cw.commentworks()
        >>>
        >>> # Detect themes
        >>> reviews = ["Great food but slow service", "Loved the ambiance"]
        >>> themes = model.detect_themes(reviews)
        >>>
        >>> # Assign themes
        >>> assigned = model.assign_themes(reviews[0], possible_themes=themes)
    """

    def __init__(self, model_name: str = DEFAULT_MODEL, device: str = "cpu"):
        """Initialize the commentworks model."""
        self.model_name = model_name
        self.device = device
        self.pipe = pipeline("text-generation", model=model_name, device=device)

    def detect_themes(self, comments: Union[str, List[str]]) -> List[str]:
        """
        Detect themes across one or more comments.

        Args:
            comments: A single comment string or list of comment strings

        Returns:
            List of detected theme strings

        Examples:
            >>> model = commentworks()
            >>> comments = ["Great food but slow service", "Loved the ambiance"]
            >>> themes = model.detect_themes(comments)
            >>> print(themes)
            ['food quality', 'service speed', 'ambiance']
        """
        # Handle different input types
        if isinstance(comments, str):
            comment_text = comments
        elif isinstance(comments, list):
            comment_text = " | ".join(comments)
        else:
            raise TypeError("comments must be a string or list of strings")

        # Build prompt
        prompt = f"""Task: theme detection

Identify the main themes from these comments:

{comment_text}"""

        messages = [{"role": "user", "content": prompt}]

        # Generate response
        result = self.pipe(messages)
        assistant_message = result[0]["generated_text"][-1]["content"]

        # Parse themes from comma-separated string
        themes = [theme.strip() for theme in assistant_message.split(",")]

        return themes

    def assign_themes(
        self,
        comments: Union[str, List[str]],
        possible_themes: List[str]
    ) -> Union[List[str], List[List[str]]]:
        """
        Assign themes to one or more comments from a predefined list.

        Args:
            comments: A single comment string or list of comment strings
            possible_themes: List of possible theme strings to choose from

        Returns:
            If single comment: List of assigned theme strings
            If multiple comments: List of lists, one theme list per comment

        Examples:
            >>> model = commentworks()
            >>> comment = "Great food but service was slow"
            >>> themes = model.assign_themes(
            ...     comment,
            ...     possible_themes=["food quality", "service", "ambiance"]
            ... )
            >>> print(themes)
            ['food quality', 'service']
        """
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
            result = self.pipe(messages)
            assistant_message = result[0]["generated_text"][-1]["content"]

            # Parse themes from comma-separated string
            selected_themes = [theme.strip() for theme in assistant_message.split(",")]
            results.append(selected_themes)

        # Return single list for single comment, list of lists for batch
        return results[0] if is_single else results
