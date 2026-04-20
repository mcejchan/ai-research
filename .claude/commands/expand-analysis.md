---
description: Deeply expand the analysis of a processed YouTube video using its transcript.
argument: video_query
---

I need you to significantly expand and deepen the analysis for a processed YouTube video.

Target provided: `{{video_query}}`

Please follow these steps:

1.  **Identify and Confirm Video**:
    - **Use the argument FIRST**: Search for `{{video_query}}` in `local-knowledge-base/youtube/` - it could be a channel name, partial folder name, or keyword.
    - **Only if argument is literally empty or contains `{{`**: Fall back to checking `git status` for recently modified video folders.
    - **Search method**: Use Glob with pattern `*{{video_query}}*` or LS to find matching folders.
    - **Verify**: Ensure the found folder contains `transcript_clean.txt`.
    - **Confirm**: **STOP** and present the identified video folder to me. Ask: "Is this the video you want to analyze?"
    - **Do not proceed** to reading or editing files until I confirm.

2.  **Read Context**:
    - Once confirmed, read the `transcript_clean.txt` (source) and the existing `analysis_main.md` (draft) from the identified folder.

3.  **Deep Analysis & Expansion**:
    - Compare the transcript against the current analysis.
    - Identify missing key thoughts, specific metaphors, complex arguments, detailed warnings, and nuanced ideas that make the content valuable.
    - The goal is to capture the full depth of the speaker's ideas, not just a high-level summary.
    - Look for overlooked sections, important context, and implicit implications.

4.  **Update the File**:
    - Overwrite `analysis_main.md` with the enriched version.
    - **Keep the structure**: Use the existing headers (Key Takeaways, Quotes, Why it matters, Practical Tips, etc.).
    - **Add depth**: Ensure "Why it matters" explains the implications fully. Add new takeaways if whole sections were missed.

5.  **Completion**:
    - Confirm which folder was updated and summarize the key additions you made.
