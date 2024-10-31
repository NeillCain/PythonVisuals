import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches

# Load the Excel file and the specific sheet for analysis
file_path = '/home/neill/source/dft_visuals/Chargepoint data structure.xlsx'
use_case_mapping_df = pd.read_excel(file_path, sheet_name='Use case field mapping')

# Updated color mappings for accessibility
ocpi_object_colors = {
    'EVSE': '#66c2a5',       # Light Blue for EVSE
    'Session': '#377eb8',    # Dark Blue for Session
    'Connector': '#e7298a',  # Dark Orange for Connector
    'N/A': '#999999'         # Gray for missing OCPI objects
}
status_colors = {
    'Available': '#1b9e77',           # Green
    'Missing Data': '#d95f02',        # Red
    'Complex to Compute': '#7570b3'   # Purple
}

# Apply Data Status logic based on rules for identifying availability
use_case_mapping_df['Data Status'] = np.where(
    use_case_mapping_df['OCPI object field'].isna() | (use_case_mapping_df['OCPI object field'] == 'N/A'), 
    'Missing Data',
    np.where(use_case_mapping_df['Field Category'].isin(['Utilisation', 'Reliability', 'Uptime']), 
             'Complex to Compute', 'Available')
)

# Create pivot tables for Data Status and OCPI objects for visualization
pivot_table_status = use_case_mapping_df.pivot_table(
    index='Use Case ID', columns='Field Category', values='Data Status', aggfunc='first'
)
pivot_table_annotations = use_case_mapping_df.pivot_table(
    index='Use Case ID', columns='Field Category', values='OCPI object', aggfunc='first'
)

# Set up the plot with two subplots: one for OCPI Object and one for Data Availability
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))

# Draw OCPI Object plot
for i, use_case in enumerate(pivot_table_annotations.index):
    for j, category in enumerate(pivot_table_annotations.columns):
        ocpi_object = pivot_table_annotations.loc[use_case, category] if pd.notna(pivot_table_annotations.loc[use_case, category]) else ''
        ocpi_color = ocpi_object_colors.get(ocpi_object, '#ffffff')
        
        # Draw cell with OCPI Object color
        rect = patches.Rectangle((j, i), 1, 1, color=ocpi_color, edgecolor='black', linewidth=1.5)
        ax1.add_patch(rect)

# Apply color highlight to y-axis labels based on MVP scope status
for i, use_case in enumerate(pivot_table_annotations.index):
    in_scope = use_case_mapping_df.loc[use_case_mapping_df['Use Case ID'] == use_case, 'In_Scope_For_MVP_Release_2'].iloc[0] == 'Y'
    label_color = "#008080" if in_scope else "#404040"
    ax1.text(-1.0, i + 0.5, use_case, ha='right', va='center', fontsize=10, color='white', weight='bold', 
            bbox=dict(facecolor=label_color, edgecolor='none', boxstyle='round,pad=0.3'))

# Set limits, labels, and grid for the OCPI Object plot
ax1.set_xlim(left=-1, right=len(pivot_table_annotations.columns))
ax1.set_ylim(bottom=len(pivot_table_annotations.index), top=0)
ax1.set_xticks(np.arange(len(pivot_table_annotations.columns)) + 0.5)
ax1.set_xticklabels(pivot_table_annotations.columns, rotation=45, ha='right', fontsize=10)
ax1.set_yticks(np.arange(len(pivot_table_annotations.index)) + 0.5)
ax1.set_yticklabels(['' for _ in pivot_table_annotations.index])
ax1.set_xlabel("Field Category", fontsize=12)
ax1.set_ylabel("Use Case ID", fontsize=12)
ax1.set_title("OCPI Object Details", fontsize=16)
ax1.grid(visible=True, color='gray', linestyle='--', linewidth=0.5)

# Draw Data Availability plot
for i, use_case in enumerate(pivot_table_status.index):
    for j, category in enumerate(pivot_table_status.columns):
        data_status = pivot_table_status.loc[use_case, category] if pd.notna(pivot_table_status.loc[use_case, category]) else ''
        status_color = status_colors.get(data_status, '#ffffff')
        
        # Draw cell with Data Status color
        rect = patches.Rectangle((j, i), 1, 1, color=status_color, edgecolor='black', linewidth=1.5)
        ax2.add_patch(rect)

# Apply color highlight to y-axis labels for the Data Availability plot
for i, use_case in enumerate(pivot_table_status.index):
    in_scope = use_case_mapping_df.loc[use_case_mapping_df['Use Case ID'] == use_case, 'In_Scope_For_MVP_Release_2'].iloc[0] == 'Y'
    label_color = "#008080" if in_scope else "#404040"
    ax2.text(-1.0, i + 0.5, use_case, ha='right', va='center', fontsize=10, color='white', weight='bold', 
            bbox=dict(facecolor=label_color, edgecolor='none', boxstyle='round,pad=0.3'))

# Set limits, labels, and grid for the Data Availability plot
ax2.set_xlim(left=-1, right=len(pivot_table_status.columns))
ax2.set_ylim(bottom=len(pivot_table_status.index), top=0)
ax2.set_xticks(np.arange(len(pivot_table_status.columns)) + 0.5)
ax2.set_xticklabels(pivot_table_status.columns, rotation=45, ha='right', fontsize=10)
ax2.set_yticks(np.arange(len(pivot_table_status.index)) + 0.5)
ax2.set_yticklabels(['' for _ in pivot_table_status.index])
ax2.set_xlabel("Field Category", fontsize=12)
ax2.set_ylabel("Use Case ID", fontsize=12)
ax2.set_title("Data Availability", fontsize=16)
ax2.grid(visible=True, color='gray', linestyle='--', linewidth=0.5)

# Separate legends for each plot
legend1_handles = [patches.Patch(color=color, label=label) for label, color in ocpi_object_colors.items()]
legend2_handles = [patches.Patch(color=color, label=label) for label, color in status_colors.items()]
legend3_handles = [patches.Patch(color="#008080", label="In Scope for MVP"), patches.Patch(color="#404040", label="Out of Scope for MVP")]

legend1 = ax1.legend(handles=legend1_handles, title="OCPI Object", bbox_to_anchor=(1.05, 1), loc='upper left')
legend2 = ax2.legend(handles=legend2_handles, title="Data Availability", bbox_to_anchor=(1.05, 1), loc='upper left')
legend3 = plt.legend(handles=legend3_handles, title="MVP Scope", bbox_to_anchor=(1.05, 0.5), loc='upper left')

# Add the MVP scope legend to the figure
fig.add_artist(legend3)

plt.tight_layout()
#plt.show()
plt.savefig('use_case_visualization5.png')
