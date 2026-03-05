# Spiral-Theme-Vectors

Controlled thematic emphasis and narrative differentiation for AI-assisted creative writing and comprehension tasks.

This module implements **grounded priority vectors** — a mechanism that allows users/agents to shift interpretive tone, sub-theme focus, and emphasis in generated or refined text while remaining strictly anchored to the source material. It is the direct software companion to the Zenodo preprint:

**Controlled Thematic Emphasis in Spiral-Assisted Creative Writing: Grounded Priority Vectors and Generality Constraints**  
DOI: [10.5281/zenodo.18881454](https://zenodo.org/records/18881454)

Built on Sir Benjamin's **Spiral Theory** and the **CreativeWriting_Assist** framework.

## Core Idea

Traditional AI summarization and creative generation often converges on generic or consensus readings.  
This module enables **controlled novelty**:  
- Detects themes with confidence scores  
- Generates a grounded default priority vector  
- Accepts safe, bounded nudges  
- Feeds emphasis into spiral refinement loops  
- Produces differentiated yet text-faithful outputs with provenance stamps

All variation stays within textual evidence (replicated word chains, motif validity, generality probability pools). No hallucinated themes or unsupported lenses.

## Quick Example

```python
from spiral_theme_vectors import ThemeAnalysisTool

tool = ThemeAnalysisTool(genre_generalities=..., author_profiles=...)
analysis = tool.analyze(full_text_of_gift_of_magi)

# Default vector: {'sacrifice': 0.42, 'irony': 0.31, ...}

# Nudge toward poverty lens
nudged_vector = tool.apply_user_nudge({"poverty": +0.52})

refined_summary = tool.refine_text(
    text=original_text,
    priority_vector=nudged_vector
)

print(refined_summary)
# → Darker, critical tone emphasizing systemic cruelty, validity 87%
