import streamlit as st
import pandas as pd

# Load the Excel file
excel_file = "Trainee guidelines 1st draft.xlsx"
guidelines_df = pd.read_excel(excel_file, sheet_name="Guidelines", header=None, engine="openpyxl")

# Extract module names and their corresponding rows
module_rows = {}
for idx, row in guidelines_df.iterrows():
    if isinstance(row[0], str) and row[0] not in ["Progress", "Comments", "Resources", "Topic Application", "Time period"]:
        module_rows[row[0]] = idx

# Sidebar: Trainee selection
st.sidebar.title("Trainee Selection")
trainee_name = st.sidebar.text_input("Enter your name")

# Main app
st.title("Trainee Learning Progress Tracker")

if trainee_name:
    st.subheader(f"Welcome, {trainee_name}!")

    progress_options = ["Not addressed", "Basic understanding", "Fully understood"]
    updated_data = {}

    for module, start_row in module_rows.items():
        st.markdown(f"### {module}")
        objectives = guidelines_df.iloc[start_row, 1:].dropna().tolist()
        progress_row = guidelines_df.iloc[start_row + 1, 1:]
        comments_row = guidelines_df.iloc[start_row + 2, 1:]

        module_updates = []

        for i, objective in enumerate(objectives):
            st.markdown(f"**Objective {i+1}:** {objective}")
            current_progress = progress_row.iloc[i] if i < len(progress_row) else "Not addressed"
            progress = st.selectbox(f"Progress for Objective {i+1}", progress_options, index=progress_options.index(current_progress), key=f"{module}_progress_{i}")
            comment = st.text_input(f"Comment for Objective {i+1}", value=comments_row.iloc[i] if i < len(comments_row) else "", key=f"{module}_comment_{i}")
            module_updates.append((objective, progress, comment))

        updated_data[module] = module_updates

    if st.button("Save Progress"):
        # Create a DataFrame to store updates
        output_rows = []
        for module, updates in updated_data.items():
            for obj, prog, comm in updates:
                output_rows.append({
                    "Trainee": trainee_name,
                    "Module": module,
                    "Objective": obj,
                    "Progress": prog,
                    "Comment": comm
                })

        output_df = pd.DataFrame(output_rows)
        output_df.to_excel("trainee_progress_updates.xlsx", index=False)
        st.success("Progress saved successfully to trainee_progress_updates.xlsx")
else:
    st.info("Please enter your name in the sidebar to begin.")