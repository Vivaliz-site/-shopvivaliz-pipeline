"""GPT (OpenAI) integration module for ShopVivaliz Pipeline.

Provides reusable helpers for:
- Generating product descriptions from SKU / product name
- Analyzing product images via Vision API
- Enriching spreadsheet data with AI-generated content
"""

from __future__ import annotations

import base64
import os
from pathlib import Path

from openai import OpenAI

_client: OpenAI | None = None


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise EnvironmentError(
                "OPENAI_API_KEY environment variable is not set."
            )
        _client = OpenAI(api_key=api_key)
    return _client


def generate_product_description(sku: str, product_name: str = "", model: str = "gpt-4o-mini") -> str:
    """Return a short marketing description for a product.

    Args:
        sku: Product SKU identifier.
        product_name: Optional human-readable product name.
        model: OpenAI chat model to use.

    Returns:
        Generated description string, or empty string on failure.
    """
    client = _get_client()
    label = product_name if product_name else sku
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Você é um copywriter especializado em e-commerce brasileiro. "
                        "Escreva descrições de produtos curtas (2-3 frases), persuasivas e em português."
                    ),
                },
                {
                    "role": "user",
                    "content": f"Crie uma descrição de produto para: {label} (SKU: {sku})",
                },
            ],
            max_tokens=150,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as exc:
        print(f"[gpt_integration] Erro ao gerar descrição para SKU {sku}: {exc}")
        return ""


def analyze_product_image(image_path: str | Path, model: str = "gpt-4o-mini") -> str:
    """Analyze a product image and return a textual description.

    Args:
        image_path: Path to the local image file.
        model: OpenAI model that supports vision.

    Returns:
        Description string, or empty string on failure.
    """
    client = _get_client()
    image_path = Path(image_path)
    if not image_path.exists():
        return ""
    try:
        with open(image_path, "rb") as f:
            encoded = base64.standard_b64encode(f.read()).decode("utf-8")
        suffix = image_path.suffix.lower().lstrip(".")
        mime = f"image/{'jpeg' if suffix in ('jpg', 'jpeg') else suffix}"
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": (
                                "Descreva este produto de forma concisa para uso em e-commerce. "
                                "Responda em português."
                            ),
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:{mime};base64,{encoded}"},
                        },
                    ],
                }
            ],
            max_tokens=200,
        )
        return response.choices[0].message.content.strip()
    except Exception as exc:
        print(f"[gpt_integration] Erro ao analisar imagem {image_path}: {exc}")
        return ""


def enrich_dataframe(df, sku_col: str = "sku", name_col: str | None = None):
    """Add AI-generated descriptions to a pandas DataFrame.

    Adds a new column ``descricao_gpt`` with a generated description for each row.

    Args:
        df: pandas DataFrame with product data.
        sku_col: Name of the column containing the SKU.
        name_col: Optional column with the product name.

    Returns:
        DataFrame with the new ``descricao_gpt`` column.
    """
    if sku_col not in df.columns:
        print(f"[gpt_integration] Coluna '{sku_col}' não encontrada no DataFrame.")
        return df

    def _describe(row):
        name = str(row[name_col]) if name_col and name_col in row.index else ""
        return generate_product_description(str(row[sku_col]), name)

    df["descricao_gpt"] = df.apply(_describe, axis=1)
    return df
