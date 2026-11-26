# Power BI dashboard

1. Run the Streamlit app and create several transformations.
2. Open Analytics and export `genai_analytics.csv`.
3. In Power BI Desktop choose Get Data → Text/CSV.
4. Select the exported CSV and Load.
5. Suggested visuals:
   - Card: total transformations
   - Clustered column chart: task vs count
   - Line chart: created_at by count (group by date)
   - Bar chart: source_name vs word_count
6. Add slicers for task and model.
7. Save as `GenAI_Analytics.pbix`.
