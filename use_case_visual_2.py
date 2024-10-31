# Updated code with both bold outer grid lines and dashed internal lines
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches

# Load the Excel file and the specific sheet for analysis
file_path = '/home/neill/source/dft_visuals/Chargepoint data structure.xlsx'

use_case_mapping_df = pd.read_excel(file_path, sheet_name='Use case field mapping')

# Define color mappings for OCPI objects and data statuses separately
ocpi_object_colors = {
    'EVSE': '#ffdd57',     # Yellow for EVSE
    'Session': '#8ecae6',  # Light Blue for Session
    'Connector': '#ffb703', # Orange for Connector
    'N/A': '#cccccc'       # Grey for missing OCPI objects
}
status_colors = {
    'Available': '#66c2a5',           # Green
    'Missing Data': '#fc8d62',        # Orange
    'Complex to Compute': '#8da0cb'   # Blue
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
    index='Use Case ID', columns='Field Category', values='Data Status', aggfunc=lambda x: ', '.join(x.unique())
)
pivot_table_annotations = use_case_mapping_df.pivot_table(
    index='Use Case ID', columns='Field Category', values='OCPI object', aggfunc=lambda x: ', '.join(x.dropna().unique())
)

# Set up the plot
fig, ax = plt.subplots(figsize=(14, 8))

# Draw each cell with a horizontal split for OCPI object (top) and Data Status (bottom)
for i, use_case in enumerate(pivot_table_annotations.index):
    for j, category in enumerate(pivot_table_annotations.columns):
        # Get OCPI object and Data Status for each cell
        ocpi_object = pivot_table_annotations.loc[use_case, category] if pd.notna(pivot_table_annotations.loc[use_case, category]) else ''
        data_status = pivot_table_status.loc[use_case, category] if pd.notna(pivot_table_status.loc[use_case, category]) else ''
        
        # Determine colors for OCPI object (top half) and Data Status (bottom half)
        ocpi_color = ocpi_object_colors.get(ocpi_object, '#ffffff')  # Default to white if not specified
        status_color = status_colors.get(data_status, '#ffffff')     # Default to white if not specified
        
        # Draw top half for OCPI object color
        rect_top = patches.Rectangle((j, i + 0.5), 1, 0.5, color=ocpi_color, edgecolor='black', linewidth=1.5)
        ax.add_patch(rect_top)
        
        # Draw bottom half for Data Status color
        rect_bottom = patches.Rectangle((j, i), 1, 0.5, color=status_color, edgecolor='black', linewidth=1.5)
        ax.add_patch(rect_bottom)

# Apply color highlight to y-axis labels for all items based on MVP scope status
for i, use_case in enumerate(pivot_table_annotations.index):
    # Determine highlight color based on scope
    in_scope = use_case_mapping_df.loc[use_case_mapping_df['Use Case ID'] == use_case, 
                                       'In_Scope_For_MVP_Release_2'].iloc[0] == 'Y'
    label_color = "green" if in_scope else "yellow"
    
    # Apply background color to y-axis labels
    ax.text(-1.0, i + 0.5, use_case, ha='right', va='center', 
            fontsize=10, color='black', weight='bold', 
            bbox=dict(facecolor=label_color, edgecolor='none', boxstyle='round,pad=0.3'))

# Setting limits for alignment and grid consistency
ax.set_xlim(left=-1, right=len(pivot_table_annotations.columns))
ax.set_ylim(bottom=len(pivot_table_annotations.index), top=0)

# Add dashed gridlines for internal cell divisions and bold solid lines for main grid divisions
ax.grid(which='both', color='gray', linestyle='--', linewidth=0.5)
for x in range(len(pivot_table_annotations.columns) + 1):
    ax.axvline(x=x, color='black', linestyle='-', linewidth=1.5)  # Bold solid vertical lines for main dividers
for y in range(len(pivot_table_annotations.index) + 1):
    ax.axhline(y=y, color='black', linestyle='-', linewidth=1.5)  # Bold solid horizontal lines for main dividers

# Set up x-axis ticks and labels
plt.xticks(np.arange(len(pivot_table_annotations.columns)) + 0.5, pivot_table_annotations.columns, rotation=45, ha='right', fontsize=10)
plt.yticks(np.arange(len(pivot_table_annotations.index)) + 0.5, ['' for _ in pivot_table_annotations.index])  # Custom y-tick labels

# Labels and title
plt.xlabel("Field Category", fontsize=12)
plt.ylabel("Use Case ID", fontsize=12)
plt.title("Use Case Field Category Mapping with Enhanced Grid Structure", fontsize=16)

# Legend focusing on Data Status, OCPI objects, and MVP scope
legend_handles = [patches.Patch(color=color, label=label) for label, color in status_colors.items()]
legend_handles.extend([patches.Patch(color=color, label=label) for label, color in ocpi_object_colors.items()])
legend_handles.append(patches.Patch(color="green", label="In Scope for MVP"))
legend_handles.append(patches.Patch(color="yellow", label="Out of Scope for MVP"))
plt.legend(handles=legend_handles, title="Legend", bbox_to_anchor=(1.05, 1), loc='upper left')

plt.tight_layout()
#plt.show()
plt.savefig('use_case_visualization2.png')
